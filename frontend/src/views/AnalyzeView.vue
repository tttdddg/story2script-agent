<template>
  <div class="workbench-container">
    <!-- 顶部导航 + 工作台头部 -->
    <header class="workbench-header">
      <div class="header-top">
        <el-button @click="$router.push('/')" link class="back-btn">
          <el-icon style="margin-right: 4px"><ArrowLeft /></el-icon>
          返回首页
        </el-button>
        <el-tag v-if="store.projectId" type="success" size="small" effect="plain">
          {{ store.title }}
        </el-tag>
      </div>
      <div class="header-main">
        <h1 class="workbench-title">📖 Story2Script 创作工作台</h1>
        <p class="workbench-desc">
          输入小说文本 → 智能解析章节 → 抽取故事要素 → 生成结构化剧本 → 校验与导出
        </p>
      </div>
    </header>

    <div class="workbench-main">
      <!-- 工作流程步骤条 -->
      <el-card class="steps-card" shadow="hover">
        <el-steps :active="currentStep" align-center finish-status="success">
          <el-step
            v-for="(step, idx) in stepsConfig"
            :key="idx"
            :title="step.title"
            :description="step.description"
          />
        </el-steps>
      </el-card>

      <!-- 统计卡片 -->
      <el-row :gutter="16" class="stats-row">
        <el-col :xs="12" :sm="8" :md="4" v-for="card in statsCards" :key="card.label">
          <el-card class="stat-card" shadow="hover">
            <div class="stat-content">
              <span class="stat-icon">{{ card.icon }}</span>
              <div class="stat-info">
                <span class="stat-value" :class="{ 'stat-placeholder': card.isPlaceholder }">
                  {{ card.displayValue }}
                </span>
                <span class="stat-label">{{ card.label }}</span>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>

      <!-- ========== 输入区 ========== -->
      <el-divider content-position="left">
        <span class="section-divider-title">📥 小说输入</span>
      </el-divider>

      <div ref="sectionInput">
        <NovelInput @done="onParseDone" />
        <ChapterList />
      </div>

      <!-- ========== 解析与生成区 ========== -->
      <template v-if="store.projectId && store.chapters.length > 0">
        <el-divider content-position="left">
          <span class="section-divider-title">🔍 故事解析与剧本生成</span>
        </el-divider>

        <!-- Step 2: Extract Story Bible -->
        <div ref="sectionExtract" class="step-section">
          <el-card>
            <div class="step-area">
              <div class="step-info">
                <span class="step-label">Story Bible 抽取</span>
                <span class="step-hint">
                  从 {{ store.chapterCount }} 个章节中抽取人物、地点、关键事件和人物关系
                </span>
              </div>
              <el-button
                type="primary"
                :loading="store.extracting"
                :disabled="store.extracting"
                @click="handleExtract"
              >
                {{ store.extracting ? 'AI 正在分析...' : store.storyBible ? '✓ 已抽取' : '抽取 Story Bible' }}
              </el-button>
            </div>
          </el-card>
          <el-alert
            v-if="extractError"
            :title="extractError"
            type="error"
            show-icon
            closable
            class="error-alert"
            @close="extractError = ''"
          />
        </div>

        <!-- Step 2 Results: Story Bible -->
        <CharacterCards />

        <!-- Step 3: Generate Script YAML -->
        <div v-if="store.storyBible" ref="sectionGenerate" class="step-section">
          <el-card>
            <div class="step-area">
              <div class="step-info">
                <span class="step-label">剧本 YAML 生成</span>
                <span class="step-hint">
                  基于 {{ store.chapterCount }} 个章节和
                  {{ store.storyBible.characters.length }} 个人物的 Story Bible 生成结构化剧本
                </span>
              </div>
              <el-button
                type="success"
                :loading="store.generating"
                :disabled="store.generating"
                @click="handleGenerate"
              >
                {{ store.generating ? 'AI 正在生成...' : store.yamlContent ? '✓ 已生成' : '生成剧本 YAML' }}
              </el-button>
            </div>
          </el-card>
          <el-alert
            v-if="generateError"
            :title="generateError"
            type="error"
            show-icon
            closable
            class="error-alert"
            @close="generateError = ''"
          />
        </div>

        <!-- Step 3 Results: YAML Viewer -->
        <YamlViewer
          :yaml-content="store.yamlContent"
          :project-id="store.projectId"
        />
      </template>

      <!-- ========== 校验与导出区 ========== -->
      <template v-if="store.yamlContent">
        <el-divider content-position="left">
          <span class="section-divider-title">✅ 校验与导出</span>
        </el-divider>

        <!-- Step 4: Validate YAML -->
        <div ref="sectionValidate" class="step-section">
          <el-card>
            <div class="step-area">
              <div class="step-info">
                <span class="step-label">YAML 校验</span>
                <span class="step-hint">
                  检查 YAML 语法、字段完整性、人物一致性
                </span>
              </div>
              <el-button
                type="info"
                :loading="store.validating"
                :disabled="store.validating"
                @click="handleValidate"
              >
                {{ store.validating ? '正在校验...' : store.validationResult ? '✓ 已校验' : '校验 YAML' }}
              </el-button>
            </div>
          </el-card>
        </div>

        <!-- Step 4 Results: Validation Panel -->
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

        <!-- Step 5: Quality Report -->
        <div ref="sectionReport" class="step-section">
          <el-card>
            <div class="step-area">
              <div class="step-info">
                <span class="step-label">剧本质量报告</span>
                <span class="step-hint">
                  统计关键指标并生成优化建议（不依赖大模型）
                </span>
              </div>
              <el-button
                type="warning"
                :loading="store.reporting"
                :disabled="store.reporting"
                @click="handleReport"
              >
                {{ store.reporting ? '正在生成...' : store.reportData ? '✓ 已生成' : '生成质量报告' }}
              </el-button>
            </div>
          </el-card>
        </div>

        <!-- Step 5 Results: Quality Report -->
        <QualityReport :report="store.reportData" />

        <!-- Step 6: Export -->
        <div ref="sectionExport" class="step-section export-section">
          <el-card>
            <div class="export-area">
              <div class="export-info">
                <span class="export-title">🎬 导出剧本</span>
                <span class="export-hint">下载 YAML 文件，可用于导入其他工具或存档</span>
              </div>
              <div class="export-actions">
                <el-button type="success" size="large" @click="handleExport">
                  <el-icon style="margin-right: 6px"><Download /></el-icon>
                  导出 YAML 文件
                </el-button>
              </div>
            </div>
          </el-card>
        </div>
      </template>

      <!-- 空状态：尚未输入小说 -->
      <div v-if="!store.projectId" class="empty-hint">
        <el-result icon="info" title="开始创作" sub-title="请在上方输入小说文本或加载示例小说，开始 AI 剧本创作流程">
          <template #extra>
            <span class="hint-steps">支持粘贴文本、上传 TXT 文件或加载内置示例</span>
          </template>
        </el-result>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, nextTick } from 'vue'
