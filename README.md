# ✨ Personal Assistant — AI Chatbot

Proyek UAS Praktikum NLP — Aplikasi **Personal Assistant** berbasis AI yang memungkinkan pengguna berinteraksi secara natural melalui antarmuka chat. Dibangun menggunakan **FastAPI** (backend) dan **Vue 3 + Vite** (frontend), dengan model **LLaMA 3.3 70B** via Groq API dan orkestrasi agen menggunakan **LangGraph**.

---

## 🖼️ Tampilan Aplikasi

Antarmuka chat mendukung **Light Mode** dan **Dark Mode**, dilengkapi sidebar riwayat percakapan, tombol New Chat, serta fitur Export percakapan ke file `.txt`.

---

## 🧱 Struktur Folder

```
UAS_PRAKTIKUMNLP/
├── backend/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── graph.py          # LangGraph agent & SQLite checkpointer
│   │   ├── notes_store.py    # Penyimpanan catatan berbasis JSON
│   │   ├── state.py          # Definisi AssistantState untuk LangGraph
│   │   └── tools.py          # Tools: datetime, kalkulator, catatan
│   ├── data/
│   │   ├── notes.json        # Penyimpanan catatan (auto-generated)
│   │   └── memory.db         # Riwayat percakapan SQLite (auto-generated)
│   ├── .env                  # API key & konfigurasi (jangan di-commit!)
│   ├── app.py                # Entry point FastAPI
│   ├── config.py             # Load environment variables
│   └── requirements.txt      # Dependensi Python
│
└── frontend/
    ├── public/
    │   ├── favicon.svg
    │   └── icons.svg
    ├── src/
    │   ├── App.vue            # Komponen utama (chat UI lengkap)
    │   ├── main.js            # Entry point Vue
    │   └── style.css          # Global styles
    ├── assets/
    │   └── styles.css
    ├── index.html
    ├── package.json
    └── vite.config.js
```

---

## ✨ Fitur

| Fitur | Deskripsi |
|---|---|
| 💬 Chat AI | Percakapan natural dengan LLaMA 3.3 70B via Groq API |
| 📝 Catatan Pribadi | Simpan, tampilkan, cari, dan hapus catatan antar sesi |
| 🧮 Kalkulator | Hitung ekspresi matematika langsung dari pesan chat |
| 🕐 Waktu & Tanggal | Cek waktu dan tanggal saat ini secara real-time |
| 🧠 Memori Percakapan | Riwayat chat tersimpan persisten via SQLite checkpointer |
| 📂 Multi-Chat | Buat, pindah, dan hapus sesi percakapan berbeda |
| 🌙 Dark / Light Mode | Tema gelap dan terang, tersimpan di localStorage |
| 📄 Export Chat | Ekspor percakapan ke file `.txt` |
| 📋 Copy Pesan | Salin balasan asisten dengan satu klik |
| 📊 LangSmith Tracing | Monitoring dan observabilitas AI agent |

---

## 🛠️ Tech Stack

