# secrets/ — 本地保密目录（不提交 GitHub）

> Local-only secrets. Everything here except this README is gitignored — it
> never goes to a public repo. This is the single home for real credentials.

本目录存放**复用所需的真实凭证与安装文件**，已被根目录 `.gitignore` 忽略。
**只有本 `README.md` 会被提交**，其余文件一律留在本地。

## 这里应放的文件

| 文件 | 说明 | 必需 |
|---|---|---|
| `ghelper_sub.yaml` | GHelper Clash 订阅（真实链接 + 节点列表） | ✅ 代理必需 |
| `mihomo-config.yaml` | 由订阅生成的真实 mihomo 配置（含节点密码） | ✅ 代理必需 |
| `ghelper_pac.js` | GHelper PAC 脚本 | 可选 |

> Codex 用 `npm install -g @openai/codex` 安装，无需在此存安装包；官方安装器随时可重新下载。

## 新机器安装

1. 把上述真实文件放进本目录 `secrets/`。
2. 按仓库根目录 `README.md` 的「安装」章节操作
   （`setup/` 里是已脱敏的模板，真实值从这里取）。

⚠️ 这些是**付费机场订阅凭证**，泄露等于把你的代理白送人。切勿提交、切勿外发。