import { ArrowLeft, Download } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import NovelInput from '@/components/NovelInput.vue'
import ChapterList from '@/components/ChapterList.vue'
import CharacterCards from '@/components/CharacterCards.vue'
import YamlViewer from '@/components/YamlViewer.vue'
import ValidationPanel from '@/components/ValidationPanel.vue'
import QualityReport from '@/components/QualityReport.vue'
import { useProjectStore } from '@/stores/projectStore'
import { extractStoryBible, generateScript, validateYaml, repairYaml, downloadYaml, getReport } from '@/api/project'

const store = useProjectStore()
const extractError = ref('')
const generateError = ref('')

// ── 步骤条区域 refs（用于自动滚动） ──
const sectionInput = ref<HTMLElement | null>(null)
const sectionExtract = ref<HTMLElement | null>(null)
const sectionGenerate = ref<HTMLElement | null>(null)
const sectionValidate = ref<HTMLElement | null>(null)
const sectionReport = ref<HTMLElement | null>(null)
const sectionExport = ref<HTMLElement | null>(null)

// ── 步骤条配置 ──
const stepsConfig = [
  { title: '章节解析', description: '输入小说，自动识别章节' },
  { title: 'Story Bible', description: '抽取人物、地点、事件' },
  { title: '剧本生成', description: '生成结构化剧本 YAML' },
  { title: '格式校验', description: 'Schema 与一致性检查' },
  { title: '质量报告', description: '统计指标与优化建议' },
  { title: '导出剧本', description: '下载 YAML 文件' },
]

