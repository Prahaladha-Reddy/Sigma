from __future__ import annotations
import asyncio
import json
import os
import sys
import time
import uuid
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import boto3

from core.new_agent_architecture import the_runner
from core.process_context import ProcessContext

from database.database import supabase  



SQS_QUEUE_URL = os.getenv("SQS_QUEUE_URL")
AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET = os.getenv("AWS_BUCKET_NAME")
FILES_TABLE = os.getenv("SUPABASE_FILES_TABLE", "files")


def get_boto_clients():
    sqs = boto3.client("sqs", region_name=AWS_REGION)
    s3 = boto3.client("s3", region_name=AWS_REGION)
    return sqs, s3


def fetch_files_metadata(file_ids: List[str]) -> List[Dict[str, str]]:
    """
    Query Supabase for file metadata. Expects a table with columns: id, s3_key, file_name.
    """
    if supabase is None:
        raise RuntimeError(
            "Supabase client is not configured. Add src/database.py with `supabase` or adjust import."
        )

    resp = (
        supabase.table(FILES_TABLE)
        .select("id, s3_key, file_name")
        .in_("id", file_ids)
        .execute()
    )


    data = getattr(resp, "data", None) or []
    return data


def download_files_to_process(
    s3_client, files_meta: List[Dict[str, str]], process_ctx: ProcessContext
) -> List[Path]:
    downloaded = []
    for meta in files_meta:
        s3_key = meta["s3_key"]
        fname = meta.get("file_name") or Path(s3_key).name
        dest = process_ctx.uploaded_dir / fname
        dest.parent.mkdir(parents=True, exist_ok=True)
        print(f"Downloading s3://{S3_BUCKET}/{s3_key} -> {dest}")
        s3_client.download_file(S3_BUCKET, s3_key, str(dest))
        downloaded.append(dest)
    return downloaded


def upload_result_pdf(s3_client, pdf_path: Path, process_id: str) -> str:
    key = f"presentations/{process_id}/final_presentation.pdf"
    print(f"Uploading result PDF to s3://{S3_BUCKET}/{key}")
    s3_client.upload_file(str(pdf_path), S3_BUCKET, key)
    return f"s3://{S3_BUCKET}/{key}"


def update_supabase_status(
    process_id: str,
    status: str,
    pdf_url: Optional[str] = None,
    table: str = "Process",  
):

    payload: Dict[str, str] = {"status": status}

    if pdf_url:
        payload["presentation_s3_url"] = pdf_url

    try:
        (
            supabase.table(table)
            .update(payload)
            .eq("process_id", process_id)
            .execute()
        )
    except Exception as exc:
        print(f"Failed to update Supabase status for {process_id}: {exc}")


def handle_message(msg_body: Dict) -> None:
    process_id = msg_body.get("process_id") or str(uuid.uuid4())

    user_query = msg_body.get("user_query") or msg_body.get("user_message")
    if not user_query:
        raise ValueError("Missing 'user_query' / 'user_message' in SQS message")

    num_slides = msg_body.get("num_slides", 12)
    file_ids = msg_body.get("file_ids", []) or []

    sqs_client, s3_client = get_boto_clients()

    with ProcessContext(process_id=process_id, cleanup=True) as ctx:
        try:
            if file_ids:
                files_meta = fetch_files_metadata(file_ids)
                if not files_meta:
                    print(f"No files found in Supabase for {file_ids}")
                else:
                    download_files_to_process(s3_client, files_meta, ctx)

            result = asyncio.run(
                the_runner(
                    user_query=user_query,
                    num_slides=num_slides,
                    process_context=ctx,
                )
            )

            pdf_path = Path(result["final_pdf"])
            pdf_url = upload_result_pdf(s3_client, pdf_path, process_id)
            update_supabase_status(process_id, "completed", pdf_url=pdf_url)
            print(f"Process {process_id} completed. PDF: {pdf_url}")
        except Exception as exc:
            update_supabase_status(process_id, "failed")
            print(f"Process {process_id} failed: {exc}")


def poll_sqs():
    if not SQS_QUEUE_URL:
        print("SQS_QUEUE_URL env not set. Exiting.")
        sys.exit(1)

    sqs_client, _ = get_boto_clients()

    while True:
        resp = sqs_client.receive_message(
            QueueUrl=SQS_QUEUE_URL,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=10,
            VisibilityTimeout=900,
        )
        messages = resp.get("Messages", [])
        if not messages:
            continue

        for msg in messages:
            receipt = msg["ReceiptHandle"]
            try:
                body = json.loads(msg["Body"])
                if "Message" in body:
                    body = json.loads(body["Message"])
                handle_message(body)
                sqs_client.delete_message(QueueUrl=SQS_QUEUE_URL, ReceiptHandle=receipt)
            except Exception as exc:
                print(f"Error handling message: {exc}")
                continue



if __name__ == "__main__":
    poll_sqs()
