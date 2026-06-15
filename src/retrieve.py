import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.embedder import embed_text
from src.db import get_connection

def retrieve(query: str, top_k: int = 3):
    query_embedding = embed_text(query)
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT chunk_text, document_name, chunk_index,
                   1 - (embedding <=> %s::vector) AS similarity
            FROM chunks
            ORDER BY embedding <=> %s::vector
            LIMIT %s
            """,
            (query_embedding.tolist(), query_embedding.tolist(), top_k)
        )
        results = cur.fetchall()
    conn.close()
    return results

if __name__ == "__main__":
    q = input("Your question: ")
    results = retrieve(q, top_k=3)
    print(f"\nTop {len(results)} results:\n")
    for i, (text, doc_name, idx, sim) in enumerate(results):
        print(f"{i+1}. [{doc_name} | chunk {idx} | similarity={sim:.4f}]")
        print(f"{text[:300]}...\n")