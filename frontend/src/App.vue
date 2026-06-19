<template>
  <div :class="['app', { dark: darkMode }]">

    <!-- Sidebar -->
    <aside class="sidebar">

      <div class="logo">✨ Personal Assistant</div>

      <button class="new-chat-btn" @click="newChat">+ New Chat</button>

      <div class="history">
        <div
          v-for="(chat, index) in chatHistory"
          :key="index"
          :class="['history-item', { active: index === activeChatIndex }]"
          @click="switchChat(index)"
        >
          <span>💬 {{ chat.title }}</span>
          <button class="delete-btn" @click.stop="deleteChat(index)">×</button>
        </div>
      </div>

      <div class="sidebar-footer">
        <button class="theme-btn" @click="toggleTheme">
          {{ darkMode ? '☀️ Light Mode' : '🌙 Dark Mode' }}
        </button>
        <div>🤖 Groq API</div>
        <div>🧠 LangGraph Active</div>
        <div>🔗 LangChain Active</div>
        <div>📊 LangSmith Active</div>

      </div>

    </aside>

    <!-- Main -->
    <main class="main">

      <header class="header">
        <div>
          <h1>Personal Assistant</h1>
          <span>Groq AI • LangGraph • LangChain • LangSmith</span>
        </div>
        <div class="header-actions">
          <button class="action-btn" @click="clearChat" title="Clear chat">🗑️ Clear</button>
          <button class="action-btn" @click="exportChat" title="Export TXT">📄 Export</button>
          <div class="status">🟢 Online</div>
        </div>
      </header>

      <div class="chat-box" ref="chatBox">

        <!-- Welcome -->
        <div v-if="messages.length === 0" class="welcome">
          <h2>👋 Halo Dinda</h2>
          <p>Ada yang ingin kamu tanyakan hari ini?</p>
          <div class="feature-list">
            <div class="feature-card" @click="quickPrompt('Tampilkan semua catatan saya')">🧠 Memory</div>
            <div class="feature-card" @click="quickPrompt('Tampilkan notes saya')">📒 Notes</div>
            <div class="feature-card" @click="quickPrompt('Hitungkan sesuatu')">🧮 Calculator</div>
            <div class="feature-card" @click="quickPrompt('Apa kemampuanmu?')">🤖 Groq AI</div>
          </div>
        </div>

        <!-- Messages -->
        <div
          v-for="(msg, index) in messages"
          :key="index"
          :class="['message', msg.role.toLowerCase()]"
        >
          <div class="avatar">{{ msg.role === 'User' ? '👩' : '🤖' }}</div>

          <div class="bubble-wrapper">
            <div class="bubble" v-html="renderMarkdown(msg.content)"></div>
            <div class="msg-actions" v-if="msg.role === 'Assistant'">
              <button class="copy-btn" @click="copyMessage(msg.content, index)" :title="copiedIndex === index ? 'Disalin!' : 'Salin'">
                {{ copiedIndex === index ? '✅' : '📋' }}
              </button>
            </div>
          </div>
        </div>

        <!-- Loading -->
        <div v-if="loading" class="message assistant">
          <div class="avatar">🤖</div>
          <div class="bubble typing">
            <span></span><span></span><span></span>
          </div>
        </div>

      </div>

      <!-- Input -->
      <div class="input-area">
        <textarea
          v-model="message"
          placeholder="Ketik pesan... (Enter kirim, Shift+Enter baris baru)"
          @keydown.enter.exact.prevent="sendMessage"
          rows="1"
          ref="inputRef"
        ></textarea>
        <button @click="sendMessage" :disabled="loading">➤</button>
      </div>

    </main>
  </div>
</template>

<script setup>
import { ref, nextTick, watch, onMounted } from "vue"
import axios from "axios"

// ─── State ───────────────────────────────────────────────
const message = ref("")
const loading = ref(false)
const chatBox = ref(null)
const inputRef = ref(null)
const copiedIndex = ref(null)
const darkMode = ref(false)
const activeChatIndex = ref(0)

const messages = ref([])
const chatHistory = ref([])

// ─── Init from localStorage ───────────────────────────────
onMounted(() => {
  darkMode.value = localStorage.getItem("theme") === "dark"

  const saved = localStorage.getItem("chatHistory")
  if (saved) {
    try {
      chatHistory.value = JSON.parse(saved)
    } catch {
      chatHistory.value = []
    }
  }

  if (chatHistory.value.length === 0) {
    chatHistory.value = [{ title: "Percakapan Baru", messages: [] }]
  }

  messages.value = chatHistory.value[activeChatIndex.value].messages
})

