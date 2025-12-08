# Beat Gamma Jupyter

AI-assisted pipeline that turns raw PDFs, Jupyter notebooks, and structured datasets into slide-ready presentations. It combines document parsing (Docling), Gemini LLMs, a Jupyter MCP server for executable analysis, and a LangGraph-powered presentation builder. An optional SQS worker can run the whole flow headlessly and publish PDFs to S3.

## What it does
- **PDF pipeline:** Extracts text, tables, and figures with Docling, generates a deep Gemini summary, aligns tables/figures to their pages, and writes a mini-presentation in Markdown (tables hydrated inline when referenced).
- **Notebook pipeline:** Converts `.ipynb` to Markdown plus assets, then drafts a narrative mini-presentation from the notebook outputs.
- **Data analyst agent:** Uses the Jupyter MCP server to execute analysis requests, save notebooks under `data/analysis`, and export Markdown reports.
- **Presentation assembler:** Chains multiple agents (narrative merge → dataset query generation → search enrichment → slide HTML + PDF via Playwright) to produce `presentation.md`, `Final_story.md`, `Final_slides.html`, and a final PDF.
- **Vector store ingestion:** Sends document Markdown chunks to Qdrant using Gemini embeddings for later retrieval.
- **Background worker:** Listens to SQS, downloads inputs from S3/Supabase metadata, runs the pipeline in an isolated `processes/<id>` sandbox, uploads the resulting PDF, and updates Supabase status.

## Architecture at a glance
- **Document processing (`src/document_processing`)**
  - `DocumentProcessor` wraps Docling PDF parsing.
  - `ContentSaver` persists images/tables/text under `data/documents/<doc>/`.
  - `document_summary.py` produces a structured Gemini summary; `extract_multimodel.py` resolves figures/tables from the summary to saved assets; `document_understanding.py` orchestrates the full PDF → mini-presentation flow and hydrates table content references.
  - `vector_store.py` ingests Markdown into Qdrant and supports similarity queries.
- **Notebook processing (`src/notebooks_processing`)**
  - `convert_notebook` extracts Markdown + assets, writes a mini-presentation via Gemini, and caches results under `data/notebook/<name>/`.
- **Data analyst (`src/data_analyst`)**
  - Connects to the MCP Jupyter server (HTTP transport on `:4040`), exposes tools, and runs a tightly scoped analysis agent (`data_analyst`) that saves notebooks in `data/analysis` then converts them to Markdown.
- **Presentation builder (`src/core/new_agent_architecture.py`)**
  - Multi-step chain: merge mini-presentations (Agent 1) → generate dataset query (Agent 2) → optional search enrichment (Agent 2 with search) → refine story (Agent 3) → theme + Tailwind slide HTML (Agent 4) → render PDF via Playwright.
  - `ProcessContext` manages per-run folders (`processes/<id>/data/...`) so worker runs stay isolated.
- **Worker (`src/worker/sqs_worker.py`)**
  - Polls SQS, fetches file metadata from Supabase, downloads from S3, runs `the_runner`, uploads the PDF back, and marks status in Supabase.
- **Deep research (experimental, `src/unused_deep_researcher`)**
  - Tavily-backed research agent kept available via `deep_researcher` tool.

## Directory layout
- `src/document_processing/` – Docling wrappers, summarization, asset resolution, table hydration, Qdrant ingestion.
- `src/notebooks_processing/` – Notebook → Markdown/mini-presentation conversion utilities.
- `src/data_analyst/` – MCP Jupyter analysis agent + helper tools.
- `src/core/` – Agent prompts, multi-agent runner, HTML/PDF conversion, process context, shared tools.
- `src/worker/` – SQS worker that orchestrates end-to-end runs in containers.
- `data/` – Runtime working directory (analysis notebooks, mini-presentations, outputs). Created on demand.
- `processes/<uuid>/` – Per-run sandboxes when using `ProcessContext` (used by the worker).

## Setup

Prerequisites: Python 3.12+, `uv` (recommended), Playwright Chromium (for HTML → PDF), and Docker if you want the container stack.

1) Install dependencies
```bash
uv sync            # creates .venv and installs runtime deps
uv run python -m playwright install --with-deps chromium  # for slide-to-PDF rendering
```

