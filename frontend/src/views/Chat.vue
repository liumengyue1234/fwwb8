<template>
  <div class="chat-page">
    <!-- 页头 -->
    <div class="page-header">
      <h1>💬 智能法律问答</h1>
      <p>基于腾讯混元大模型 × 得理法律知识库，自然语言咨询法律问题</p>
    </div>

    <div class="chat-container">
      <!-- 消息列表 -->
      <div class="messages-area" ref="messagesRef">
        <!-- 欢迎引导 -->
        <div v-if="messages.length === 0" class="welcome-area">
          <div class="welcome-icon">⚖️</div>
          <h2>您好，我是审思明辨智能助手</h2>
          <p>我能帮您检索法律法规、分析类案、解答法律疑问</p>
          <div class="quick-questions">
            <div class="quick-title">💡 常见问题快速提问</div>
            <div class="quick-grid">
              <button
                v-for="q in quickQuestions"
                :key="q"
                class="quick-btn"
                @click="sendQuick(q)"
              >{{ q }}</button>
            </div>
          </div>
        </div>

        <!-- 消息气泡 -->
        <div v-for="(msg, i) in messages" :key="i" :class="['msg-row', msg.role]">
          <div class="msg-avatar">
            <span v-if="msg.role === 'assistant'">⚖️</span>
            <span v-else>👤</span>
          </div>
          <div class="msg-bubble">
            <div class="msg-content" v-html="renderMarkdown(msg.content)"></div>
            <div class="msg-time">{{ msg.time }}</div>
          </div>
        </div>

        <!-- 加载中 -->
        <div v-if="loading" class="msg-row assistant">
          <div class="msg-avatar">⚖️</div>
          <div class="msg-bubble">
            <div class="typing-indicator">
              <span></span><span></span><span></span>
            </div>
          </div>
        </div>
      </div>

      <!-- 输入区 -->
      <div class="input-area">
        <div class="input-wrapper">
          <textarea
            v-model="input"
            class="chat-input"
            placeholder="输入法律问题，例如：劳动合同中不签合同有哪些法律后果？"
            rows="2"
            @keydown.enter.exact.prevent="sendMessage"
            @keydown.enter.shift.exact="input += '\n'"
            :disabled="loading"
          ></textarea>
          <div class="input-actions">
            <span class="input-tip">Enter 发送 · Shift+Enter 换行</span>
            <button
              class="btn btn-primary send-btn"
              @click="sendMessage"
              :disabled="loading || !input.trim()"
            >
              <span v-if="loading" class="loading-spinner"></span>
              <span v-else>发送</span>
            </button>
          </div>
        </div>
        <button class="clear-btn" @click="clearChat" title="清空对话">🗑️ 清空</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import axios from 'axios'
import { marked } from 'marked'

const messages = ref([])
const input = ref('')
const loading = ref(false)
const messagesRef = ref(null)

const quickQuestions = [
  '合同违约后如何索赔？',
  '劳动者被违法解雇有什么权利？',
  '房屋买卖合同纠纷怎么处理？',
  '交通事故赔偿标准是什么？',
  '离婚财产分割的法律规定？',
  '借款不还如何起诉？'
]

function renderMarkdown(text) {
  return marked(text || '', { breaks: true })
}

function getTime() {
  return new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
}

function sendQuick(q) {
  input.value = q
  sendMessage()
}

async function sendMessage() {
  const text = input.value.trim()
  if (!text || loading.value) return

  messages.value.push({ role: 'user', content: text, time: getTime() })
  input.value = ''
  loading.value = true

  await nextTick()
  scrollToBottom()

  try {
    const payload = {
      messages: messages.value
        .filter(m => m.role !== 'system')
        .map(m => ({ role: m.role, content: m.content })),
      user_id: 'user_web'
    }
    const { data } = await axios.post('/api/chat', payload)
    messages.value.push({
      role: 'assistant',
      content: data.content || '抱歉，暂时无法获取回复，请稍后重试。',
      time: getTime()
    })
  } catch (e) {
    messages.value.push({
      role: 'assistant',
      content: '⚠️ 请求失败，请检查后端服务是否正常运行（http://localhost:8000）',
      time: getTime()
    })
  } finally {
    loading.value = false
    await nextTick()
    scrollToBottom()
  }
}

function scrollToBottom() {
  if (messagesRef.value) {
    messagesRef.value.scrollTop = messagesRef.value.scrollHeight
  }
}

function clearChat() {
  messages.value = []
}
</script>

<style scoped>
.chat-page {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.chat-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  padding: 0;
}

