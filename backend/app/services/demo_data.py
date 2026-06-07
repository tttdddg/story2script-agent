"""
Demo 模式数据

当未配置 DEEPSEEK_API_KEY 时，后端自动进入 Demo 模式，
使用预计算的示例数据（基于 samples/sample_novel.txt），
让评委无需配置 API Key 也能完整体验系统流程。
"""

from app.schemas.response_schema import (
    CharacterInfo,
    KeyEventInfo,
    RelationshipInfo,
    StoryBibleData,
)
from app.schemas.script_schema import (
    Dialogue,
    Scene,
    ScriptCharacter,
    ScriptMeta,
    ScriptSource,
    ScriptYaml,
)


def get_demo_story_bible() -> StoryBibleData:
    """返回基于示例小说的预计算 Story Bible"""
    return StoryBibleData(
        characters=[
            CharacterInfo(
                id="char_001",
                name="林晚",
                aliases=["小晚"],
                role="protagonist",
                personality="敏感、倔强、重视表达真实",
                motivation="坚持自己的创作方式，不愿为商业化妥协",
            ),
            CharacterInfo(
                id="char_002",
                name="周屿",
                aliases=[],
                role="supporting",
                personality="沉默但坚定",
                motivation="弥补过去的遗憾，帮助林晚实现创作理想",
            ),
            CharacterInfo(
                id="char_003",
                name="陈姐",
                aliases=[],
                role="supporting",
                personality="理性、直接",
                motivation="帮助作者完成商业化改编",
            ),
        ],
        locations=["老城区咖啡馆", "咖啡馆门口", "出版社会议室", "老城区街道"],
        key_events=[
            KeyEventInfo(
                event_id="event_001",
                description="林晚收到编辑陈姐的修改意见，面临商业化改编压力",
                related_chapters=["第一章 退稿的傍晚"],
                related_characters=["林晚", "陈姐"],
            ),
            KeyEventInfo(
                event_id="event_002",
                description="雨夜中林晚与周屿在咖啡馆门口重逢",
                related_chapters=["第二章 雨夜重逢"],
                related_characters=["林晚", "周屿"],
            ),
            KeyEventInfo(
                event_id="event_003",
                description="林晚在出版社向陈姐展示新旧两版稿件",
                related_chapters=["第三章 旧稿与新剧本"],
                related_characters=["林晚", "陈姐"],
            ),
            KeyEventInfo(
                event_id="event_004",
                description="周屿带来出版的小说集，揭示过去的秘密付出",
                related_chapters=["第四章 改写与抉择"],
                related_characters=["林晚", "周屿"],
            ),
        ],
        relationships=[
            RelationshipInfo(
                from_char="林晚",
                to="周屿",
                relation="旧友，曾一起做纪录片，因误会断联三年后重逢",
            ),
            RelationshipInfo(
                from_char="林晚",
                to="陈姐",
                relation="编辑与作者，职业合作关系",
            ),
            RelationshipInfo(
                from_char="周屿",
                to="林晚",
                relation="默默帮助林晚实现创作理想",
            ),
        ],
    )


