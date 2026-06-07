<template>
  <div class="scene-preview" v-if="parsedData">
    <!-- 剧本信息 -->
    <div class="script-info" v-if="parsedData.script">
      <h2>{{ parsedData.script.title }}</h2>
      <div class="info-tags">
        <el-tag v-if="parsedData.script.genre" size="small">{{ parsedData.script.genre }}</el-tag>
        <el-tag v-if="parsedData.script.logline" type="info" size="small" class="logline-tag">
          {{ parsedData.script.logline }}
        </el-tag>
      </div>
    </div>

    <!-- 场景列表 -->
    <div class="scenes-list">
      <div
        v-for="scene in parsedData.scenes"
        :key="scene.scene_id"
        class="scene-card-wrap"
      >
        <el-card class="scene-card" shadow="hover">
          <template #header>
            <div class="scene-header">
              <span class="scene-title">
                {{ scene.scene_id }} · {{ scene.location || '未知地点' }}
              </span>
              <el-tag size="small" effect="plain">
                {{ scene.time || '' }}
              </el-tag>
            </div>
          </template>

          <!-- 场景信息 -->
          <div class="scene-meta">
            <div v-if="scene.source_chapter" class="meta-item">
              <span class="meta-label">来源章节：</span>
              <span>{{ scene.source_chapter }}</span>
            </div>
            <div v-if="scene.dramatic_purpose" class="meta-item">
              <span class="meta-label">戏剧目的：</span>
              <span>{{ scene.dramatic_purpose }}</span>
            </div>
            <div v-if="scene.conflict" class="meta-item">
              <span class="meta-label">冲突：</span>
              <span class="conflict-text">{{ scene.conflict }}</span>
            </div>
          </div>

          <!-- 出场人物 -->
          <div v-if="scene.characters?.length" class="scene-section">
            <span class="section-label">出场人物：</span>
            <el-tag
              v-for="char in scene.characters"
              :key="char"
              size="small"
              class="char-tag"
            >
              {{ char }}
            </el-tag>
          </div>

          <!-- 动作 -->
          <div v-if="scene.actions?.length" class="scene-section">
            <span class="section-label">动作：</span>
            <ul class="action-list">
              <li v-for="(act, i) in scene.actions" :key="i">{{ act }}</li>
            </ul>
          </div>

          <!-- 对白 -->
          <div v-if="scene.dialogues?.length" class="scene-section">
            <span class="section-label">对白：</span>
            <div class="dialogue-list">
              <div
                v-for="(d, i) in scene.dialogues"
                :key="i"
                class="dialogue-item"
              >
                <span class="dialogue-speaker">{{ d.speaker }}</span>
                <span v-if="d.emotion" class="dialogue-emotion">
                  [{{ d.emotion }}]
                </span>
                <span class="dialogue-line">{{ d.line }}</span>
              </div>
            </div>
          </div>

          <!-- 舞台提示 -->
          <div v-if="scene.stage_directions?.length" class="scene-section">
            <span class="section-label">舞台提示：</span>
            <ul class="stage-list">
              <li v-for="(sd, i) in scene.stage_directions" :key="i">{{ sd }}</li>
            </ul>
          </div>
        </el-card>
      </div>
    </div>
  </div>

  <div v-else-if="!parsedData" class="parse-error">
    <el-alert
      title="无法解析 YAML 内容，请查看源码视图"
      type="warning"
      show-icon
    />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import * as yaml from 'js-yaml'

const props = defineProps<{
  yamlContent: string
}>()

interface ParsedScript {
  script?: { title?: string; genre?: string; logline?: string }
  characters?: Array<Record<string, unknown>>
  scenes?: Array<{
    scene_id: string
    source_chapter?: string
    source_excerpt?: string
    location?: string
    time?: string
    characters?: string[]
    dramatic_purpose?: string
    conflict?: string
    actions?: string[]
    dialogues?: Array<{ speaker: string; emotion?: string; line: string }>
    stage_directions?: string[]
  }>
}

const parsedData = computed<ParsedScript | null>(() => {
  try {
    return yaml.load(props.yamlContent) as ParsedScript
  } catch {
    return null
  }
})
</script>

<style scoped>
.scene-preview {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.script-info {
  text-align: center;
  padding: 8px 0;
}
.script-info h2 {
  font-size: 1.4rem;
  color: var(--text-primary);
  margin: 0 0 8px;
  text-shadow: 1px 1px 0 rgba(255,255,255,0.5);
}

.info-tags {
  display: flex;
  gap: 8px;
  justify-content: center;
}

.logline-tag { max-width: 400px; }

/* Scene cards */
.scenes-list {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.scene-card-wrap :deep(.el-card) {
  border-radius: var(--neu-radius) !important;
  box-shadow: var(--neu-shadow-out) !important;
  transition: all 0.2s;
}
.scene-card-wrap :deep(.el-card):hover {
  box-shadow: var(--neu-shadow-sm-out) !important;
}

.scene-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.scene-title {
  font-weight: 600;
  color: var(--text-primary);
}

/* Meta */
.scene-meta {
  margin-bottom: 12px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.meta-item {
  font-size: 0.85rem;
  color: var(--text-secondary);
  line-height: 1.6;
}
.meta-label {
  color: var(--text-hint);
  font-weight: 500;
}
.conflict-text {
  color: var(--accent-orange);
  background: var(--accent-orange-light);
  padding: 2px 8px;
  border-radius: 6px;
}

/* Sections */
.scene-section {
  margin-top: 10px;
  font-size: 0.85rem;
}
.section-label {
  font-weight: 600;
  color: var(--accent-blue);
  display: block;
  margin-bottom: 6px;
}

.char-tag { margin: 2px 4px 2px 0; }

/* Lists */
.action-list, .stage-list {
  margin: 0;
  padding-left: 18px;
  color: var(--text-secondary);
  line-height: 1.6;
}

/* Dialogues — neumorphic inset */
.dialogue-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.dialogue-item {
  padding: 8px 12px;
  background: var(--neu-bg);
  border-radius: var(--neu-radius-sm);
  box-shadow: var(--neu-shadow-sm-in);
  border-left: 3px solid var(--accent-blue);
}
.dialogue-speaker {
  font-weight: 600;
  color: var(--accent-blue);
  margin-right: 6px;
}
.dialogue-emotion {
  color: var(--text-hint);
  font-size: 0.8rem;
  margin-right: 6px;
}
.dialogue-line {
  color: var(--text-primary);
  line-height: 1.5;
}

.parse-error { padding: 20px 0; }
</style>
