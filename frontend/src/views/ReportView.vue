<template>
  <div class="report-container">
    <div class="report-header">
      <el-button @click="$router.push('/')" link>
        <el-icon style="margin-right: 4px"><ArrowLeft /></el-icon>
        返回首页
      </el-button>
      <h1>剧本质量报告</h1>
    </div>

    <div class="report-main" v-if="store.reportData">
      <QualityReport :report="store.reportData" />
    </div>

    <div class="report-empty" v-else>
      <el-empty description="暂无报告数据，请先完成剧本生成">
        <el-button type="primary" @click="$router.push('/analyze')">
          前往生成
        </el-button>
      </el-empty>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ArrowLeft } from '@element-plus/icons-vue'
import QualityReport from '@/components/QualityReport.vue'
import { useProjectStore } from '@/stores/projectStore'

const store = useProjectStore()
</script>

<style scoped>
.report-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e7ed 100%);
  display: flex;
  flex-direction: column;
}

.report-header {
  text-align: center;
  padding: 30px 20px 20px;
}

.report-header h1 {
  font-size: 1.8rem;
  color: #303133;
  margin: 8px 0 4px;
}

.report-main {
  width: 100%;
  max-width: 900px;
  margin: 0 auto;
  padding: 0 20px 60px;
}

.report-empty {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
