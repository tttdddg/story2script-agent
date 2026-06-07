<template>
  <div class="validation-panel" v-if="validation">
    <el-card>
      <template #header>
        <div class="panel-header">
          <span class="panel-title">YAML 校验结果</span>
          <div class="header-actions">
            <el-tag
              :type="validation.valid ? 'success' : 'danger'"
              size="large"
              effect="dark"
            >
              {{ validation.valid ? '✅ 校验通过' : '❌ 校验未通过' }}
            </el-tag>
            <el-button
              type="primary"
              size="small"
              :loading="revalidating"
              @click="$emit('revalidate')"
              style="margin-left: 8px"
            >
              {{ revalidating ? '校验中...' : '🔄 重新校验' }}
            </el-button>
            <el-button
              v-if="!validation.valid"
              type="warning"
              size="small"
              :loading="repairing"
              @click="$emit('repair')"
              style="margin-left: 4px"
            >
              {{ repairing ? '修复中...' : '🔧 自动修复' }}
            </el-button>
            <el-button
              type="success"
              size="small"
              plain
              @click="$emit('export')"
              style="margin-left: 4px"
            >
              <el-icon style="margin-right: 4px"><Download /></el-icon>
              导出 YAML
            </el-button>
          </div>
        </div>
      </template>

      <!-- 校验清单 -->
      <div class="checklist-section">
        <h4 class="section-title">📋 校验清单</h4>
        <div
          v-for="item in checklist"
          :key="item.key"
          class="checklist-item"
          :class="'checklist-' + item.status"
        >
          <span class="checklist-icon">
            <span v-if="item.status === 'pass'">✅</span>
            <span v-else-if="item.status === 'warning'">⚠️</span>
            <span v-else>❌</span>
          </span>
          <div class="checklist-body">
            <span class="checklist-label">{{ item.label }}</span>
            <span class="checklist-detail">{{ item.description }}</span>
            <div v-if="item.issues.length" class="checklist-issues">
              <div
                v-for="(issue, i) in item.issues"
                :key="i"
                class="checklist-issue-item"
              >
                <code class="issue-path-tag">{{ issue.path }}</code>
                <span class="issue-msg-tag">{{ issue.message }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <el-divider />

      <!-- 统计摘要 -->
      <div class="validation-summary">
        <el-row :gutter="16">
          <el-col :span="8">
            <div class="stat-item stat-error">
              <span class="stat-count">{{ validation.errors.length }}</span>
              <span class="stat-label">错误</span>
            </div>
          </el-col>
          <el-col :span="8">
            <div class="stat-item stat-warning">
              <span class="stat-count">{{ validation.warnings.length }}</span>
              <span class="stat-label">警告</span>
            </div>
          </el-col>
          <el-col :span="8">
            <div class="stat-item" :class="validation.valid ? 'stat-ok' : 'stat-fail'">
              <span class="stat-count">{{ validation.valid ? '✓' : '✗' }}</span>
              <span class="stat-label">状态</span>
            </div>
          </el-col>
        </el-row>
      </div>

      <!-- 错误列表（有错误时展开） -->
      <div v-if="validation.errors.length" class="issue-list">
        <el-collapse>
          <el-collapse-item>
            <template #title>
              <div class="collapse-title error-collapse">
                <el-icon style="margin-right: 4px"><CircleCloseFilled /></el-icon>
                错误详情（{{ validation.errors.length }} 项）
              </div>
            </template>
            <div
              v-for="(err, i) in validation.errors"
              :key="'err' + i"
              class="issue-item issue-error"
            >
              <span class="issue-path">{{ err.path }}</span>
              <span class="issue-msg">{{ err.message }}</span>
            </div>
          </el-collapse-item>
        </el-collapse>
      </div>

      <!-- 警告列表（有警告时展开） -->
      <div v-if="validation.warnings.length" class="issue-list">
        <el-collapse>
          <el-collapse-item>
            <template #title>
              <div class="collapse-title warning-collapse">
                <el-icon style="margin-right: 4px"><WarningFilled /></el-icon>
                警告详情（{{ validation.warnings.length }} 项）
              </div>
            </template>
            <div
              v-for="(warn, i) in validation.warnings"
              :key="'warn' + i"
              class="issue-item issue-warning"
            >
              <span class="issue-path">{{ warn.path }}</span>
              <span class="issue-msg">{{ warn.message }}</span>
            </div>
          </el-collapse-item>
        </el-collapse>
      </div>

      <!-- 修复结果 -->
      <div v-if="repairNotes.length" class="repair-result">
        <el-divider />
        <h4>修复记录</h4>
        <el-timeline>
          <el-timeline-item
            v-for="(note, i) in repairNotes"
            :key="i"
            :type="i === repairNotes.length - 1 && repairSuccess ? 'success' : 'primary'"
          >
            {{ note }}
          </el-timeline-item>
        </el-timeline>
      </div>

      <!-- 无问题 -->
      <div v-if="!validation.errors.length && !validation.warnings.length" class="all-clear">
        <el-result icon="success" title="一切正常" sub-title="YAML 已通过所有校验项" />
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { CircleCloseFilled, WarningFilled, Download } from '@element-plus/icons-vue'
import type { ValidationResult } from '@/api/project'

const props = defineProps<{
  validation: ValidationResult | null
  repairing: boolean
  revalidating?: boolean
  repairNotes: string[]
  repairSuccess: boolean
}>()

defineEmits<{
  (e: 'repair'): void
  (e: 'revalidate'): void
  (e: 'export'): void
}>()

// ── 校验清单 ──
interface CheckEntry {
  key: string
  label: string
  description: string
  status: 'pass' | 'warning' | 'error'
  issues: { path: string; message: string }[]
}

const checklist = computed<CheckEntry[]>(() => {
  if (!props.validation) return []

  const { errors, warnings } = props.validation

  // 按路径分类错误
  const syntaxErrors = errors.filter(e => e.path === '(root)')
  const topFieldErrors = errors.filter(e =>
    e.path === '(root).script' || e.path === '(root).characters' ||
    e.path === '(root).scenes' || e.path === 'characters' || e.path === 'scenes'
  )
  const charFieldErrors = errors.filter(e =>
    /^characters\[\d+\]\.(id|name|role)$/.test(e.path) ||
    /^characters\[\d+\]$/.test(e.path)
  )
  const sceneReqErrors = errors.filter(e =>
    /^scenes\[\d+\]\.(scene_id|source_chapter|location|characters|dialogues)$/.test(e.path) ||
    (/^scenes\[\d+\]$/.test(e.path) && !e.path.includes('dialogues'))
  )
  const dialogueFieldErrors = errors.filter(e =>
    /^scenes\[\d+\]\.dialogues\[\d+\]\.(speaker|line)$/.test(e.path) &&
    !e.message.includes('未在 characters 中定义')
  )
  const consistencyErrors = errors.filter(e =>
    /^scenes\[\d+\]\.dialogues\[\d+\]\.speaker$/.test(e.path) &&
    e.message.includes('未在 characters 中定义')
  )

  // 增强建议的警告
  const enhanceWarnings = warnings.filter(e =>
    /^scenes\[\d+\]\.(conflict|time|actions)$/.test(e.path) ||
    /^scenes\[\d+\]\.dialogues$/.test(e.path)
  )

  return [
    {
      key: 'syntax',
      label: 'YAML 语法',
      description: syntaxErrors.length
        ? `${syntaxErrors.length} 个语法错误`
        : 'YAML 解析正常',
      status: syntaxErrors.length ? 'error' : 'pass',
      issues: syntaxErrors,
    },
    {
      key: 'top_fields',
      label: '顶层字段',
      description: topFieldErrors.length
        ? `缺少 ${topFieldErrors.length} 个顶层字段`
        : 'script / characters / scenes 完整',
      status: topFieldErrors.length ? 'error' : 'pass',
      issues: topFieldErrors,
    },
    {
      key: 'char_fields',
      label: '人物字段',
      description: charFieldErrors.length
        ? `${charFieldErrors.length} 个人物字段问题`
        : 'id / name / role 完整',
      status: charFieldErrors.length ? 'error' : 'pass',
      issues: charFieldErrors,
    },
    {
      key: 'scene_fields',
      label: '场景必填字段',
      description: sceneReqErrors.length
        ? `${sceneReqErrors.length} 个场景字段缺失`
        : 'scene_id / source_chapter / location / characters / dialogues 完整',
      status: sceneReqErrors.length ? 'error' : 'pass',
      issues: sceneReqErrors,
    },
    {
      key: 'dialogue_fields',
      label: '对白字段',
      description: dialogueFieldErrors.length
        ? `${dialogueFieldErrors.length} 个对白字段缺失`
        : 'speaker / line 完整',
      status: dialogueFieldErrors.length ? 'error' : 'pass',
      issues: dialogueFieldErrors,
    },
    {
      key: 'consistency',
      label: '人物一致性',
      description: consistencyErrors.length
        ? `${consistencyErrors.length} 处 Speaker 未在人物表中`
        : '所有 Speaker 均在人物表中',
      status: consistencyErrors.length ? 'error' : 'pass',
      issues: consistencyErrors,
    },
    {
      key: 'enhance',
      label: '增强建议',
      description: enhanceWarnings.length
        ? `${enhanceWarnings.length} 个建议项`
        : '所有增强字段完整',
      status: enhanceWarnings.length ? 'warning' : 'pass',
      issues: enhanceWarnings,
    },
  ]
})
</script>

<style scoped>
.validation-panel {
  margin-top: 24px;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
}

.panel-title {
  font-weight: 600;
}

.header-actions {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
}

/* ── 校验清单 ── */
.checklist-section {
  margin-bottom: 8px;
}

.section-title {
  margin: 0 0 12px;
  font-size: 1rem;
  color: #303133;
}

.checklist-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 10px 12px;
  margin-bottom: 6px;
  border-radius: 6px;
  border: 1px solid #ebeef5;
}

