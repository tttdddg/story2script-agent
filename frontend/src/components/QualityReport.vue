<template>
  <div class="quality-report" v-if="report">
    <!-- 统计摘要卡片 -->
    <el-card class="report-section">
      <template #header>
        <span>📊 剧本统计</span>
      </template>
      <el-row :gutter="16">
        <el-col :xs="12" :sm="8" :md="4" v-for="stat in statCards" :key="stat.label">
          <div class="stat-card">
            <span class="stat-num">{{ stat.value }}</span>
            <span class="stat-label">{{ stat.label }}</span>
          </div>
        </el-col>
      </el-row>
    </el-card>

    <!-- 图表区 -->
    <el-row :gutter="16" class="charts-row">
      <!-- 人物出场次数 -->
      <el-col :xs="24" :md="12" v-if="report.character_appearances?.length">
        <el-card class="report-section">
          <template #header>
            <span>👤 人物出场次数</span>
          </template>
          <div ref="charChartRef" class="chart-container"></div>
        </el-card>
      </el-col>

      <!-- 场景对白数量 -->
      <el-col :xs="24" :md="12" v-if="report.scene_dialogue_stats?.length">
        <el-card class="report-section">
          <template #header>
            <span>💬 场景对白分布</span>
          </template>
          <div ref="dialogueChartRef" class="chart-container"></div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 冲突 / 对白饼图 -->
    <el-row :gutter="16" class="charts-row">
      <el-col :xs="24" :md="12">
        <el-card class="report-section">
          <template #header>
            <span>⚡ 冲突场景占比</span>
          </template>
          <div ref="conflictChartRef" class="chart-container chart-sm"></div>
        </el-card>
      </el-col>
      <el-col :xs="24" :md="12">
        <el-card class="report-section">
          <template #header>
            <span>📝 动作与对白</span>
          </template>
          <div ref="actionDialogueChartRef" class="chart-container chart-sm"></div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 优化建议 -->
    <el-card class="report-section" v-if="report.suggestions?.length">
      <template #header>
        <div class="section-header">
          <span>💡 优化建议</span>
          <el-tag size="small" type="warning">{{ report.suggestions.length }} 条</el-tag>
        </div>
      </template>
      <div class="suggestions-list">
        <div
          v-for="(s, i) in report.suggestions"
          :key="i"
          class="suggestion-item"
        >
          <el-icon style="margin-right: 8px; color: #e6a23c"><WarningFilled /></el-icon>
          <span>{{ s }}</span>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch, onMounted, nextTick } from 'vue'
import { WarningFilled } from '@element-plus/icons-vue'
import * as echarts from 'echarts'
import type { QualityReport } from '@/api/project'

const props = defineProps<{
  report: QualityReport | null
}>()

const charChartRef = ref<HTMLDivElement>()
const dialogueChartRef = ref<HTMLDivElement>()
const conflictChartRef = ref<HTMLDivElement>()
const actionDialogueChartRef = ref<HTMLDivElement>()

let charChart: echarts.ECharts | null = null
let dialogueChart: echarts.ECharts | null = null
let conflictChart: echarts.ECharts | null = null
let actionDialogueChart: echarts.ECharts | null = null

const statCards = computed(() => {
  if (!props.report) return []
  const r = props.report
  return [
    { label: '章节数', value: r.chapter_count },
    { label: '场景数', value: r.scene_count },
    { label: '人物数', value: r.character_count },
    { label: '对白数', value: r.dialogue_count },
    { label: '动作数', value: r.action_count },
    { label: '含冲突场景', value: r.conflict_scene_count },
  ]
})

