#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
按产品名拉 CVE + PoC 链接（§01 情报源的封装）

用法:
  python3 cvefetch.py nginx
  python3 cvefetch.py "new api" --limit 20
  python3 cvefetch.py wordpress --json

数据源（按顺序尝试）:
  1. cve.circl.lu     最快，响应简洁
  2. NVD             官方，最全
  3. GitHub          相关 PoC 仓库
"""
import argparse, json, ssl, sys, urllib.parse
import urllib.request, urllib.error

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE
UA = "pentest-pro-cvefetch/1.0"


def get(url, timeout=25):
    try:
        r = urllib.request.Request(url, headers={"User-Agent": UA,
                                                 "Accept": "application/json"})
        with urllib.request.urlopen(r, timeout=timeout, context=CTX) as x:
            return json.loads(x.read(3000000).decode("utf-8", "ignore"))
    except Exception as e:
        return {"_error": str(e)[:80]}


def from_circl(kw, limit):
    """CVE 搜索 — circl（注意：API 端点已变更，失败则返回空，自动回退 NVD）"""
    # 旧端点已失效，尝试新端点
    for u in (f"https://vulnerability.circl.lu/api/search/{urllib.parse.quote(kw)}",
              f"https://cve.circl.lu/api/search/{urllib.parse.quote(kw)}"):
        d = get(u, timeout=20)
        if isinstance(d, dict) and "_error" in d:
            continue
        if isinstance(d, str):
            continue
        items = d if isinstance(d, list) else d.get("data", [])
        if not items:
            continue
        out = []
        for it in items[:limit]:
            cid = it.get("id") or it.get("cve")
            if not cid or not str(cid).startswith("CVE"):
                continue
            out.append({
                "cve": cid,
                "cvss": it.get("cvss") or it.get("cvss31"),
                "summary": (it.get("summary") or it.get("details") or "")[:220],
                "published": (it.get("Published") or it.get("published") or "")[:10],
                "refs": [r if isinstance(r, str) else r.get("url", "")
                         for r in (it.get("references") or [])][:3],
            })
        if out:
            return out
    return []


def from_nvd(kw, limit, retries=2):
    u = ("https://services.nvd.nist.gov/rest/json/cves/2.0?"
         f"keywordSearch={urllib.parse.quote(kw)}&resultsPerPage={limit}")
    d = {}
    for _ in range(retries + 1):
        d = get(u, timeout=60)
        if "_error" not in d and "vulnerabilities" in d:
            break
    if "_error" in d or "vulnerabilities" not in d:
        print(f"  [NVD 错误] {d.get('_error', 'no vulnerabilities key')}",
              file=sys.stderr)
        return []
    out = []
    for v in d["vulnerabilities"]:
        c = v["cve"]
        metrics = c.get("metrics", {})
        score = None
        for k in ("cvssMetricV31", "cvssMetricV30", "cvssMetricV2"):
            if k in metrics and metrics[k]:
                score = metrics[k][0].get("cvssData", {}).get("baseScore")
                break
        out.append({
            "cve": c["id"],
            "cvss": score,
            "summary": next((d2["value"] for d2 in c.get("descriptions", [])
                             if d2["lang"] == "en"), "")[:220],
            "published": c.get("published", "")[:10],
            "refs": [r["url"] for r in c.get("references", [])][:3],
        })
    return out


def from_github(kw, limit):
    """找 PoC 仓库"""
    q = urllib.parse.quote(f"{kw} exploit OR poc OR cve")
    u = f"https://api.github.com/search/repositories?q={q}&sort=stars&per_page={limit}"
    d = get(u)
    if "_error" in d or "items" not in d:
        return []
    return [{"repo": it["full_name"], "stars": it["stargazers_count"],
             "desc": (it.get("description") or "")[:100],
             "url": it["html_url"]}
            for it in d["items"]]


def main():
    ap = argparse.ArgumentParser(description="按产品名拉 CVE + PoC")
    ap.add_argument("keyword")
    ap.add_argument("--limit", type=int, default=15)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--source", choices=["circl", "nvd", "github", "all"],
                    default="all")
    a = ap.parse_args()

    # ── 先全部取数据，再统一打印（避免流式打印与请求耗时错位）──
    results = {}
    if a.source in ("nvd", "all"):
        print("[*] 查询 NVD...", file=sys.stderr)
        results["nvd"] = from_nvd(a.keyword, a.limit)
    if a.source in ("circl", "all"):
        print("[*] 查询 circl...", file=sys.stderr)
        results["circl"] = from_circl(a.keyword, a.limit)
    if a.source in ("github", "all"):
        print("[*] 查询 GitHub PoC...", file=sys.stderr)
        results["github"] = from_github(a.keyword, min(a.limit, 10))

    labels = {"nvd": "CVE (NVD)", "circl": "CVE (circl.lu)",
              "github": "PoC 仓库 (GitHub)"}
    i = 0
    for src in ("nvd", "circl", "github"):
        if src not in results:
            continue
        i += 1
        print(f"\n{'='*60}\n[{i}] {labels[src]} — {a.keyword}\n{'='*60}",
              file=sys.stderr)
        rows = results[src]
        if not rows:
            print("  (无结果 / 源不可用)", file=sys.stderr)
        for c in rows:
            if a.json:
                print(json.dumps({"source": src, **c}, ensure_ascii=False))
            elif src == "github":
                print(f"★{c['stars']:<5} {c['repo']}\n      {c['desc']}\n      {c['url']}")
            else:
                print(f"{c['cve']}  CVSS={c['cvss']}  {c['published']}\n  {c['summary']}")
                for r in c["refs"][:2]:
                    print(f"    → {r}")


if __name__ == "__main__":
    main()