**Backend**
- [FastAPI](https://fastapi.tiangolo.com/) — Web framework Python
- [LangGraph](https://langchain-ai.github.io/langgraph/) — Orkestrasi AI agent dengan StateGraph
- [LangChain](https://www.langchain.com/) — Framework integrasi LLM dan tools
- [Groq API](https://groq.com/) — Inferensi cepat model LLaMA 3.3 70B Versatile
- [LangSmith](https://www.langchain.com/langsmith) — Tracing dan observabilitas AI
- SQLite — Penyimpanan riwayat percakapan persisten

**Frontend**
- [Vue 3](https://vuejs.org/) — Framework UI reaktif dengan Composition API
- [Vite](https://vitejs.dev/) — Build tool modern
- [Axios](https://axios-http.com/) — HTTP client untuk komunikasi ke API

---

## ⚙️ Persyaratan Sistem

- Python **3.10+**
- Node.js **18+** dan npm
- API Key dari [Groq](https://console.groq.com/) *(gratis)*
- API Key dari [LangSmith](https://smith.langchain.com/) *(opsional, untuk tracing)*

---

## 🚀 Instalasi & Menjalankan

### 1. Clone Repository

```bash
git clone https://github.com/Adindameilaniputri/UAS_PRAKTIKUMNLP.git
cd UAS_PRAKTIKUMNLP
```

---

### 2. Setup Backend

#### a. Masuk ke folder backend

```bash
cd backend
```

#### b. Buat virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

#### c. Install dependensi

```bash
pip install -r requirements.txt
```

Selain itu, install juga paket yang digunakan langsung di kode:

```bash
pip install fastapi uvicorn langchain-groq
```

#### d. Konfigurasi file `.env`

Buka atau buat file `.env` di dalam folder `backend/`:

```env
GROQ_API_KEY=your_groq_api_key_here
LANGCHAIN_API_KEY=your_langsmith_api_key_here
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=PersonalAssistant
```

> **Cara mendapat API key:**
> - **Groq:** Daftar di [console.groq.com](https://console.groq.com/) → buat API key baru (gratis)
> - **LangSmith:** Daftar di [smith.langchain.com](https://smith.langchain.com/) → buat API key *(opsional)*

> ⚠️ **Jangan pernah commit file `.env` ke GitHub!**

#### e. Jalankan server backend

```bash
uvicorn app:app --reload
```

Server berjalan di: **http://localhost:8000**

Cek status server:
```
http://localhost:8000/
```

Respons yang diharapkan:
```json
{
  "status": "ok",
  "message": "Personal Assistant is running 🚀"
}
```

Dokumentasi API otomatis (Swagger UI):
```
http://localhost:8000/docs
```

---

### 3. Setup Frontend

#### a. Masuk ke folder frontend

```bash
cd ../frontend
```

#### b. Install dependensi Node

```bash
npm install
```

#### c. Jalankan development server

```bash
npm run dev
```

Aplikasi berjalan di: **http://localhost:5173**

---

## 🖥️ Menjalankan Keduanya Sekaligus

Buka **dua terminal** secara bersamaan:

**Terminal 1 — Backend:**
```bash
cd backend
source venv/bin/activate        # Windows: venv\Scripts\activate
uvicorn app:app --reload
```

**Terminal 2 — Frontend:**
```bash
cd frontend
npm run dev
```

Kemudian buka browser di **http://localhost:5173** 🎉

---

## 📡 Endpoint API

### `GET /`
Mengecek status server.

**Response:**
```json
{
  "status": "ok",
  "message": "Personal Assistant is running 🚀"
}
```

---

### `POST /chat`
Mengirim pesan ke AI dan mendapatkan balasan.

**Request Body:**
```json
{
  "message": "Catat: beli susu besok pagi",
  "thread_id": "user1"
}
```

| Field | Tipe | Default | Deskripsi |
|---|---|---|---|
| `message` | `string` | — | Pesan yang dikirim ke AI |
| `thread_id` | `string` | `"default"` | ID sesi percakapan |

**Response:**
```json
{
  "reply": "Baik, catatan 'beli susu besok pagi' sudah tersimpan! 📝"
}
```

---

## 🧠 Arsitektur AI Agent

```
User Input (Frontend Vue)
        │
        ▼
  POST /chat (FastAPI)
        │
        ▼
  LangGraph StateGraph
        │
        ├──► assistant node
        │      └─ LLaMA 3.3 70B via Groq
        │           └─ Jika butuh tool ──► tools node
        │                                     ├── get_current_datetime
        │                                     ├── calculator
        │                                     ├── add_note
        │                                     ├── list_notes
        │                                     ├── search_notes
        │                                     └── delete_note
        │
        ▼
  SQLite Checkpointer
  (simpan riwayat percakapan)
        │
        ▼
  Response → Frontend
```

---

## 🔧 Tools yang Tersedia

| Tool | Deskripsi | Contoh Penggunaan |
|---|---|---|
| `get_current_datetime` | Mengembalikan waktu dan tanggal saat ini | *"Jam berapa sekarang?"* |
| `calculator` | Menghitung ekspresi matematika (`+ - * / ** %`) | *"Hitung 12 * (3 + 4) / 2"* |
| `add_note` | Menyimpan catatan/pengingat baru | *"Catat: rapat jam 3 sore"* |
| `list_notes` | Menampilkan semua catatan tersimpan | *"Tampilkan semua catatanku"* |
| `search_notes` | Mencari catatan berdasarkan kata kunci | *"Cari catatan tentang rapat"* |
| `delete_note` | Menghapus catatan berdasarkan ID | *"Hapus catatan nomor 2"* |

---

## 📁 File `.gitignore` yang Direkomendasikan

Buat file `.gitignore` di root project:

```gitignore
# Python
__pycache__/
*.pyc
*.pyo
venv/
testenv/
.env

# Data (hapus baris ini jika ingin menyertakan contoh data)
backend/data/memory.db
backend/data/notes.json

# Node
node_modules/
dist/
dist-ssr/
*.local

# Editor
.vscode/
.idea/
.DS_Store
```

---

## 🐛 Troubleshooting

**`ModuleNotFoundError: No module named 'langchain_groq'`**
```bash
pip install langchain-groq
```

**`ModuleNotFoundError: No module named 'fastapi'` atau `uvicorn`**
```bash
pip install fastapi uvicorn
```

**`GROQ_API_KEY tidak ditemukan` / model tidak merespons**
- Pastikan file `.env` ada di dalam folder `backend/`
- Pastikan nama variabel persis `GROQ_API_KEY` (huruf kapital semua)
- Coba jalankan `echo $GROQ_API_KEY` (Linux/Mac) atau `echo %GROQ_API_KEY%` (Windows)

**Frontend error: `❌ Gagal terhubung ke backend`**
- Pastikan backend sudah berjalan di port `8000`
- Periksa apakah ada pesan error di terminal backend

**Port sudah dipakai**
```bash
# Jalankan di port lain
uvicorn app:app --reload --port 8001
```
Lalu update URL di `frontend/src/App.vue` baris axios dari `8000` ke `8001`.

---

## 👩‍💻 Dibuat Oleh

**Adinda Meilani Putri**  
UAS Praktikum Natural Language Processing

---

> Dibangun dengan ❤️ menggunakan FastAPI · LangGraph · LangChain · Groq · Vue 3
