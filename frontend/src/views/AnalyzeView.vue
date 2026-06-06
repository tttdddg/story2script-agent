<template>
  <div class="analyze-container">
    <div class="analyze-header">
      <el-button @click="$router.push('/')" link>
        <el-icon style="margin-right: 4px"><ArrowLeft /></el-icon>
        返回首页
      </el-button>
      <h1>小说章节解析</h1>
      <p class="subtitle">输入小说文本，自动识别章节 → 抽取 Story Bible → 生成剧本 YAML</p>
    </div>

    <div class="analyze-main">
      <!-- Step 1: Input & Parse -->
      <NovelInput @done="onParseDone" />
      <ChapterList />

      <!-- Step 2: Extract Story Bible -->
      <div v-if="store.projectId && store.chapters.length > 0" class="step-section">
        <el-card>
          <div class="step-area">
            <div class="step-info">
              <span class="step-label">Step 2: Story Bible 抽取</span>
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
      <div v-if="store.storyBible" class="step-section">
        <el-card>
          <div class="step-area">
            <div class="step-info">
              <span class="step-label">Step 3: 生成剧本 YAML</span>
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

      <!-- Step 4: Validate YAML -->
      <div v-if="store.yamlContent" class="step-section">
        <el-card>
          <div class="step-area">
            <div class="step-info">
              <span class="step-label">Step 4: YAML 校验</span>
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
        :repair-notes="store.repairNotes"
        :repair-success="store.repairSuccess"
        @repair="handleRepair"
      />

      <!-- Step 5: Export -->
      <div v-if="store.yamlContent" class="step-section export-section">
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

      <!-- Step 6: Quality Report -->
      <div v-if="store.yamlContent" class="step-section">
        <el-card>
          <div class="step-area">
            <div class="step-info">
              <span class="step-label">Step 6: 剧本质量报告</span>
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

      <!-- Step 6 Results: Quality Report -->
      <QualityReport :report="store.reportData" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
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
.analyze-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e7ed 100%);
  display: flex;
  flex-direction: column;
}

.analyze-header {
  text-align: center;
  padding: 30px 20px 20px;
}

.analyze-header h1 {
  font-size: 1.8rem;
  color: #303133;
  margin: 8px 0 4px;
}

.subtitle {
  font-size: 0.95rem;
  color: #909399;
  margin: 0;
}

.analyze-main {
  width: 100%;
  max-width: 900px;
  margin: 0 auto;
  padding: 0 20px 60px;
}

.step-section {
  margin-top: 24px;
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

.export-section {
  margin-top: 24px;
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
</style>
