<template>
  <div class="law-page">
    <div class="page-header">
      <h1>📚 精准法条检索</h1>
      <p>基于得理法律知识库，支持语义检索与关键词检索，精准定位相关法律法规</p>
    </div>

    <div class="page-body">
      <!-- 搜索区 -->
      <div class="card">
        <div class="search-bar">
          <div class="search-input-wrap">
            <span class="search-icon">🔍</span>
            <input
              v-model="query"
              class="search-input"
              placeholder="输入法律问题或关键词，例如：劳动合同解除、房屋买卖纠纷..."
              @keydown.enter="search"
            />
          </div>
          <div class="search-mode">
            <label class="mode-label">检索方式：</label>
            <select v-model="fieldName" class="mode-select">
              <option value="semantic">语义检索（推荐）</option>
              <option value="title">关键词检索</option>
            </select>
          </div>
          <button class="btn btn-primary" @click="search" :disabled="loading || !query.trim()">
            <span v-if="loading" class="loading-spinner"></span>
            <span v-else>🔍 检索</span>
          </button>
        </div>

        <!-- 热门示例 -->
        <div class="examples">
          <span class="example-label">热门检索：</span>
          <span
            v-for="e in examples"
            :key="e"
            class="example-tag"
            @click="quickSearch(e)"
          >{{ e }}</span>
        </div>
      </div>

      <!-- 错误提示 -->
      <div v-if="error" class="error-card">
        ⚠️ {{ error }}
      </div>

      <!-- 结果区 -->
      <div v-if="results.length > 0">
        <div class="result-meta">
          共检索到 <strong>{{ results.length }}</strong> 条相关法律法规
        </div>

        <div v-for="(item, i) in results" :key="i" class="law-card">
          <div class="law-header">
            <div class="law-index">{{ i + 1 }}</div>
            <div class="law-info">
              <div class="law-title">{{ item.title || '未知法规' }}</div>
              <div class="law-meta-row">
                <span v-if="item.levelName" class="tag tag-blue">{{ item.levelName }}</span>
                <span v-if="item.publisherName" class="tag tag-gray">{{ item.publisherName }}</span>
                <span v-if="item.publishDate" class="tag tag-gray">{{ item.publishDate }}</span>
                <span
                  v-if="item.timelinessName"
                  :class="['tag', item.timelinessName === '现行有效' ? 'tag-green' : 'tag-orange']"
                >{{ item.timelinessName }}</span>
              </div>
            </div>
            <button
              class="btn-detail"
              @click="loadDetail(item)"
              :disabled="detailLoading === item.id"
            >
              <span v-if="detailLoading === item.id" class="loading-spinner-sm"></span>
              <span v-else>查看详情 →</span>
            </button>
          </div>

          <!-- 展开详情 -->
          <transition name="expand">
            <div v-if="expandedId === item.id" class="law-detail">
              <div class="law-detail-content" v-if="detailContent">
                <pre class="law-text">{{ detailContent }}</pre>
              </div>
              <div v-else class="loading-text">加载中...</div>
            </div>
          </transition>
        </div>
      </div>

      <!-- 空状态 -->
      <div v-else-if="searched && !loading" class="empty-state">
        <div class="empty-icon">📜</div>
        <p>未找到相关法律法规，建议更换关键词重试</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const query = ref('')
const fieldName = ref('semantic')
const loading = ref(false)
const results = ref([])
const error = ref('')
const searched = ref(false)
const expandedId = ref(null)
const detailContent = ref('')
const detailLoading = ref(null)

const examples = ['劳动合同法', '房屋买卖合同', '交通事故赔偿', '婚姻家庭', '知识产权保护', '合同违约责任']

function quickSearch(e) {
  query.value = e
  search()
}

async function search() {
  if (!query.value.trim() || loading.value) return
  loading.value = true
  error.value = ''
  results.value = []
  searched.value = false
  expandedId.value = null

  try {
    const { data } = await axios.post('/api/law/search', {
      query: query.value,
      page_no: 1,
      page_size: 10,
      field_name: fieldName.value
    })

    const list = data?.data?.body?.data || data?.data?.body || []
    results.value = Array.isArray(list) ? list : []
    searched.value = true
  } catch (e) {
    error.value = '检索失败，请确认后端服务已启动（http://localhost:8000）'
  } finally {
    loading.value = false
  }
}

