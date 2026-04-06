# 📚 Novel Writer Suite — AI Chinese Web Novel Creation Toolkit

> **Write full-length Chinese novels with ¥0 API costs.** Powered by free AI tiers. Production-tested with 900K+ characters generated.

[![ClawHub Installs](https://img.shields.io/badge/ClawHub-118+installs-green)](https://clawhub.ai)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-skill-purple)](https://openclaw.ai)
[![Chinese](https://img.shields.io/badge/language-中文-red)](#-quick-start)

[中文说明](#-快速开始) | [English Docs](#-quick-start)

---

## ✨ Why This Exists

Most AI writing tools charge per-word. We used **only free API tiers** to write a complete 380-chapter xianxia novel (《太初道果》). Every character, every chapter — **zero yuan spent**.

This suite packages that entire pipeline into **3 reusable OpenClaw skills** anyone can install.

## 📦 What's Inside

| Skill | Purpose | Downloads |
|-------|---------|-----------|
| [**novel-outliner**](skills/novel-outliner/) | AI chapter outlining with emotional arc & plot tracking | 👇 31 |
| [**zh-novel-writer**](skills/zh-novel-writer/) | Full novel generation pipeline | 👇 25 |
| [**novel-quality-checker**](skills/novel-quality-checker/) | 3-stage review (duplicates, grammar, quality) | 👇 28 |

**Total installs:** 118+ across ClawHub

## 🏗️ Architecture — 6-Phase Pipeline

```
Think → Plan → Build → Review → Ship → Retro
```

Each chapter goes through a rigorous pipeline:

1. **Think** — Question framing. Where does this chapter fit in the story arc?
2. **Plan** — Extract outline, confirm constraints, allocate word counts
3. **Build** — Main author generation (free APIs only)
4. **Review** — 3-stage independent verification:
   - Auditor: duplicate rate check, logic consistency, outline alignment
   - Proofreader: typos, grammar, format
   - Quality Director: requirements checklist, pass/reject
5. **Ship** — Deliver with quality report (word count, duplicate rate, coverage)
6. **Retro** — Post-chapter review, update lessons learned

## 💰 Zero Cost Breakdown

| API Provider | Model | Free Tier | Our Usage |
|-------------|-------|-----------|-----------|
| ModelScope | DeepSeek-V3.2 | 2,000 req/day | Primary generation |
| Zhipu AI | GLM-4-Flash | Free tier | Quality review |
| Fyra.im | Kimi-K2 / Mistral | Free tier | Backup generation |

**Total monthly API spend: ¥0**

## 🚀 Quick Start

### Install via OpenClaw CLI

```bash
# Install all 3 skills
openclaw skills install novel-outliner
openclaw skills install zh-novel-writer
openclaw skills install novel-quality-checker
```

### Or from ClawHub

Visit [clawhub.ai](https://clawhub.ai) and search "novel writer"

### Usage

1. **Start with outliner** → generate your chapter outline
2. **Run the writer** → feed it the outline, get chapters
3. **Quality check** → verify consistency and quality before shipping

## 📊 Results

| Metric | Value |
|--------|-------|
| Novel | 《太初道果》(Taichu Daoguo) |
| Genre | 玄幻修仙 (Xianxia) |
| Chapters generated | 90+ chapters |
| Total characters | 900,000+ |
| API costs | ¥0 |
| Quality pass rate | >90% on first review |

## 🔧 Supported Features

- ✅ Chinese web novel writing (玄幻/修仙/言情/武侠)
- ✅ Emotional arc tracking across chapters
- ✅ Foreshadowing management
- ✅ Character consistency checks
- ✅ Duplicate rate detection (<10%)
- ✅ Multi-API fallback (auto-switch on failure)
- ✅ Quality reports with every chapter
- ✅ Post-chapter retrospectives

## 📝 Project Structure

```
novel-writer-skills/
├── skills/
│   ├── novel-outliner/        # Chapter outline generation
│   ├── zh-novel-writer/       # Full novel pipeline
│   └── novel-quality-checker/ # Quality assurance
├── README.md
└── LICENSE
```

## 🤝 Contributing

PRs welcome! We welcome:
- New language support
- Additional review criteria
- Novel genre expansions
- Bug fixes and improvements

## 📜 License

MIT License — free to use, modify, and distribute.

## 🔗 Links

- **Source:** https://github.com/Shine8592/novel-writer-skills
- **ClawHub:** https://clawhub.ai
- **OpenClaw:** https://openclaw.ai
- **Report issues:** https://github.com/Shine8592/novel-writer-skills/issues

---

_Built by an OpenClaw user who proved you can write a novel without spending a single yuan._

---

## 🇨🇳 快速开始

### 用 OpenClaw CLI 安装

```bash
openclaw skills install novel-outliner
openclaw skills install zh-novel-writer
openclaw skills install novel-quality-checker
```

### 从 ClawHub 安装

访问 [clawhub.ai](https://clawhub.ai) 搜索 "novel writer"

### 使用步骤

1. **先出大纲** → 用 outliner 生成章节大纲
2. **写小说** → 交给 writer，按流水线生成章节
3. **质检** → 质量审核，三重验证后交付

### 核心卖点

- **¥0 成本** — 全部使用免费 API
- **久经考验** — 90万字小说已验证
- **质量可控** — 每章带质量报告
- **流水线架构** — Think→Plan→Build→Review→Ship→Retro
