#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Web 批量指纹 + 路径探测器
用法: python3 webprobe.py <domain> [<domain> ...]      # 或完整 URL
输出: jsonl（指纹 + 命中路径）
"""
import sys, json, ssl, re, urllib.request, urllib.error, concurrent.futures

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

PROBE_PATHS = [
    "/", "/robots.txt", "/.env", "/.git/HEAD", "/config.json", "/config.js",
    "/admin", "/admin/", "/manage/login", "/api/admin", "/api/v1/admin",
    "/actuator", "/actuator/health", "/actuator/env", "/actuator/beans",
    "/swagger-ui.html", "/v3/api-docs", "/openapi.json", "/api-docs",
    "/api/site", "/api/config", "/api/health", "/health", "/version",
    "/api/v1/guest", "/api/v1/announcement", "/api/query/keys/batch",
    "/api/v1/recharge/verify-cdk", "/api/v1/lookup/tasks", "/api/verify/cdk",
    "/api/auth/login", "/api/auth/verify", "/login", "/dashboard",
    "/backup.zip", "/db.sql", "/phpinfo.php", "/info.php", "/server-status",
]

def req(url, method="GET", data=None, timeout=12, headers=None):
    h = {"User-Agent": UA, "Accept": "*/*"}
    if headers: h.update(headers)
    body = None
    if data is not None:
        body = json.dumps(data).encode()
        h["Content-Type"] = "application/json"
    r = urllib.request.Request(url, data=body, headers=h, method=method)
    try:
        with urllib.request.urlopen(r, timeout=timeout, context=CTX) as resp:
            raw = resp.read(4000)
            return resp.status, dict(resp.headers), raw
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers or {}), (e.read(4000) if e.fp else b"")
    except Exception as e:
        return 0, {}, str(e).encode()

def scan(domain):
    out = {"domain": domain, "hits": [], "errors": []}
    # 指纹
    st, hd, bd = req(f"https://{domain}/")
    txt = bd.decode("utf-8", "replace")
    out["root_status"] = st
    out["server"] = hd.get("Server") or hd.get("server")
    m = re.search(r"<title[^>]*>([^<]*)", txt, re.I)
    out["title"] = m.group(1).strip() if m else ""
    out["frameworks"] = sorted(set(re.findall(
        r"(dujiaoka|独角数卡|ruoyi|若依|spring|actuator|vue|react|nuxt|next|vite|"
        r"laravel|thinkphp|django|flask|express|gin|subvault|new-api|one-api)",
        txt + str(hd), re.I)))
    # 路径探测
    for p in PROBE_PATHS:
        s, h, b = req(f"https://{domain}{p}")
        if s in (200, 201, 301, 302, 401, 403, 405, 500):
            bt = b[:300].decode("utf-8", "replace")
            # 过滤 SPA 兜底（同 root 长度 + text/html）
            if s == 200 and bt[:60] == txt[:60] and len(b) == len(bd):
                continue
            out["hits"].append({"path": p, "status": s,
                                "ct": h.get("Content-Type", "")[:40],
                                "len": len(b), "body": bt[:220]})
    return out

def main():
    domains = sys.argv[1:]
    if not domains:
        print(__doc__.strip())
        sys.exit(0)
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
        for r in ex.map(scan, domains):
            print(json.dumps(r, ensure_ascii=False))

if __name__ == "__main__":
    main()
