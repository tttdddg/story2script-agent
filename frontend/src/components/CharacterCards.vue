<template>
  <div class="story-bible" v-if="store.storyBible">
    <!-- Characters -->
    <el-card class="bible-section">
      <template #header>
        <div class="section-header">
          <span>👤 人物列表</span>
          <el-tag size="small" type="primary">
            {{ store.storyBible.characters.length }} 人
          </el-tag>
        </div>
      </template>
      <el-row :gutter="16">
        <el-col
          v-for="char in store.storyBible.characters"
          :key="char.id"
          :xs="24"
          :sm="12"
          :md="8"
        >
          <el-card class="character-card" shadow="hover">
            <div class="char-header">
              <span class="char-name">{{ char.name }}</span>
              <el-tag
                :type="roleType(char.role)"
                size="small"
                effect="dark"
              >
                {{ roleLabel(char.role) }}
              </el-tag>
            </div>
            <div v-if="char.aliases.length" class="char-aliases">
              别名：{{ char.aliases.join('、') }}
            </div>
            <div v-if="char.personality" class="char-detail">
              <span class="label">性格：</span>{{ char.personality }}
            </div>
            <div v-if="char.motivation" class="char-detail">
              <span class="label">动机：</span>{{ char.motivation }}
            </div>
          </el-card>
        </el-col>
      </el-row>
    </el-card>

    <!-- Locations & Events row -->
    <el-row :gutter="16" class="bible-row">
      <!-- Locations -->
      <el-col :xs="24" :md="12">
        <el-card class="bible-section">
          <template #header>
            <div class="section-header">
              <span>📍 地点列表</span>
              <el-tag size="small" type="success">
                {{ store.storyBible.locations.length }} 处
              </el-tag>
            </div>
          </template>
          <el-tag
            v-for="loc in store.storyBible.locations"
            :key="loc"
            class="location-tag"
            size="large"
          >
            {{ loc }}
          </el-tag>
          <el-empty
            v-if="!store.storyBible.locations.length"
            description="暂无地点数据"
            :image-size="40"
          />
        </el-card>
      </el-col>

      <!-- Key Events -->
      <el-col :xs="24" :md="12">
        <el-card class="bible-section">
          <template #header>
            <div class="section-header">
              <span>⚡ 关键事件</span>
              <el-tag size="small" type="warning">
                {{ store.storyBible.key_events.length }} 件
              </el-tag>
            </div>
          </template>
          <el-timeline v-if="store.storyBible.key_events.length">
            <el-timeline-item
              v-for="evt in store.storyBible.key_events"
              :key="evt.event_id"
              :timestamp="evt.related_chapters?.join('、')"
              placement="top"
            >
              <p class="event-desc">{{ evt.description }}</p>
              <p v-if="evt.related_characters?.length" class="event-chars">
                相关人物：{{ evt.related_characters.join('、') }}
              </p>
            </el-timeline-item>
          </el-timeline>
          <el-empty
            v-else
            description="暂无事件数据"
            :image-size="40"
          />
        </el-card>
      </el-col>
    </el-row>

    <!-- Relationships -->
    <el-card class="bible-section" v-if="store.storyBible.relationships.length">
      <template #header>
        <div class="section-header">
          <span>🔗 人物关系</span>
          <el-tag size="small" type="info">
            {{ store.storyBible.relationships.length }} 组
          </el-tag>
        </div>
      </template>
      <div class="relation-list">
        <el-tag
          v-for="rel in store.storyBible.relationships"
          :key="`${rel.from_char}-${rel.to}`"
          class="relation-tag"
          size="large"
        >
          {{ rel.from_char }} → {{ rel.to }}：{{ rel.relation }}
        </el-tag>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { useProjectStore } from '@/stores/projectStore'

const store = useProjectStore()

function roleType(role: string): '' | 'primary' | 'danger' | 'warning' | 'info' {
  const map: Record<string, '' | 'primary' | 'danger' | 'warning' | 'info'> = {
    protagonist: '',
    antagonist: 'danger',
    supporting: 'primary',
    minor: 'info',
  }
  return map[role] || 'info'
}

function roleLabel(role: string): string {
  const map: Record<string, string> = {
    protagonist: '主角',
    antagonist: '对手',
    supporting: '配角',
    minor: '次要',
  }
  return map[role] || role
}
</script>

<style scoped>
.story-bible {
  margin-top: 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.bible-section {
  width: 100%;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.character-card {
  margin-bottom: 12px;
  height: 100%;
}

.char-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.char-name {
  font-size: 1.05rem;
  font-weight: 600;
  color: #303133;
}

.char-aliases {
  color: #909399;
  font-size: 0.85rem;
  margin-bottom: 8px;
}

.char-detail {
  font-size: 0.85rem;
  color: #606266;
  margin-bottom: 4px;
  line-height: 1.5;
}

.char-detail .label {
  color: #909399;
}

.bible-row {
  margin-bottom: 0;
}

.location-tag {
  margin: 4px 8px 4px 0;
}

.event-desc {
  color: #303133;
  margin: 0 0 4px;
  line-height: 1.5;
}

.event-chars {
  color: #909399;
  font-size: 0.8rem;
  margin: 0;
}

.relation-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.relation-tag {
  max-width: 100%;
}
</style>
