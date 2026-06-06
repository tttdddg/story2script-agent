<template>
  <div class="analyze-container">
    <div class="analyze-header">
      <el-button @click="$router.push('/')" link>
        <el-icon style="margin-right: 4px"><ArrowLeft /></el-icon>
        返回首页
      </el-button>
      <h1>小说章节解析</h1>
      <p class="subtitle">输入小说文本，自动识别章节并统计信息</p>
    </div>

    <div class="analyze-main">
      <NovelInput @done="onParseDone" />
      <ChapterList />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ArrowLeft } from '@element-plus/icons-vue'
import NovelInput from '@/components/NovelInput.vue'
import ChapterList from '@/components/ChapterList.vue'

function onParseDone() {
  // Parse complete — ChapterList will reactively show results via the store
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
</style>