function initCharChart() {
  if (!charChartRef.value || !props.report?.character_appearances?.length) return
  charChart?.dispose()
  charChart = echarts.init(charChartRef.value)

  const data = props.report.character_appearances
  charChart.setOption({
    tooltip: { trigger: 'axis' },
    grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
    xAxis: {
      type: 'category',
      data: data.map(d => d.name),
      axisLabel: { rotate: data.length > 4 ? 30 : 0 },
    },
    yAxis: { type: 'value', minInterval: 1 },
    series: [{
      type: 'bar',
      data: data.map(d => d.count),
      itemStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: '#409eff' },
          { offset: 1, color: '#79bbff' },
        ]),
        borderRadius: [4, 4, 0, 0],
      },
    }],
  })
}

function initDialogueChart() {
  if (!dialogueChartRef.value || !props.report?.scene_dialogue_stats?.length) return
  dialogueChart?.dispose()
  dialogueChart = echarts.init(dialogueChartRef.value)

  const data = props.report.scene_dialogue_stats
  dialogueChart.setOption({
    tooltip: { trigger: 'axis' },
    grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
    xAxis: {
      type: 'category',
      data: data.map(d => d.scene_id),
      axisLabel: { rotate: data.length > 4 ? 30 : 0 },
    },
    yAxis: { type: 'value', minInterval: 1 },
    series: [{
      type: 'line',
      data: data.map(d => d.dialogue_count),
      smooth: true,
      itemStyle: { color: '#67c23a' },
      areaStyle: { color: 'rgba(103, 194, 58, 0.1)' },
    }],
  })
}

function initConflictChart() {
  if (!conflictChartRef.value || !props.report) return
  conflictChart?.dispose()
  conflictChart = echarts.init(conflictChartRef.value)

  const r = props.report
  conflictChart.setOption({
    tooltip: { trigger: 'item' },
    series: [{
      type: 'pie',
      radius: ['45%', '75%'],
      center: ['50%', '55%'],
      data: [
        { name: '含冲突场景', value: r.conflict_scene_count, itemStyle: { color: '#67c23a' } },
        { name: '缺少冲突', value: r.scene_count - r.conflict_scene_count, itemStyle: { color: '#e6a23c' } },
      ],
      label: { formatter: '{b}\n{d}%' },
    }],
  })
}

function initActionDialogueChart() {
  if (!actionDialogueChartRef.value || !props.report) return
  actionDialogueChart?.dispose()
  actionDialogueChart = echarts.init(actionDialogueChartRef.value)

  const r = props.report
  actionDialogueChart.setOption({
    tooltip: { trigger: 'item' },
    series: [{
      type: 'pie',
      radius: ['45%', '75%'],
      center: ['50%', '55%'],
      data: [
        { name: '对白', value: r.dialogue_count, itemStyle: { color: '#409eff' } },
        { name: '动作', value: r.action_count, itemStyle: { color: '#e6a23c' } },
      ],
      label: { formatter: '{b}: {c} 条\n{d}%' },
    }],
  })
}

function initAllCharts() {
  nextTick(() => {
    initCharChart()
    initDialogueChart()
    initConflictChart()
    initActionDialogueChart()
  })
}

watch(() => props.report, () => {
  if (props.report) initAllCharts()
})

onMounted(() => {
  if (props.report) initAllCharts()
})
</script>

<style scoped>
.quality-report {
  margin-top: 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.stat-card {
  text-align: center;
  padding: 16px 8px;
  background: #f5f7fa;
  border-radius: 8px;
  margin-bottom: 12px;
}

.stat-num {
  display: block;
  font-size: 1.8rem;
  font-weight: 700;
  color: #409eff;
}

.stat-label {
  font-size: 0.85rem;
  color: #909399;
  margin-top: 4px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.charts-row {
  margin-bottom: 0;
}

.chart-container {
  height: 280px;
  width: 100%;
}

.chart-sm {
  height: 240px;
}

.suggestions-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.suggestion-item {
  display: flex;
  align-items: flex-start;
  padding: 10px 14px;
  background: #fdf6ec;
  border-radius: 6px;
  border-left: 3px solid #e6a23c;
  font-size: 0.9rem;
  color: #606266;
  line-height: 1.6;
}
</style>
