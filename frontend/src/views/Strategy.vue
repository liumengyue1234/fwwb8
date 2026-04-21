<template>
  <div class="strategy-page">
    <div class="page-header">
      <h1>🎯 诉讼策略推演</h1>
      <p>上传案情后，智能体自动切换"对方律师"视角，生成质证意见、风险提示及诉讼策略报告</p>
    </div>

    <div class="page-body">
      <!-- 输入区 -->
      <div class="card">
        <div class="input-header">
          <span class="input-title">📝 案情描述</span>
          <span class="input-hint">支持起诉状、案情摘要、争议焦点等文本</span>
        </div>
        <textarea
          v-model="caseText"
          class="input-field"
          rows="8"
          placeholder="请详细描述案情，例如：
原告张三与被告李四于2023年签订房屋买卖合同，约定购买位于某市的房产，总价200万元。原告已支付定金30万元，但被告以市场价格上涨为由拒绝履行合同，要求双倍返还定金并赔偿损失..."
        ></textarea>
        <div class="actions">
          <span class="word-count">已输入 {{ caseText.length }} 字</span>
          <div class="action-btns">
            <button class="btn btn-outline" @click="caseText = ''">清空</button>
            <button
              class="btn btn-gold"
              @click="analyze"
              :disabled="loading || !caseText.trim()"
            >
              <span v-if="loading" class="loading-spinner"></span>
              <span v-else>⚡ 开始推演</span>
            </button>
          </div>
        </div>
      </div>

      <div v-if="error" class="error-card">⚠️ {{ error }}</div>

      <!-- 分析结果 -->
      <div v-if="report" class="report-container">
        <div class="report-title">
          <span class="report-icon">📊</span>
          <span>诉讼策略分析报告</span>
          <span class="report-badge">AI 生成</span>
        </div>

        <!-- 总览 -->
        <div class="report-section overview">
          <p>{{ report.overview }}</p>
        </div>

        <!-- 数据统计 -->
        <div class="stats-row">
          <div class="stat-card">
            <div class="stat-num">{{ relevantLaws.length }}</div>
            <div class="stat-label">相关法规</div>
          </div>
          <div class="stat-card">
            <div class="stat-num">{{ relevantCases.length }}</div>
            <div class="stat-label">类案参考</div>
          </div>
          <div class="stat-card">
            <div class="stat-num">{{ report.risk_assessment?.risks?.length || 0 }}</div>
            <div class="stat-label">风险项</div>
          </div>
          <div class="stat-card">
            <div class="stat-num">{{ report.strategy_suggestions?.suggestions?.length || 0 }}</div>
            <div class="stat-label">策略建议</div>
          </div>
        </div>

        <!-- 对方律师视角 -->
        <div class="report-section">
          <div class="section-title">
            <span class="section-icon">⚔️</span>
            {{ report.opponent_perspective?.title }}
          </div>
          <div class="points-list">
            <div
              v-for="(point, i) in report.opponent_perspective?.points"
              :key="i"
              class="point-item"
              v-html="renderMd(point)"
            ></div>
          </div>
        </div>

        <!-- 风险评估 -->
        <div class="report-section">
          <div class="section-title">
            <span class="section-icon">⚠️</span>
            {{ report.risk_assessment?.title }}
          </div>
          <div class="risk-list">
            <div v-for="(risk, i) in report.risk_assessment?.risks" :key="i" class="risk-item">
              <span :class="['risk-level', `level-${levelClass(risk.level)}`]">{{ risk.level }}风险</span>
              <div class="risk-content">
                <div class="risk-item-title">{{ risk.item }}</div>
                <div class="risk-desc">{{ risk.desc }}</div>
              </div>
            </div>
          </div>
        </div>

        <!-- 诉讼策略 -->
        <div class="report-section">
          <div class="section-title">
            <span class="section-icon">💡</span>
            {{ report.strategy_suggestions?.title }}
          </div>
          <div class="suggestions-list">
            <div
              v-for="(s, i) in report.strategy_suggestions?.suggestions"
              :key="i"
              class="suggestion-item"
              v-html="renderMd(s)"
            ></div>
          </div>
        </div>

        <!-- 类案参考 -->
        <div class="report-section">
          <div class="section-title"><span class="section-icon">📚</span>类案参考</div>
          <p class="similar-summary">{{ report.similar_cases_summary }}</p>
          <div v-if="relevantCases.length > 0" class="cases-mini-list">
            <div v-for="(c, i) in relevantCases" :key="i" class="case-mini-item">
              <span class="case-mini-num">{{ i + 1 }}</span>
              <div>
                <div class="case-mini-name">{{ c.name || '案件' }}</div>
                <div class="case-mini-meta">{{ c.court }} {{ c.date }}</div>
              </div>
            </div>
          </div>
        </div>

        <!-- 相关法规 -->
        <div v-if="relevantLaws.length > 0" class="report-section">
          <div class="section-title"><span class="section-icon">📜</span>相关法规</div>
          <div class="laws-mini-list">
            <div v-for="(l, i) in relevantLaws" :key="i" class="law-mini-item">
              <span class="tag tag-blue">{{ l.level }}</span>
              <span class="law-mini-name">{{ l.title }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { marked } from 'marked'

const caseText = ref('')
const loading = ref(false)
const error = ref('')
const report = ref(null)
const relevantLaws = ref([])
const relevantCases = ref([])

function renderMd(text) {
  return marked.parseInline(text || '')
}

function levelClass(level) {
  if (level === '高') return 'high'
  if (level === '中') return 'mid'
  return 'low'
}

async function analyze() {
  if (!caseText.value.trim() || loading.value) return
  loading.value = true
  error.value = ''
  report.value = null

  try {
    const { data } = await axios.post('/api/strategy', {
      case_text: caseText.value,
      user_id: 'user_web'
    })
    report.value = data.report
    relevantLaws.value = data.relevant_laws || []
    relevantCases.value = data.relevant_cases || []
  } catch {
    error.value = '推演失败，请确认后端服务已启动（http://localhost:8000）'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.input-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
}

.input-title { font-size: 15px; font-weight: 600; color: #1a3a6b; }
.input-hint { font-size: 12px; color: #9ca3af; }

.actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 10px;
}

.word-count { font-size: 12px; color: #9ca3af; }

.action-btns { display: flex; gap: 10px; }

.btn-outline {
  padding: 8px 18px;
  border: 1.5px solid #e5e7eb;
  background: white;
  border-radius: 8px;
  cursor: pointer;
  font-size: 13px;
  color: #6b7280;
  transition: all 0.2s;
}

.btn-outline:hover { border-color: #9ca3af; }

.error-card {
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 10px;
  padding: 14px 18px;
  color: #dc2626;
  font-size: 14px;
  margin-bottom: 16px;
}

/* 报告 */
.report-container {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  overflow: hidden;
}

.report-title {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 16px 20px;
  background: linear-gradient(135deg, #0d2444, #1a3a6b);
  color: white;
  font-size: 16px;
  font-weight: 700;
}

.report-icon { font-size: 20px; }

.report-badge {
  margin-left: auto;
  font-size: 11px;
  padding: 2px 8px;
  background: rgba(201,168,76,0.3);
  border: 1px solid rgba(201,168,76,0.5);
  border-radius: 10px;
  color: #e8c76a;
}

.report-section {
  padding: 18px 20px;
  border-bottom: 1px solid #f3f4f6;
}

.report-section:last-child { border-bottom: none; }

.overview {
  background: #f8faff;
  font-size: 14px;
  color: #374151;
  line-height: 1.8;
}

.stats-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0;
  border-bottom: 1px solid #f3f4f6;
}

.stat-card {
  text-align: center;
  padding: 16px;
  border-right: 1px solid #f3f4f6;
}

.stat-card:last-child { border-right: none; }

.stat-num {
  font-size: 28px;
  font-weight: 700;
  color: #1a3a6b;
}

.stat-label { font-size: 12px; color: #9ca3af; margin-top: 2px; }

.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 15px;
  font-weight: 700;
  color: #1a3a6b;
  margin-bottom: 14px;
}

.section-icon { font-size: 18px; }

.points-list, .suggestions-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.point-item, .suggestion-item {
  font-size: 13px;
  line-height: 1.7;
  color: #374151;
  padding: 10px 14px;
  background: #f9fafb;
  border-radius: 8px;
  border-left: 3px solid #2352a0;
}

.suggestion-item { border-left-color: #c9a84c; }

.point-item :deep(strong), .suggestion-item :deep(strong) {
  color: #1a3a6b;
}

.risk-list { display: flex; flex-direction: column; gap: 10px; }

.risk-item { display: flex; align-items: flex-start; gap: 12px; }

.risk-level {
  padding: 3px 10px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  white-space: nowrap;
  flex-shrink: 0;
  margin-top: 2px;
}

.level-high { background: #fee2e2; color: #991b1b; }
.level-mid { background: #fef3c7; color: #92400e; }
.level-low { background: #d1fae5; color: #065f46; }

.risk-content { flex: 1; }
.risk-item-title { font-size: 14px; font-weight: 600; color: #1f2937; margin-bottom: 2px; }
.risk-desc { font-size: 13px; color: #6b7280; line-height: 1.6; }

.similar-summary { font-size: 13px; color: #4b5563; line-height: 1.7; margin-bottom: 12px; }

.cases-mini-list { display: flex; flex-direction: column; gap: 8px; }

.case-mini-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 10px 12px;
  background: #f9fafb;
  border-radius: 8px;
}

.case-mini-num {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #c9a84c;
  color: white;
  font-size: 11px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.case-mini-name { font-size: 13px; font-weight: 600; color: #1f2937; }
.case-mini-meta { font-size: 12px; color: #9ca3af; margin-top: 2px; }

.laws-mini-list { display: flex; flex-direction: column; gap: 8px; }

.law-mini-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 12px;
  background: #f9fafb;
  border-radius: 8px;
}

.law-mini-name { font-size: 13px; color: #1a3a6b; font-weight: 500; }

@keyframes spin { to { transform: rotate(360deg); } }
</style>
