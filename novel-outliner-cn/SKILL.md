---
name: novel-outliner-cn
description: >
  从小说大纲自动拆解逐章prompt。支持纯文本、JSON、Markdown格式大纲，
  一键生成每章写作指令。
  用法：用户给出大纲文件并要求"拆解大纲"/"生成每章prompt"/"把大纲转成写作指令"。
NOT for: 写作、扩写——只负责从大纲生成prompt
---

# Novel Outliner — 大纲拆解

## 用法

```bash
python3 scripts/parse_outline.py --outline <大纲文件> --output <输出目录>
```

## 支持格式

- **纯文本**：按"第X章"分隔
- **JSON**：`{"chapters": {"1": {"title": "...", "plot": "..."}}}`
- **Markdown**：`# 第X章` 格式

## 输出

每章一个 prompt 文件（`.txt`）+ `chapters.json`（供 batch_generate.py 使用）

## 衔接逻辑

生成第N章prompt时，自动读取第N-1章已写好的内容结尾300字，注入「前章衔接」约束，保证连贯性。
