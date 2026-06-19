import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb
from sentence_transformers import SentenceTransformer

from config import DOCS_PATH, DB_PATH


# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def get_embedding(text):
    return model.encode(text).tolist()


def load_documents():
    docs = []
    
    for file in os.listdir(DOCS_PATH):
        if file.endswith(".txt"):
            loader = TextLoader(os.path.join(DOCS_PATH, file), encoding="utf-8")
            docs.extend(loader.load())
    
    return docs


def split_docs(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    return splitter.split_documents(docs)


def main():
    print("Loading documents...")
    docs = load_documents()

    print("Splitting documents...")
    chunks = split_docs(docs)

    print("Creating vector DB...")

    client = chromadb.PersistentClient(path=DB_PATH)
    collection = client.get_or_create_collection("chatbot_docs")

    for i, chunk in enumerate(chunks):
        collection.add(
            ids=[str(i)],
            documents=[chunk.page_content],
            embeddings=[get_embedding(chunk.page_content)]
        )

    print("Done! Documents stored in Chroma DB")


if __name__ == "__main__":
    main()