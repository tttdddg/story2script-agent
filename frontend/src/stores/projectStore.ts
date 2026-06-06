import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { ChapterInfo, QualityReport, StoryBibleData, ValidationResult } from '@/api/project'

export const useProjectStore = defineStore('project', () => {
  const projectId = ref<string>('')
  const title = ref<string>('')
  const novelText = ref<string>('')
  const chapterCount = ref<number>(0)
  const wordCount = ref<number>(0)
  const chapters = ref<ChapterInfo[]>([])
  const loading = ref(false)
  const error = ref<string>('')

  const extracting = ref(false)
  const storyBible = ref<StoryBibleData | null>(null)

  const generating = ref(false)
  const yamlContent = ref<string>('')
  const sceneCount = ref<number>(0)

  const validating = ref(false)
  const repairing = ref(false)
  const validationResult = ref<ValidationResult | null>(null)
  const repairNotes = ref<string[]>([])
  const repairSuccess = ref(false)

  const reporting = ref(false)
  const reportData = ref<QualityReport | null>(null)

  function setProject(data: {
    project_id: string; title: string; chapter_count: number; word_count: number
  }) {
    projectId.value = data.project_id
    title.value = data.title
    chapterCount.value = data.chapter_count
    wordCount.value = data.word_count
  }

  function setChapters(data: { chapters: ChapterInfo[]; chapter_count: number }) {
    chapters.value = data.chapters
    chapterCount.value = data.chapter_count
  }

  function setNovelText(text: string, projectTitle?: string) {
    novelText.value = text
    if (projectTitle) title.value = projectTitle
  }

  function setLoading(val: boolean) { loading.value = val }
  function setError(msg: string) { error.value = msg }
  function setStoryBible(data: StoryBibleData) { storyBible.value = data }
  function setExtracting(val: boolean) { extracting.value = val }
  function setYamlContent(content: string) { yamlContent.value = content }
  function setSceneCount(count: number) { sceneCount.value = count }
  function setGenerating(val: boolean) { generating.value = val }
  function setValidationResult(r: ValidationResult | null) { validationResult.value = r }
  function setValidating(val: boolean) { validating.value = val }
  function setRepairing(val: boolean) { repairing.value = val }
  function setRepairNotes(notes: string[]) { repairNotes.value = notes }
  function setRepairSuccess(val: boolean) { repairSuccess.value = val }
  function setReportData(data: QualityReport | null) { reportData.value = data }
  function setReporting(val: boolean) { reporting.value = val }

  function reset() {
    projectId.value = ''
    title.value = ''
    novelText.value = ''
    chapterCount.value = 0
    wordCount.value = 0
    chapters.value = []
    loading.value = false
    error.value = ''
    storyBible.value = null
    extracting.value = false
    yamlContent.value = ''
    sceneCount.value = 0
    generating.value = false
    validationResult.value = null
    validating.value = false
    repairing.value = false
    repairNotes.value = []
    repairSuccess.value = false
    reportData.value = null
    reporting.value = false
  }

  return {
    projectId, title, novelText, chapterCount, wordCount, chapters,
    loading, error, storyBible, extracting,
    yamlContent, sceneCount, generating,
    validationResult, validating, repairing, repairNotes, repairSuccess,
    reportData, reporting,
    setProject, setChapters, setNovelText, setLoading, setError,
    setStoryBible, setExtracting, setYamlContent, setSceneCount, setGenerating,
    setValidationResult, setValidating, setRepairing, setRepairNotes, setRepairSuccess,
    setReportData, setReporting,
    reset,
  }
})
