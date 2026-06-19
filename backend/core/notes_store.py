"""
Penyimpanan catatan pribadi sederhana berbasis file JSON.
Digunakan oleh tools (add_note, list_notes, search_notes, delete_note)
sehingga asisten dapat "mengingat" data pribadi pengguna antar sesi.
"""

import json
import os
from datetime import datetime
from threading import Lock

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DATA_DIR = os.path.join(_BASE_DIR, "data")
_NOTES_PATH = os.path.join(_DATA_DIR, "notes.json")
_lock = Lock()


def _ensure_store() -> None:
    os.makedirs(_DATA_DIR, exist_ok=True)
    if not os.path.exists(_NOTES_PATH):
        with open(_NOTES_PATH, "w", encoding="utf-8") as f:
            json.dump([], f)


def _read_all() -> list:
    _ensure_store()
    with open(_NOTES_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _write_all(notes: list) -> None:
    with open(_NOTES_PATH, "w", encoding="utf-8") as f:
        json.dump(notes, f, ensure_ascii=False, indent=2)


def add_note(content: str) -> int:
    with _lock:
        notes = _read_all()
        new_id = max((n["id"] for n in notes), default=0) + 1
        notes.append(
            {
                "id": new_id,
                "content": content,
                "created_at": datetime.now().isoformat(timespec="seconds"),
            }
        )
        _write_all(notes)
        return new_id


def list_notes() -> list:
    with _lock:
        return _read_all()


def search_notes(keyword: str) -> list:
    with _lock:
        notes = _read_all()
        keyword_lower = keyword.lower()
        return [n for n in notes if keyword_lower in n["content"].lower()]


def delete_note(note_id: int) -> bool:
    with _lock:
        notes = _read_all()
        filtered = [n for n in notes if n["id"] != note_id]
        if len(filtered) == len(notes):
            return False
        _write_all(filtered)
        return True