async function loadDetail(item) {
  const id = item.id || item.lawsId
  if (!id) return

  if (expandedId.value === id) {
    expandedId.value = null
    detailContent.value = ''
    return
  }

  expandedId.value = id
  detailContent.value = ''
  detailLoading.value = id

  try {
    const { data } = await axios.get(`/api/law/detail/${id}`)
    detailContent.value = data?.data?.body?.lawDetailContent || '暂无详细内容'
  } catch {
    detailContent.value = '加载详情失败'
  } finally {
    detailLoading.value = null
  }
}
</script>

<style scoped>
.search-bar {
  display: flex;
  gap: 12px;
  align-items: center;
  flex-wrap: wrap;
}

.search-input-wrap {
  flex: 1;
  min-width: 240px;
  display: flex;
  align-items: center;
  border: 1.5px solid #e5e7eb;
  border-radius: 10px;
  padding: 0 14px;
  gap: 8px;
  transition: border-color 0.2s;
}

.search-input-wrap:focus-within {
  border-color: #2352a0;
  box-shadow: 0 0 0 3px rgba(35,82,160,0.1);
}

.search-icon { font-size: 16px; }

.search-input {
  flex: 1;
  border: none;
  outline: none;
  padding: 11px 0;
  font-size: 14px;
  font-family: inherit;
}

.mode-label { font-size: 13px; color: #6b7280; }

.mode-select {
  border: 1.5px solid #e5e7eb;
  border-radius: 8px;
  padding: 8px 10px;
  font-size: 13px;
  outline: none;
  cursor: pointer;
}

.examples {
  margin-top: 12px;
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
}

.example-label {
  font-size: 12px;
  color: #9ca3af;
}

.example-tag {
  padding: 4px 12px;
  background: #f3f4f6;
  border-radius: 20px;
  font-size: 12px;
  color: #4b5563;
  cursor: pointer;
  transition: all 0.2s;
}

.example-tag:hover {
  background: #dbeafe;
  color: #1d4ed8;
}

.result-meta {
  font-size: 13px;
  color: #6b7280;
  margin-bottom: 12px;
}

.error-card {
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 10px;
  padding: 14px 18px;
  color: #dc2626;
  font-size: 14px;
  margin-bottom: 16px;
}

.law-card {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  overflow: hidden;
  margin-bottom: 12px;
  transition: box-shadow 0.2s;
}

.law-card:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

.law-header {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  padding: 16px 18px;
}

.law-index {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: linear-gradient(135deg, #1a3a6b, #2352a0);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 700;
  flex-shrink: 0;
  margin-top: 2px;
}

.law-info { flex: 1; }

.law-title {
  font-size: 15px;
  font-weight: 600;
  color: #1a3a6b;
  margin-bottom: 8px;
  line-height: 1.4;
}

.law-meta-row {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.btn-detail {
  background: none;
  border: 1.5px solid #e5e7eb;
  border-radius: 8px;
  padding: 6px 12px;
  font-size: 12px;
  color: #2352a0;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
  flex-shrink: 0;
}

.btn-detail:hover {
  background: #f0f4ff;
  border-color: #2352a0;
}

.law-detail {
  border-top: 1px solid #f3f4f6;
  padding: 16px 18px;
  background: #fafafa;
}

.law-text {
  font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
  font-size: 13px;
  line-height: 1.8;
  color: #374151;
  white-space: pre-wrap;
  word-break: break-all;
  max-height: 400px;
  overflow-y: auto;
}

.loading-text { color: #9ca3af; font-size: 13px; }

.loading-spinner-sm {
  display: inline-block;
  width: 12px;
  height: 12px;
  border: 2px solid rgba(35,82,160,0.3);
  border-top-color: #2352a0;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }

.empty-state {
  text-align: center;
  padding: 60px;
  color: #9ca3af;
}

.empty-icon { font-size: 48px; margin-bottom: 12px; }

.expand-enter-active, .expand-leave-active { transition: all 0.3s; }
.expand-enter-from, .expand-leave-to { opacity: 0; max-height: 0; }
.expand-enter-to, .expand-leave-from { opacity: 1; max-height: 500px; }
</style>
