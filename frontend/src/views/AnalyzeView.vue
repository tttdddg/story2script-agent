<template>
  <div class="workbench">
    <!-- ═══ 顶部 Header ═══ -->
    <header class="wb-header">
      <div class="wb-header-inner">
        <div class="wb-header-left">
          <button class="neu-btn neu-btn-sm" @click="$router.push('/')">
            ← 首页
          </button>
        </div>
        <div class="wb-header-center">
          <h1 class="wb-title">Story2Script 创作工作台</h1>
          <p class="wb-subtitle">输入 3 章以上小说文本，自动生成可编辑、可校验、可导出的 YAML 剧本初稿</p>
        </div>
        <div class="wb-header-right">
          <button
            v-if="store.yamlContent"
            class="neu-btn neu-btn-sm"
            @click="handleExportMarkdown"
            style="margin-right:8px"
          >📝 导出 Markdown</button>
          <button
            v-if="store.yamlContent"
            class="neu-btn neu-btn-sm neu-btn-green"
            @click="handleExport"
          >📥 导出 YAML</button>
        </div>
      </div>
    </header>

    <div class="wb-body">
      <!-- ═══ 统计卡片 ═══ -->
      <div class="stats-row">
        <div v-for="c in statsCards" :key="c.label" class="neu-card stat-card">
          <span class="stat-icon">{{ c.icon }}</span>
          <span class="stat-val" :class="{ muted: c.ph }">{{ c.val }}</span>
          <span class="stat-lbl">{{ c.label }}</span>
        </div>
      </div>

      <!-- ═══ 主工作区：左 + 右 ═══ -->
      <div class="work-area">
        <!-- ═══ 左侧面板 ═══ -->
        <aside class="left-panel">
          <!-- 小说输入 -->
          <div class="neu-card">
            <div class="card-title">📝 小说输入</div>
            <div class="input-actions">
              <el-upload :auto-upload="false" :show-file-list="false" accept=".txt" @change="onFileUpload">
                <button class="neu-btn neu-btn-sm">📤 上传 TXT</button>
              </el-upload>
              <button class="neu-btn neu-btn-sm" @click="loadSampleText">📄 加载示例</button>
            </div>
            <textarea
              v-model="novelText"
              class="neu-textarea"
              rows="10"
              placeholder="请粘贴小说文本（不少于 3 个章节），支持格式：第一章 / 第1章 / Chapter 1 / 一、..."
              :disabled="loading"
            ></textarea>
            <div class="input-footer">
              <span class="char-count">{{ novelText.length }} 字符</span>
              <button
                class="neu-btn neu-btn-blue"
                :disabled="!novelText.trim() || loading"
                @click="doParse"
              >
                {{ loading ? '解析中...' : '▶ 开始解析' }}
              </button>
            </div>
            <div v-if="store.error" class="error-msg">{{ store.error }}</div>
          </div>

          <!-- 章节列表 -->
          <div v-if="store.chapters.length" class="neu-card">
            <div class="card-title">📑 章节解析 ({{ store.chapterCount }})</div>
            <div v-if="store.chapterCount < 3" class="hint-warn">⚠ 至少需要 3 个章节</div>
            <div
              v-for="ch in store.chapters"
              :key="ch.chapter_id"
              class="neu-item chapter-item"
            >
              <span class="ch-id">{{ ch.chapter_id }}</span>
              <span class="ch-title">{{ ch.title }}</span>
              <span class="ch-wc">{{ ch.word_count }} 字</span>
            </div>
          </div>

          <!-- 操作按钮区 -->
          <div class="neu-card">
            <div class="card-title">🎬 操作</div>
            <div class="action-grid">
              <button
                v-if="store.projectId && store.chapters.length"
                class="neu-btn neu-btn-blue"
                :disabled="store.extracting || !store.projectId"
                @click="handleExtract"
              >{{ store.extracting ? '抽取中...' : store.storyBible ? '✓ Story Bible' : '抽取 Story Bible' }}</button>

              <button
                v-if="store.storyBible"
                class="neu-btn neu-btn-purple"
                :disabled="store.generating"
                @click="handleGenerate"
              >{{ store.generating ? '生成中...' : store.yamlContent ? '✓ 剧本 YAML' : '生成剧本 YAML' }}</button>

              <button
                v-if="store.yamlContent"
                class="neu-btn"
                :disabled="store.validating"
                @click="handleValidate"
              >{{ store.validating ? '校验中...' : store.validationResult ? '✓ 已校验' : '重新校验' }}</button>

              <button
                v-if="store.yamlContent && !store.validationResult?.valid"
                class="neu-btn neu-btn-orange"
                :disabled="store.repairing"
                @click="handleRepair"
              >{{ store.repairing ? '修复中...' : '🔧 自动修复' }}</button>

              <button
                v-if="store.yamlContent"
                class="neu-btn"
                :disabled="store.reporting"
                @click="handleReport"
              >{{ store.reporting ? '生成中...' : store.reportData ? '✓ 质量报告' : '生成质量报告' }}</button>

              <button
                v-if="store.yamlContent"
                class="neu-btn neu-btn-green"
                @click="handleExport"
              >📥 导出 YAML</button>
            </div>
          </div>
        </aside>

        <!-- ═══ 右侧工作区 ═══ -->
        <main class="right-panel">
          <div class="neu-card result-card">
            <el-tabs v-model="activeTab" type="card" class="neu-tabs">
              <!-- Tab 1: Story Bible -->
              <el-tab-pane label="📖 Story Bible" name="bible">
                <div v-if="store.storyBible" class="tab-content">
                  <CharacterCards />
                </div>
                <div v-else class="empty-tab">
                  <div class="empty-icon">📖</div>
                  <p>尚未抽取 Story Bible</p>
                  <p class="hint">请先在左侧输入小说并点击「抽取 Story Bible」</p>
                </div>
              </el-tab-pane>

              <!-- Tab 2: 剧本预览 -->
              <el-tab-pane label="🎭 剧本预览" name="preview">
                <div v-if="store.yamlContent" class="tab-content">
                  <ScenePreview :yaml-content="store.yamlContent" />
                </div>
                <div v-else class="empty-tab">
                  <div class="empty-icon">🎭</div>
                  <p>尚未生成剧本</p>
                  <p class="hint">请先完成 Story Bible 抽取，然后点击「生成剧本 YAML」</p>
                </div>
              </el-tab-pane>

              <!-- Tab 3: YAML 源码 -->
              <el-tab-pane label="💻 YAML 源码" name="yaml">
                <div v-if="store.yamlContent" class="tab-content">
                  <div class="yaml-actions">
                    <button class="neu-btn neu-btn-sm" @click="copyYaml">📋 复制</button>
                    <button class="neu-btn neu-btn-sm neu-btn-green" @click="handleExport">📥 导出</button>
                  </div>
                  <pre class="yaml-code">{{ store.yamlContent }}</pre>
                </div>
                <div v-else class="empty-tab">
                  <div class="empty-icon">💻</div>
                  <p>尚未生成 YAML</p>
                  <p class="hint">请先完成剧本生成</p>
                </div>
              </el-tab-pane>

              <!-- Tab 4: Schema 校验 -->
              <el-tab-pane label="✅ Schema 校验" name="validate">
                <div v-if="store.validationResult" class="tab-content">
                  <ValidationPanel
                    :validation="store.validationResult"
                    :repairing="store.repairing"
                    :revalidating="store.validating"
                    :repair-notes="store.repairNotes"
                    :repair-success="store.repairSuccess"
                    @repair="handleRepair"
                    @revalidate="handleValidate"
                    @export="handleExport"
                  />
                </div>
                <div v-else class="empty-tab">
                  <div class="empty-icon">✅</div>
                  <p>尚未校验 YAML</p>
                  <p class="hint">请先生成剧本 YAML，然后点击「重新校验」</p>
                </div>
              </el-tab-pane>

              <!-- Tab 5: 质量报告 -->
              <el-tab-pane label="📊 质量报告" name="report">
                <div v-if="store.reportData" class="tab-content">
                  <QualityReport :report="store.reportData" />
                </div>
                <div v-else class="empty-tab">
                  <div class="empty-icon">📊</div>
                  <p>尚未生成质量报告</p>
                  <p class="hint">请先完成 YAML 校验，然后点击「生成质量报告」</p>
                </div>
              </el-tab-pane>
            </el-tabs>
          </div>
        </main>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import type { UploadFile } from 'element-plus'
