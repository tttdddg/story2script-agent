1. 1. PR 2：新增小说输入、上传与章节解析功能

      #### PR 标题

      ```text
      PR 2: 新增小说输入、上传与章节解析功能
      ```

      #### 开发目标

      完成小说文本输入能力，支持用户粘贴文本或上传 txt 文件，并自动识别章节数量。

      #### 主要功能

      1. 前端新增小说输入组件。
      2. 支持 txt 文件上传。
      3. 后端新增项目创建接口。
      4. 后端实现章节识别逻辑。
      5. 校验输入文本是否不少于 3 个章节。
      6. 返回章节数量、章节标题、字数统计。

      #### 具体做法

      前端：

      1. 创建 `NovelInput.vue`。
      2. 提供文本输入框。
      3. 提供上传按钮。
      4. 提供“加载示例小说”按钮。
      5. 点击“开始解析”后调用后端接口。
      6. 展示章节数量和字数。

      后端：

      1. 创建 `chapter_parser.py`。
      2. 使用正则识别章节标题。
      3. 支持以下格式：
         - `第一章`
         - `第1章`
         - `Chapter 1`
         - `一、`
      4. 如果章节数少于 3，返回错误提示。
      5. 将解析结果保存到本地项目文件。

      #### 核心逻辑

      章节解析流程：

      ```text
      接收 novel_text
      → 清洗空行和特殊字符
      → 正则匹配章节标题
      → 按章节切分文本
      → 统计章节数和字数
      → 返回 chapters 列表
      ```

      #### 涉及文件

      ```text
      frontend/src/components/NovelInput.vue
      frontend/src/api/project.ts
      frontend/src/stores/projectStore.ts
      backend/app/api/routes_project.py
      backend/app/services/chapter_parser.py
      backend/app/schemas/request_schema.py
      backend/app/schemas/response_schema.py
      samples/sample_novel.txt
      ```

      #### 验收标准

      1. 可以粘贴小说文本。
      2. 可以上传 txt 文件。
      3. 可以加载示例小说。
      4. 系统能识别 3 个以上章节。
      5. 如果不足 3 章，前端显示明确错误提示。
      6. 章节标题和字数统计正常展示。

      #### 测试方式

      1. 使用示例小说测试。
      2. 使用不足 3 章文本测试。
      3. 使用不同章节标题格式测试。
      4. 检查接口返回是否正确。