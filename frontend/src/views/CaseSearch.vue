<template>
  <div class="case-page">
    <div class="page-header">
      <h1>🔍 相似案例匹配</h1>
      <p>海量司法裁判文书检索，快速定位与您案件高度相关的类案裁判要旨</p>
    </div>

    <div class="page-body">
      <!-- 搜索区 -->
      <div class="card">
        <div class="search-area">
          <textarea
            v-model="query"
            class="input-field"
            rows="3"
            placeholder="输入案情描述、争议焦点或关键词，例如：劳动者上班途中发生交通事故，能否认定工伤？"
            @keydown.ctrl.enter="search"
          ></textarea>
          <div class="filter-row">
            <div class="filter-group">
              <label>法院层级：</label>
              <div class="checkbox-group">
                <label v-for="c in courtOptions" :key="c.value" class="checkbox-label">
                  <input type="checkbox" :value="c.value" v-model="selectedCourts" />
                  {{ c.label }}
                </label>
              </div>
            </div>
            <div class="filter-group">
              <label>裁判年份：</label>
              <input v-model="yearStart" type="text" placeholder="起始年" class="year-input" />
              <span>—</span>
              <input v-model="yearEnd" type="text" placeholder="截止年" class="year-input" />
            </div>
            <div class="filter-group">
              <label>每页数量：</label>
              <select v-model="pageSize" class="mode-select">
                <option value="5">5条</option>
                <option value="10">10条</option>
              </select>
            </div>
            <button class="btn btn-primary" @click="search" :disabled="loading || !query.trim()">
              <span v-if="loading" class="loading-spinner"></span>
              <span v-else>🔍 检索类案</span>
            </button>
          </div>
        </div>
        <div class="tip-row">💡 Ctrl + Enter 快速检索</div>
      </div>

      <div v-if="error" class="error-card">⚠️ {{ error }}</div>

      <!-- 结果 -->
      <div v-if="results.length > 0">
        <div class="result-meta">
          共找到 <strong>{{ results.length }}</strong> 件类似案例
        </div>

        <div v-for="(item, i) in results" :key="i" class="case-card">
          <div class="case-header">
            <div class="case-num">{{ i + 1 }}</div>
            <div class="case-main">
              <div class="case-name">{{ item.name || item.title || '案件名称未知' }}</div>
              <div class="case-meta-row">
                <span v-if="item.court || item.courtName" class="tag tag-blue">
                  🏛️ {{ item.court || item.courtName }}
                </span>
                <span v-if="item.caseYear || item.judgeDate" class="tag tag-gray">
                  📅 {{ item.caseYear || item.judgeDate }}
                </span>
                <span v-if="item.caseType" class="tag tag-orange">{{ item.caseType }}</span>
                <span v-if="item.judgementType" class="tag tag-gray">{{ item.judgementType }}</span>
              </div>
            </div>
          </div>
          <div v-if="item.abstract || item.summary" class="case-abstract">
            <span class="abstract-label">裁判摘要：</span>
            {{ item.abstract || item.summary }}
          </div>
          <div v-if="item.caseNo || item.docNo" class="case-no">
            案号：{{ item.caseNo || item.docNo }}
          </div>
        </div>
      </div>

      <div v-else-if="searched && !loading" class="empty-state">
        <div class="empty-icon">⚖️</div>
        <p>未找到相关案例，建议调整关键词或放宽筛选条件</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const query = ref('')
const loading = ref(false)
const results = ref([])
const error = ref('')
const searched = ref(false)
const selectedCourts = ref([])
const yearStart = ref('')
const yearEnd = ref('')
const pageSize = ref('5')

const courtOptions = [
  { value: '0', label: '最高法院' },
  { value: '1', label: '高级法院' },
  { value: '2', label: '中级法院' },
  { value: '3', label: '基层法院' }
]

async function search() {
  if (!query.value.trim() || loading.value) return
  loading.value = true
  error.value = ''
  results.value = []
  searched.value = false

  const payload = {
    query: query.value,
    page_no: 1,
    page_size: parseInt(pageSize.value)
  }
  if (selectedCourts.value.length > 0) payload.court_level = selectedCourts.value
  if (yearStart.value) payload.year_start = yearStart.value
  if (yearEnd.value) payload.year_end = yearEnd.value

  try {
    const { data } = await axios.post('/api/case/search', payload)
    const list = data?.data?.body?.data || data?.data?.body || []
    results.value = Array.isArray(list) ? list : []
    searched.value = true
  } catch {
    error.value = '检索失败，请确认后端服务已启动（http://localhost:8000）'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.search-area { display: flex; flex-direction: column; gap: 12px; }

.filter-row {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  align-items: center;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: #374151;
}

.checkbox-group {
  display: flex;
  gap: 12px;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 4px;
  cursor: pointer;
  font-size: 13px;
}

.year-input {
  width: 80px;
  padding: 6px 10px;
  border: 1.5px solid #e5e7eb;
  border-radius: 6px;
  font-size: 13px;
  outline: none;
}

.mode-select {
  border: 1.5px solid #e5e7eb;
  border-radius: 8px;
  padding: 6px 10px;
  font-size: 13px;
  outline: none;
  cursor: pointer;
}

.tip-row { font-size: 12px; color: #9ca3af; margin-top: 4px; }

.result-meta { font-size: 13px; color: #6b7280; margin-bottom: 12px; }

.error-card {
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 10px;
  padding: 14px 18px;
  color: #dc2626;
  font-size: 14px;
  margin-bottom: 16px;
}

.case-card {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 18px;
  margin-bottom: 12px;
  transition: box-shadow 0.2s;
}

.case-card:hover { box-shadow: 0 4px 12px rgba(0,0,0,0.08); }

.case-header { display: flex; gap: 14px; align-items: flex-start; margin-bottom: 10px; }

.case-num {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: linear-gradient(135deg, #c9a84c, #e8c76a);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 700;
  flex-shrink: 0;
}

.case-main { flex: 1; }

.case-name {
  font-size: 15px;
  font-weight: 600;
  color: #1a3a6b;
  margin-bottom: 8px;
  line-height: 1.4;
}

.case-meta-row { display: flex; flex-wrap: wrap; gap: 6px; }

.case-abstract {
  font-size: 13px;
  color: #4b5563;
  line-height: 1.7;
  padding: 10px 12px;
  background: #f9fafb;
  border-radius: 8px;
  border-left: 3px solid #c9a84c;
  margin-bottom: 8px;
}

.abstract-label { font-weight: 600; color: #1a3a6b; }

.case-no { font-size: 12px; color: #9ca3af; }

.empty-state { text-align: center; padding: 60px; color: #9ca3af; }
.empty-icon { font-size: 48px; margin-bottom: 12px; }

@keyframes spin { to { transform: rotate(360deg); } }
</style>