import CharacterCards from '@/components/CharacterCards.vue'
import ScenePreview from '@/components/ScenePreview.vue'
import ValidationPanel from '@/components/ValidationPanel.vue'
import QualityReport from '@/components/QualityReport.vue'
import { useProjectStore } from '@/stores/projectStore'
import { createProject, parseChapters, extractStoryBible, generateScript, validateYaml, repairYaml, downloadYaml, getReport } from '@/api/project'
import yaml from 'js-yaml'

const store = useProjectStore()

// ── 局部状态 ──
const novelText = ref(store.novelText)
const loading = ref(false)
const extractError = ref('')
const generateError = ref('')
const activeTab = ref('bible')

const currentStep = computed(() => {
  if (!store.projectId) return 0
  if (store.chapters.length === 0) return 0
  if (!store.storyBible) return 1
  if (!store.yamlContent) return 2
  if (!store.validationResult) return 3
  if (!store.reportData) return 4
  return 5
})

// ── 统计卡片 ──
const statsCards = computed(() => {
  const cc = store.chapterCount
  const wc = store.wordCount
  const ch = store.storyBible?.characters.length
  const sc = store.sceneCount
  const vr = store.validationResult
  return [
    { label: '章节数', icon: '📄', val: cc > 0 ? String(cc) : '--', ph: cc === 0 },
    { label: '总字数', icon: '📝', val: wc > 0 ? wc.toLocaleString() : '--', ph: wc === 0 },
    { label: '人物数', icon: '👤', val: ch != null ? String(ch) : '--', ph: ch == null },
    { label: '场景数', icon: '🎬', val: sc > 0 ? String(sc) : '--', ph: sc === 0 },
    { label: '校验', icon: vr?.valid ? '✅' : vr ? '⚠️' : '⏳', val: vr?.valid ? '通过' : vr ? '未通过' : '--', ph: !vr },
  ]
})

