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

// ── 剧本生成相关 ──

export interface GenerateScriptResponse {
  project_id: string
  yaml_content: string
  scene_count: number
}

/** 生成剧本 YAML */
export async function generateScript(
  projectId: string
): Promise<GenerateScriptResponse> {
  const response = await extractApi.post<GenerateScriptResponse>(
    `/projects/${projectId}/generate`
  )
  return response.data
}

// ── YAML 校验与修复相关 ──

export interface ValidationError {
  path: string
  message: string
}

export interface ValidationResult {
  valid: boolean
  errors: ValidationError[]
  warnings: ValidationError[]
}

export interface ValidateResponse {
  project_id: string
  validation: ValidationResult
}

export interface RepairResponse {
  project_id: string
  repaired_yaml: string
  valid: boolean
  repair_notes: string[]
  remaining_errors: ValidationError[]
  remaining_warnings: ValidationError[]
}

/** 校验 YAML */
export async function validateYaml(
  projectId: string
): Promise<ValidateResponse> {
  const response = await api.post<ValidateResponse>(
    `/projects/${projectId}/validate`
  )
  return response.data
}

/** 自动修复 YAML */
export async function repairYaml(
  projectId: string
): Promise<RepairResponse> {
  const response = await extractApi.post<RepairResponse>(
    `/projects/${projectId}/repair`
  )
  return response.data
}