def get_demo_script_yaml() -> ScriptYaml:
    """返回基于示例小说的预计算剧本 YAML"""
    return ScriptYaml(
        script=ScriptMeta(
            title="雨夜重逢",
            genre="都市情感短剧",
            logline="一位被退稿的小说作者在雨夜重逢旧人，被迫重新面对过去与创作的选择。",
            source=ScriptSource(chapter_count=4, word_count=1021),
        ),
        characters=[
            ScriptCharacter(
                id="char_001",
                name="林晚",
                aliases=["小晚"],
                role="protagonist",
                personality="敏感、倔强、重视表达真实",
                motivation="坚持自己的创作方式，不愿为商业化妥协",
            ),
            ScriptCharacter(
                id="char_002",
                name="周屿",
                role="supporting",
                personality="沉默但坚定",
                motivation="弥补过去的遗憾，帮助林晚实现创作理想",
            ),
            ScriptCharacter(
                id="char_003",
                name="陈姐",
                role="supporting",
                personality="理性、直接",
                motivation="帮助作者完成商业化改编",
            ),
        ],
        scenes=[
            Scene(
                scene_id="scene_001",
                source_chapter="第一章 退稿的傍晚",
                source_excerpt="林晚坐在老城区咖啡馆的角落，盯着电脑屏幕上编辑发来的修改意见。",
                location="老城区咖啡馆",
                time="傍晚",
                characters=["林晚"],
                dramatic_purpose="引出女主的创作困境和内心挣扎",
                conflict="商业修改要求与作者表达之间的冲突",
                actions=[
                    "林晚低头看着电脑屏幕，手指停在删除键上。",
                    "她望向窗外的雨，合上电脑。",
                ],
                dialogues=[
                    Dialogue(
                        speaker="林晚",
                        emotion="压抑、自问",
                        line="如果所有沉默都要改成争吵，那它还是我的故事吗？",
                    ),
                ],
                stage_directions=[
                    "窗外开始下雨，咖啡馆灯光昏暗。",
                    "角落里有人在画速写，笔尖摩擦纸面的声音清晰可闻。",
                ],
            ),
            Scene(
                scene_id="scene_002",
                source_chapter="第二章 雨夜重逢",
                source_excerpt="雨越下越大，林晚站在咖啡馆门廊下犹豫着要不要冒雨离开。",
                location="老城区咖啡馆门口",
                time="夜晚",
                characters=["林晚", "周屿"],
                dramatic_purpose="引入男主的再次出现，制造重逢的情感张力",
                conflict="暌违三年的复杂情绪与未解的心结",
                actions=[
                    "周屿收起黑色长柄伞，雨水从伞尖滴落。",
                    "林晚握紧电脑包带子，脚步停在原地。",
                    "两人在昏暗的灯光下对视。",
                ],
                dialogues=[
                    Dialogue(speaker="周屿", emotion="克制、复杂", line="好久不见。"),
                    Dialogue(speaker="林晚", emotion="震惊、压抑", line="你怎么会在这里？"),
                ],
                stage_directions=[
                    "雨声渐大，雨水打在玻璃门上。",
                    "店员收拾桌椅的声音从店内传来。",
                ],
            ),
            Scene(
                scene_id="scene_003",
                source_chapter="第三章 旧稿与新剧本",
                source_excerpt="第二天上午，林晚比平时早了半小时到达出版社。会议室里只有她一个人。",
                location="出版社会议室",
                time="上午",
                characters=["林晚", "陈姐"],
                dramatic_purpose="展现女主在外部压力与内心坚持之间的抉择",
                conflict="两种创作理念的碰撞",
                actions=[
                    "林晚将新剧本大纲和旧稿并排摆在桌上。",
                    "陈姐推门进来，看到发黄的打印稿。",
                ],
                dialogues=[
                    Dialogue(speaker="陈姐", emotion="疑惑、好奇", line="这是什么？"),
                    Dialogue(
                        speaker="林晚",
                        emotion="坚定",
                        line="我的故事最初的样子。我已经知道怎么改剧本了。",
                    ),
                ],
                stage_directions=[
                    "晨光透过百叶窗照在会议桌上。",
                    "旧稿页面边缘的铅笔批注在光线下微微发亮。",
                ],
            ),
            Scene(
                scene_id="scene_004",
                source_chapter="第四章 改写与抉择",
                source_excerpt="周五傍晚，周屿再次出现在咖啡馆。这次没有雨，他带了一本新出版的小说集。",
                location="老城区咖啡馆",
                time="傍晚",
                characters=["林晚", "周屿"],
                dramatic_purpose="揭示男主过去的秘密付出，推动女主做出选择",
                conflict="对过去误解的释怀与创作方向的重新确认",
                actions=[
                    "周屿将一本新出版的小说集放在桌上。",
                    "林晚翻开扉页，看到自己的名字。",
                    "她抬头看他，眼睛里涌起泪光。",
                ],
                dialogues=[
                    Dialogue(
                        speaker="周屿",
                        emotion="平静、真诚",
                        line="三年前你写的那些，不该只留在我一个人的批注里。",
                    ),
                    Dialogue(
                        speaker="林晚", emotion="哽咽、释然", line="所以你一直在帮我。"
                    ),
                ],
                stage_directions=[
                    "夕阳从窗外照进来，咖啡馆染上暖金色。",
                    "角落里的速写本合上了，画画的人已经离开。",
                ],
            ),
        ],
    )


# ── 供 API 使用的便捷函数 ──


def get_demo_yaml_string() -> str:
    """返回预计算剧本的 YAML 字符串"""
    import yaml

    return yaml.dump(
        get_demo_script_yaml().model_dump(),
        allow_unicode=True,
        default_flow_style=False,
        sort_keys=False,
        indent=2,
    )


def get_demo_scene_count() -> int:
    """返回 Demo 剧本的场景数"""
    return 4
