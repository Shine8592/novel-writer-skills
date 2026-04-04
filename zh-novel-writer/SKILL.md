---
name: zh-novel-writer
description: >
  批量生成网络小说章节。从大纲文件自动生成每章prompt，后台连续写作，
  自动分段生成，支持多API切换和重试。适用于中文网文（玄幻、修仙、都市等）。
  使用场景：用户给出大纲并要求"批量生成章节"、"写第X章到第Y章"、"直接开始写"、
  "不用问直接生成"、"后台静默写作"。NOT for: 单章精修、人工审稿、出版级校对。
---

# Novel Writer — 网络小说批量生成

## Quick Start

1. 确认大纲文件和章节范围
2. 读 `references/api-config.md` 获取可用API
3. 运行 `scripts/batch_generate.py` 或直接调用

## Workflow

```
大纲 → 逐章prompt → 逐个调用API → 分段生成 → 保存文件
```

## 关键规则

### 分段生成
单次API最大输出受限于模型的 max_tokens 参数。当章节内容超过单次输出上限时，
脚本会自动分段追加生成，直到达到目标字数（默认12000字）。

### API 容错
脚本按以下顺序尝试 API：
1. **ModelScope** (deepseek-ai/DeepSeek-V3.2) — 主力
2. **Fyra** (mistral-large-3-675b-instruct) — 备份
3. **Ph8** (qwen3-235b-a22b-2507) — 短文本补位

每个API 429 限流后自动等 30-60 秒重试，失败后切下一个API。

## References
- API 配置 → `references/api-config.md`
- Prompt 模板 → `references/prompt-template.md`