// ─── Persist chatHistory on change ───────────────────────
watch(chatHistory, (val) => {
  localStorage.setItem("chatHistory", JSON.stringify(val))
}, { deep: true })

// ─── Dark mode ───────────────────────────────────────────
function toggleTheme() {
  darkMode.value = !darkMode.value
  localStorage.setItem("theme", darkMode.value ? "dark" : "light")
}

// ─── Chat management ─────────────────────────────────────
function newChat() {
  const chat = { title: "Chat Baru", messages: [] }
  chatHistory.value.unshift(chat)
  activeChatIndex.value = 0
  messages.value = chat.messages
}

function switchChat(index) {
  activeChatIndex.value = index
  messages.value = chatHistory.value[index].messages
  scrollBottom()
}

function deleteChat(index) {
  chatHistory.value.splice(index, 1)
  if (chatHistory.value.length === 0) {
    chatHistory.value = [{ title: "Percakapan Baru", messages: [] }]
  }
  activeChatIndex.value = 0
  messages.value = chatHistory.value[0].messages
}

function clearChat() {
  if (!confirm("Hapus semua pesan di chat ini?")) return
  messages.value.splice(0)
  chatHistory.value[activeChatIndex.value].messages = messages.value
  chatHistory.value[activeChatIndex.value].title = "Chat Baru"
}

// ─── Auto-title ──────────────────────────────────────────
function autoTitle(text) {
  const title = text.slice(0, 30).replace(/\n/g, " ").trim()
  chatHistory.value[activeChatIndex.value].title = title || "Percakapan"
}

// ─── Export TXT ──────────────────────────────────────────
function exportChat() {
  const lines = messages.value.map(m => `[${m.role}]\n${m.content}`).join("\n\n---\n\n")
  const blob = new Blob([lines], { type: "text/plain" })
  const url = URL.createObjectURL(blob)
  const a = document.createElement("a")
  a.href = url
  a.download = `chat-${Date.now()}.txt`
  a.click()
  URL.revokeObjectURL(url)
}

// ─── Copy message ─────────────────────────────────────────
function copyMessage(text, index) {
  navigator.clipboard.writeText(text).then(() => {
    copiedIndex.value = index
    setTimeout(() => { copiedIndex.value = null }, 2000)
  })
}

