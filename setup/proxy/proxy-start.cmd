@echo off
REM ============================================================
REM proxy-start.cmd: 启动 GHelper 订阅的 mihomo 本地代理
REM 端口: HTTP/SOCKS 混合 127.0.0.1:7890, 控制API 127.0.0.1:9090
REM ============================================================
tasklist /FI "IMAGENAME eq mihomo.exe" 2>nul | find /I "mihomo.exe" >nul
if %errorlevel%==0 (
    echo mihomo 已在运行
) else (
    start "" /min "%USERPROFILE%\AppData\Local\mihomo\mihomo.exe" -d "%USERPROFILE%\AppData\Local\mihomo" -f "%USERPROFILE%\AppData\Local\mihomo\config.yaml"
    timeout /t 3 /nobreak >nul
    echo mihomo 已启动
)
REM 切换到 AI 专用节点组（OpenAI 要求非受限地区出口）
curl -s -X PUT "http://127.0.0.1:9090/proxies/Ghelper" -H "Content-Type: application/json" -d "{\"name\":\"AI专用\"}" >nul 2>&1
echo 代理端口: http://127.0.0.1:7890  (节点组: AI专用)
