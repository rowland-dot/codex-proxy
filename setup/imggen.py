#!/usr/bin/env python3
"""Codex 图像生成工具 - 通过硅基流动 (SiliconFlow) API 生成图片

用法:
    python imggen.py "一只在月球上骑自行车的猫，赛博朋克风格"
    python imggen.py "prompt" --model black-forest-labs/FLUX.1-schnell --size 1024x1024 --out output.png
    python imggen.py --list   # 列出可用模型

模型说明:
    Kwai-Kolors/Kwai-Kolors          免费, 中文提示词友好
    black-forest-labs/FLUX.1-schnell 付费(约0.2元/张), 质量更高, 速度快
    black-forest-labs/FLUX.1-dev     付费(约0.5元/张), 质量最好, 较慢

Key 来源(按优先级):
    1. 环境变量 SILICONFLOW_API_KEY
    2. 文件 ~/.codex/sf_api_key (纯文本一行)
"""
import argparse
import base64
import json
import os
import sys
import time
import urllib.request
import urllib.error

API_URL = "https://api.siliconflow.cn/v1/images/generations"
DEFAULT_MODEL = "Kwai-Kolors/Kolors"

MODELS = {
    "kolors": "Kwai-Kolors/Kolors",
    "qwen": "Qwen/Qwen-Image",
    "zimage-turbo": "Tongyi-MAI/Z-Image-Turbo",
    "zimage": "Tongyi-MAI/Z-Image",
    "ernie": "baidu/ERNIE-Image-Turbo",
}


def get_key():
    key = os.environ.get("SILICONFLOW_API_KEY", "").strip()
    if key:
        return key
    keyfile = os.path.join(os.path.expanduser("~"), ".codex", "sf_api_key")
    if os.path.exists(keyfile):
        with open(keyfile, encoding="utf-8") as f:
            k = f.read().strip()
            if k:
                return k
    print("ERROR: 未找到 API Key。", file=sys.stderr)
    print("请设置环境变量 SILICONFLOW_API_KEY，", file=sys.stderr)
    print("或把 Key 保存到 ~/.codex/sf_api_key (一行纯文本)。", file=sys.stderr)
    print("获取地址: https://cloud.siliconflow.cn/account/ak", file=sys.stderr)
    sys.exit(2)


def generate(prompt, model=DEFAULT_MODEL, size="1024x1024", out=None, b64=False):
    if model in MODELS:
        model = MODELS[model]
    key = get_key()
    payload = {
        "model": model,
        "prompt": prompt,
        "image_size": size,
    }
    req = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")[:500]
        print(f"API 错误 HTTP {e.code}: {body}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"请求失败: {e}", file=sys.stderr)
        sys.exit(1)

    images = data.get("images") or data.get("data") or []
    if not images:
        print(f"API 未返回图片: {json.dumps(data)[:500]}", file=sys.stderr)
        sys.exit(1)

    img = images[0]
    if not out:
        ts = time.strftime("%Y%m%d_%H%M%S")
        out = os.path.abspath(f"codex_image_{ts}.png")

    url = img.get("url")
    b64_data = img.get("b64_json")
    if b64_data or b64:
        with open(out, "wb") as f:
            f.write(base64.b64decode(b64_data or ""))
    elif url:
        with urllib.request.urlopen(url, timeout=120) as r, open(out, "wb") as f:
            f.write(r.read())
    else:
        print(f"返回格式无法识别: {json.dumps(img)[:300]}", file=sys.stderr)
        sys.exit(1)

    dt = time.time() - t0
    print(f"OK: {out}  (model={model}, size={size}, {dt:.1f}s)")
    return out


if __name__ == "__main__":
    # 清除可能由旧版 CC-Switch / 代理软件残留的代理变量，避免国内 API 直连失败
    for k in ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy", "NO_PROXY", "no_proxy"):
        if k in os.environ:
            del os.environ[k]

    ap = argparse.ArgumentParser(description="Codex 图像生成工具 (SiliconFlow)")
    ap.add_argument("prompt", nargs="?", help="图片描述(中文即可)")
    ap.add_argument("--model", "-m", default=DEFAULT_MODEL, help="模型名或别名: kolors/qwen/zimage-turbo/zimage/ernie")
    ap.add_argument("--size", "-s", default="1024x1024", help="尺寸, 如 1024x1024 / 1280x720 / 768x1024")
    ap.add_argument("--out", "-o", help="输出文件路径 (默认当前目录 codex_image_时间戳.png)")
    ap.add_argument("--list", action="store_true", help="列出模型别名")
    args = ap.parse_args()

    if args.list or not args.prompt:
        print("可用模型别名:")
        for k, v in MODELS.items():
            tag = " (免费额度内)" if "Kolors" in v else ""
            print(f"  {k:14s} -> {v}{tag}")
        if not args.prompt:
            print("\n用法: python imggen.py \"提示词\" [--model kolors|qwen|zimage-turbo] [--size 1024x1024] [--out 文件名.png]")
        sys.exit(0)

    generate(args.prompt, args.model, args.size, args.out)
