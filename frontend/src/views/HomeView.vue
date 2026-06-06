<template>
  <div class="home-container">
    <header class="home-header">
      <h1>Story2Script Agent</h1>
      <p class="subtitle">AI 小说剧本结构化改编平台</p>
      <p class="description">
        输入 3 个章节以上的小说文本，自动完成章节解析、人物信息抽取、
        场景拆分、结构化剧本生成与校验，帮助创作者快速获得可编辑的剧本初稿。
      </p>
      <el-button
        type="primary"
        size="large"
        style="margin-top: 24px"
        @click="$router.push('/analyze')"
      >
        开始使用
      </el-button>
    </header>

    <main class="home-main">
      <el-card class="status-card">
        <template #header>
          <span>系统状态</span>
        </template>
        <div class="status-content">
          <el-tag :type="backendStatus === 'ok' ? 'success' : 'danger'">
            {{ backendStatus === 'ok' ? '后端服务正常' : '后端服务未连接' }}
          </el-tag>
        </div>
      </el-card>

      <el-card class="feature-card">
        <template #header>
          <span>功能模块</span>
        </template>
        <el-steps direction="vertical">
          <el-step title="小说输入与章节解析 ✅" description="粘贴文本或上传 .txt 文件，自动识别章节" status="success" />
          <el-step title="Story Bible 抽取 ✅" description="人物、地点、事件、关系抽取" status="success" />
          <el-step title="剧本 YAML 生成 ✅" description="结构化剧本生成与预览" status="success" />
          <el-step title="Schema 校验" description="格式与内容校验" />
          <el-step title="剧本预览与导出" description="结构化预览与 YAML 导出" />
        </el-steps>
      </el-card>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'

const backendStatus = ref<string>('unknown')

onMounted(async () => {
  try {
    const response = await axios.get('/api/health')
    backendStatus.value = response.data.status
  } catch {
    backendStatus.value = 'error'
  }
})
</script>

<style scoped>
.home-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  display: flex;
  flex-direction: column;
  align-items: center;
}

.home-header {
  text-align: center;
  padding: 60px 20px 40px;
}

.home-header h1 {
  font-size: 2.5rem;
  color: #303133;
  margin-bottom: 12px;
}

.subtitle {
  font-size: 1.2rem;
  color: #606266;
  margin-bottom: 8px;
}

.description {
  font-size: 0.95rem;
  color: #909399;
  max-width: 600px;
  margin: 0 auto;
  line-height: 1.6;
}

.home-main {
  width: 100%;
  max-width: 800px;
  padding: 0 20px 60px;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.status-content {
  display: flex;
  align-items: center;
  gap: 12px;
}
</style>