// ── 自动切换 Tab ──
watch(currentStep, (s) => {
  if (s >= 5) activeTab.value = 'report'
  else if (s >= 4) activeTab.value = 'report'
  else if (s >= 3) activeTab.value = 'validate'
  else if (s >= 2) activeTab.value = 'preview'
  else if (s >= 1) activeTab.value = 'bible'
})

// ── 加载示例 ──
async function loadSampleText() {
  try {
    loading.value = true
    const res = await fetch('/samples/sample_novel.txt')
    if (!res.ok) return ElMessage.error('示例加载失败')
    const text = await res.text()
    novelText.value = text
    store.setNovelText(text, '示例小说')
    ElMessage.success('示例小说已加载')
  } catch { ElMessage.error('示例加载失败') } finally { loading.value = false }
}

// ── 文件上传 ──
function onFileUpload(file: UploadFile) {
  const reader = new FileReader()
  reader.onload = (e) => {
    const text = e.target?.result as string
    if (text) { novelText.value = text; store.setNovelText(text); ElMessage.success('文件已加载') }
  }
  reader.onerror = () => ElMessage.error('文件读取失败')
  if (file.raw) reader.readAsText(file.raw, 'UTF-8')
}

// ── 解析 ──
async function doParse() {
  if (!novelText.value.trim()) return
  store.reset()
  store.setNovelText(novelText.value)
  if (!store.title) store.setNovelText(novelText.value, novelText.value.trim().split('\n')[0].slice(0, 50) || '未命名')
  loading.value = true
  store.setLoading(true)
  store.setError('')
  try {
    const result = await createProject({ title: store.title, novel_text: novelText.value })
    store.setProject(result)
    // 获取章节列表
    const chResult = await parseChapters(result.project_id)
    store.setChapters({ chapters: chResult.chapters, chapter_count: chResult.chapter_count })
    ElMessage.success(`解析成功：${result.chapter_count} 章，${result.word_count} 字`)
    // 自动推进
    store.setStoryBible(null as any); store.setYamlContent(''); store.setValidationResult(null); store.setReportData(null)
    extractError.value = ''; generateError.value = ''
    setTimeout(() => handleExtract(), 200)
  } catch (err: any) {
    store.setError(err?.response?.data?.detail || '网络错误')
  } finally { loading.value = false; store.setLoading(false) }
}

// ── 抽取 Story Bible ──
async function handleExtract() {
  if (!store.projectId || store.extracting) return
  store.setExtracting(true); extractError.value = ''; let ok = false
  try {
    const result = await extractStoryBible(store.projectId)
    store.setStoryBible(result.story_bible); ok = true
    ElMessage.success(`抽取完成：${result.story_bible.characters.length} 人物，${result.story_bible.locations.length} 地点，${result.story_bible.key_events.length} 事件`)
  } catch (err: any) {
    extractError.value = err?.response?.data?.detail || '抽取失败'
  } finally { store.setExtracting(false) }
  if (ok) setTimeout(() => handleGenerate(), 200)
}

