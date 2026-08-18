# codex-proxy

**在中国用现有 ChatGPT Pro 订阅访问 OpenAI —— 无需 OpenAI API Key、不产生额外 OpenAI 费用**
（境外代理机场需另行付费）。包含可直接复用的 Codex CLI 部署方案（含**免费内置生图**）。

> English summary at the bottom.

---

## ⚠️ 免责声明 · Disclaimer

**本项目仅供学习与技术研究（educational / research use only）。**

- 仅用于个人使用**自己合法持有**的 ChatGPT 订阅账号，配置自己的开发工具。
- 使用者须**自行遵守** OpenAI 服务条款、GitHub 使用条款，以及自己所在地的法律法规。
  是否使用、如何使用，责任完全在使用者本人。
- 本项目**不涉及、不鼓励**任何账号买卖／共享、绕过付费、滥用配额或规避封禁的行为。
- 按「现状」提供，不作任何担保；作者不对使用本项目产生的任何后果负责。

**English:** This project is for **educational and research purposes only**. Use it
only with a **ChatGPT subscription you legitimately own**, to configure your own dev
tools. **You** are solely responsible for complying with OpenAI's Terms of Service,
GitHub's Terms, and the laws of your jurisdiction. It does **not** endorse or enable
account trading/sharing, payment bypass, quota abuse, or ban evasion. Provided as-is,
no warranty; the author accepts no liability for how you use it.

---

## 这个仓库分两部分

| 部分 | 内容 | 去向 |
|---|---|---|
| **公开** | `README.md` · `docs/` · `setup/`（已脱敏） | 可提交 GitHub、可公开分享 |
| **本地** | `secrets/` —— 真实订阅、节点密码、安装包 | 只留本地，`.gitignore` 永不提交 |

## 图像生成（免费，走订阅额度）

Codex 内置 `image_gen` 工具可直接生图，**走 ChatGPT Pro 订阅额度，无需 OpenAI API Key**
（codex 生图 skill 说明：*"Does not require `OPENAI_API_KEY`"*）。直接让 codex 画图即可，
成品存到 `~/.codex/generated_images/`。

> OpenAI **Images API**（`gpt-image-1.5`）才需要付费额度；默认的内置路径在订阅额度内免费。

## 目录结构

```
codex-proxy/
├── README.md                 本文件
├── .gitignore                只提交公开部分，secrets/ 忽略
├── docs/                     文档（公开）
│   ├── codex-setup-guide.md      Codex + 代理 + 生图 完整指南
│   ├── troubleshooting.md        疑难排查
│   └── deployment-diagram.svg    部署架构图
├── setup/                    可复用配置与脚本（公开，已脱敏）
│   ├── codex/                    config.toml / AGENTS.md / 备用 profile
│   ├── proxy/                    mihomo 配置模板 + 启动/更新脚本
│   └── imggen.py                 SiliconFlow 免费生图（备用）
└── secrets/                  真实凭证（本地，.gitignore 忽略）
    └── README.md                 说明放什么（唯一会提交的文件）
```

无重复、无深层嵌套：脱敏模板在 `setup/`，真实密钥只在 `secrets/`。

---

## 安装

完整步骤见 [`docs/codex-setup-guide.md`](docs/codex-setup-guide.md)（配 [`troubleshooting.md`](docs/troubleshooting.md)）。精简版：

### 1. 装 Codex CLI
```bash
npm install -g @openai/codex        # v0.147.0+，全局命令 codex
```

### 2. 代理（仅国内机器需要）
OpenAI 封中国 IP，国内机器要一个境外出口。需要一个**付费的** Clash 兼容机场订阅
（本方案用 **GHelper**，需自行购买），用 **mihomo**（Clash Meta 内核）加载订阅，
本地监听 `127.0.0.1:7890`，开机自启。

- 模板：`setup/proxy/`（`mihomo-config.example.yaml` + 脚本）
- 真实订阅：放 `secrets/ghelper_sub.yaml`（见 `secrets/README.md`）
- 分流规则：只有 OpenAI/ChatGPT 域名走隧道，其余直连
- 境外机器（如美国服务器）直连 OpenAI，**不用代理**

### 3. 认证（这一步解决 401）
```bash
codex logout
codex login --device-auth           # 用 Codex 自己的设备认证流程登录 ChatGPT
```
**不要**复用 ChatGPT 桌面应用的 token —— 它缺 `api.responses.write` 权限，会 401。
设备认证流程拿到的才对。

### 4. 配置（内置 provider，不要写死 base_url）
用 Codex 内置 `openai` provider，**不指定 model**，让它自动选默认（`gpt-5.6-sol`）并
自动路由到 `chatgpt.com/backend-api/codex/responses`（Pro 额度，无 Key、无余额）。
参考 `setup/codex/config.toml`。

### 5. 验证
```bash
codex "你好"                          # 正常回复（gpt-5.6-sol）
codex "画一只戴礼帽的橘猫，水彩风格"    # 内置生图，存到 ~/.codex/generated_images/
```

---

## 使用

```bash
codex                               # 交互模式，默认 ChatGPT Pro
codex "帮我写一个快速排序"            # 直接带提示词
codex exec "统计代码行数"            # 非交互（脚本/CI）
codex "画一个 …"                     # 生图 —— 内置，无需 API Key
codex --profile deep                # 备用：DeepSeek（需 DEEPSEEK_API_KEY）
codex --profile ollama              # 离线：本地 Ollama
codex resume                        # 恢复上次会话
codex doctor                        # 健康检查
```

- 生图结果在 `~/.codex/generated_images/`，并复制到工作目录。
- **不消耗 Pro 额度的免费生图**：`setup/imggen.py`（SiliconFlow 免费额度，
  Kolors / 通义万相 / ERNIE，需 SiliconFlow key）。

---

## 密钥与 git

- `secrets/` 及所有订阅/认证文件已被 `.gitignore` 忽略，只留本地，永不提交。
  验证：`git check-ignore secrets/ghelper_sub.yaml`。
- 公开可提交的只有 `docs/`、`setup/`（已脱敏，节点密码/订阅链接/用户名都已移除）。
- 新机器：把真实文件放进 `secrets/`，按上面「安装」操作。

---

## English (alternative)

Access OpenAI from China on your existing **ChatGPT Pro** subscription — **no OpenAI
API key needed** — including **free built-in image generation** via Codex's
`image_gen` tool (it does not require `OPENAI_API_KEY`).

Two parts: **public** (`README.md`, `docs/`, `setup/` — scrubbed, commit to GitHub)
and **local** (`secrets/` — your proxy subscription, node passwords; gitignored,
local only).

Install (condensed): `npm i -g @openai/codex` → run mihomo with a **paid** Clash
proxy subscription (this setup uses GHelper — buy your own) on `127.0.0.1:7890`
(China machines only) → `codex login --device-auth`
(not the desktop-app token — it lacks the `api.responses.write` scope) → use the
built-in `openai` provider, don't pin a model. Then `codex "…"` and
`codex "draw …"` for free image gen. Full guide: `docs/codex-setup-guide.md`.

Real credentials live only in `secrets/` (see `secrets/README.md`); the scrubbed
templates are in `setup/`.

---

## 许可 · License

教育用途许可 —— 仅限教育、研究、个人非商业用途；使用者自行遵守 OpenAI、GitHub 条款
及当地法律；按现状提供，作者不担责。详见 [`LICENSE`](LICENSE)。

Educational Use License — educational / research / personal non-commercial use only;
you comply with OpenAI's & GitHub's terms and your local law; provided as-is, no
liability. See [`LICENSE`](LICENSE).
