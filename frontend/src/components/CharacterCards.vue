<template>
  <div class="story-bible" v-if="store.storyBible">
    <!-- ═══ 人物卡片区：占满整行 ═══ -->
    <section class="bible-section characters-section">
      <div class="section-header">
        <span>👤 人物列表</span>
        <el-tag size="small" type="primary">{{ store.storyBible.characters.length }} 人</el-tag>
      </div>
      <div class="char-grid">
        <div v-for="char in store.storyBible.characters" :key="char.id" class="char-card">
          <div class="char-head">
            <span class="char-name">{{ char.name }}</span>
            <el-tag :type="roleType(char.role)" size="small" effect="dark">
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
        </div>
      </div>
    </section>

    <!-- ═══ 下方：左右分区 ═══ -->
    <div class="bible-grid">
      <!-- 左侧：地点 + 人物关系 -->
      <aside class="bible-left">
        <!-- 地点列表 -->
        <section class="bible-section">
          <div class="section-header">
            <span>📍 地点列表</span>
            <el-tag size="small" type="success">{{ store.storyBible.locations.length }} 处</el-tag>
          </div>
          <div class="location-tags">
            <el-tag v-for="loc in store.storyBible.locations" :key="loc" class="loc-tag" size="large">
              {{ loc }}
            </el-tag>
          </div>
          <el-empty
            v-if="!store.storyBible.locations.length"
            description="暂无地点数据"
            :image-size="40"
          />
        </section>

        <!-- 人物关系 -->
        <section class="bible-section" v-if="store.storyBible.relationships.length">
          <div class="section-header">
            <span>🔗 人物关系</span>
            <el-tag size="small" type="info">{{ store.storyBible.relationships.length }} 组</el-tag>
          </div>
          <div class="relation-list">
            <div v-for="rel in store.storyBible.relationships" :key="`${rel.from_char}-${rel.to}`" class="rel-item">
              <span class="rel-from">{{ rel.from_char }}</span>
              <span class="rel-arrow">→</span>
              <span class="rel-to">{{ rel.to }}</span>
              <span class="rel-desc">{{ rel.relation }}</span>
            </div>
          </div>
        </section>
      </aside>

      <!-- 右侧：关键事件时间线 -->
      <section class="bible-section bible-right">
        <div class="section-header">
          <span>⚡ 关键事件</span>
          <el-tag size="small" type="warning">{{ store.storyBible.key_events.length }} 件</el-tag>
        </div>
        <div class="events-scroll" v-if="store.storyBible.key_events.length">
          <el-timeline>
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
        </div>
        <el-empty v-else description="暂无事件数据" :image-size="40" />
      </section>
    </div>
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
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* ── 通用 section ── */
.bible-section {
  background: var(--neu-bg-light);
  border-radius: var(--neu-radius);
  box-shadow: var(--neu-shadow-out);
  padding: 16px 20px;
}
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 14px;
  font-weight: 600;
  color: var(--text-primary);
  font-size: 0.95rem;
}

/* ── 人物卡片网格 ── */
.char-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 12px;
}

.char-card {
  background: var(--neu-bg);
  border-radius: var(--neu-radius-sm);
  box-shadow: var(--neu-shadow-sm-out);
  padding: 14px 16px;
  transition: all 0.2s;
}
.char-card:hover {
  box-shadow: var(--neu-shadow-sm-in);
}

.char-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}
.char-name {
  font-size: 1.05rem;
  font-weight: 600;
  color: var(--text-primary);
}
.char-aliases {
  color: var(--text-hint);
  font-size: 0.83rem;
  margin-bottom: 6px;
}
.char-detail {
  font-size: 0.83rem;
  color: var(--text-secondary);
  margin-bottom: 3px;
  line-height: 1.5;
}
.char-detail .label {
  color: var(--text-hint);
}

/* ── 下方网格：36% / 64% ── */
.bible-grid {
  display: grid;
  grid-template-columns: 36% 1fr;
  gap: 20px;
  align-items: start;
}

/* ── 左侧 ── */
.bible-left {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* 地点标签 */
.location-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
.loc-tag {
  margin: 0;
}

/* 人物关系 */
.relation-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.rel-item {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 12px;
  background: var(--neu-bg);
  border-radius: var(--neu-radius-sm);
  box-shadow: var(--neu-shadow-sm-in);
  font-size: 0.85rem;
  flex-wrap: wrap;
}
.rel-from, .rel-to {
  font-weight: 600;
  color: var(--text-primary);
}
.rel-arrow {
  color: var(--accent-blue);
  font-weight: 600;
}
.rel-desc {
  color: var(--text-secondary);
  margin-left: 4px;
}

/* ── 右侧：关键事件时间线 ── */
.bible-right {
  display: flex;
  flex-direction: column;
  min-height: 0;
}

.events-scroll {
  max-height: 440px;
  overflow-y: auto;
  padding-right: 4px;
}

.event-desc {
  color: var(--text-primary);
  margin: 0 0 4px;
  line-height: 1.5;
  font-size: 0.9rem;
}
.event-chars {
  color: var(--text-hint);
  font-size: 0.8rem;
  margin: 0;
}

/* ── 响应式 ── */
@media (max-width: 768px) {
  .bible-grid {
    grid-template-columns: 1fr;
  }
  .char-grid {
    grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  }
  .events-scroll {
    max-height: 340px;
  }
}
</style>
