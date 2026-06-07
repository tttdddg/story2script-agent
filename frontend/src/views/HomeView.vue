<template>
  <div class="landing">
    <!-- ═══ 导航栏 ═══ -->
    <nav class="navbar">
      <div class="nav-inner">
        <span class="nav-logo">Story2Script Agent</span>
        <div class="nav-links">
          <button class="nav-btn" @click="scrollTo('features')">功能亮点</button>
          <button class="nav-btn nav-btn-cta" @click="$router.push('/analyze')">开始使用</button>
        </div>
      </div>
    </nav>

    <!-- ═══ Hero 主视觉 ═══ -->
    <section class="hero">
      <div class="hero-inner">
        <!-- 左侧文案 -->
        <div class="hero-left">
          <h1 class="hero-title">Story2Script <span class="accent">Agent</span></h1>
          <p class="hero-sub">AI 小说剧本结构化改编平台</p>
          <p class="hero-desc">
            输入 3 章以上小说文本，自动完成章节解析、人物抽取、场景拆分、结构化剧本生成、Schema 校验与 YAML 导出。
          </p>
          <div class="hero-actions">
            <button class="neu-btn neu-btn-blue neu-btn-lg" @click="$router.push('/analyze')">开始使用 →</button>
            <a href="/docs/YAML_SCHEMA.md" target="_blank" class="neu-btn neu-btn-lg">查看 Schema</a>
          </div>
          <div class="hero-tags">
            <span class="hero-tag">📖 Story Bible</span>
            <span class="hero-tag">📋 YAML Schema</span>
            <span class="hero-tag">🎭 结构化剧本</span>
            <span class="hero-tag">🔍 人物一致性</span>
            <span class="hero-tag">📎 可追溯改编</span>
          </div>
        </div>

        <!-- 右侧预览卡片 -->
        <div class="hero-right">
          <div class="preview-card">
            <div class="preview-title">🎬 创作工作流</div>
            <div class="preview-flow">
              <div class="flow-step"><span class="flow-dot"></span>小说输入</div>
              <span class="flow-arrow">→</span>
              <div class="flow-step"><span class="flow-dot"></span>章节解析</div>
              <span class="flow-arrow">→</span>
              <div class="flow-step"><span class="flow-dot active"></span>Story Bible</div>
              <span class="flow-arrow">→</span>
              <div class="flow-step"><span class="flow-dot"></span>YAML 剧本</div>
              <span class="flow-arrow">→</span>
              <div class="flow-step"><span class="flow-dot"></span>Schema 校验</div>
              <span class="flow-arrow">→</span>
              <div class="flow-step"><span class="flow-dot"></span>导出</div>
            </div>
            <div class="preview-stats">
              <div class="pstat"><span class="pstat-val">4</span><span class="pstat-lbl">章节数</span></div>
              <div class="pstat"><span class="pstat-val">3</span><span class="pstat-lbl">人物数</span></div>
              <div class="pstat"><span class="pstat-val">5</span><span class="pstat-lbl">场景数</span></div>
              <div class="pstat"><span class="pstat-val ok">✓</span><span class="pstat-lbl">校验通过</span></div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ═══ 核心能力 ═══ -->
    <section class="features" id="features">
      <h2 class="section-title">核心能力</h2>
      <div class="features-grid">
        <div class="feature-card">
          <div class="feat-icon">📑</div>
          <h3>章节解析</h3>
          <p>自动识别 3 章以上小说文本，提取章节结构与字数信息，支持多种中文章节格式。</p>
        </div>
        <div class="feature-card">
          <div class="feat-icon">📖</div>
          <h3>Story Bible</h3>
          <p>抽取人物、地点、关键事件和人物关系，构建结构化故事设定表，减少角色漂移。</p>
        </div>
        <div class="feature-card">
          <div class="feat-icon">🎭</div>
          <h3>YAML 剧本生成</h3>
          <p>按照预定义 Schema 生成结构化剧本初稿，包含场景、对白、舞台提示与来源追溯。</p>
        </div>
        <div class="feature-card">
          <div class="feat-icon">✅</div>
          <h3>Schema 校验</h3>
          <p>检查 YAML 语法、字段完整性和人物一致性，确保输出剧本格式规范、可程序化处理。</p>
        </div>
      </div>
    </section>

    <!-- ═══ 流程说明 ═══ -->
    <section class="flow-section">
      <h2 class="section-title">创作流程</h2>
      <div class="flow-bar">
        <div class="flow-node">
          <div class="node-circle">1</div>
          <span>小说输入</span>
        </div>
        <div class="flow-line"></div>
        <div class="flow-node">
          <div class="node-circle">2</div>
          <span>故事解析</span>
        </div>
        <div class="flow-line"></div>
        <div class="flow-node">
          <div class="node-circle">3</div>
          <span>剧本生成</span>
        </div>
        <div class="flow-line"></div>
        <div class="flow-node">
          <div class="node-circle">4</div>
          <span>Schema 校验</span>
        </div>
        <div class="flow-line"></div>
        <div class="flow-node">
          <div class="node-circle">5</div>
          <span>预览导出</span>
        </div>
      </div>
    </section>

    <!-- ═══ 底部 CTA ═══ -->
    <section class="cta">
      <p class="cta-text">开始将小说改编为可编辑、可校验、可导出的剧本初稿。</p>
      <button class="neu-btn neu-btn-blue neu-btn-lg" @click="$router.push('/analyze')">
        立即开始创作 →
      </button>
    </section>

    <!-- 底部 -->
    <footer class="footer">
      <span>Story2Script Agent · AI 小说剧本结构化改编平台</span>
    </footer>
  </div>
