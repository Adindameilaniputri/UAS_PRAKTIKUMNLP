"""
Definisi State (skema data) yang dialirkan di antara node-node LangGraph.
"""

from typing import Annotated
from typing_extensions import TypedDict

from langgraph.graph.message import add_messages


class AssistantState(TypedDict):
    """State percakapan asisten.

    `messages` menggunakan reducer `add_messages` dari LangGraph
    sehingga setiap node cukup mengembalikan pesan baru, dan LangGraph
    akan otomatis menggabungkannya dengan riwayat percakapan sebelumnya.
    """

    messages: Annotated[list, add_messages]
