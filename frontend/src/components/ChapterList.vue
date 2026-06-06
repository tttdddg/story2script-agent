<template>
  <div class="chapter-list" v-if="store.chapters.length > 0">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>章节列表</span>
          <el-tag type="info" size="small">
            {{ store.chapterCount }} 章 · {{ store.wordCount }} 字
          </el-tag>
        </div>
      </template>

      <el-table
        :data="store.chapters"
        stripe
        style="width: 100%"
        :default-sort="{ prop: 'chapter_id', order: 'ascending' }"
      >
        <el-table-column prop="chapter_id" label="编号" width="120" sortable />
        <el-table-column prop="title" label="章节标题" min-width="200" />
        <el-table-column
          prop="word_count"
          label="字数"
          width="100"
          sortable
          align="right"
        />
        <el-table-column label="预览" width="80" align="center">
          <template #default="{ row }">
            <el-popover
              placement="left"
              :width="400"
              trigger="click"
              :title="row.title"
            >
              <template #reference>
                <el-button size="small" link type="primary">预览</el-button>
              </template>
              <div class="content-preview">{{ row.content }}</div>
            </el-popover>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { useProjectStore } from '@/stores/projectStore'

const store = useProjectStore()
</script>

<style scoped>
.chapter-list {
  margin-top: 24px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.content-preview {
  max-height: 300px;
  overflow-y: auto;
  white-space: pre-wrap;
  font-size: 0.9rem;
  line-height: 1.6;
  color: #303133;
}
</style>
