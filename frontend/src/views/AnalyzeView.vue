<template>
  <div class="analyze-container">
    <div class="analyze-header">
      <el-button @click="$router.push('/')" link>
        <el-icon style="margin-right: 4px"><ArrowLeft /></el-icon>
        返回首页
      </el-button>
      <h1>小说章节解析</h1>
      <p class="subtitle">输入小说文本，自动识别章节并抽取 Story Bible</p>
    </div>

    <div class="analyze-main">
      <!-- Step 1: Input & Parse -->
      <NovelInput @done="onParseDone" />
      <ChapterList />

      <!-- Step 2: Extract Story Bible -->
      <div v-if="store.projectId && store.chapters.length > 0" class="extract-section">
        <el-card>
          <div class="extract-area">
            <div class="extract-info">
              <span class="extract-label">Step 2: Story Bible 抽取</span>
              <span class="extract-hint">
                从 {{ store.chapterCount }} 个章节中抽取人物、地点、关键事件和人物关系
              </span>
            </div>
            <el-button
              type="primary"
              :loading="store.extracting"
              :disabled="store.extracting"
              @click="handleExtract"
            >
              {{ store.extracting ? 'AI 正在分析...' : '抽取 Story Bible' }}
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
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ArrowLeft } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import NovelInput from '@/components/NovelInput.vue'
import ChapterList from '@/components/ChapterList.vue'
import CharacterCards from '@/components/CharacterCards.vue'
import { useProjectStore } from '@/stores/projectStore'
import { extractStoryBible } from '@/api/project'

const store = useProjectStore()
const extractError = ref('')

function onParseDone() {
  // Reset extraction state when new parse happens
  store.setStoryBible(null as any)
  extractError.value = ''
}

async function handleExtract() {
  if (!store.projectId) return

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

.extract-section {
  margin-top: 24px;
}

.extract-area {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
}

.extract-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.extract-label {
  font-weight: 600;
  color: #303133;
}

.extract-hint {
  font-size: 0.85rem;
  color: #909399;
}

.error-alert {
  margin-top: 12px;
}
</style>
