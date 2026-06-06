import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { ChapterInfo } from '@/api/project'

export const useProjectStore = defineStore('project', () => {
  const projectId = ref<string>('')
  const title = ref<string>('')
  const novelText = ref<string>('')
  const chapterCount = ref<number>(0)
  const wordCount = ref<number>(0)
  const chapters = ref<ChapterInfo[]>([])
  const loading = ref(false)
  const error = ref<string>('')

  function setProject(data: {
    project_id: string
    title: string
    chapter_count: number
    word_count: number
  }) {
    projectId.value = data.project_id
    title.value = data.title
    chapterCount.value = data.chapter_count
    wordCount.value = data.word_count
  }

  function setChapters(data: {
    chapters: ChapterInfo[]
    chapter_count: number
  }) {
    chapters.value = data.chapters
    chapterCount.value = data.chapter_count
  }

  function setNovelText(text: string, projectTitle?: string) {
    novelText.value = text
    if (projectTitle) {
      title.value = projectTitle
    }
  }

  function setLoading(val: boolean) {
    loading.value = val
  }

  function setError(msg: string) {
    error.value = msg
  }

  function reset() {
    projectId.value = ''
    title.value = ''
    novelText.value = ''
    chapterCount.value = 0
    wordCount.value = 0
    chapters.value = []
    loading.value = false
    error.value = ''
  }

  return {
    projectId,
    title,
    novelText,
    chapterCount,
    wordCount,
    chapters,
    loading,
    error,
    setProject,
    setChapters,
    setNovelText,
    setLoading,
    setError,
    reset,
  }
})
