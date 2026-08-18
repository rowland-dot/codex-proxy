# Codex CLI 本地部署使用指南

> 部署时间：2026-08-18 · Codex CLI v0.147.0 · Windows 11

## 一、已完成的部署

| 组件 | 状态 | 说明 |
|------|------|------|
| Codex CLI v0.147.0 | ✅ 已安装 | `npm install -g @openai/codex`，命令 `codex` 全局可用 |
| **ChatGPT Pro 模式** | ✅ **默认** | ChatGPT OAuth 登录，走 chatgpt.com 后端，**消耗 Pro 订阅额度** |
| DeepSeek 云端模型 | ✅ 备用 | `codex --profile deep`，Key 在用户环境变量 DEEPSEEK_API_KEY |
| 图像生成 | ✅ **内置** | Codex CLI 内置图像生成（ChatGPT Pro 额度），**无需 API Key** |
| mihomo 本地代理 | ✅ 开机自启 | GHelper 订阅，端口 7890，全局透明 |
| Ollama 本地模型 | 🔄 部署中 | 安装包正在后台下载（网络原因较慢） |

## 二、配置文件位置

| 文件 | 路径 | 作用 |
|------|------|------|
| 主配置 | `C:\Users\<用户名>\.codex\config.toml` | 默认 provider（OpenAI 内置）、沙箱、安全策略 |
| 认证 | `C:\Users\<用户名>\.codex\auth.json` | ChatGPT OAuth token（设备认证流程生成） |
| DeepSeek Key | 用户环境变量 `DEEPSEEK_API_KEY` | 备用模式认证 |
| Profile：deep | `C:\Users\<用户名>\.codex\deep.config.toml` | DeepSeek 备用模式 |
| Profile：ollama | `C:\Users\<用户名>\.codex\ollama.config.toml` | 本地离线模式 |
| 全局规则 | `C:\Users\<用户名>\.codex\AGENTS.md` | 图像生成等 Agent 工作规则 |
| SF 生图脚本 | `C:\Users\<用户名>\.codex\imggen.py` | SiliconFlow 免费降级方案 |

## 二.一、图像生成（已全部内置）

直接告诉 Codex 画图即可，例如：
```bash
codex exec "画一只戴礼帽的橘猫，水彩风格"
```
Codex CLI 内置图像生成能力，图片自动保存到 `~/.codex/generated_images/` 并复制到工作目录。
**完全走 ChatGPT Pro 订阅额度，无需 API Key**。

如果需要"不消耗 ChatGPT 次数"的免费方案，使用 `imggen.py`（详见末尾备选方案）。

### 手动调用图像脚本
```bash
python "C:\Users\<用户名>\.codex\imggen.py" "提示词" --model kolors --size 1024x1024 --out demo.png
```

| 模型别名 | 对应模型 | 备注 |
|----------|----------|------|
| `kolors`（默认） | `Kwai-Kolors/Kolors` | 免费额度内，中文提示词友好 |
| `qwen` | `Qwen/Qwen-Image` | 通义万相，高质量 |
| `zimage-turbo` | `Tongyi-MAI/Z-Image-Turbo` | 通义MAI，速度快 |
| `ernie` | `baidu/ERNIE-Image-Turbo` | 百度 |

常见尺寸：`1024x1024`、`1280x720`、`768x1024`。

### 修改图像 API Key
- 环境变量：`SILICONFLOW_API_KEY`（已写入用户环境变量，新终端生效）
- 文件：`C:\Users\<用户名>\.codex\sf_api_key`（一行纯文本）
- 管理/充值：https://cloud.siliconflow.cn/account/ak

## 二.二、ChatGPT Pro 直连模式（默认，2026-08-18 起）

**原理**：Codex CLI 通过 ChatGPT 账号 OAuth 登录 → 路由到 `chatgpt.com/backend-api/codex/responses` → 消耗你 ChatGPT Pro 订阅额度。**不需要 API Key、不需要余额**。

**链路**：GHelper 账号的 Clash 订阅 → mihomo 内核本地代理 `127.0.0.1:7890` → chatgpt.com 后端。验证：
- 默认 `codex` → 回复 OK（gpt-5.6-sol）
- 内置生图 → 成功生成（走 ChatGPT Pro 额度）
- `codex --profile deep` → DeepSeek 备用通道

### 关键修复（解决了 401 scopes 错误）
| 错误原因 | 解决 |
|---------|------|
| auth.json 里的 OAuth token 来源于 ChatGPT 桌面应用，scopes 缺少 `api.responses.write` | `codex logout` + `codex login --device-auth` 重新认证（Codex CLI 自己的流程） |
| `config.toml` 里自定义 `openai-native` provider 强制 `base_url = https://api.openai.com/v1`，导致请求被路由到错误端点 | 改用 Codex 内置 `"openai"` provider，让它自动根据认证方式选择端点 |
| 自定义 `model = "gpt-5.3-codex"` 不被 ChatGPT 账户模式支持 | 不指定 model，让 Codex 自动选默认（gpt-5.6-sol） |