// ─── Markdown renderer (lightweight) ─────────────────────
function renderMarkdown(text) {
  return text
    // Code blocks
    .replace(/```([\s\S]*?)```/g, (_, code) =>
      `<pre><code>${escapeHtml(code.trim())}</code></pre>`)
    // Inline code
    .replace(/`([^`]+)`/g, (_, c) => `<code>${escapeHtml(c)}</code>`)
    // Bold
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    // Italic
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    // Newlines
    .replace(/\n/g, '<br>')
}

function escapeHtml(str) {
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
}

// ─── Scroll ───────────────────────────────────────────────
function scrollBottom() {
  nextTick(() => {
    if (chatBox.value) chatBox.value.scrollTop = chatBox.value.scrollHeight
  })
}

// ─── Prompt shortcuts ─────────────────────────────────────
function quickPrompt(text) {
  if (loading.value) return
  message.value = text
  sendMessage()
}

// ─── Send message ─────────────────────────────────────────
async function sendMessage() {
  if (!message.value.trim()) return

  const text = message.value.trim()

  // Auto-title on first message
  if (messages.value.length === 0) autoTitle(text)

  messages.value.push({ role: "User", content: text })
  message.value = ""
  scrollBottom()
  loading.value = true

  // Reset textarea height
  nextTick(() => {
    if (inputRef.value) inputRef.value.style.height = "auto"
  })

  try {
    const response = await axios.post("http://127.0.0.1:8000/chat", {
      message: text,
      thread_id: "user1"
    })

    messages.value.push({
      role: "Assistant",
      content: response.data.reply
    })

  } catch (error) {
    console.error(error)
    messages.value.push({
      role: "Assistant",
      content: "❌ Gagal terhubung ke backend. Pastikan server FastAPI berjalan di port 8000."
    })
  } finally {
    loading.value = false
    scrollBottom()
  }
}
</script>

<style>
*, *::before, *::after {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', system-ui, sans-serif;
}

/* ─── CSS Variables ───────────────────────────────── */
.app {
  --bg-gradient: linear-gradient(135deg, #ffd6ea, #fbc2eb, #c9d6ff);
  --sidebar-bg: rgba(255, 255, 255, 0.15);
  --sidebar-border: rgba(255, 255, 255, 0.2);
  --text-main: white;
  --bubble-user-bg: #ff4f9d;
  --bubble-assistant-bg: white;
  --bubble-assistant-text: #333;
  --input-bg: white;
  --input-text: #333;
  --btn-primary: #ff4f9d;
  --history-bg: rgba(255, 255, 255, 0.15);
  --history-active: rgba(255, 255, 255, 0.35);
  --header-text: white;
  --action-btn-bg: rgba(255, 255, 255, 0.2);
  --code-bg: #f1f1f1;
  --code-text: #d63384;

  height: 100vh;
  display: flex;
  background: var(--bg-gradient);
  transition: background 0.3s;
}

/* ─── Dark Mode ───────────────────────────────────── */
.app.dark {
  --bg-gradient: linear-gradient(135deg, #1a0a2e, #2d1b4e, #0f2027);
  --sidebar-bg: rgba(0, 0, 0, 0.3);
  --sidebar-border: rgba(255, 255, 255, 0.08);
  --text-main: #eee;
  --bubble-user-bg: #c2185b;
  --bubble-assistant-bg: #1e1e2e;
  --bubble-assistant-text: #ddd;
  --input-bg: #1e1e2e;
  --input-text: #eee;
  --history-bg: rgba(255, 255, 255, 0.06);
  --history-active: rgba(255, 105, 180, 0.2);
  --header-text: #f0c0e0;
  --action-btn-bg: rgba(255, 255, 255, 0.08);
  --code-bg: #2a2a3e;
  --code-text: #ff79c6;
}

/* ─── Sidebar ─────────────────────────────────────── */
.sidebar {
  width: 280px;
  padding: 20px;
  background: var(--sidebar-bg);
  backdrop-filter: blur(20px);
  display: flex;
  flex-direction: column;
  border-right: 1px solid var(--sidebar-border);
  gap: 0;
}

.logo {
  font-size: 22px;
  font-weight: bold;
  color: var(--text-main);
  margin-bottom: 16px;
}

.new-chat-btn {
  border: none;
  background: var(--btn-primary);
  color: white;
  padding: 13px;
  border-radius: 14px;
  cursor: pointer;
  font-size: 15px;
  font-weight: 600;
  margin-bottom: 16px;
  transition: opacity 0.2s;
}
.new-chat-btn:hover { opacity: 0.85; }

.history {
  flex: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.history-item {
  background: var(--history-bg);
  color: var(--text-main);
  padding: 11px 12px;
  border-radius: 12px;
  cursor: pointer;
  font-size: 14px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: background 0.2s;
}
.history-item.active { background: var(--history-active); font-weight: 600; }
.history-item:hover { background: var(--history-active); }

.delete-btn {
  background: none;
  border: none;
  color: var(--text-main);
  font-size: 18px;
  cursor: pointer;
  opacity: 0.5;
  line-height: 1;
  padding: 0 2px;
  transition: opacity 0.2s;
}
.delete-btn:hover { opacity: 1; }

.sidebar-footer {
  color: var(--text-main);
  font-size: 13px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding-top: 16px;
  border-top: 1px solid var(--sidebar-border);
  margin-top: 12px;
}

.theme-btn {
  background: var(--action-btn-bg);
  border: none;
  color: var(--text-main);
  padding: 10px;
  border-radius: 10px;
  cursor: pointer;
  font-size: 13px;
  transition: background 0.2s;
}
.theme-btn:hover { opacity: 0.8; }

/* ─── Main ────────────────────────────────────────── */
.main {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.header {
  padding: 18px 28px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header h1 { color: var(--header-text); font-size: 22px; }
.header span { color: var(--header-text); font-size: 13px; opacity: 0.8; }

.header-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.action-btn {
  background: var(--action-btn-bg);
  border: none;
  color: var(--text-main);
  padding: 8px 14px;
  border-radius: 12px;
  cursor: pointer;
  font-size: 13px;
  backdrop-filter: blur(10px);
  transition: background 0.2s;
}
.action-btn:hover { opacity: 0.8; }

.status {
  background: #22c55e;
  color: white;
  padding: 8px 15px;
  border-radius: 20px;
  font-size: 14px;
}

/* ─── Chat ────────────────────────────────────────── */
.chat-box {
  flex: 1;
  overflow-y: auto;
  padding: 24px 30px;
  display: flex;
  flex-direction: column;
}

.welcome {
  text-align: center;
  margin: auto;
  color: var(--text-main);
  padding: 40px 20px;
}
.welcome h2 { font-size: 38px; margin-bottom: 10px; }
.welcome p { font-size: 16px; opacity: 0.85; }

.feature-list {
  margin-top: 28px;
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 14px;
}

.feature-card {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  padding: 14px 20px;
  border-radius: 14px;
  cursor: pointer;
  transition: transform 0.2s, background 0.2s;
  font-size: 15px;
}
.feature-card:hover {
  transform: translateY(-4px);
  background: rgba(255, 255, 255, 0.35);
}

/* ─── Messages ────────────────────────────────────── */
.message {
  display: flex;
  gap: 12px;
  margin-bottom: 18px;
  align-items: flex-start;
}

.message.user {
  justify-content: flex-end;
}
.message.user .avatar { order: 2; }
.message.user .bubble-wrapper { align-items: flex-end; }

.avatar {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  background: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  flex-shrink: 0;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.bubble-wrapper {
  display: flex;
  flex-direction: column;
  gap: 4px;
  max-width: 70%;
}

.bubble {
  padding: 13px 17px;
  border-radius: 18px;
  line-height: 1.65;
  font-size: 15px;
  word-break: break-word;
}

.user .bubble {
  background: var(--bubble-user-bg);
  color: white;
  border-bottom-right-radius: 4px;
}

.assistant .bubble {
  background: var(--bubble-assistant-bg);
  color: var(--bubble-assistant-text);
  border-bottom-left-radius: 4px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
}

/* Markdown inside bubbles */
.bubble pre {
  background: var(--code-bg);
  border-radius: 8px;
  padding: 12px;
  margin: 8px 0;
  overflow-x: auto;
  font-size: 13px;
}

.bubble code {
  background: var(--code-bg);
  color: var(--code-text);
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 13px;
  font-family: 'Courier New', monospace;
}

.bubble pre code {
  background: none;
  color: inherit;
  padding: 0;
}

/* ─── Copy button ────────────────────────────────── */
.msg-actions {
  display: flex;
  gap: 6px;
}

.copy-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 14px;
  opacity: 0.5;
  transition: opacity 0.2s;
  padding: 2px 4px;
}
.copy-btn:hover { opacity: 1; }

/* ─── Typing ─────────────────────────────────────── */
.typing {
  display: flex;
  gap: 6px;
  align-items: center;
  padding: 16px 18px !important;
}

.typing span {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #aaa;
  animation: bounce 1.2s infinite;
}
.typing span:nth-child(2) { animation-delay: 0.2s; }
.typing span:nth-child(3) { animation-delay: 0.4s; }

@keyframes bounce {
  0%, 80%, 100% { transform: translateY(0); }
  40% { transform: translateY(-8px); }
}

/* ─── Input ──────────────────────────────────────── */
.input-area {
  padding: 16px 20px;
  display: flex;
  gap: 10px;
  align-items: flex-end;
  background: var(--sidebar-bg);
  backdrop-filter: blur(20px);
  border-top: 1px solid var(--sidebar-border);
}

.input-area textarea {
  flex: 1;
  border: none;
  border-radius: 16px;
  padding: 14px 18px;
  outline: none;
  font-size: 15px;
  font-family: inherit;
  resize: none;
  max-height: 140px;
  background: var(--input-bg);
  color: var(--input-text);
  line-height: 1.5;
}

.input-area button {
  width: 52px;
  height: 52px;
  border: none;
  border-radius: 14px;
  background: var(--btn-primary);
  color: white;
  font-size: 18px;
  cursor: pointer;
  flex-shrink: 0;
  transition: opacity 0.2s, transform 0.1s;
}
.input-area button:hover:not(:disabled) { opacity: 0.85; transform: scale(0.97); }
.input-area button:disabled { opacity: 0.4; cursor: not-allowed; }

/* ─── Responsive ─────────────────────────────────── */
@media (max-width: 768px) {
  .sidebar { display: none; }
  .bubble-wrapper { max-width: 85%; }
  .header { padding: 14px 16px; }
  .chat-box { padding: 16px; }
  .action-btn span { display: none; }
}
</style>