2) Configure environment variables (create `.env`)
- `GOOGLE_API_KEY` – required for Gemini models and embeddings.
- `MCP_JUPYTER_URL` – MCP endpoint (default `http://127.0.0.1:4040/mcp`).
- `QDRANT_URL`, `QDRANT_API_KEY` – enable vector store ingestion/query.
- `SUPABASE_URL`, `SUPABASE_KEY`, `SUPABASE_FILES_TABLE` (default `files`) – used by the worker to look up S3 keys.
- `AWS_BUCKET_NAME`, `AWS_REGION`, `SQS_QUEUE_URL` plus standard AWS credentials – required for the worker’s S3/SQS operations.
- `TAVILY_API_KEY` – only if you use the deep research agent.

3) (Optional) Bring up the container stack
```bash
docker compose up --build
```
- Jupyter Lab: http://localhost:8888
- MCP server: http://localhost:4040
- Worker runs `sqs_worker` in the background; data and processes directories are volume-mounted.

## Usage

### 1) Process a PDF into a mini-presentation
Place a PDF under `data/uploaded/` (or your `ProcessContext` uploaded dir) and run:
```bash
uv run python -m src.document_processing.document_understanding data/uploaded/example.pdf
```
Outputs:
- `data/documents/<doc>/` with `images/`, `tables/` (CSV + JSON + Markdown), `text/document.md`
- `data/mini_presentation_<doc>.md` (hydrated tables embedded)
- `data/documents/<doc>/result.json` (summary + resolved assets metadata)

### 2) Convert a notebook to a mini-presentation
```bash
uv run python - <<'PY'
from notebooks_processing.notebook_processing import convert_notebook
mini_md, assets = convert_notebook("data/uploaded/example.ipynb")
print("Mini-presentation:", mini_md)
print("Assets:", assets)
PY
```
Creates `data/notebook/<name>/...` plus `<name>_mini_presentation.md` in `data/`.

### 3) Run the Jupyter data analyst agent
Ensure the dataset is under `data/uploaded/` and the MCP Jupyter server is reachable.
```bash
uv run python - <<'PY'
import asyncio
from data_analyst.data_analyst_agent import data_analyst
from core.process_context import ProcessContext

with ProcessContext() as ctx:
    result = asyncio.run(
        data_analyst("Take a quick look at adults.csv: clean and basic stats, one histogram.", process_context=ctx)
    )
    print(result)
PY
```
New notebooks land in `processes/<id>/data/analysis/` and are auto-converted to Markdown.

### 4) Full presentation build (docs + notebooks + optional dataset)
Drop PDFs/notebooks (and optionally a CSV/XLSX) into your `ProcessContext` upload folder and run:
```bash
uv run python - <<'PY'
import asyncio
from core.new_agent_architecture import the_runner
from core.process_context import ProcessContext

with ProcessContext() as ctx:
    result = asyncio.run(the_runner(user_query="Build slides on inflation, interest, and unemployment", num_slides=12, process_context=ctx))
    print(result["final_pdf"])
PY
```
Artifacts are written under `processes/<id>/data/`: `presentation.md`, `Final_story.md`, `Final_slides.html`, and `final_presentation.pdf`.

### 5) Ingest Markdown into Qdrant
```bash
uv run python - <<'PY'
from document_processing.vector_store import ingest_markdown_file_to_qdrant, retrieve_context
collection = ingest_markdown_file_to_qdrant("data/documents/mydoc/text/document.md")
results = retrieve_context("What are the main findings?", collection, k=3)
for doc in results:
    print(doc.page_content[:200], "...\n")
PY
```

### 6) Run the worker directly
```bash
uv run python -m src.worker.sqs_worker
```
Requires SQS, Supabase, and S3 env vars. Messages should include `process_id`, `user_query`, optional `num_slides`, and `file_ids` resolvable via Supabase metadata.

## Runtime outputs and conventions
- **Data roots:** `data/` in local runs, or `processes/<id>/data/` when using `ProcessContext`/worker.
- **Documents:** `data/documents/<doc>/images|tables|text|result.json`, hydrated mini-presentation at `data/mini_presentation_<doc>.md`.
- **Notebooks:** `data/notebook/<name>/...` plus `<name>_mini_presentation.md`; analysis notebooks from the MCP agent under `data/analysis/`.
- **Final deliverables:** `presentation.md`, `Final_story.md`, `Final_slides.html`, `final_presentation.pdf`.
- **Table hydration:** Any Markdown line like `(Table source: path/to/table.md)` will be replaced with the table contents by `hydrate_markdown_content`.

## Notes

- Keep assets under `data/` to respect the file-management tools’ root restrictions.
- The deep researcher tooling is optional; enable Tavily only if you need web research in your workflow.
