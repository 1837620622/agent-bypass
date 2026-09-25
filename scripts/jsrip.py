#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JS 静态文件提取器（§01 Step 8 侧枝折射）

从 JS bundle 里提取:
  · API 接口路径
  · 硬编码密钥/token
  · sourcemap 地址
  · 内网地址 / 埋点上报地址
  · 注释 / TODO / 调试信息

用法:
  python3 jsrip.py https://target.com/static/app.js
  python3 jsrip.py https://target.com --scan       # 自动找页面引用的 JS
  python3 jsrip.py https://target.com/app.js --json
"""
import argparse, json, re, ssl, sys, urllib.parse
import urllib.request, urllib.error

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"

# 提取规则
RULES = {
    "api_path": re.compile(r'["\'`](/[a-zA-Z0-9_\-/]{2,60}(?:/[a-zA-Z0-9_\-{}:.]{1,40})*)["\'`]'),
    "full_url": re.compile(r'https?://[a-zA-Z0-9._\-]+(?::\d+)?[a-zA-Z0-9._\-/?#=&%]*'),
    "secret": re.compile(r'(?i)(?:api[_-]?key|apikey|secret|token|passwd|password|auth)["\']?\s*[:=]\s*["\']([^"\']{8,80})["\']'),
    "aws_key": re.compile(r'AKIA[0-9A-Z]{16}'),
    "jwt": re.compile(r'eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}'),
    "sourcemap": re.compile(r'//[#@]\s*sourceMappingURL=([^\s]+)'),
    "internal_ip": re.compile(r'\b(?:10|172\.(?:1[6-9]|2\d|3[01])|192\.168)\.\d{1,3}\.\d{1,3}\b'),
    "comment": re.compile(r'/\*\s*(?:TODO|FIXME|HACK|XXX|NOTE)[^*]{0,200}\*/', re.I),
    "graphql": re.compile(r'(?:query|mutation)\s+\w+\s*[({]'),
    "websocket": re.compile(r'wss?://[a-zA-Z0-9._\-:]+[a-zA-Z0-9._\-/?#=&%]*'),
}


def get(url, timeout=20):
    h = {"User-Agent": UA, "Accept": "*/*"}
    try:
        r = urllib.request.Request(url, headers=h)
        with urllib.request.urlopen(r, timeout=timeout, context=CTX) as x:
            return x.read(3000000).decode("utf-8", "ignore")
    except Exception as e:
        print(f"  [错误] {url}: {str(e)[:60]}", file=sys.stderr)
        return ""


def find_js_urls(base):
    """从 HTML 里找 JS 引用"""
    html = get(base)
    if not html:
        return []
    urls = set()
    for m in re.finditer(r'<script[^>]+src=["\']([^"\']+)["\']', html, re.I):
        urls.add(m.group(1))
    for m in re.finditer(r'<link[^>]+href=["\']([^"\']+\.js)["\']', html, re.I):
        urls.add(m.group(1))
    out = []
    for u in urls:
        out.append(urllib.parse.urljoin(base, u))
    return out


def analyze(url, content):
    hits = {}
    for name, rx in RULES.items():
        found = rx.findall(content)
        if not found:
            continue
        # 去重 + 截断
        uniq = []
        seen = set()
        for f in found:
            v = f if isinstance(f, str) else f[0]
            v = v.strip()
            if len(v) < 3 or v in seen:
                continue
            seen.add(v)
            uniq.append(v[:150])
        if uniq:
            hits[name] = uniq[:40]
    return hits


def main():
    ap = argparse.ArgumentParser(description="JS 静态文件提取器")
    ap.add_argument("target", help="JS 文件 URL 或站点 URL（配合 --scan）")
    ap.add_argument("--scan", action="store_true", help="从 HTML 自动找 JS")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--depth", type=int, default=5, help="最多分析几个 JS")
    a = ap.parse_args()

    targets = []
    if a.scan:
        print(f"[*] 扫描 {a.target} 引用的 JS...", file=sys.stderr)
        targets = find_js_urls(a.target)[:a.depth]
        if not targets:
            print("  (未找到 JS 引用)", file=sys.stderr)
    else:
        targets = [a.target]

    allhits = {}
    for u in targets:
        print(f"[*] 分析 {u}", file=sys.stderr)
        c = get(u)
        if not c:
            continue
        hits = analyze(u, c)
        if hits:
            allhits[u] = hits

    if a.json:
        print(json.dumps(allhits, ensure_ascii=False, indent=1))
        return

    # 人类可读输出
    LABEL = {
        "api_path": "接口路径", "full_url": "完整 URL", "secret": "★ 疑似密钥",
        "aws_key": "★★ AWS Key", "jwt": "★★ JWT", "sourcemap": "★ sourcemap",
        "internal_ip": "★ 内网 IP", "comment": "注释/TODO",
        "graphql": "GraphQL", "websocket": "WebSocket",
    }
    for u, hits in allhits.items():
        print(f"\n{'='*66}\n{u}\n{'='*66}")
        for name in ("aws_key", "jwt", "secret", "sourcemap", "internal_ip",
                     "websocket", "graphql", "api_path", "full_url", "comment"):
            if name not in hits:
                continue
            print(f"\n[{LABEL.get(name, name)}] {len(hits[name])} 条")
            for v in hits[name][:25]:
                print(f"   {v}")
            if len(hits[name]) > 25:
                print(f"   ... 还有 {len(hits[name])-25} 条")


if __name__ == "__main__":
    main()
