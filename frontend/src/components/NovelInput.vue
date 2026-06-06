<template>
  <div class="novel-input">
    <el-card class="input-card">
      <template #header>
        <div class="card-header">
          <span>小说输入</span>
          <div class="header-actions">
            <el-upload
              :auto-upload="false"
              :show-file-list="false"
              accept=".txt"
              @change="handleFileUpload"
            >
              <el-button size="small" :disabled="loading">
                <el-icon style="margin-right: 4px"><Upload /></el-icon>
                上传 TXT
              </el-button>
            </el-upload>
            <el-button size="small" @click="loadSample" :disabled="loading">
              <el-icon style="margin-right: 4px"><Document /></el-icon>
              加载示例小说
            </el-button>
          </div>
        </div>
      </template>

      <el-input
        v-model="novelText"
        type="textarea"
        :rows="14"
        placeholder="请粘贴小说文本（不少于 3 个章节），支持格式：第一章 / 第1章 / Chapter 1 / 一、"
        :disabled="loading"
      />

      <div class="input-footer">
        <div class="text-stats">
          <span v-if="novelText.length">共 {{ novelText.length }} 字符</span>
        </div>
        <el-button
          type="primary"
          size="large"
          @click="handleSubmit"
          :loading="loading"
          :disabled="!novelText.trim()"
        >
          {{ loading ? '正在解析...' : '开始解析' }}
        </el-button>
      </div>
    </el-card>

    <!-- Error alert -->
    <el-alert
      v-if="store.error"
      :title="store.error"
      type="error"
      show-icon
      closable
      class="error-alert"
      @close="store.setError('')"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Upload, Document } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { useProjectStore } from '@/stores/projectStore'
import { createProject } from '@/api/project'
import type { UploadFile } from 'element-plus'

const store = useProjectStore()
const novelText = ref(store.novelText)

interface Emits {
  (e: 'done'): void
}

const emit = defineEmits<Emits>()

const loading = ref(false)

function handleFileUpload(file: UploadFile) {
  const reader = new FileReader()
  reader.onload = (e) => {
    const text = e.target?.result as string
    if (text) {
      novelText.value = text
      store.setNovelText(text)
      ElMessage.success('文件已加载')
    }
  }
  reader.onerror = () => {
    ElMessage.error('文件读取失败')
  }
  if (file.raw) {
    reader.readAsText(file.raw, 'UTF-8')
  }
}

async function loadSample() {
  try {
    loading.value = true
    const response = await fetch('/samples/sample_novel.txt')
    if (!response.ok) {
      ElMessage.error('示例小说加载失败，请确认文件存在')
      return
    }
    const text = await response.text()
    novelText.value = text
    store.setNovelText(text, '示例小说')
    ElMessage.success('示例小说已加载')
  } catch {
    ElMessage.error('示例小说加载失败')
  } finally {
    loading.value = false
  }
}

async function handleSubmit() {
  if (!novelText.value.trim()) return

  store.reset()
  store.setNovelText(novelText.value)

  if (!store.title) {
    // 尝试从文本中提取第一行作为标题
    const firstLine = novelText.value.trim().split('\n')[0]
    store.setNovelText(novelText.value, firstLine.slice(0, 50) || '未命名项目')
  }

  loading.value = true
  store.setLoading(true)
  store.setError('')

  try {
    const result = await createProject({
      title: store.title,
      novel_text: novelText.value,
    })

    store.setProject(result)
    ElMessage.success(
      `解析成功：识别到 ${result.chapter_count} 个章节，共 ${result.word_count} 字`
    )
    emit('done')
  } catch (err: unknown) {
    if (err && typeof err === 'object' && 'response' in err) {
      const axiosErr = err as { response?: { data?: { detail?: string } } }
      const detail = axiosErr.response?.data?.detail || '请求失败'
      store.setError(detail)
    } else {
      store.setError('网络错误，请检查后端服务是否启动')
    }
  } finally {
    loading.value = false
    store.setLoading(false)
  }
}
</script>

<style scoped>
.novel-input {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-actions {
  display: flex;
  gap: 8px;
}

.input-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 16px;
}

.text-stats {
  color: #909399;
  font-size: 0.9rem;
}

.error-alert {
  margin-top: 8px;
}
</style>
