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

// ── 导出相关 ──

/** 获取导出 YAML 文件的下载 URL */
export function getExportUrl(projectId: string): string {
  return `/api/projects/${projectId}/export`
}

/** 通过后端导出并下载 YAML 文件 */
export async function downloadYaml(projectId: string): Promise<void> {
  const response = await fetch(getExportUrl(projectId))
  if (!response.ok) {
    const err = await response.json().catch(() => ({ detail: '导出失败' }))
    throw new Error(err.detail || '导出失败')
  }

  // 从 Content-Disposition 头提取文件名
  const disposition = response.headers.get('Content-Disposition')
  let filename = 'story2script_output.yaml'
  if (disposition) {
    const match = disposition.match(/filename="?([^"]+)"?/)
    if (match) {
      filename = match[1]
    }
  }

  const blob = await response.blob()
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = filename
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}