</template>

<script setup lang="ts">
function scrollTo(id: string) {
  const el = document.getElementById(id)
  if (el) el.scrollIntoView({ behavior: 'smooth' })
}
</script>

<style scoped>
.landing {
  background: var(--neu-bg);
  min-height: 100vh;
  font-family: 'Inter', 'PingFang SC', 'Microsoft YaHei', system-ui, sans-serif;
  color: var(--text-primary);
}

/* ── 导航栏 ── */
.navbar {
  position: sticky;
  top: 0;
  z-index: 100;
  background: rgba(224,229,236,0.85);
  backdrop-filter: blur(12px);
  padding: 12px 24px;
}
.nav-inner {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.nav-logo {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.02em;
}
.nav-links {
  display: flex;
  gap: 8px;
  align-items: center;
}
.nav-btn {
  background: var(--neu-bg-light);
  border: none;
  border-radius: 24px;
  box-shadow: var(--neu-shadow-sm-out);
  padding: 8px 18px;
  font-size: 0.85rem;
  font-weight: 500;
  color: var(--text-secondary);
  cursor: pointer;
  text-decoration: none;
  transition: all 0.2s;
  font-family: inherit;
  white-space: nowrap;
}
.nav-btn:hover {
  box-shadow: var(--neu-shadow-hover);
  color: var(--text-primary);
  transform: translateY(-1px);
}
.nav-btn-cta {
  background: var(--accent-blue);
  color: #fff;
}

/* ── Hero ── */
.hero {
  padding: 60px 24px 50px;
}
.hero-inner {
  max-width: 1180px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 60px;
  align-items: center;
}

.hero-left {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.hero-title {
  font-size: 2.8rem;
  font-weight: 800;
  margin: 0;
  color: var(--text-primary);
  letter-spacing: -0.03em;
  text-shadow: 2px 2px 0 rgba(255,255,255,0.5);
}
.hero-title .accent {
  color: var(--accent-blue);
}
.hero-sub {
  font-size: 1.2rem;
  font-weight: 500;
  color: var(--text-secondary);
  margin: 0;
}
.hero-desc {
  font-size: 0.95rem;
  color: var(--text-hint);
  line-height: 1.7;
  margin: 0;
  max-width: 480px;
}

.hero-actions {
  display: flex;
  gap: 12px;
  margin-top: 4px;
}

/* Neumorphic buttons */
.neu-btn {
  border: none;
  border-radius: var(--neu-radius-sm);
  box-shadow: var(--neu-shadow-sm-out);
  cursor: pointer;
  font-family: inherit;
  font-weight: 500;
  transition: all 0.2s;
  background: var(--neu-bg-light);
  color: var(--text-primary);
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}
.neu-btn:hover {
  box-shadow: var(--neu-shadow-hover);
  transform: translateY(-1px);
}
.neu-btn:active {
  box-shadow: var(--neu-shadow-sm-in);
  transform: translateY(0);
}
.neu-btn-blue { background: var(--accent-blue); color: #fff; }
.neu-btn-lg { padding: 12px 32px; font-size: 1rem; }

/* Hero tags */
.hero-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 4px;
}
.hero-tag {
  font-size: 0.8rem;
  padding: 5px 12px;
  background: var(--neu-bg);
  border-radius: 20px;
  box-shadow: var(--neu-shadow-sm-in);
  color: var(--text-secondary);
  font-weight: 500;
}

/* ── 右侧预览卡片 ── */
.hero-right {
  display: flex;
  justify-content: center;
}
.preview-card {
  background: var(--neu-bg-light);
  border-radius: var(--neu-radius-lg);
  box-shadow: var(--neu-shadow-out);
  padding: 28px 32px;
  width: 100%;
  max-width: 480px;
}
.preview-title {
  font-weight: 700;
  font-size: 1rem;
  color: var(--text-primary);
  margin-bottom: 20px;
}

/* 流程 */
.preview-flow {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 4px;
  margin-bottom: 24px;
}
.flow-step {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.78rem;
  color: var(--text-secondary);
  font-weight: 500;
}
.flow-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--neu-bg-dark);
  box-shadow: var(--neu-shadow-sm-in);
}
.flow-dot.active {
  background: var(--accent-blue);
  box-shadow: 0 0 6px rgba(108,142,191,0.4);
}
.flow-arrow {
  color: var(--text-hint);
  font-size: 0.7rem;
  margin: 0 2px;
}

