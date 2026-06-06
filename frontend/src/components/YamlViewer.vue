<template>
  <div class="yaml-viewer" v-if="yamlContent">
    <el-card>
      <template #header>
        <div class="viewer-header">
          <span>剧本 YAML</span>
          <div class="viewer-actions">
            <el-button-group style="margin-right: 12px">
              <el-button
                :type="viewMode === 'source' ? 'primary' : ''"
                size="small"
                @click="viewMode = 'source'"
              >
                YAML 源码
              </el-button>
              <el-button
                :type="viewMode === 'preview' ? 'primary' : ''"
                size="small"
                @click="viewMode = 'preview'"
              >
                结构化预览
              </el-button>
            </el-button-group>
            <el-button size="small" @click="copyYaml">
              <el-icon style="margin-right: 4px"><CopyDocument /></el-icon>
              复制
            </el-button>
            <el-button size="small" @click="handleDownload">
              <el-icon style="margin-right: 4px"><Download /></el-icon>
              下载 YAML
            </el-button>
          </div>
        </div>
      </template>

      <!-- YAML 源码视图 -->
      <div v-if="viewMode === 'source'" class="source-view">
        <pre class="yaml-code"><code>{{ yamlContent }}</code></pre>
      </div>

      <!-- 结构化预览 -->
      <div v-else class="preview-view">
        <ScenePreview :yaml-content="yamlContent" />
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { CopyDocument, Download } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import ScenePreview from './ScenePreview.vue'

const props = defineProps<{
  yamlContent: string
  projectId?: string
}>()

const viewMode = ref<'source' | 'preview'>('preview')

async function copyYaml() {
  try {
    await navigator.clipboard.writeText(props.yamlContent)
    ElMessage.success('已复制到剪贴板')
  } catch {
    ElMessage.error('复制失败，请手动复制')
  }
}

async function handleDownload() {
  if (props.projectId) {
    // 使用后端导出（含正确文件名）
    try {
      const { downloadYaml } = await import('@/api/project')
      await downloadYaml(props.projectId)
      ElMessage.success('YAML 文件下载已开始')
      return
    } catch (e: unknown) {
      console.warn('后端导出失败，使用前端下载:', e)
    }
  }
  // 回退：前端直接下载
  const blob = new Blob([props.yamlContent], { type: 'text/yaml;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `story2script_output_${Date.now()}.yaml`
  a.click()
  URL.revokeObjectURL(url)
  ElMessage.success('下载已开始')
}
</script>

<style scoped>
.yaml-viewer {
  margin-top: 24px;
}

.viewer-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
}

.viewer-actions {
  display: flex;
  align-items: center;
}

.source-view {
  overflow: auto;
}

.yaml-code {
  background: #1e1e2e;
  color: #cdd6f4;
  padding: 20px;
  border-radius: 6px;
  font-size: 0.85rem;
  line-height: 1.6;
  overflow-x: auto;
  white-space: pre;
  margin: 0;
  font-family: 'Cascadia Code', 'Fira Code', 'Consolas', monospace;
}

.yaml-code code {
  font-family: inherit;
}
</style>