.checklist-pass {
  background: #f0f9eb;
  border-color: #e1f3d8;
}

.checklist-warning {
  background: #fdf6ec;
  border-color: #faecd8;
}

.checklist-error {
  background: #fef0f0;
  border-color: #fde2e2;
}

.checklist-icon {
  font-size: 1.2rem;
  flex-shrink: 0;
  margin-top: 1px;
}

.checklist-body {
  flex: 1;
  min-width: 0;
}

.checklist-label {
  font-weight: 600;
  color: #303133;
  display: block;
}

.checklist-detail {
  font-size: 0.85rem;
  color: #909399;
  display: block;
  margin-top: 2px;
}

.checklist-issues {
  margin-top: 6px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.checklist-issue-item {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  font-size: 0.82rem;
}

.issue-path-tag {
  font-family: monospace;
  font-size: 0.8rem;
  color: #909399;
  background: rgba(0,0,0,0.04);
  padding: 1px 6px;
  border-radius: 3px;
  flex-shrink: 0;
}

.issue-msg-tag {
  color: #606266;
}

/* ── 统计摘要 ── */
.validation-summary {
  margin-bottom: 8px;
}

.stat-item {
  text-align: center;
  padding: 12px;
  border-radius: 8px;
  background: #f5f7fa;
}

.stat-count {
  display: block;
  font-size: 1.5rem;
  font-weight: 700;
}

.stat-label {
  font-size: 0.85rem;
  color: #909399;
}

.stat-error .stat-count { color: #f56c6c; }
.stat-warning .stat-count { color: #e6a23c; }
.stat-ok .stat-count { color: #67c23a; }
.stat-fail .stat-count { color: #f56c6c; }

/* ── 折叠面板 ── */
.issue-list {
  margin-bottom: 4px;
}

.collapse-title {
  display: flex;
  align-items: center;
  font-weight: 600;
  font-size: 0.95rem;
}

.error-collapse { color: #f56c6c; }
.warning-collapse { color: #e6a23c; }

.issue-item {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  padding: 6px 10px;
  margin-bottom: 4px;
  border-radius: 4px;
  font-size: 0.85rem;
  line-height: 1.5;
}

.issue-error {
  background: #fef0f0;
  border-left: 3px solid #f56c6c;
}

.issue-warning {
  background: #fdf6ec;
  border-left: 3px solid #e6a23c;
}

.issue-path {
  font-family: monospace;
  color: #909399;
  flex-shrink: 0;
  min-width: 120px;
}

.issue-msg {
  color: #303133;
}

/* ── 修复结果 ── */
.repair-result {
  margin-top: 8px;
}

/* ── 全部通过 ── */
.all-clear {
  padding: 20px 0;
}
</style>
