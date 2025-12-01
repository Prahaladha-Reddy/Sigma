import os
import re
from typing import List, Tuple

from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from langchain_core.documents import Document
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_google_embeddings():
    """
    Initializes the Google Generative AI Embeddings.
    Ensure GOOGLE_API_KEY is set in your environment.
    """
    if not os.getenv("GOOGLE_API_KEY"):
        raise ValueError("GOOGLE_API_KEY environment variable is not set")
    
    # Using the standard model 'models/embedding-001' or 'models/text-embedding-004'
    return GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

def get_qdrant_credentials() -> Tuple[str, str]:
    """Helper to fetch Qdrant credentials from environment."""
    url = os.getenv("QDRANT_URL")
    key = os.getenv("QDRANT_API_KEY")
    if not url or not key:
        raise ValueError("QDRANT_URL and QDRANT_API_KEY environment variables must be set")
    return url, key

def ingest_markdown_file_to_qdrant(file_path: str):
    """
    Reads a markdown file, splits it by headers, embeds it, and pushes to Qdrant Cloud.
    The collection name is derived automatically from the directory structure.
    
    Args:
        file_path (str): The path to the markdown file.
        
    Returns:
        Tuple[str, str]: (Success message, Collection Name used)
    """
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file '{file_path}' was not found.")

    # 1. Derive Collection Name from Path structure
    # Logic: If path is ".../{CollectionName}/text/document.md", extract "{CollectionName}"
    # We check if the immediate parent folder is named "text". 
    # If yes, we take the grandparent folder name. Otherwise, we fallback to filename.
    
    abs_path = os.path.abspath(file_path)
    parent_dir_path = os.path.dirname(abs_path)
    parent_dir_name = os.path.basename(parent_dir_path)
    
    if parent_dir_name == 'text':
        # Structure matches: .../CollectionName/text/document.md
        grandparent_dir_path = os.path.dirname(parent_dir_path)
        raw_collection_name = os.path.basename(grandparent_dir_path)
    else:
        # Fallback for flat files or different structures
        raw_collection_name = os.path.splitext(os.path.basename(file_path))[0]
    
    # Sanitize: replace special chars with underscores, but PRESERVE CASE
    # Qdrant allows: letters, numbers, hyphens, and underscores
    collection_name = re.sub(r'[^a-zA-Z0-9_-]', '_', raw_collection_name)
    print(collection_name)
    # 2. Read the file content
    with open(file_path, 'r', encoding='utf-8') as f:
        markdown_text = f.read()

    # 3. Define headers to split on
    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
    ]

    # 4. Split the markdown text
    markdown_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=headers_to_split_on, 
        strip_headers=False
    )
    docs = markdown_splitter.split_text(markdown_text)
    
    print(f"Read file '{file_path}', derived collection name '{collection_name}', and split into {len(docs)} chunks.")

    embeddings = get_google_embeddings()
    qdrant_url, qdrant_api_key = get_qdrant_credentials()

    QdrantVectorStore.from_documents(
        documents=docs,
        embedding=embeddings,
        url=qdrant_url,
        api_key=qdrant_api_key,
        collection_name=collection_name,
        prefer_grpc=True
    )
    
    return collection_name


def retrieve_context(query: str, collection_name: str, k: int = 4) -> List[Document]:
    """
    Retrieves relevant text chunks from Qdrant based on a text query.
    
    Args:
        query (str): The question or search text.
        collection_name (str): The collection to search in.
        k (int): Number of results to return.
        
    Returns:
        List[Document]: A list of matched LangChain Documents.
    """
    
    # 1. Initialize Embeddings & Credentials
    embeddings = get_google_embeddings()
    qdrant_url, qdrant_api_key = get_qdrant_credentials()

    vector_store = QdrantVectorStore.from_existing_collection(
        embedding=embeddings,
        collection_name=collection_name,
        url=qdrant_url,
        api_key=qdrant_api_key,
        prefer_grpc=True
    )

    results = vector_store.similarity_search(query, k=k)
    
    return results

if __name__ == "__main__":
    try:
        print("--- Ingesting Data from File ---")
        

        target_file = "data/documents/WP-514-Fakih-Amrin-Kamaluddin-Final/text/document.md" 
        
        message, collection_name = ingest_markdown_file_to_qdrant(target_file)
        print(message)
        print(f"Using Collection Name: {collection_name}")

        print("\n--- Retrieving Data ---")
        user_query = "What are the milestones for Q1?"
        
        results = retrieve_context(user_query, collection_name)

        for i, doc in enumerate(results):
            print(f"\nResult {i+1}:")
            print(f"Content: {doc.page_content}")
            print(f"Metadata: {doc.metadata}")

    except Exception as e:
        print(f"Error: {e}")
        print("Please ensure GOOGLE_API_KEY, QDRANT_URL, and QDRANT_API_KEY are set in your environment or .env file.")
