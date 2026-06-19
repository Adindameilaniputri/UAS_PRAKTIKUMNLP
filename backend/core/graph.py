"""
Inti dari sistem: membangun graph LangGraph yang menghubungkan
model grokapi dengan tools, serta menyimpan
riwayat percakapan secara persisten menggunakan SQLite checkpointer.
"""

import os
import sqlite3
from dotenv import load_dotenv 

load_dotenv()



from langchain_core.messages import SystemMessage
from langchain_groq import ChatGroq
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import StateGraph, START
from langgraph.prebuilt import ToolNode, tools_condition

from core.state import AssistantState
from core.tools import TOOLS

SYSTEM_PROMPT = (
    "Kamu adalah asisten pribadi yang ramah, ringkas, dan suka membantu. "
    "Gunakan tools yang tersedia bila relevan, misalnya untuk mencatat "
    "sesuatu, mencari catatan lama, menghitung angka, atau mengecek waktu "
    "saat ini. Jangan mengarang isi catatan; selalu gunakan tool list_notes "
    "atau search_notes untuk membacanya. Jawab dalam Bahasa Indonesia, "
    "kecuali pengguna menulis dalam bahasa lain."
)

_DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "memory.db")


def _build_model():
    return ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.4,
        api_key=os.getenv("GROQ_API_KEY")
    ).bind_tools(TOOLS)


def _build_checkpointer() -> SqliteSaver:
    """Checkpointer SQLite agar riwayat percakapan tetap ada walau program ditutup."""
    os.makedirs(os.path.dirname(_DB_PATH), exist_ok=True)
    conn = sqlite3.connect(_DB_PATH, check_same_thread=False)
    return SqliteSaver(conn)


def build_graph():
    model = _build_model()

    def assistant_node(state: AssistantState):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + state["messages"]
        response = model.invoke(messages)
        return {"messages": [response]}

    graph_builder = StateGraph(AssistantState)
    graph_builder.add_node("assistant", assistant_node)
    graph_builder.add_node("tools", ToolNode(TOOLS))

    graph_builder.add_edge(START, "assistant")
    graph_builder.add_conditional_edges("assistant", tools_condition)
    graph_builder.add_edge("tools", "assistant")

    checkpointer = _build_checkpointer()
    return graph_builder.compile(checkpointer=checkpointer)