/* 预览统计 */
.preview-stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
}
.pstat {
  text-align: center;
  background: var(--neu-bg);
  border-radius: var(--neu-radius-sm);
  box-shadow: var(--neu-shadow-sm-in);
  padding: 12px 8px;
}
.pstat-val {
  display: block;
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-primary);
}
.pstat-val.ok { color: var(--accent-green); }
.pstat-lbl {
  display: block;
  font-size: 0.72rem;
  color: var(--text-hint);
  margin-top: 2px;
}

/* ── 核心能力 ── */
.features {
  padding: 40px 24px 50px;
}
.section-title {
  text-align: center;
  font-size: 1.6rem;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 32px;
  text-shadow: 1px 1px 0 rgba(255,255,255,0.5);
}
.features-grid {
  max-width: 1180px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}
.feature-card {
  background: var(--neu-bg-light);
  border-radius: var(--neu-radius);
  box-shadow: var(--neu-shadow-out);
  padding: 28px 24px;
  text-align: center;
  transition: all 0.3s;
}
.feature-card:hover {
  box-shadow: var(--neu-shadow-hover);
  transform: translateY(-2px);
}
.feat-icon {
  font-size: 2rem;
  margin-bottom: 12px;
}
.feature-card h3 {
  margin: 0 0 8px;
  font-size: 1.05rem;
  font-weight: 600;
  color: var(--text-primary);
}
.feature-card p {
  margin: 0;
  font-size: 0.85rem;
  color: var(--text-secondary);
  line-height: 1.6;
}

/* ── 流程说明 ── */
.flow-section {
  padding: 30px 24px 50px;
}
.flow-bar {
  max-width: 900px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0;
}
.flow-node {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  font-size: 0.85rem;
  font-weight: 500;
  color: var(--text-secondary);
}
.node-circle {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: var(--neu-bg-light);
  box-shadow: var(--neu-shadow-out);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1rem;
  color: var(--accent-blue);
}
.flow-line {
  flex: 1;
  height: 2px;
  background: var(--neu-bg-dark);
  box-shadow: var(--neu-shadow-sm-in);
  margin: 0 8px;
  max-width: 80px;
  min-width: 30px;
  margin-bottom: 24px;
}

/* ── CTA ── */
.cta {
  text-align: center;
  padding: 40px 24px 50px;
}
.cta-text {
  font-size: 1.1rem;
  color: var(--text-secondary);
  margin: 0 0 20px;
  font-weight: 500;
}

/* ── Footer ── */
.footer {
  text-align: center;
  padding: 20px 24px 30px;
  font-size: 0.8rem;
  color: var(--text-hint);
}

/* ── 响应式 ── */
@media (max-width: 900px) {
  .hero-inner {
    grid-template-columns: 1fr;
    gap: 36px;
  }
  .hero-title { font-size: 2.2rem; }
  .features-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .nav-links { display: none; }
}
@media (max-width: 600px) {
  .hero-title { font-size: 1.8rem; }
  .features-grid {
    grid-template-columns: 1fr;
  }
  .preview-flow { flex-direction: column; align-items: flex-start; }
  .flow-arrow { display: none; }
  .preview-stats { grid-template-columns: repeat(2, 1fr); }
  .flow-bar { flex-direction: column; gap: 16px; }
  .flow-line { display: none; }
}
</style>
