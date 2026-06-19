from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from core.graph import build_graph
from langchain_core.messages import HumanMessage

app = FastAPI(title="Personal Assistant API")

# CORS biar Vue bisa akses
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=".*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

graph = None


class ChatRequest(BaseModel):
    message: str
    thread_id: str = "default"


@app.on_event("startup")
def startup_event():
    global graph
    graph = build_graph()


@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "Personal Assistant is running 🚀"
    }


@app.post("/chat")
def chat(req: ChatRequest):
    global graph

    if graph is None:
        return {"error": "Graph belum siap"}

    result = graph.invoke(
        {
            "messages": [
                HumanMessage(content=req.message)
            ]
        },
        config={
            "configurable": {
                "thread_id": req.thread_id
            }
        }
    )

    content = result["messages"][-1].content

    # DEBUG
    print("\n=== DEBUG CONTENT ===")
    print(content)
    print(type(content))
    print("=====================\n")

    # Jika Gemini mengembalikan list
    if isinstance(content, list):
        text_parts = []

        for item in content:
            if isinstance(item, dict):
                if item.get("type") == "text":
                    text_parts.append(item.get("text", ""))

        content = "\n".join(text_parts)

    # Jika masih bukan string
    if not isinstance(content, str):
        content = str(content)

    return {
        "reply": content
    }