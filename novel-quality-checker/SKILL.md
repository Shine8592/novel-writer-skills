---
name: novel-quality-checker
description: >
  检查小说章节质量：字数、中文纯度、AI标记、模板化结尾、段落长度等8项指标。
  支持单章和批量检查，输出审核报告。
  使用场景：用户说"检查第X章质量"、"审核一下"、"看看这章行不行"、"批量检查所有章节"。
  NOT for: 创作、修改内容——只审核不写作。
---

# Novel Quality Checker — 章节质量审核

## 快速检查（5项核心）

```bash
python3 scripts/quality_check.py --file <章节文件> --quick
```

- 字数达标（≥12000）
- 中文纯度（>95%汉字）
- AI标记检测
- 模板化结尾检测
- 角色名一致性

## 全量检查（8项）

```bash
python3 scripts/quality_check.py --file <章节文件> --full
# 或批量扫描整个目录
python3 scripts/quality_check.py --dir <目录> --full
```

全量在快速基础上增加：对话比例、标点使用、段落长度。

## 审核维度

| 维度 | 标准 |
|------|------|
| 字数达标 | ≥12000字 |
| 中文纯度 | >95%汉字 |
| AI标记词 | 0个 |
| 模板化结尾 | 0个 |
| 角色名一致性 | 全文统一 |
| 对话比例 | 30-50% |
| 段落长度 | 无超长段落 |
| 标点使用 | 合理分布 |

## 脚本

- `scripts/quality_check.py` — 审核脚本（纯Python标准库，无需安装）
