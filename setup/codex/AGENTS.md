# 全局工作规则

## 当前默认配置（2026-08-18 起）

- **默认模式 = ChatGPT Pro 订阅**：直接运行 `codex` 即是 OpenAI，
  Codex CLI 通过 ChatGPT OAuth 自动路由到 `chatgpt.com/backend-api/codex/responses`。
  网络自动走本地 mihomo 透明通道（全局代理环境变量已设好），无需任何手动操作。
  使用你的 ChatGPT Pro 订阅额度，**不需要 API Key、不需要余额**。
- **备用模式 = DeepSeek**：`codex --profile deep`（ChatGPT 故障时用，国内直连）。

## 图像生成策略（重要）

### 默认：Codex CLI 内置图像生成（ChatGPT Pro 订阅）
当需要生成图片时，**直接告诉 Codex 即可**（如"画一只戴礼帽的橘猫"），
Codex CLI 已内置图像生成能力，图片会自动保存到 `~/.codex/generated_images/` 并复制到当前工作目录。
**消耗的是 ChatGPT Pro 订阅额度，无需 API Key**。

### 备用：SiliconFlow 免费生图
如果用户明确要求"不消耗 ChatGPT 次数"或 Codex 图像生成不可用，使用：
```
python "C:\Users\<用户名>\.codex\imggen.py" "图片描述提示词"
```
- `--model kolors`（默认，免费）/ `--model qwen` / `--model zimage-turbo`
- Key 在环境变量 SILICONFLOW_API_KEY 或 ~/.codex/sf_api_key，无需向用户索要。

### 已弃用
`imggen_openai.py`（调用 api.openai.com 图像 API）已不再需要——OpenAI API Key
账户无余额，且 ChatGPT OAuth 不支持该端点。

## 语言

与用户交流、代码注释、提交信息默认使用简体中文。