// 当前活跃步骤 (0-based)
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
  const charCount = store.storyBible?.characters.length
  const sc = store.sceneCount
  const vr = store.validationResult

  return [
    {
      label: '章节数',
      icon: '📄',
      displayValue: cc > 0 ? String(cc) : '--',
      isPlaceholder: cc === 0,
    },
    {
      label: '总字数',
      icon: '📝',
      displayValue: wc > 0 ? wc.toLocaleString() : '--',
      isPlaceholder: wc === 0,
    },
    {
      label: '人物数',
      icon: '👤',
      displayValue: charCount != null ? String(charCount) : '--',
      isPlaceholder: charCount == null,
    },
    {
      label: '场景数',
      icon: '🎬',
      displayValue: sc > 0 ? String(sc) : '--',
      isPlaceholder: sc === 0,
    },
    {
      label: '校验状态',
      icon: vr?.valid === true ? '✅' : vr?.valid === false ? '⚠️' : '⏳',
      displayValue: vr?.valid === true ? '通过' : vr?.valid === false ? '未通过' : '--',
      isPlaceholder: vr == null,
    },
  ]
})

// ── 自动滚动到当前步骤 ──
const sectionRefs: Record<number, ReturnType<typeof ref<HTMLElement | null>>> = {
  0: sectionInput,
  1: sectionExtract,
  2: sectionGenerate,
  3: sectionValidate,
  4: sectionReport,
  5: sectionExport,
}

watch(currentStep, async (newStep) => {
  await nextTick()
  const target = sectionRefs[newStep]?.value
  if (target) {
    target.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }
})

// ── 事件处理 ──
function onParseDone() {
  store.setStoryBible(null as any)
  store.setYamlContent('')
  store.setValidationResult(null)
  store.setReportData(null)
  extractError.value = ''
  generateError.value = ''
}

async function handleExtract() {
  if (!store.projectId || store.extracting) return

  store.setExtracting(true)
  extractError.value = ''

  try {
    const result = await extractStoryBible(store.projectId)
    store.setStoryBible(result.story_bible)
    ElMessage.success(
      `抽取完成：${result.story_bible.characters.length} 个人物，` +
      `${result.story_bible.locations.length} 个地点，` +
      `${result.story_bible.key_events.length} 个事件`
    )
  } catch (err: unknown) {
    if (err && typeof err === 'object' && 'response' in err) {
      const axiosErr = err as { response?: { data?: { detail?: string } } }
      extractError.value = axiosErr.response?.data?.detail || '抽取失败'
    } else {
      extractError.value = '网络错误，请检查后端服务是否启动'
    }
  } finally {
    store.setExtracting(false)
  }
}

async function handleGenerate() {
  if (!store.projectId || store.generating) return

  store.setGenerating(true)
  generateError.value = ''

  try {
    const result = await generateScript(store.projectId)
    store.setYamlContent(result.yaml_content)
    store.setSceneCount(result.scene_count)
    ElMessage.success(
      `剧本生成完成：共 ${result.scene_count} 个场景`
    )
  } catch (err: unknown) {
    if (err && typeof err === 'object' && 'response' in err) {
      const axiosErr = err as { response?: { data?: { detail?: string } } }
      generateError.value = axiosErr.response?.data?.detail || '生成失败'
    } else {
      generateError.value = '网络错误，请检查后端服务是否启动'
    }
  } finally {
    store.setGenerating(false)
  }
}

async function handleValidate() {
  if (!store.projectId || store.validating) return

  store.setValidating(true)

  try {
    const result = await validateYaml(store.projectId)
    store.setValidationResult(result.validation)
    if (result.validation.valid) {
      ElMessage.success('YAML 校验通过')
    } else {
      ElMessage.warning(
        `校验发现 ${result.validation.errors.length} 个错误，` +
        `${result.validation.warnings.length} 个警告`
      )
    }
  } catch (err: unknown) {
    if (err && typeof err === 'object' && 'response' in err) {
      const axiosErr = err as { response?: { data?: { detail?: string } } }
      ElMessage.error(axiosErr.response?.data?.detail || '校验失败')
    } else {
      ElMessage.error('网络错误，请检查后端服务是否启动')
    }
  } finally {
    store.setValidating(false)
  }
}

