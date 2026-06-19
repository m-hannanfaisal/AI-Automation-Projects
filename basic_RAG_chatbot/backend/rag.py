import chromadb
from sentence_transformers import SentenceTransformer
import google.generativeai as genai

from config import DB_PATH, GEMINI_KEY

# Setup Gemini
genai.configure(api_key=GEMINI_KEY)
model_llm = genai.GenerativeModel("gemini-3-flash-preview")

# Embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path=DB_PATH)
collection = client.get_or_create_collection("chatbot_docs")


def get_embedding(text):
    return model.encode(text).tolist()


def search_docs(query, top_k=3):
    query_embedding = get_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results["documents"][0]


def generate_answer(query):
    docs = search_docs(query)
    context = "\n".join(docs)

    prompt = f"""
You are a helpful AI assistant.

Use ONLY the context below to answer the user.

Context:
{context}

Question:
{query}

Answer in a clear and helpful way:
"""

    response = model_llm.generate_content(prompt)
    return response.text