// ── 生成剧本 ──
async function handleGenerate() {
  if (!store.projectId || store.generating) return
  store.setGenerating(true); generateError.value = ''; let ok = false
  try {
    const result = await generateScript(store.projectId)
    store.setYamlContent(result.yaml_content); store.setSceneCount(result.scene_count); ok = true
    ElMessage.success(`生成完成：${result.scene_count} 个场景`)
  } catch (err: any) {
    generateError.value = err?.response?.data?.detail || '生成失败'
  } finally { store.setGenerating(false) }
  if (ok) setTimeout(() => handleValidate(), 200)
}

// ── 校验 ──
async function handleValidate() {
  if (!store.projectId || store.validating) return
  store.setValidating(true); let ok = false
  try {
    const result = await validateYaml(store.projectId)
    store.setValidationResult(result.validation); ok = true
    if (result.validation.valid) ElMessage.success('YAML 校验通过')
    else ElMessage.warning(`${result.validation.errors.length} 错误，${result.validation.warnings.length} 警告`)
  } catch (err: any) {
    ElMessage.error(err?.response?.data?.detail || '校验失败')
  } finally { store.setValidating(false) }
  if (ok) setTimeout(() => handleReport(), 200)
}

// ── 修复 ──
async function handleRepair() {
  if (!store.projectId || store.repairing) return
  store.setRepairing(true); store.setRepairNotes([]); store.setRepairSuccess(false)
  try {
    const result = await repairYaml(store.projectId)
    store.setRepairNotes(result.repair_notes); store.setRepairSuccess(result.valid)
    if (result.repaired_yaml) store.setYamlContent(result.repaired_yaml)
    if (result.valid) {
      ElMessage.success('修复成功')
      const vr = await validateYaml(store.projectId)
      store.setValidationResult(vr.validation)
    } else {
      ElMessage.warning(`仍有 ${result.remaining_errors.length} 个错误`)
    }
  } catch (err: any) {
    ElMessage.error(err?.response?.data?.detail || '修复失败')
  } finally { store.setRepairing(false) }
}

// ── 导出 ──
async function handleExport() {
  if (!store.projectId) return
  try { await downloadYaml(store.projectId); ElMessage.success('导出成功') }
  catch (e: any) { ElMessage.error(e.message || '导出失败') }
}

