# 常见问题与排错指南

## 1. 401 Unauthorized: Missing scopes: api.responses.write

**根因**: auth.json 中的 OAuth token 来源错误 + config.toml 强制路由到错误端点。

**原因分析**:
- ChatGPT 桌面 app 的 OAuth token 只有 `api.connectors.read/invoke` scope
- Codex CLI 的 `codex login --device-auth` 流程获取的 token 才有正确权限
- 自定义 provider 强制 `base_url=api.openai.com/v1` 会导致 ChatGPT OAuth token 被发送到错误端点

**解决方案**:
```bash
# 1. 登出旧认证
codex logout

# 2. 重新认证 (Codex 自己的 OAuth 流程)
codex login --device-auth
# 浏览器打开 https://chatgpt.com/device-code
# 输入显示的验证码, 完成授权

# 3. config.toml 使用内置 provider (不要自定义 base_url)
model_provider = "openai"
# 不要指定 model, 让 Codex 自动选默认模型
# 不要使用 [model_providers.openai-native] 等自定义 provider
```

## 2. OpenAI API insufficient_quota

**根因**: OpenAI API 账户无余额。

**解决方案**: 使用 ChatGPT Pro 订阅替代 API Key。运行 `codex login --device-auth` 后, Codex 自动走 ChatGPT Pro 后端, 不需要 API 余额。

## 3. mihomo 代理不通 / OpenAI 连接超时

**排查步骤**:
```bash
# 1. 检查 mihomo 是否在运行
tasklist /FI "IMAGENAME eq mihomo.exe"

# 2. 检查 7890 端口
curl -s --max-time 5 -x http://127.0.0.1:7890 https://api.openai.com/v1/models

# 3. 检查控制接口
curl http://127.0.0.1:9090/version

# 4. 检查当前节点组
curl http://127.0.0.1:9090/proxies
```

**解决方案**:
- 手动启动: 运行 `proxy-start.cmd`
- 更新订阅: 运行 `proxy-update.cmd` (节点失效时)
- 确保节点组为「AI专用」(避免香港节点 403)

## 4. 7890 端口被占用

**根因**: Clash for Windows (CFW) 可能占用 7890 端口。

**解决方案**:
```bash
# 查看占用端口的进程
netstat -ano | findstr :7890

# 如果是 CFW, 先退出 CFW, 再启动 mihomo
# 或修改 mihomo config 的 mixed-port 为其他端口
```

## 5. mihomo 启动失败: GeoIP 数据库缺失

**解决方案**: 预下载 GeoIP 数据库到 mihomo 目录:
```bash
# Country.mmdb
curl -L -o "%LOCALAPPDATA%\mihomo\Country.mmdb" https://gh-proxy.com/https://github.com/MetaCubeX/meta-rules-dat/releases/download/latest/Country.mmdb

# geoip.dat
curl -L -o "%LOCALAPPDATA%\mihomo\geoip.dat" https://gh-proxy.com/https://github.com/MetaCubeX/meta-rules-dat/releases/download/latest/geoip.dat
```

## 6. DeepSeek 备用模式报 401

**根因**: auth.json 放了 OpenAI OAuth token 后, DeepSeek provider 缺少 `env_key` 导致错用该 token。

**解决方案**: 确保 config.toml 中 DeepSeek provider 配置了 `env_key`:
```toml
[model_providers.deepseek]
name = "DeepSeek"
base_url = "https://api.deepseek.com/v1"
wire_api = "responses"
requires_openai_auth = false
env_key = "DEEPSEEK_API_KEY"
```
并设置用户环境变量: `DEEPSEEK_API_KEY=sk-xxxx`

## 7. Codex profile 机制变更 (0.147+)

**问题**: 在主 config.toml 中写 `[profiles.deepseek]` 报错。

**原因**: Codex 0.147+ 的 profile 是独立文件 (如 `deep.config.toml`), 不是主 config 中的表。

**解决方案**: 创建独立 profile 文件:
- `~/.codex/deep.config.toml` → `codex --profile deep`
- `~/.codex/ollama.config.toml` → `codex --profile ollama`

## 8. 香港节点 403 错误

**根因**: OpenAI 对部分香港 IP 返回 403。

**解决方案**: 在 mihomo 中使用「AI专用」节点组 (只包含日本/美国/新加坡等节点), 排除香港节点。运行:
```bash
curl -s -X PUT "http://127.0.0.1:9090/proxies/Ghelper" -H "Content-Type: application/json" -d "{\"name\":\"AI专用\"}"
```

## 9. 图像生成失败

**默认方案**: 直接告诉 Codex 画图, 内置能力消耗 Pro 额度。

**备选方案** (不消耗 Pro 额度):
```bash
python "C:\Users\<用户名>\.codex\imggen.py" "提示词" --model kolors --size 1024x1024 --out output.png
```

**注意**: `imggen_openai.py` 已弃用 (需要 API 余额, Pro 订阅不支持该端点)。

## 10. 开机自启失效

**检查**:
1. 确认 `start-mihomo.vbs` 在启动文件夹中
2. 路径: `C:\Users\<用户名>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\`
3. VBS 脚本使用 WMI 查重, 如果 mihomo 已运行则跳过

**手动修复**: 将 `proxy/start-mihomo.vbs` 复制到上述启动文件夹。
