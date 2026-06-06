import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
})

export interface CreateProjectRequest {
  title: string
  novel_text: string
}

export interface CreateProjectResponse {
  project_id: string
  title: string
  chapter_count: number
  word_count: number
}

export interface ChapterInfo {
  chapter_id: string
  title: string
  word_count: number
  content: string
}

export interface ParseChaptersResponse {
  project_id: string
  chapter_count: number
  chapters: ChapterInfo[]
}

/** 创建项目并上传小说 */
export async function createProject(
  data: CreateProjectRequest
): Promise<CreateProjectResponse> {
  const response = await api.post<CreateProjectResponse>('/projects', data)
  return response.data
}

/** 重新解析项目章节 */
export async function parseChapters(
  projectId: string
): Promise<ParseChaptersResponse> {
  const response = await api.post<ParseChaptersResponse>(
    `/projects/${projectId}/parse`
  )
  return response.data
}

// ── Story Bible 相关 ──

export interface CharacterInfo {
  id: string
  name: string
  aliases: string[]
  role: string
  personality: string
  motivation: string
}

export interface KeyEventInfo {
  event_id: string
  description: string
  related_chapters: string[]
  related_characters: string[]
}

export interface RelationshipInfo {
  from_char: string
  to: string
  relation: string
}

export interface StoryBibleData {
  characters: CharacterInfo[]
  locations: string[]
  key_events: KeyEventInfo[]
  relationships: RelationshipInfo[]
}

export interface ExtractStoryBibleResponse {
  project_id: string
  story_bible: StoryBibleData
}

const extractApi = axios.create({
  baseURL: '/api',
  timeout: 120000, // LLM calls can be slow
})

/** 抽取 Story Bible */
export async function extractStoryBible(
  projectId: string
): Promise<ExtractStoryBibleResponse> {
  const response = await extractApi.post<ExtractStoryBibleResponse>(
    `/projects/${projectId}/extract`
  )
  return response.data
}