// ── 导出 Markdown ──
function handleExportMarkdown() {
  if (!store.yamlContent) return
  try {
    const data = yaml.load(store.yamlContent) as any
    const script = data?.script || {}
    const characters = data?.characters || []
    const scenes = data?.scenes || []

    let md = ''
    // 封面
    md += `# ${script.title || '剧本'}\n\n`
    if (script.genre) md += `**类型**：${script.genre}\n\n`
    if (script.logline) md += `> ${script.logline}\n\n`
    md += `---\n\n`

    // 人物表
    md += `## 人物表\n\n`
    md += `| 姓名 | 角色 | 性格 | 动机 |\n`
    md += `|------|------|------|------|\n`
    for (const ch of characters) {
      const roleMap: Record<string, string> = { protagonist: '主角', antagonist: '对手', supporting: '配角', minor: '次要' }
      md += `| ${ch.name || ''} | ${roleMap[ch.role] || ch.role || ''} | ${ch.personality || ''} | ${ch.motivation || ''} |\n`
    }
    md += `\n---\n\n`

    // 场景
    md += `## 场景列表\n\n`
    for (const sc of scenes) {
      md += `### ${sc.scene_id || ''} · ${sc.location || '未知地点'}\n\n`
      if (sc.source_chapter) md += `- **来源章节**：${sc.source_chapter}\n`
      if (sc.time) md += `- **时间**：${sc.time}\n`
      if (sc.characters?.length) md += `- **出场人物**：${sc.characters.join('、')}\n`
      if (sc.dramatic_purpose) md += `- **戏剧目的**：${sc.dramatic_purpose}\n`
      if (sc.conflict) md += `- **核心冲突**：${sc.conflict}\n`
      md += `\n`

      if (sc.actions?.length) {
        md += `**动作描写**：\n`
        for (const a of sc.actions) md += `- ${a}\n`
        md += `\n`
      }

      if (sc.dialogues?.length) {
        md += `**对白**：\n\n`
        for (const d of sc.dialogues) {
          const emo = d.emotion ? `（${d.emotion}）` : ''
          md += `> **${d.speaker || '?'}**${emo}：${d.line || ''}\n\n`
        }
      }

      if (sc.stage_directions?.length) {
        md += `**舞台提示**：\n`
        for (const sd of sc.stage_directions) md += `- ${sd}\n`
        md += `\n`
      }
      md += `---\n\n`
    }

    // 下载
    const blob = new Blob([md], { type: 'text/markdown;charset=utf-8' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${script.title || 'script'}_剧本.md`
    a.click()
    URL.revokeObjectURL(url)
    ElMessage.success('Markdown 导出成功')
  } catch (e: any) {
    ElMessage.error('Markdown 导出失败：' + (e.message || '未知错误'))
  }
}

// ── 报告 ──
async function handleReport() {
  if (!store.projectId || store.reporting) return
  store.setReporting(true)
  try {
    const result = await getReport(store.projectId)
    store.setReportData(result.report)
    ElMessage.success(`报告完成：${result.report.scene_count} 场景，${result.report.character_count} 人物`)
  } catch (err: any) {
    ElMessage.error(err?.response?.data?.detail || '报告失败')
  } finally { store.setReporting(false) }
}

// ── 复制 YAML ──
async function copyYaml() {
  try { await navigator.clipboard.writeText(store.yamlContent); ElMessage.success('已复制') }
  catch { ElMessage.error('复制失败') }
}
</script>

<style scoped>
/* ═══════════════════════════════════
   Workbench Layout
   ═══════════════════════════════════ */
.workbench {
  min-height: 100vh;
  background: var(--neu-bg);
  display: flex;
  flex-direction: column;
}

/* ── Header ── */
.wb-header {
  background: linear-gradient(135deg, #dce3ed 0%, #c8d4e2 50%, #d5dded 100%);
  padding: 18px 24px 14px;
}
.wb-header-inner {
  max-width: 1280px;
  margin: 0 auto;
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
}
.wb-header-left, .wb-header-right {
  flex-shrink: 0;
  display: flex;
  gap: 8px;
  align-items: center;
}
.wb-header-center {
  text-align: center;
  flex: 1;
}
.wb-title {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.02em;
  text-shadow: 1px 1px 0 rgba(255,255,255,0.5);
}
.wb-subtitle {
  margin: 4px 0 0;
  font-size: 0.85rem;
  color: var(--text-secondary);
}

/* ── Body ── */
.wb-body {
  max-width: 1280px;
  margin: 0 auto;
  padding: 16px 24px 40px;
  width: 100%;
  box-sizing: border-box;
}

/* ── Neumorphic base classes ── */
.neu-card {
  background: var(--neu-bg-light);
  border-radius: var(--neu-radius);
  box-shadow: var(--neu-shadow-out);
  padding: 16px 20px;
  border: none;
}
.neu-item {
  background: var(--neu-bg);
  border-radius: var(--neu-radius-sm);
  box-shadow: var(--neu-shadow-sm-out);
  padding: 10px 14px;
  margin-bottom: 6px;
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 0.85rem;
  transition: all 0.15s;
}
.neu-item:hover {
  box-shadow: var(--neu-shadow-sm-in);
}

/* ── Neumorphic buttons ── */
.neu-btn {
  background: var(--neu-bg-light);
  border: none;
  border-radius: var(--neu-radius-sm);
  box-shadow: var(--neu-shadow-sm-out);
  padding: 8px 16px;
  font-size: 0.85rem;
  font-weight: 500;
  color: var(--text-primary);
  cursor: pointer;
  transition: all 0.2s;
  font-family: inherit;
  white-space: nowrap;
}
.neu-btn:hover {
  box-shadow: var(--neu-shadow-hover);
  transform: translateY(-1px);
}
.neu-btn:active {
  box-shadow: var(--neu-shadow-sm-in);
  transform: translateY(0);
}
.neu-btn:disabled {
  opacity: 0.45;
  cursor: not-allowed;
}
.neu-btn-sm { padding: 6px 12px; font-size: 0.8rem; }
.neu-btn-blue { background: var(--accent-blue); color: #fff; }
.neu-btn-green { background: var(--accent-green); color: #fff; }
.neu-btn-purple { background: var(--accent-purple); color: #fff; }
.neu-btn-orange { background: var(--accent-orange); color: #fff; }

/* ── Neumorphic textarea ── */
.neu-textarea {
  width: 100%;
  background: var(--neu-bg);
  border: none;
  border-radius: var(--neu-radius-sm);
  box-shadow: var(--neu-shadow-sm-in);
  padding: 12px 14px;
  font-size: 0.85rem;
  font-family: 'SF Mono', 'Cascadia Code', 'Consolas', 'Microsoft YaHei', monospace;
  color: var(--text-primary);
  resize: vertical;
  box-sizing: border-box;
  line-height: 1.6;
}
.neu-textarea:focus {
  outline: none;
  box-shadow: var(--neu-shadow-sm-in), 0 0 0 2px var(--accent-blue-light);
}
.neu-textarea:disabled {
  opacity: 0.5;
}

/* ── Steps bar ── */
.steps-bar {
  margin-bottom: 14px;
}
.steps-bar :deep(.el-card__body) { padding: 14px 24px; }

/* ── Stats row ── */
.stats-row {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 12px;
  margin-bottom: 16px;
}
.stat-card {
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  padding: 14px 10px;
}
.stat-icon { font-size: 1.4rem; }
.stat-val { font-size: 1.6rem; font-weight: 700; color: var(--text-primary); }
.stat-val.muted { color: var(--text-hint); font-weight: 400; }
.stat-lbl { font-size: 0.75rem; color: var(--text-secondary); }

/* ── Work area ── */
.work-area {
  display: flex;
  gap: 16px;
  align-items: flex-start;
}

/* ── Left panel ── */
.left-panel {
  width: 32%;
  min-width: 280px;
  display: flex;
  flex-direction: column;
  gap: 14px;
  flex-shrink: 0;
}
.card-title {
  font-weight: 600;
  font-size: 0.95rem;
  color: var(--text-primary);
  margin-bottom: 12px;
}
.input-actions {
  display: flex;
  gap: 8px;
  margin-bottom: 10px;
}
.input-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 10px;
}
.char-count {
  font-size: 0.8rem;
  color: var(--text-hint);
}
.error-msg {
  margin-top: 8px;
  padding: 8px 12px;
  background: var(--accent-red-light);
  color: #b87070;
  border-radius: var(--neu-radius-sm);
  font-size: 0.85rem;
}
.hint-warn {
  padding: 6px 12px;
  background: var(--accent-orange-light);
  color: #b89060;
  border-radius: var(--neu-radius-sm);
  font-size: 0.8rem;
  margin-bottom: 8px;
}

/* Chapter items */
.chapter-item .ch-id {
  font-family: monospace;
  color: var(--accent-blue);
  font-size: 0.8rem;
  flex-shrink: 0;
}
.chapter-item .ch-title {
  flex: 1;
  font-weight: 500;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.chapter-item .ch-wc {
  font-size: 0.8rem;
  color: var(--text-hint);
  flex-shrink: 0;
}

/* Action grid */
.action-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
}
.action-grid .neu-btn {
  text-align: center;
  justify-content: center;
}

/* ── Right panel ── */
.right-panel {
  flex: 1;
  min-width: 0;
}
.result-card {
  min-height: 500px;
}
.neu-tabs {
  --el-tabs-header-height: 38px;
}

/* Tab content */
.tab-content {
  max-height: 620px;
  overflow-y: auto;
}

/* Empty tab */
.empty-tab {
  text-align: center;
  padding: 60px 20px;
  color: var(--text-secondary);
}
.empty-icon { font-size: 3rem; margin-bottom: 12px; }
.empty-tab p { margin: 4px 0; }
.empty-tab .hint { font-size: 0.85rem; color: var(--text-hint); }

/* YAML code */
.yaml-actions {
  display: flex;
  gap: 8px;
  margin-bottom: 10px;
}
.yaml-code {
  background: var(--neu-bg);
  box-shadow: var(--neu-shadow-sm-in);
  border-radius: var(--neu-radius-sm);
  padding: 16px;
  font-family: 'SF Mono', 'Cascadia Code', 'Consolas', monospace;
  font-size: 0.82rem;
  line-height: 1.6;
  color: var(--text-primary);
  max-height: 500px;
  overflow: auto;
  white-space: pre-wrap;
  word-break: break-all;
  margin: 0;
}

/* ── Responsive ── */
@media (max-width: 900px) {
  .stats-row { grid-template-columns: repeat(3, 1fr); }
  .work-area { flex-direction: column; }
  .left-panel { width: 100%; min-width: 0; }
}
@media (max-width: 600px) {
  .stats-row { grid-template-columns: repeat(2, 1fr); }
  .wb-header-inner { flex-direction: column; align-items: center; }
  .action-grid { grid-template-columns: 1fr; }
}
</style>
