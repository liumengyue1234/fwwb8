<template>
  <div class="app-layout">
    <!-- 侧边栏 -->
    <aside class="sidebar">
      <div class="logo">
        <div class="logo-icon">⚖️</div>
        <div class="logo-text">
          <div class="logo-title">审思明辨</div>
          <div class="logo-sub">智判法案双擎系统</div>
        </div>
      </div>
      <nav class="nav-menu">
        <router-link to="/chat" class="nav-item" active-class="active">
          <span class="nav-icon">💬</span>
          <span class="nav-label">智能问答</span>
          <span class="nav-badge">AI</span>
        </router-link>
        <router-link to="/law" class="nav-item" active-class="active">
          <span class="nav-icon">📚</span>
          <span class="nav-label">法条检索</span>
        </router-link>
        <router-link to="/case" class="nav-item" active-class="active">
          <span class="nav-icon">🔍</span>
          <span class="nav-label">类案匹配</span>
        </router-link>
        <router-link to="/strategy" class="nav-item" active-class="active">
          <span class="nav-icon">🎯</span>
          <span class="nav-label">策略推演</span>
          <span class="nav-badge hot">热</span>
        </router-link>
      </nav>
      <div class="sidebar-footer">
        <div class="powered-by">
          <span>Powered by</span>
          <span class="brand">腾讯混元 × 得理科技</span>
        </div>
      </div>
    </aside>

    <!-- 主内容区 -->
    <main class="main-content">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
  </div>
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

:root {
  --primary: #1a3a6b;
  --primary-light: #2352a0;
  --gold: #c9a84c;
  --gold-light: #e8c76a;
  --bg: #f0f2f5;
  --card-bg: #ffffff;
  --text: #1f2937;
  --text-muted: #6b7280;
  --border: #e5e7eb;
  --success: #10b981;
  --warning: #f59e0b;
  --danger: #ef4444;
  --sidebar-w: 240px;
}

body {
  font-family: 'PingFang SC', 'Microsoft YaHei', -apple-system, BlinkMacSystemFont, sans-serif;
  background: var(--bg);
  color: var(--text);
}

.app-layout {
  display: flex;
  height: 100vh;
  overflow: hidden;
}

/* ===== 侧边栏 ===== */
.sidebar {
  width: var(--sidebar-w);
  background: linear-gradient(180deg, #0d2444 0%, #1a3a6b 60%, #1e4080 100%);
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
  box-shadow: 2px 0 12px rgba(0,0,0,0.15);
}

.logo {
  padding: 24px 20px 20px;
  display: flex;
  align-items: center;
  gap: 12px;
  border-bottom: 1px solid rgba(201,168,76,0.2);
}

.logo-icon {
  font-size: 28px;
  filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));
}

.logo-title {
  font-size: 18px;
  font-weight: 700;
  color: var(--gold);
  letter-spacing: 2px;
}

.logo-sub {
  font-size: 10px;
  color: rgba(201,168,76,0.7);
  letter-spacing: 1px;
  margin-top: 2px;
}

.nav-menu {
  flex: 1;
  padding: 16px 12px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 14px;
  border-radius: 10px;
  color: rgba(255,255,255,0.7);
  text-decoration: none;
  transition: all 0.2s;
  position: relative;
}

.nav-item:hover {
  background: rgba(255,255,255,0.1);
  color: #fff;
}

.nav-item.active {
  background: linear-gradient(135deg, rgba(201,168,76,0.25), rgba(201,168,76,0.1));
  color: var(--gold-light);
  border: 1px solid rgba(201,168,76,0.3);
}

.nav-icon { font-size: 18px; }
.nav-label { flex: 1; font-size: 14px; font-weight: 500; }

.nav-badge {
  font-size: 10px;
  padding: 1px 6px;
  border-radius: 10px;
  background: rgba(201,168,76,0.3);
  color: var(--gold-light);
  font-weight: 600;
}

.nav-badge.hot {
  background: rgba(239,68,68,0.3);
  color: #fca5a5;
}

.sidebar-footer {
  padding: 16px 20px;
  border-top: 1px solid rgba(255,255,255,0.08);
}

.powered-by {
  display: flex;
  flex-direction: column;
  gap: 2px;
  font-size: 11px;
  color: rgba(255,255,255,0.4);
}

.brand {
  color: rgba(201,168,76,0.6);
  font-size: 11px;
}

/* ===== 主内容 ===== */
.main-content {
  flex: 1;
  overflow-y: auto;
  background: var(--bg);
}

/* ===== 通用卡片样式 ===== */
.page-header {
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
  color: white;
  padding: 28px 32px;
}

.page-header h1 {
  font-size: 22px;
  font-weight: 700;
  margin-bottom: 6px;
}

.page-header p {
  font-size: 14px;
  opacity: 0.8;
}

.page-body {
  padding: 24px 32px;
}

.card {
  background: var(--card-bg);
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.08);
  border: 1px solid var(--border);
  margin-bottom: 16px;
}

.btn {
  padding: 10px 20px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.2s;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.btn-primary {
  background: linear-gradient(135deg, var(--primary), var(--primary-light));
  color: white;
}

.btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(26,58,107,0.4);
}

.btn-gold {
  background: linear-gradient(135deg, #b8860b, var(--gold));
  color: white;
}

.btn-gold:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(201,168,76,0.4);
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

.input-field {
  width: 100%;
  padding: 10px 14px;
  border: 1.5px solid var(--border);
  border-radius: 8px;
  font-size: 14px;
  transition: border-color 0.2s;
  font-family: inherit;
}

.input-field:focus {
  outline: none;
  border-color: var(--primary-light);
  box-shadow: 0 0 0 3px rgba(35,82,160,0.1);
}

textarea.input-field {
  resize: vertical;
  min-height: 100px;
}

.tag {
  display: inline-flex;
  align-items: center;
  padding: 2px 10px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
}

.tag-blue { background: #dbeafe; color: #1d4ed8; }
.tag-green { background: #d1fae5; color: #065f46; }
.tag-orange { background: #fef3c7; color: #92400e; }
.tag-red { background: #fee2e2; color: #991b1b; }
.tag-gray { background: #f3f4f6; color: #4b5563; }

.loading-spinner {
  display: inline-block;
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255,255,255,0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.fade-enter-active, .fade-leave-active { transition: opacity 0.2s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

/* 滚动条美化 */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #d1d5db; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #9ca3af; }

/* 响应式 */
@media (max-width: 768px) {
  :root { --sidebar-w: 64px; }
  .logo-text, .nav-label, .nav-badge, .sidebar-footer { display: none; }
  .nav-item { justify-content: center; }
  .page-body { padding: 16px; }
}
</style>
