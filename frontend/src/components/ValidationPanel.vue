<template>
  <div class="validation-panel" v-if="validation">
    <el-card>
      <template #header>
        <div class="panel-header">
          <span>YAML 校验结果</span>
          <div class="header-actions">
            <el-tag
              :type="validation.valid ? 'success' : 'danger'"
              size="large"
              effect="dark"
            >
              {{ validation.valid ? '✅ 校验通过' : '❌ 校验未通过' }}
            </el-tag>
            <el-button
              v-if="!validation.valid"
              type="warning"
              size="small"
              :loading="repairing"
              @click="$emit('repair')"
              style="margin-left: 12px"
            >
              {{ repairing ? '正在修复...' : '🔧 自动修复' }}
            </el-button>
          </div>
        </div>
      </template>

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

      <!-- 错误列表 -->
      <div v-if="validation.errors.length" class="issue-list">
        <h4 class="issue-title error-title">
          <el-icon style="margin-right: 4px"><CircleCloseFilled /></el-icon>
          错误（{{ validation.errors.length }} 项）
        </h4>
        <div
          v-for="(err, i) in validation.errors"
          :key="'err' + i"
          class="issue-item issue-error"
        >
          <span class="issue-path">{{ err.path }}</span>
          <span class="issue-msg">{{ err.message }}</span>
        </div>
      </div>

      <!-- 警告列表 -->
      <div v-if="validation.warnings.length" class="issue-list">
        <h4 class="issue-title warning-title">
          <el-icon style="margin-right: 4px"><WarningFilled /></el-icon>
          警告（{{ validation.warnings.length }} 项）
        </h4>
        <div
          v-for="(warn, i) in validation.warnings"
          :key="'warn' + i"
          class="issue-item issue-warning"
        >
          <span class="issue-path">{{ warn.path }}</span>
          <span class="issue-msg">{{ warn.message }}</span>
        </div>
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
import { CircleCloseFilled, WarningFilled } from '@element-plus/icons-vue'
import type { ValidationResult } from '@/api/project'

defineProps<{
  validation: ValidationResult | null
  repairing: boolean
  repairNotes: string[]
  repairSuccess: boolean
}>()

defineEmits<{
  (e: 'repair'): void
}>()
</script>

<style scoped>
.validation-panel {
  margin-top: 24px;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-actions {
  display: flex;
  align-items: center;
}

.validation-summary {
  margin-bottom: 20px;
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

.issue-list {
  margin-bottom: 16px;
}

.issue-title {
  display: flex;
  align-items: center;
  margin: 0 0 8px;
  font-size: 1rem;
}

.error-title { color: #f56c6c; }
.warning-title { color: #e6a23c; }

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

.repair-result {
  margin-top: 8px;
}

.all-clear {
  padding: 20px 0;
}
</style>
