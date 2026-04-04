# API Config

## 配置

设置以下环境变量来配置 API keys

| API | 环境变量 | 模型 | 说明 |
|-----|---------|------|------|
| ModelScope | `NOVEL_MODELSCOPE_KEY` | deepseek-ai/DeepSeek-V3.2 | 主力，最稳定 |
| Fyra | `NOVEL_FYRA_KEY` | mistral-large-3-675b-instruct | 备份 |
| Ph8 | `NOVEL_PH8_KEY` | qwen3-235b-a22b-2507 | 短文本 |

## 调用策略

1. 默认顺序：ModelScope → Fyra → Ph8
2. 429 限流：自动等 30 秒重试
3. 失败：自动切下一个 API

## 脚本内使用

`scripts/batch_generate.py` 自动从以上环境变量读取 keys。
