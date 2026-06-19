"""
Kumpulan "tools" (kemampuan) yang dapat dipanggil oleh model Groq
melalui mekanisme tool-calling LangChain. Setiap fungsi yang diberi
dekorator @tool akan otomatis dikenali sebagai kemampuan oleh agent.
"""

import ast
import operator
from datetime import datetime

from langchain_core.tools import tool

from core import notes_store


# ---------------------------------------------------------------------------
# Tool: waktu & tanggal
# ---------------------------------------------------------------------------
@tool
def get_current_datetime() -> str:
    """Mendapatkan tanggal dan waktu saat ini secara lengkap."""
    return datetime.now().strftime("%A, %d %B %Y - %H:%M:%S")


# ---------------------------------------------------------------------------
# Tool: kalkulator aman (tanpa eval() langsung)
# ---------------------------------------------------------------------------
_ALLOWED_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
}


def _safe_eval(node):
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Hanya angka yang diperbolehkan dalam ekspresi.")
    if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_OPS:
        return _ALLOWED_OPS[type(node.op)](_safe_eval(node.left), _safe_eval(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_OPS:
        return _ALLOWED_OPS[type(node.op)](_safe_eval(node.operand))
    raise ValueError("Ekspresi matematika tidak didukung.")


@tool
def calculator(expression: str) -> str:
    """Menghitung ekspresi matematika sederhana.

    Contoh input: "12 * (3 + 4) / 2" atau "2 ** 10".
    Hanya mendukung operator + - * / ** % dan tanda kurung.
    """
    try:
        tree = ast.parse(expression, mode="eval")
        result = _safe_eval(tree.body)
        return str(result)
    except Exception as exc:  # noqa: BLE001
        return f"Gagal menghitung ekspresi: {exc}"


# ---------------------------------------------------------------------------
# Tool: catatan pribadi (personal notes)
# ---------------------------------------------------------------------------
@tool
def add_note(content: str) -> str:
    """Menyimpan catatan/pengingat pribadi baru.

    Gunakan tool ini ketika pengguna minta dicatat sesuatu,
    misalnya tugas, ide, atau pengingat.
    """
    note_id = notes_store.add_note(content)
    return f"Catatan tersimpan dengan id {note_id}: \"{content}\""


@tool
def list_notes() -> str:
    """Menampilkan semua catatan pribadi yang tersimpan."""
    notes = notes_store.list_notes()
    if not notes:
        return "Belum ada catatan tersimpan."
    baris = [f"[{n['id']}] {n['content']} (dibuat: {n['created_at']})" for n in notes]
    return "\n".join(baris)


@tool
def search_notes(keyword: str) -> str:
    """Mencari catatan pribadi yang mengandung kata kunci tertentu."""
    hasil = notes_store.search_notes(keyword)
    if not hasil:
        return f"Tidak ditemukan catatan yang cocok dengan kata kunci '{keyword}'."
    baris = [f"[{n['id']}] {n['content']}" for n in hasil]
    return "\n".join(baris)


@tool
def delete_note(note_id: int) -> str:
    """Menghapus sebuah catatan pribadi berdasarkan id-nya."""
    berhasil = notes_store.delete_note(note_id)
    if berhasil:
        return f"Catatan dengan id {note_id} berhasil dihapus."
    return f"Catatan dengan id {note_id} tidak ditemukan."


TOOLS = [
    get_current_datetime,
    calculator,
    add_note,
    list_notes,
    search_notes,
    delete_note,
]
