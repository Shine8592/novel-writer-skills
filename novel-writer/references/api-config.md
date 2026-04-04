# API Config — 小说生成 API 配置

## 当前可用 API（截至 2026-04-03 测试结论）

### 1. ModelScope（主力）
- **URL**: `https://api-inference.modelscope.cn/v1/chat/completions`
- **Model**: `deepseek-ai/DeepSeek-V3.2`
- **Key**: `ms-cbf54443-9984-41d8-86a7-6909ef4353f9`
- **Timeout**: 300s
- **Max Output**: ~8000-10000 汉字/次
- **限制**: 429 限流频繁
- **适用**: 主力生成，最稳定

### 2. Fyra（备份主力）
- **URL**: `https://Fyra.im/v1/chat/completions`
- **Model**: `mistral-large-3-675b-instruct`
- **Key**: `lj-840347b7a2b7534bc07cae15fb697a98a967c0ddb7ac07fb084b8985cb320651`
- **Timeout**: 240s
- **Max Output**: ~8000 汉字/次
- **限制**: 429 限流，间歇性 upstream error
- **其他可用模型**: `qwen3-next-80b-a3b-instruct`, `devstral-2-123b`
- **注意**: 每日100万字节免费额度循环

### 3. Ph8（短文本补位）
- **URL**: `https://ph8.co/v1/chat/completions`
- **Model**: `qwen3-235b-a22b-2507`
- **Key**: `sk-80647fc395d243b89fdff21fb115c4f3`
- **Timeout**: 180s
- **Max Output**: ~4000-6000 汉字/次
- **限制**: openresty 网关 504 超时，只适合短文本
- **适用**: 扩写2000字以下片段

### 不可用 API
- **CherryIn**: 余额 $0，全部拒绝
- **Modal**: 超时 >60s
- **HuggingFace**: HTTP 410，key 过期
- **Kilo.ai**: 免费期已过

## 调用策略
1. 优先 ModelScope（最稳定）
2. 429 → 等 30-60 秒重试
3. 仍 429 → 切 Fyra
4. 均失败 → 等下次心跳或用户手动触发

## 调用间隔
- 同 API 连续调用：≥15 秒
- 429 后重试：≥30 秒
- 跨 API 切换：≥5 秒
