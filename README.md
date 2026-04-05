# 📚 Novel Writer Suite — AI Chinese Web Novel Creation Toolkit

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![Chinese](https://img.shields.io/badge/language-中文-red.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)
![Cost](https://img.shields.io/badge/cost-%A50-brightgreen.svg)

> **💰 Zero-cost creation.** From outline to full manuscript, completely free.
> **💰 零成本创作。** 从大纲到成稿，全流程免费。
> Already battle-tested: **50 chapters, 70+万字 (700K+ chars)** of xianxia novel《太初道果》Vol.1, **API cost = ¥0**.

---

## 🌟 Overview / 项目概述

**EN:** Novel Writer Suite is a batch creation toolchain for Chinese web novels, built on the OpenClaw skill ecosystem. From outline parsing → chapter generation → quality review, it provides an **end-to-end automated writing solution** — completely free.

**中文:** 一套专为中文网络小说设计的批量创作工具链，基于 OpenClaw/ClawHub 技能生态构建。大纲解析 → 章节生成 → 质量审核，端到端全自动写作。

| 对比项 / Contrast | 竞品 Competitors | Novel Writer Suite |
|--------|-------------------|
| **API 费用 Cost** | ChatGPT ~¥500/十万字 Claude ~¥800/十万字 | **¥0 — 全免费** |
| **订阅 Subscription** | ChatGPT Plus $20/mo, Claude Pro $20/mo | **无需任何订阅** |
| **创作上限 Limit** | 余额用完就停 | **无限制** |
| **50章成本 50 ch cost** | ¥100-300+ | **💰 ¥0** |

### 核心能力 / Core Features

- **大纲拆解** Parse outline → per-chapter prompts
- **批量生成** Batch generate 12,000-20,000 字/章 using free APIs (ModelScope DeepSeek-V3.2, Fyra, Ph8)
- **多API容错** ModelScope → Fyra → Ph8 auto-failover, 429 smart retry
- **上下文衔接** Previous chapter ending auto-injected for continuity
- **33维质量审核** 33-dimension quality checker (word count, Chinese purity, AI markers, repetition rate, outline compliance…)

---

## 🚀 Quick Start / 快速开始

### Install

```bash
git clone https://github.com/Shine8592/novel-writer-skills.git
cp -r novel-writer-skills/* ~/.openclaw/workspace/skills/
openclaw gateway restart
```

### 3 Steps to Generate a Novel

```bash
# ① Parse outline → per-chapter prompts
python3 novel-outliner/scripts/parse_outline.py --outline 大纲.md --output prompts/

# ② Batch generate chapters
python3 zh-novel-writer/scripts/batch_generate.py --start 1 --end 50 --output chapters/

# ③ Quality review (33 dimensions)
python3 novel-quality-checker/scripts/quality_check.py --dir chapters/ --full
```

---

## 📦 Toolchain / 工具链

### 1️⃣ Novel Outliner — 大纲解析器

> **Input:** Raw outline (text/JSON/Markdown)
> **Output:** Per-chapter writing prompts + `chapters.json`

- Auto-detect outline format
- 逐章拆解剧情、角色、备注
- 自动注入硬性约束（纯中文、零AI标记…）
- 前章结尾自动注入保证衔接

### 2️⃣ Novel Writer — 批量生成引擎

> **Input:** Outline / prompt files
> **Output:** Complete chapters, 12,000-20,000 字/章

- **分段生成** Auto-split 12,000+ chars into multiple API calls (ModelScope ~8K limit)
- **段落合并** Smart dedup with 200-char window overlap matching
- **多API容错** ModelScope → Fyra → Ph8 automatic fallback
- **429智能重试** Auto-wait 30-60s on rate limit, exponential backoff
- **上下文衔接** Read previous chapter ending 300 chars, inject into prompt
- **进度追踪** Auto-save after each chapter, resume on interrupt

| API | Model | 免费形式 Free Form | Status |
|-----|-------|------|--------|
| ModelScope | DeepSeek-V3.2 | 免费调用 Free | ✅ |
| Fyra | Mistral-Large-3-675B | 每日免费额度 Daily free | ✅ |
| Fyra | Qwen3-Next-80B | 每日免费额度 Daily free | ✅ |
| Ph8 | Qwen3-235B | 免费 Free | ⚠️ |

### 3️⃣ Quality Checker — 质量审核

> **33维审核 5层体系** (33 dimensions, 5 layers)

| Layer | Items | Examples |
|-------|-------|---------|
| L1 基础 | 5 | 字数、中文纯度、AI标记词、模板化结尾、段落长度 |
| L2 结构 | 8 | 重复率、对话比例、标点密度、段落节奏、句长… |
| L3 内容 | 7 | 情节推进、主角密度、冲突张力、金手指提及… |
| L4 格式 | 5 | 无阿拉伯数字、无英文、格式一致性… |
| L5 文学 | 8 | 开头吸引力、结尾完整度、角色一致性… |

---

## 📊 Battle-Tested Results / 实战成果

已完成《太初道果》第一卷（玄幻修仙，6卷×380章计划）：

| 指标 / Metric | 数据 / Data |
|------|------|
| **完成章节 Chapters** | 50/50 (100%) |
| **达标章节 Passed** | 42/50 (84%) |
| **总字数 Total Words** | 700,000+ 字 |
| **单章字数 Per Chapter** | 12,000-23,000 字 |
| **大纲符合度 Outline Coverage** | 100% |
| **API总花费 API Cost** | **💰 ¥0** |
| **质量审核通过率 Quality** | 31-33/33 维度 |

---

## 🎯 Use Cases / 适用场景

- ✅ **网文批量创作** — 修仙、玄幻、都市、言情
- ✅ **大纲驱动写作** — Outline-driven writing
- ✅ **长篇小说** — 60-380章长篇连载
- ✅ **零预算创作者** — Zero-budget, high quality
- ❌ 单篇精修 / 诗歌散文 / 出版级校对

---

## 📁 Directory Structure / 目录结构

```
novel-writer-skills/
├── README.md
├── novel-outliner/
│   ├── SKILL.md
│   └── scripts/parse_outline.py
├── zh-novel-writer/
│   ├── SKILL.md
│   ├── scripts/batch_generate.py
│   └── references/
│       ├── api-config.md
│       └── prompt-template.md
└── novel-quality-checker/
    ├── SKILL.md
    └── scripts/quality_check.py
```

---

## ⚡ FAQ

### Q: 真的完全免费吗？/ Is it really free?
**是的。** 多厂商免费额度 + 智能路由 = 永不花钱。已实测 70万字 ¥0 成本。

### Q: 可以自定义约束吗？/ Can I customize constraints?
可以。修改 `batch_generate.py` 中的 `HARD_CONSTRAINTS`，或在 prompt 中注入额外约束。

### Q: 支持其他 AI 服务吗？/ Other AI services?
支持任何 OpenAI-Compatible API。在 `api-config.md` 中添加配置即可。

---

## 🤝 Contributing

欢迎提交 Issue 和 Pull Request!

- 🐛 Bug → [New Issue](https://github.com/Shine8592/novel-writer-skills/issues)
- 💡 Feature Request → [New Issue](https://github.com/Shine8592/novel-writer-skills/issues)
- 📖 Doc → PR directly

---

## 📄 License

MIT License. See [LICENSE](LICENSE).

---

## 🙏 Acknowledgments

- **[OpenClaw](https://openclaw.ai/)** — 技能平台生态
- **[ClawHub](https://clawhub.ai/)** — 技能注册中心
- **[ModelScope](https://modelscope.cn/)** — DeepSeek-V3.2 免费 API
- **[Fyra.im](https://Fyra.im/)** — 免费额度支持
- **[Ph8.co](https://ph8.co/)** — Qwen 系列免费

---

> **Novel Writer Suite** — 让 AI 成为你的网文主笔，零成本创作 ✍️🔥