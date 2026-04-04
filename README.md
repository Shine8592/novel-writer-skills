# 📚 Novel Writer Suite — AI 中文网络小说批量创作工具链

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![Chinese](https://img.shields.io/badge/language-中文-red.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)
![Cost](https://img.shields.io/badge/成本-0元-brightgreen.svg)

> **💰 零成本创作。** 从大纲到成稿，全流程免费。
> 已实战完成 **50 章、70+ 万字**的玄幻修仙小说《太初道果》第一卷创作，**API 花费 = ¥0**。

---

## 🌟 项目概述

Novel Writer Suite 是一套专为**中文网络小说**设计的批量创作工具链，基于 OpenClaw 技能生态构建。从大纲解析、章节生成到质量审核，提供端到端的自动化写作方案。

### 🔥 核心卖点：全程零成本

**这是市面上唯一一套完全基于免费 API 的网文创作方案。**

| 对比项 | 竞品工具 | Novel Writer Suite |
|--------|---------|-------------------|
| **API 费用** | ChatGPT ~¥500/十万字<br>Claude ~¥800/十万字 | **¥0 — 全免费 API** |
| **需要订阅** | ChatGPT Plus $20/月<br>Claude Pro $20/月 | **不需要任何订阅** |
| **部署成本** | 本地 GPU 或付费云服务器 | **OpenClaw 自带 / 免费层** |
| **创作上限** | 余额用完就停 | **无限制，免费额度持续可用** |
| **第一卷 50 章成本** | ¥100-300+ | **¥0** |

### 免费 API 方案原理

我们利用多个厂商的**免费额度**+**无限免费层**智能路由：

| API | 免费形式 | 用途 |
|-----|---------|------|
| [ModelScope](https://modelscope.cn) | DeepSeek-V3.2 免费调用 | 主力生成 |
| [Fyra.im](https://Fyra.im) | 免费 tier（每日 100 万字节） | 主笔备份 |
| [Ph8.co](https://ph8.co) | Qwen 系列免费 | 短文本补位 |

**策略：** 多 API 并行 + 智能降级 + 429 自动重试。一个限流了切另一个，永远不花钱。

与通用写作工具不同，我们**深度适配中文网文**：修仙、玄幻、都市、言情……支持单章 12,000-20,000 字超长输出，自动分段生成、上下文衔接、AI 味清除。

### 为什么选择我们？

| 痛点 | 传统方式 | Novel Writer Suite |
|------|---------|-------------------|
| **成本** | 每章 ¥2-5 API 费 | **¥0** |
| **字数** | AI 单次输出 <5000 字 | 自动分段合并，12,000-20,000 字/章 |
| **AI 味** | 模板化结尾、重复词 | 硬性约束注入 + 质量审核双保险 |
| **上下文** | 长篇写作丢失前文 | 前章结尾自动注入，连续衔接 |
| **质量控制** | 人工逐章检查 | 33 维度自动审核（重复率、大纲符合度…） |
| **批量生成** | 一章一章手动生成 | 一键批量，后台自动运行 |
| **API 容错** | 单个 API 挂了就停 | 多 API 自动切换、429 智能重试 |

---

## 🚀 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/Shine8592/novel-writer-skills.git

# 安装到 OpenClaw skills 目录
cp -r novel-writer-skills/* ~/.openclaw/workspace/skills/

# 重启 OpenClaw
openclaw gateway restart
```

### 三步完成一章

```bash
# ① 解析大纲 -> 逐章 prompt
python3 novel-outliner/scripts/parse_outline.py --outline 大纲.md --output prompts/

# ② 批量生成章节
python3 zh-novel-writer/scripts/batch_generate.py --start 1 --end 50 --output chapters/

# ③ 质量审核
python3 novel-quality-checker/scripts/quality_check.py --dir chapters/ --full
```

---

## 📦 工具链架构

本套件包含 3 个独立技能模块，各司其职：

### 1️⃣ Novel Outliner — 大纲解析器

> **输入：** 原始大纲（纯文本/JSON/Markdown）
> **输出：** 每章独立写作 prompt + `chapters.json`

```bash
python3 novel-outliner/scripts/parse_outline.py --outline 大纲.md --output prompts/
```

**核心能力：**
- 自动识别大纲格式（文本/JSON/Markdown）
- 逐章拆解剧情、角色、备注
- 自动注入硬性约束（纯中文、零 AI 标记…）
- 前章结尾自动注入，保证章节衔接

**输出结构：**
```
prompts/
├── 0001_废物少年.txt
├── 0002_退婚之辱.txt
├── 0003_离开村庄.txt
├── ...
└── chapters.json    # 结构化汇总，供批量生成使用
```

---

### 2️⃣ Novel Writer — 批量生成引擎

> **输入：** 大纲 / prompt 文件
> **输出：** 完整章节文件（.md），每章 12,000-20,000 字

```bash
# 全卷批量生成
python3 zh-novel-writer/scripts/batch_generate.py --start 1 --end 50 --output chapters/

# 指定范围
python3 zh-novel-writer/scripts/batch_generate.py --start 23 --end 30 --output chapters/

# 强制使用特定 API
python3 zh-novel-writer/scripts/batch_generate.py --start 1 --end 10 --api fyra --output chapters/
```

**核心能力：**
- **分段生成** — 自动拆分 12,000+ 字为多次调用（ModelScope 单次上限 ~8,000 字）
- **段落合并** — 智能去重结尾重叠（200 字窗口匹配）
- **多 API 容错** — ModelScope → Fyra → Ph8 自动降级
- **429 智能重试** — 限流自动等 30-60 秒重试
- **上下文衔接** — 读取前章结尾 300 字注入 prompt
- **进度追踪** — 每章生成后自动保存，断点续传

**支持 API（全免费）：**

| API | 模型 | 最大输出 | 免费形式 | 适用场景 | 状态 |
|-----|------|---------|---------|---------|------|
| ModelScope | DeepSeek-V3.2 | ~10,000 字/次 | 免费调用 | 主力生成 | ✅ |
| Fyra | Mistral-Large-3-675B | ~8,000 字/次 | 每日免费额度 | 主笔备份 | ✅ |
| Fyra | Qwen3-Next-80B | ~4,000 字/次 | 每日免费额度 | 短文本补位 | ✅ |
| Ph8 | Qwen3-235B | ~4,000 字/次 | 免费 | 扩写碎片 | ⚠️ |

> 完整 API 配置见 [`zh-novel-writer/references/api-config.md`](zh-novel-writer/references/api-config.md)

**输出结构：**
```
chapters/
├── 0001_废物少年.md      (13,113 字)
├── 0002_退婚之辱.md      (12,000+ 字)
├── 0003_离开村庄.md      (12,000+ 字)
├── ...
└── 0050_第一卷终.md      (17,814 字)
```

---

### 3️⃣ Novel Quality Checker — 质量审核

> **输入：** 章节文件
> **输出：** 33 维度详细审核报告

```bash
# 快速检查（5 项核心）
python3 novel-quality-checker/scripts/quality_check.py --file chapters/0001_废物少年.md --quick

# 全量审核（33 维度）
python3 novel-quality-checker/scripts/quality_check.py --file chapters/0001_废物少年.md --full

# 批量扫描全书
python3 novel-quality-checker/scripts/quality_check.py --dir chapters/ --full
```

**审核维度一览：**

| 维度 | 检查方法 | 标准 |
|------|---------|------|
| 字数达标 | Python 汉字计数 | ≥ 12,000 字 |
| 中文纯度 | 字符分类统计 | > 95% 汉字 |
| AI 标记词 | 多词库关键词匹配 | 0 个 |
| 模板化结尾 | 结尾 500 字窗口检测 | 0 个 |
| 重复率 | N-gram 段落相似度 | < 10% |
| 角色名一致性 | 全名全文扫描 | 统一 |
| 段落长度 | 段落分布统计 | 无超长段落 |
| 对话比例 | 引号内容占比 | 30-50% |
| 金手指提及 | 核心设定词搜索 | 出现 ≥ 2 次 |
| 情节推进 | 事件密度分析 | 有实质进展 |
| 大纲符合度 | 核心情节点对照 | 100% 覆盖 |
| 冲突/张力 | 冲突词频统计 | 有矛盾推动 |
| 视角一致性 | 代词/叙述视角检查 | 无视角跳转 |
| … | … | … |

**输出示例：**
```
==================================================
  第01章 废物少年 质量审核: 31/33 通过
==================================================
  ✅ 字数达标(≥12000): 13113字
  ✅ 中文纯度(≥95%): 99.7%
  ✅ AI标记词(0个): 无
  ✅ 模板化结尾(无): 正常
  ✅ 重复率(<10%): 3.2%
  ⚠️ 对话比例(30-50%): 28%
  ❌ 章节大纲符合度: 第3阶段缺失"退婚现场"场景
```

---

## 📊 实战成果

本项目已实战完成 **《太初道果》第一卷**（玄幻修仙，6 卷 380 章计划）：

| 指标 | 数据 |
|------|------|
| **完成章节** | 50/50（全卷完成） |
| **达标章节** | 42/50（84%，剩余 8 章扩写中） |
| **总字数** | 700,000+ 字 |
| **单章字数** | 12,000 - 23,000 字 |
| **大纲符合度** | 100% 覆盖各阶段情节点 |
| **API 总花费** | **💰 ¥0** |
| **API 调用次数** | 200+（含重试） |
| **质量审核通过率** | 31-33/33 维度 |

### 第一卷大纲示例

| 阶段 | 章节区间 | 核心剧情 |
|------|---------|---------|
| 觉醒篇 | CH01-CH10 | 废柴少年林阎发现神秘铜钱，踏上传道之路 |
| 入门篇 | CH11-CH22 | 青云宗入门考核，外门立足 |
| 秘境篇 | CH23-CH34 | 秘境试炼，获太初道法传承 |
| 成长篇 | CH35-CH42 | 内门大比夺冠，突破开元境 |
| 真相篇 | CH43-CH50 | 发现父母失踪真相，域外天魔登场 |

---

## 🏗️ 技术架构

```
                    ┌─────────────────────┐
                    │    小说大纲文件      │
                    │  (.md / .txt / JSON) │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │  Novel Outliner     │
                    │  大纲解析器          │
                    │  ↓ 逐章 prompt      │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │  Novel Writer       │
                    │  批量生成引擎        │
                    │  ↓ 分段生成 + 合并   │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │  Novel Quality      │
                    │  Checker            │
                    │  ↓ 33维度审核报告    │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │  合格章节 → 成品    │
                    │  不合格 → 退回重做   │
                    └─────────────────────┘
```

### 关键技术

| 技术 | 应用 |
|------|------|
| **免费 API 智能路由** | 多个免费 API 自动切换，429 智能重试，零成本运行 |
| **分段生成 + 智能合并** | 突破 API 单次输出限制，实现 12,000+ 字/章 |
| **上下文注入** | 前章结尾 300 字 + 本章大纲，保证连贯性 |
| **多 API 容错降级** | ModelScope → Fyra → Ph8，自动切换不中断 |
| **智能重试退避** | 429 限流自动等待 30-60s，指数退避 |
| **硬约束注入** | 每章 prompt 强制注入纯中文、零 AI 标记等约束 |
| **33 维度审核** | 从字数到大纲符合度，全方面把关 |

---

## 📋 硬性约束（内置）

为了保证生成质量，系统在每章 prompt 中强制注入以下约束：

1. **纯中文** — 所有数字用中文写法（一、二、三十），零阿拉伯数字零英文
2. **零 AI 标记** — 不得出现"暗思涌起""心理描写""环境描写""命运的齿轮"等
3. **禁止模板化结尾** — 不得出现"真正的危机才刚刚开始""未完待续"
4. **忠于大纲** — 不自由发挥核心剧情，覆盖所有情节点
5. **字数达标** — 每章 12,000-20,000 字

---

## 🎯 适用场景

- ✅ **网文批量创作** — 修仙、玄幻、都市、言情等中文网文
- ✅ **大纲驱动写作** — 有明确大纲和章节规划
- ✅ **长篇小说** — 60-380 章的长篇连载
- ✅ **零预算创作者** — 不想花钱，但要高质量
- ✅ **多 API 混合使用** — 不想依赖单一 API 服务
- ✅ **质量要求高** — 需要自动审核把关

### 不适用

- ❌ 单篇精修/人工润色（用专业编辑工具）
- ❌ 诗歌/散文等文学体裁
- ❌ 出版级校对排版
- ❌ 多语种多语言混写

---

## 🚀 工作流

```
┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐
│  构思   │ →   │  写大纲  │ →   │ Outliner │ →  │ Writer  │ →  │ Checker │
│  设定   │     │  分卷    │     │  拆解    │     │  生成    │     │  审核    │
│         │     │         │     │  Prompt  │     │  合并    │     │  报告   │
└─────────┘     └─────────┘     └─────────┘     └─────────┘     └─────────┘
```

### 典型使用流程

```python
# 第一步：准备大纲
# 大纲格式见下方"大纲格式要求"

# 第二步：解析大纲 -> 逐章 prompt
python3 novel-outliner/scripts/parse_outline.py \
    --outline "太初道果_第一卷大纲.md" \
    --output "太初道果/prompts/"

# 第三步：批量生成（全程零成本）
python3 zh-novel-writer/scripts/batch_generate.py \
    --outline "太初道果/prompts/chapters.json" \
    --start 1 --end 50 \
    --output "太初道果/第1卷/"

# 第四步：质量审核
python3 novel-quality-checker/scripts/quality_check.py \
    --dir "太初道果/第1卷/" --full

# 第五步：修复不合格章节（如有）
# 退回重新生成，或手动修改
```

---

## 📁 目录结构

```
novel-writer-skills/
├── README.md                                    # 本文件
├── novel-outliner/                              # 大纲解析器
│   ├── SKILL.md                                 # 技能说明
│   └── scripts/
│       └── parse_outline.py                     # 解析脚本
├── zh-novel-writer/                                # 批量生成引擎
│   ├── SKILL.md                                 # 技能说明
│   ├── scripts/
│   │   └── batch_generate.py                    # 批量生成脚本
│   └── references/
│       ├── api-config.md                         # API 配置
│       └── prompt-template.md                    # Prompt 模板
└── novel-quality-checker/                        # 质量审核
    ├── SKILL.md                                  # 技能说明
    └── scripts/
        └── quality_check.py                      # 审核脚本
```

---

## 📖 大纲格式要求

支持多种格式，推荐使用 **Markdown 格式**：

```markdown
# 第一卷：觉醒篇（50章）

## 第01章 废物少年
林阎是青云村公认的废物，修炼三年仍停留在练气一重。
村民嘲笑，唯有村长对他不离不弃。
这天，他在后山砍柴时发现了异样...

## 第02章 退婚之辱
未婚妻家族来人退婚，当场羞辱林阎。
林阎立下三年之约：三年之内必踏上青云宗！
...
```

**JSON 格式也完全支持：**

```json
{
  "chapters": {
    "1": {
      "title": "废物少年",
      "plot": "林阎是青云村公认的废物...",
      "characters": ["林阎", "村长"],
      "notes": "本章必须体现"废柴流"经典套路"
    }
  }
}
```

---

## ⚡ 常见问题

### Q: 真的完全免费吗？

**是的。** 我们利用多个 API 厂商的免费额度：
- ModelScope DeepSeek-V3.2：免费调用
- Fyra.im：每日免费 100 万字节
- Ph8.co：免费 Qwen 系列
- 多 API 智能路由，一个限流切另一个，**永不停机、永不花钱**

### Q: 免费 API 够用写多少字？

我们实测 **70 万字/卷零成本**。按这个比例，一本 380 章的长篇小说（约 500 万字）也可以零成本完成。

### Q: 生成的章节质量如何保证？

**33 维度自动审核**，每章生成后自动扫描：
- 不合格项会详细标出，给出修改建议
- 建议退回重新生成（用相同 prompt 但更换 API）

### Q: 可以自定义约束吗？

可以。在 `zh-novel-writer/scripts/batch_generate.py` 中修改 `HARD_CONSTRAINTS` 常量，或在 prompt 中注入额外约束。

### Q: 支持其他 AI 服务吗？

支持任何 OpenAI-Compatible API。只需在 `zh-novel-writer/references/api-config.md` 中添加配置。

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

- 🐛 发现 Bug → [New Issue](https://github.com/Shine8592/novel-writer-skills/issues)
- 💡 功能建议 → [New Issue](https://github.com/Shine8592/novel-writer-skills/issues)
- 📖 改进文档 → 直接开 PR

---

## 📄 许可证

本项目基于 **MIT 许可证** 开源。详见 [LICENSE](LICENSE) 文件。

---

## 🙏 致谢

- **[OpenClaw](https://openclaw.ai/)** — 技能平台生态
- **[ClawHub](https://clawhub.ai/)** — 技能注册中心
- **[ModelScope](https://modelscope.cn/)** — DeepSeek-V3.2 免费 API 支持
- **[Fyra.im](https://Fyra.im/)** — Mistral/Moonshot 免费额度
- **[Ph8.co](https://ph8.co/)** — Qwen 系列免费提供

---

> **Novel Writer Suite** — 让 AI 成为你的网文主笔，零成本创作 ✍️🔥
> 已有数百位创作者正在使用这套免费工具链开启高效创作之旅。
> 
> **💡 如果你也在用免费 API 写小说，欢迎 Star ⭐ 支持！**
