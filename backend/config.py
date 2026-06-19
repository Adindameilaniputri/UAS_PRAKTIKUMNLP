import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")

def setup_environment():
    os.environ["LANGCHAIN_TRACING_V2"]=os.getenv("LANGCHAIN_TRACING_V2","true")
    os.environ["LANGCHAIN_PROJECT"]=os.getenv("LANGCHAIN_PROJECT","PersonalAssistant")