async function handleRepair() {
  if (!store.projectId || store.repairing) return

  store.setRepairing(true)
  store.setRepairNotes([])
  store.setRepairSuccess(false)

  try {
    const result = await repairYaml(store.projectId)
    store.setRepairNotes(result.repair_notes)
    store.setRepairSuccess(result.valid)

    if (result.repaired_yaml) {
      store.setYamlContent(result.repaired_yaml)
    }

    if (result.valid) {
      ElMessage.success('修复成功！YAML 已通过校验')
      // Re-validate to update the validation panel
      const validationResult = await validateYaml(store.projectId)
      store.setValidationResult(validationResult.validation)
    } else {
      if (result.remaining_errors.length === 0) {
        ElMessage.warning('部分修复完成，仍有警告')
      } else {
        ElMessage.warning(
          `修复完成但仍有 ${result.remaining_errors.length} 个错误`
        )
      }
    }
  } catch (err: unknown) {
    if (err && typeof err === 'object' && 'response' in err) {
      const axiosErr = err as { response?: { data?: { detail?: string } } }
      ElMessage.error(axiosErr.response?.data?.detail || '修复失败')
    } else {
      ElMessage.error('网络错误，请检查后端服务是否启动')
    }
  } finally {
    store.setRepairing(false)
  }
}

async function handleExport() {
  if (!store.projectId) return
  try {
    await downloadYaml(store.projectId)
    ElMessage.success('YAML 文件导出成功')
  } catch (err: unknown) {
    const msg = err instanceof Error ? err.message : '导出失败'
    ElMessage.error(msg)
  }
}

async function handleReport() {
  if (!store.projectId || store.reporting) return

  store.setReporting(true)

  try {
    const result = await getReport(store.projectId)
    store.setReportData(result.report)
    ElMessage.success(
      `报告生成完成：${result.report.scene_count} 场景，` +
      `${result.report.character_count} 人物，` +
      `${result.report.suggestions.length} 条建议`
    )
  } catch (err: unknown) {
    if (err && typeof err === 'object' && 'response' in err) {
      const axiosErr = err as { response?: { data?: { detail?: string } } }
      ElMessage.error(axiosErr.response?.data?.detail || '报告生成失败')
    } else {
      ElMessage.error('网络错误，请检查后端服务是否启动')
    }
  } finally {
    store.setReporting(false)
  }
}
</script>

<style scoped>
/* ── 整体容器 ── */
.workbench-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e7ed 100%);
  display: flex;
  flex-direction: column;
}

/* ── 工作台头部 ── */
.workbench-header {
  background: linear-gradient(135deg, #409eff 0%, #337ecc 100%);
  padding: 24px 20px 28px;
  color: #fff;
}

.header-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.back-btn {
  color: rgba(255, 255, 255, 0.85) !important;
}
.back-btn:hover {
  color: #fff !important;
}

.header-main {
  text-align: center;
}

.workbench-title {
  font-size: 1.8rem;
  font-weight: 700;
  margin: 0 0 8px;
  color: #fff;
}

.workbench-desc {
  font-size: 0.95rem;
  color: rgba(255, 255, 255, 0.8);
  margin: 0;
}

/* ── 主内容区 ── */
.workbench-main {
  width: 100%;
  max-width: 960px;
  margin: 0 auto;
  padding: 0 20px 60px;
}

/* ── 步骤条卡片 ── */
.steps-card {
  margin-top: -16px;
  position: relative;
  z-index: 1;
}

.steps-card :deep(.el-card__body) {
  padding: 20px 16px;
}

/* ── 统计卡片行 ── */
.stats-row {
  margin-top: 20px;
}

.stat-card {
  text-align: center;
}

.stat-card :deep(.el-card__body) {
  padding: 16px 12px;
}

.stat-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
}

.stat-icon {
  font-size: 1.8rem;
}

.stat-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #303133;
}

.stat-placeholder {
  color: #c0c4cc;
  font-weight: 400;
}

.stat-label {
  font-size: 0.8rem;
  color: #909399;
}

/* ── 区域分隔标题 ── */
.section-divider-title {
  font-weight: 600;
  font-size: 1rem;
  color: #303133;
}

/* ── 步骤区域 ── */
.step-section {
  margin-top: 20px;
}

.step-area {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
}

.step-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.step-label {
  font-weight: 600;
  color: #303133;
}

.step-hint {
  font-size: 0.85rem;
  color: #909399;
}

.error-alert {
  margin-top: 12px;
}

/* ── 导出区域 ── */
.export-section {
  margin-top: 20px;
}

.export-area {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
}

.export-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.export-title {
  font-weight: 600;
  font-size: 1.1rem;
  color: #303133;
}

.export-hint {
  font-size: 0.85rem;
  color: #909399;
}

.export-actions {
  flex-shrink: 0;
}

/* ── 空状态 ── */
.empty-hint {
  margin-top: 40px;
}

.hint-steps {
  color: #909399;
  font-size: 0.9rem;
}
</style>
