from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv()


def get_llm():
    model = os.getenv("GEMINI_MODEL")
    api_key = os.getenv("GOOGLE_API_KEY")
    if not model or not api_key:
        raise RuntimeError("Set GEMINI_MODEL and GOOGLE_API_KEY in environment")


    llm = ChatGoogleGenerativeAI(
    model=model,
    temperature=0,
    google_api_key=api_key,
    )
    return llm