"""剧本 YAML 对应的 Pydantic 模型"""

from pydantic import BaseModel, Field


class ScriptSource(BaseModel):
    """来源小说信息"""
    chapter_count: int = Field(0, description="原文章节数")
    word_count: int = Field(0, description="原文总字数")


class ScriptMeta(BaseModel):
    """剧本元信息"""
    title: str = Field(..., description="剧本标题")
    genre: str = Field("", description="剧本类型")
    logline: str = Field("", description="一句话梗概")
    source: ScriptSource = Field(default_factory=ScriptSource, description="来源信息")


class ScriptCharacter(BaseModel):
    """剧本人物"""
    id: str = Field(..., description="人物唯一 ID")
    name: str = Field(..., description="人物名称")
    aliases: list[str] = Field(default_factory=list, description="别名列表")
    role: str = Field("supporting", description="角色类型")
    personality: str = Field("", description="性格描述")
    motivation: str = Field("", description="角色动机")


class Dialogue(BaseModel):
    """结构化对白"""
    speaker: str = Field(..., description="说话人名称")
    emotion: str = Field("", description="情绪描述")
    line: str = Field(..., description="台词内容")


class Scene(BaseModel):
    """剧本场景"""
    scene_id: str = Field(..., description="场景唯一 ID")
    source_chapter: str = Field(..., description="来源章节标题")
    source_excerpt: str = Field("", description="原文相关片段")
    location: str = Field("", description="场景地点")
    time: str = Field("", description="时间描述")
    characters: list[str] = Field(default_factory=list, description="出场人物名称")
    dramatic_purpose: str = Field("", description="戏剧目的")
    conflict: str = Field("", description="核心冲突")
    actions: list[str] = Field(default_factory=list, description="动作描写")
    dialogues: list[Dialogue] = Field(default_factory=list, description="对白列表")
    stage_directions: list[str] = Field(default_factory=list, description="舞台提示")


class ScriptYaml(BaseModel):
    """完整剧本 YAML 结构"""
    script: ScriptMeta = Field(..., description="剧本元信息")
    characters: list[ScriptCharacter] = Field(default_factory=list, description="人物表")
    scenes: list[Scene] = Field(default_factory=list, description="场景列表")
