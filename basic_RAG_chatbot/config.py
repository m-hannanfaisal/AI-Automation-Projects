import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_KEY = os.getenv("GOOGLE_API_KEY")

DOCS_PATH = r"C:\Users\HP\Downloads\chatbot1\docs_project"
DB_PATH = r"C:\Users\HP\Downloads\chatbot1\chroma_db"