### 相关文件
| 文件 | 作用 |
|------|------|
| `C:\Users\<用户名>\AppData\Local\mihomo\` | mihomo 代理常驻安装（含 GHelper 订阅配置） |
| `启动文件夹\start-mihomo.vbs` | mihomo 开机自启（隐藏窗口，已存在则跳过） |
| `C:\Users\<用户名>\.codex\proxy-start.cmd` | 手动启动代理（自启失败时用） |
| `C:\Users\<用户名>\.codex\proxy-update.cmd` | 更新订阅节点（节点失效时运行） |
| `C:\Users\<用户名>\.codex\auth.json` | ChatGPT OAuth token（Codex 设备认证生成） |
| `C:\Users\<用户名>\.codex\auth.json.broken` | 旧的错误 token 备份（可删除） |

### 使用方法
```bash
# 无需任何前置操作，直接：
codex                              # 默认 ChatGPT Pro 模式
codex "画一只戴礼帽的橘猫"          # 内置生图（消耗 Pro 额度）
codex --profile deep               # 备用：DeepSeek
```

### 注意事项
- 你的 ChatGPT Pro 订阅有效期至 2026-09-05
- 代理走 mihomo，标准端口 **7890**，控制接口 http://127.0.0.1:9090
- 节点组固定「AI专用」（日本/美国节点）
- 订阅链接：<YOUR_GHELPER_CLASH_SUBSCRIPTION_URL>
- `imggen_openai.py` / `openai.config.toml` / `codex-openai.cmd` 已弃用，可删除

### 关于 Clash for Windows（CFW）
- 已把 GHelper 订阅预置进 CFW：配置在 `C:\Users\<用户名>\.config\clash\profiles\`（ghelper.yml + list.yml）
- 若想改用 CFW 图形界面：先停掉 mihomo（避免 7890 端口冲突），再从开始菜单启动 Clash for Windows
- CFW 0.20.39 内核较旧（2023 年版），若启动后节点不通，请继续用 mihomo（功能等同且更新）

## 三、日常使用

### 启动交互模式（最常用）

```bash
cd 你的项目目录        # 建议在 git 仓库中使用
codex                  # 启动交互式 TUI，默认 OpenAI gpt-5.3-codex
```

### 常用命令速查

```bash
codex                              # 交互模式（默认 OpenAI gpt-5.3-codex）
codex --profile deep               # 备用模式（DeepSeek deepseek-v4-pro）
codex --profile ollama             # 本地离线模式（需 Ollama 就绪）
codex "帮我写一个快速排序"          # 直接带提示词启动
codex exec "统计代码行数"           # 非交互模式（CI/脚本用）
codex resume                       # 恢复上次会话
codex doctor                       # 健康诊断
codex --help                       # 查看全部选项
```

### 安全模式说明

| 模式 | 行为 |
|------|------|
| 默认（workspace-write） | 可读写工作区文件，执行命令需确认 |
| `--dangerously-bypass-approvals-and-sandbox` | 跳过一切审批（危险，慎用） |

### 切换模型（临时）

```bash
codex -m deepseek-v4-pro           # 本次会话用 v4-pro
codex -c model_reasoning_effort="low"   # 降低推理力度省 token
```

## 四、模型说明

### DeepSeek 云端（默认，联网）
- **deepseek-v4-flash**：快速、便宜，日常编码首选
- **deepseek-v4-pro**：深度推理，复杂任务用（`--profile deep`）
- API 地址：`https://api.deepseek.com/v1`（国内直连，无需代理）
- 充值/管理 Key：https://platform.deepseek.com

### Ollama 本地（离线，需下载完成后可用）
- 模型：gpt-oss:20b（OpenAI 开源编程模型）
- 启动：`codex --profile ollama` 或 `codex --oss`
- 显存不足 8GB 时会自动使用内存，速度略降

## 五、常见问题

| 问题 | 解决 |
|------|------|
| 请求超时 | 检查网络；DeepSeek 国内可直连，一般无此问题 |
| 不在 git 仓库警告 | `git init` 或加 `--skip-git-repo-check` |
| 想用官方 OpenAI 模型 | 需自备代理 + 官方 API Key，运行 `codex login` 配置 |
| 更新 Codex | `codex update` 或 `npm install -g @openai/codex@latest` |

## 六、历史背景

本机此前通过 CC-Switch（`~/.cc-switch/`）管理 Codex 配置。本次部署已改为**直连 DeepSeek**（其 API 已原生支持 Codex 所需的 Responses 协议），不再依赖 CC-Switch 本地代理（127.0.0.1:15721）。如不再需要 CC-Switch 可正常卸载，不影响 Codex 使用。