.messages-area {
  flex: 1;
  overflow-y: auto;
  padding: 24px 32px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* 欢迎区 */
.welcome-area {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 40px 20px;
  gap: 12px;
}

.welcome-icon {
  font-size: 56px;
  filter: drop-shadow(0 4px 8px rgba(0,0,0,0.1));
}

.welcome-area h2 {
  font-size: 22px;
  color: #1a3a6b;
  font-weight: 700;
}

.welcome-area p {
  color: #6b7280;
  font-size: 14px;
}

.quick-questions {
  margin-top: 20px;
  width: 100%;
  max-width: 600px;
}

.quick-title {
  font-size: 13px;
  color: #9ca3af;
  margin-bottom: 12px;
}

.quick-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
}

.quick-btn {
  padding: 10px 14px;
  background: #ffffff;
  border: 1.5px solid #e5e7eb;
  border-radius: 10px;
  cursor: pointer;
  font-size: 13px;
  color: #374151;
  text-align: left;
  transition: all 0.2s;
}

.quick-btn:hover {
  border-color: #2352a0;
  color: #1a3a6b;
  background: #f0f4ff;
  transform: translateY(-1px);
}

/* 消息行 */
.msg-row {
  display: flex;
  gap: 12px;
  max-width: 800px;
}

.msg-row.user {
  flex-direction: row-reverse;
  align-self: flex-end;
}

.msg-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: #f3f4f6;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  flex-shrink: 0;
  border: 2px solid #e5e7eb;
}

.msg-row.assistant .msg-avatar {
  background: linear-gradient(135deg, #1a3a6b, #2352a0);
}

.msg-bubble {
  max-width: 600px;
  min-width: 60px;
}

.msg-content {
  padding: 12px 16px;
  border-radius: 12px;
  font-size: 14px;
  line-height: 1.7;
  word-break: break-word;
}

.msg-row.user .msg-content {
  background: linear-gradient(135deg, #1a3a6b, #2352a0);
  color: white;
  border-radius: 12px 4px 12px 12px;
}

.msg-row.assistant .msg-content {
  background: white;
  color: #1f2937;
  border: 1px solid #e5e7eb;
  border-radius: 4px 12px 12px 12px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}

.msg-row.assistant .msg-content :deep(p) { margin: 0 0 8px; }
.msg-row.assistant .msg-content :deep(p:last-child) { margin-bottom: 0; }
.msg-row.assistant .msg-content :deep(strong) { color: #1a3a6b; }
.msg-row.assistant .msg-content :deep(blockquote) {
  border-left: 3px solid #c9a84c;
  padding-left: 12px;
  color: #6b7280;
  font-size: 12px;
  margin: 8px 0 0;
}

.msg-time {
  font-size: 11px;
  color: #9ca3af;
  margin-top: 4px;
  padding: 0 4px;
}

.msg-row.user .msg-time { text-align: right; }

/* 打字动画 */
.typing-indicator {
  display: flex;
  gap: 4px;
  padding: 14px 18px;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 4px 12px 12px 12px;
}

.typing-indicator span {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #9ca3af;
  animation: bounce 1.2s infinite ease-in-out;
}

.typing-indicator span:nth-child(2) { animation-delay: 0.2s; }
.typing-indicator span:nth-child(3) { animation-delay: 0.4s; }

@keyframes bounce {
  0%, 60%, 100% { transform: translateY(0); }
  30% { transform: translateY(-6px); }
}

/* 输入区 */
.input-area {
  padding: 16px 32px 20px;
  background: white;
  border-top: 1px solid #e5e7eb;
  display: flex;
  gap: 10px;
  align-items: flex-end;
}

.input-wrapper {
  flex: 1;
  border: 1.5px solid #e5e7eb;
  border-radius: 12px;
  overflow: hidden;
  transition: border-color 0.2s;
}

.input-wrapper:focus-within {
  border-color: #2352a0;
  box-shadow: 0 0 0 3px rgba(35,82,160,0.1);
}

.chat-input {
  width: 100%;
  padding: 12px 16px 8px;
  border: none;
  outline: none;
  font-size: 14px;
  font-family: inherit;
  resize: none;
  line-height: 1.5;
  color: #1f2937;
}

.input-actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 6px 12px;
  background: #f9fafb;
  border-top: 1px solid #f3f4f6;
}

.input-tip {
  font-size: 11px;
  color: #9ca3af;
}

.send-btn {
  padding: 6px 16px;
  font-size: 13px;
}

.clear-btn {
  background: none;
  border: 1.5px solid #e5e7eb;
  border-radius: 8px;
  padding: 8px 12px;
  font-size: 13px;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}

.clear-btn:hover {
  border-color: #ef4444;
  color: #ef4444;
}
</style>
