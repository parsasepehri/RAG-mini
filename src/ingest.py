import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.pdf_loader import load_pdf
from src.chunker import chunk_text
from src.embedder import embed_text
from src.db import get_connection, init_table

def ingest_pdf(pdf_path: str, doc_name: str = None):
    if doc_name is None:
        doc_name = os.path.basename(pdf_path)

    print(f"Loading PDF: {pdf_path}")
    text = load_pdf(pdf_path)
    print(f"Total characters: {len(text)}")

    print("Chunking...")
    chunks = chunk_text(text, chunk_size=500, overlap=100)
    print(f"Number of chunks: {len(chunks)}")

    conn = get_connection()
    init_table(conn)

    with conn.cursor() as cur:
        for idx, chunk in enumerate(chunks):
            print(f"Processing chunk {idx+1}/{len(chunks)}...")
            embedding = embed_text(chunk)
            cur.execute(
                """
                INSERT INTO chunks (document_name, chunk_index, chunk_text, embedding)
                VALUES (%s, %s, %s, %s)
                """,
                (doc_name, idx, chunk, embedding.tolist())
            )
        conn.commit()

    print("Ingestion finished successfully!")
    conn.close()

if __name__ == "__main__":
    ingest_pdf("data/sample.pdf")   # مسیر PDF خود را تنظیم کنید