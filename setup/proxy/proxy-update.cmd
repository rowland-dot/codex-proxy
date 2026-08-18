@echo off
REM ============================================================
REM proxy-update.cmd: 更新 GHelper 订阅节点并重启 mihomo
REM ============================================================
set SUB_URL=<YOUR_GHELPER_CLASH_SUBSCRIPTION_URL>
set MDIR=%USERPROFILE%\AppData\Local\mihomo

echo [1/4] 下载最新订阅...
curl -sL -m 60 -o "%TEMP%\ghelper_sub.yaml" "%SUB_URL%"
if %errorlevel% neq 0 (
    echo 订阅下载失败，请检查网络
    exit /b 1
)

echo [2/4] 生成配置...
python -c "src=open(r'%TEMP%\ghelper_sub.yaml',encoding='utf-8').read();src=src.replace('mixed-port: 9981','mixed-port: 7891').replace('allow-lan: true','allow-lan: false').replace('log-level: warning','log-level: warning'+chr(10)+'external-controller: 127.0.0.1:9090');open(r'%MDIR%\config.yaml','w',encoding='utf-8').write(src)"

echo [3/4] 重启 mihomo...
taskkill /F /IM mihomo.exe >nul 2>&1
timeout /t 2 /nobreak >nul
start "" /min "%MDIR%\mihomo.exe" -d "%MDIR%" -f "%MDIR%\config.yaml"
timeout /t 4 /nobreak >nul

echo [4/4] 切换 AI 专用节点...
curl -s -X PUT "http://127.0.0.1:9090/proxies/Ghelper" -H "Content-Type: application/json" -d "{\"name\":\"AI专用\"}" >nul 2>&1

curl -s -m 20 -x http://127.0.0.1:7891 -o nul -w "OpenAI 连通性: HTTP %%{http_code}\n" "https://api.openai.com/v1/models"
echo 完成。代理端口: http://127.0.0.1:7891
