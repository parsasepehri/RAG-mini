import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.retrieve import retrieve

# ================================
# LLM Method Selection (activate only one)
# ================================

# --- Option 1: Ollama (local, free) ---
def answer_with_ollama(question: str, context: str, model: str = "tinyteapot") -> str:
    import requests
    prompt = f"""Answer the question based ONLY on the following context.
If the answer is not in the context, say "I don't know".

Context:
{context}

Question: {question}

Answer:"""
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": model, "prompt": prompt, "stream": False},
            timeout=60
        )
        return response.json()["response"]
    except Exception as e:
        return f"Error calling Ollama: {e}"

# --- Option 2: OpenAI API ---
def answer_with_openai(question: str, context: str, model: str = "gpt-3.5-turbo") -> str:
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = f"""Answer the question based ONLY on the following context.
If the answer is not in the context, say "I don't know".

Context:
{context}

Question: {question}

Answer:"""
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error calling OpenAI: {e}"

# ================================
# Default method (change as needed)
# ================================
LLM_METHOD = "ollama"   # or "openai"

def get_llm_answer(question: str, context: str):
    if LLM_METHOD == "ollama":
        return answer_with_ollama(question, context)
    elif LLM_METHOD == "openai":
        return answer_with_openai(question, context)
    else:
        return "LLM method not configured. Please edit rag_qa.py and set LLM_METHOD."

def rag_qa(question: str, top_k: int = 3):
    print("Retrieving relevant chunks...")
    chunks = retrieve(question, top_k)
    context = "\n\n---\n\n".join([chunk[0] for chunk in chunks])
    print("Generating answer with LLM...")
    answer = get_llm_answer(question, context)
    return answer

if __name__ == "__main__":
    print("NOTE: LLM part is NOT tested due to resource constraints.")
    print("You must install Ollama or set OpenAI API key.\n")
    q = input("Your question: ")
    ans = rag_qa(q)
    print("\nAnswer:\n", ans)