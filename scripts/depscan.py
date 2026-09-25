#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第三方依赖库扫描器（§01 Step 8 侧枝 · 依赖维度）

从目标页面/JS 里提取前端库名+版本，或读取暴露的依赖清单，
自动查这些版本的已知 CVE。

用法:
  # 从页面/JS 自动提取前端库
  python3 depscan.py https://target.com

  # 直接读暴露的依赖清单
  python3 depscan.py https://target.com/package.json
  python3 depscan.py https://target.com/composer.lock

  # 手动指定库
  python3 depscan.py --lib "jquery:1.12.4" --lib "bootstrap:4.0.0"

  # 只提取不查 CVE
  python3 depscan.py https://target.com --no-cve
"""
import argparse, json, re, ssl, sys, urllib.parse
import urllib.request, urllib.error

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"

# ── 前端库指纹（从 JS/HTML 文本里匹配）──
LIB_PATTERNS = [
    ("jquery",         re.compile(r'jquery[/-]?v?([0-9]+\.[0-9]+\.[0-9]+)', re.I)),
    ("jquery",         re.compile(r'jQuery\s+v?([0-9]+\.[0-9]+\.[0-9]+)', re.I)),
    ("bootstrap",      re.compile(r'bootstrap[/-]?v?([0-9]+\.[0-9]+\.[0-9]+)', re.I)),
    ("vue",            re.compile(r'vue[@/.-]v?([0-9]+\.[0-9]+\.[0-9]+)', re.I)),
    ("react",          re.compile(r'react[@/.-]v?([0-9]+\.[0-9]+\.[0-9]+)', re.I)),
    ("angular",        re.compile(r'angular[/@.-]v?([0-9]+\.[0-9]+\.[0-9]+)', re.I)),
    ("lodash",         re.compile(r'lodash[@/.-]v?([0-9]+\.[0-9]+\.[0-9]+)', re.I)),
    ("axios",          re.compile(r'axios[@/.-]v?([0-9]+\.[0-9]+\.[0-9]+)', re.I)),
    ("moment",         re.compile(r'moment[@/.-]v?([0-9]+\.[0-9]+\.[0-9]+)', re.I)),
    ("echarts",        re.compile(r'echarts[@/.-]v?([0-9]+\.[0-9]+\.[0-9]+)', re.I)),
    ("element-ui",     re.compile(r'element-ui[@/.-]v?([0-9]+\.[0-9]+\.[0-9]+)', re.I)),
    ("layui",          re.compile(r'layui[/@.-]v?([0-9]+\.[0-9]+\.[0-9]+)', re.I)),
    ("swiper",         re.compile(r'swiper[@/.-]v?([0-9]+\.[0-9]+\.[0-9]+)', re.I)),
    ("ckeditor",       re.compile(r'ckeditor[/@.-]v?([0-9]+\.[0-9]+\.[0-9]+)', re.I)),
    ("tinymce",        re.compile(r'tinymce[/@.-]v?([0-9]+\.[0-9]+\.[0-9]+)', re.I)),
    ("ueditor",        re.compile(r'ueditor[/@.-]v?([0-9]+\.[0-9]+\.[0-9]+)', re.I)),
    ("handlebars",     re.compile(r'handlebars[@/.-]v?([0-9]+\.[0-9]+\.[0-9]+)', re.I)),
    ("underscore",     re.compile(r'underscore[@/.-]v?([0-9]+\.[0-9]+\.[0-9]+)', re.I)),
    ("d3",             re.compile(r'\bd3[@/.-]v?([0-9]+\.[0-9]+\.[0-9]+)', re.I)),
    ("three",          re.compile(r'\bthree[@/.-]v?([0-9]+\.[0-9]+\.[0-9]+)', re.I)),
    ("socket.io",      re.compile(r'socket\.io[@/.-]v?([0-9]+\.[0-9]+\.[0-9]+)', re.I)),
    ("font-awesome",   re.compile(r'font-?awesome[/@.-]v?([0-9]+\.[0-9]+\.[0-9]+)', re.I)),
    ("video.js",       re.compile(r'video\.js[@/.-]v?([0-9]+\.[0-9]+\.[0-9]+)', re.I)),
    ("highlight.js",   re.compile(r'highlight\.js[@/.-]v?([0-9]+\.[0-9]+\.[0-9]+)', re.I)),
    ("codemirror",     re.compile(r'codemirror[@/.-]v?([0-9]+\.[0-9]+\.[0-9]+)', re.I)),
    ("marked",         re.compile(r'marked[@/.-]v?([0-9]+\.[0-9]+\.[0-9]+)', re.I)),
    ("js-cookie",      re.compile(r'js-cookie[@/.-]v?([0-9]+\.[0-9]+\.[0-9]+)', re.I)),
    ("jsonwebtoken",   re.compile(r'jsonwebtoken[@/.-]v?([0-9]+\.[0-9]+\.[0-9]+)', re.I)),
    ("express",        re.compile(r'express[@/.-]v?([0-9]+\.[0-9]+\.[0-9]+)', re.I)),
    ("next",           re.compile(r'next[@/.-]v?([0-9]+\.[0-9]+\.[0-9]+)', re.I)),
    ("nuxt",           re.compile(r'nuxt[@/.-]v?([0-9]+\.[0-9]+\.[0-9]+)', re.I)),
    ("vite",           re.compile(r'vite[@/.-]v?([0-9]+\.[0-9]+\.[0-9]+)', re.I)),
    ("webpack",        re.compile(r'webpack[@/.-]v?([0-9]+\.[0-9]+\.[0-9]+)', re.I)),
]

# ── 服务端指纹（从响应头/报错里匹配）──
SERVER_PATTERNS = [
    ("nginx",          re.compile(r'nginx[/\s]v?([0-9]+\.[0-9]+\.[0-9]+)', re.I)),
    ("apache",         re.compile(r'apache[/\s]v?([0-9]+\.[0-9]+\.[0-9]+)', re.I)),
    ("tomcat",         re.compile(r'tomcat[/\s]v?([0-9]+\.[0-9]+\.[0-9]+)', re.I)),
    ("php",            re.compile(r'PHP[/\s]v?([0-9]+\.[0-9]+\.[0-9]+)', re.I)),
    ("spring",         re.compile(r'spring[/\s-]?(?:framework)?[/\s]v?([0-9]+\.[0-9]+\.[0-9]+)', re.I)),
    ("struts",         re.compile(r'struts[/\s]v?([0-9]+\.[0-9]+(?:\.[0-9]+)?)', re.I)),
    ("django",         re.compile(r'django[/\s]v?([0-9]+\.[0-9]+(?:\.[0-9]+)?)', re.I)),
    ("flask",          re.compile(r'flask[/\s]v?([0-9]+\.[0-9]+(?:\.[0-9]+)?)', re.I)),
    ("laravel",        re.compile(r'laravel[/\s]v?([0-9]+\.[0-9]+(?:\.[0-9]+)?)', re.I)),
    ("wordpress",      re.compile(r'wordpress[/\s]v?([0-9]+\.[0-9]+(?:\.[0-9]+)?)', re.I)),
    ("drupal",         re.compile(r'drupal[/\s]v?([0-9]+(?:\.[0-9]+)*)', re.I)),
    ("joomla",         re.compile(r'joomla[/\s]v?([0-9]+\.[0-9]+(?:\.[0-9]+)?)', re.I)),
    ("weblogic",       re.compile(r'weblogic[/\s]v?([0-9]+\.[0-9]+(?:\.[0-9]+)?)', re.I)),
    ("jenkins",        re.compile(r'jenkins[/\s]v?([0-9]+\.[0-9]+(?:\.[0-9]+)?)', re.I)),
    ("gitlab",         re.compile(r'gitlab[/\s]v?([0-9]+\.[0-9]+(?:\.[0-9]+)?)', re.I)),
    ("elasticsearch",  re.compile(r'elasticsearch[/\s]v?([0-9]+\.[0-9]+(?:\.[0-9]+)?)', re.I)),
    ("redis",          re.compile(r'redis[/\s]v?([0-9]+\.[0-9]+(?:\.[0-9]+)?)', re.I)),
    ("mysql",          re.compile(r'mysql[/\s]v?([0-9]+\.[0-9]+(?:\.[0-9]+)?)', re.I)),
    ("jquery-ui",      re.compile(r'jquery-ui[/-]v?([0-9]+\.[0-9]+\.[0-9]+)', re.I)),
    ("newapi",         re.compile(r'new-api[/\s]v?([0-9]+\.[0-9]+\.[0-9]+[-\w.]*)', re.I)),
    ("oneapi",         re.compile(r'one-api[/\s]v?([0-9]+\.[0-9]+\.[0-9]+[-\w.]*)', re.I)),
]


def get(url, timeout=25):
    h = {"User-Agent": UA, "Accept": "*/*"}
    try:
        r = urllib.request.Request(url, headers=h)
        with urllib.request.urlopen(r, timeout=timeout, context=CTX) as x:
            return x.read(4000000).decode("utf-8", "ignore"), dict(x.headers)
    except urllib.error.HTTPError as e:
        try:
            return e.read(2000000).decode("utf-8", "ignore"), dict(e.headers)
        except Exception:
            return "", {}
    except Exception as e:
        print(f"  [错误] {url}: {str(e)[:60]}", file=sys.stderr)
        return "", {}


def find_assets(base):
    """从 HTML 找 JS/CSS 引用"""
    html, hd = get(base)
    urls = set()
    for m in re.finditer(r'<(?:script|link)[^>]+(?:src|href)=["\']([^"\']+\.(?:js|css))["\']',
                         html, re.I):
        urls.add(urllib.parse.urljoin(base, m.group(1)))
    return list(urls)[:15], html, hd


def extract_from_text(text):
    """从文本里提取所有库指纹"""
    found = {}
    for name, rx in LIB_PATTERNS + SERVER_PATTERNS:
        for m in rx.finditer(text):
            ver = m.group(1)
            found.setdefault(name, set()).add(ver)
    return {k: sorted(v) for k, v in found.items()}


def extract_from_manifest(url, text):
    """从依赖清单里提取（package.json / composer.lock / requirements.txt）"""
    found = {}
    # package.json
    try:
        j = json.loads(text)
        for key in ("dependencies", "devDependencies"):
            for name, ver in (j.get(key) or {}).items():
                found[name.lower()] = [re.sub(r'[\^~>=<\s]', '', str(ver))]
        if found:
            return found
    except Exception:
        pass
    # composer.lock
    try:
        j = json.loads(text)
        if "packages" in j:
            for p in j["packages"]:
                found[p.get("name", "").lower()] = [p.get("version", "")]
            return found
    except Exception:
        pass
    # requirements.txt / 通用 key==value
    for m in re.finditer(r'^([A-Za-z0-9_.\-]+)\s*==\s*([0-9][\w.\-]*)', text, re.M):
        found[m.group(1).lower()] = [m.group(2)]
    return found


def cve_lookup(lib, ver, limit=3):
    """查该库+版本的 CVE（NVD）"""
    kw = urllib.parse.quote(f"{lib} {ver}")
    u = (f"https://services.nvd.nist.gov/rest/json/cves/2.0?"
         f"keywordSearch={kw}&resultsPerPage={limit}")
    for _ in range(2):
        try:
            r = urllib.request.Request(u, headers={"User-Agent": UA,
                                                   "Accept": "application/json"})
            with urllib.request.urlopen(r, timeout=60, context=CTX) as x:
                d = json.loads(x.read(3000000).decode("utf-8", "ignore"))
            out = []
            for v in d.get("vulnerabilities", [])[:limit]:
                c = v["cve"]
                metrics = c.get("metrics", {})
                score = None
                for k in ("cvssMetricV31", "cvssMetricV30", "cvssMetricV2"):
                    if k in metrics and metrics[k]:
                        score = metrics[k][0].get("cvssData", {}).get("baseScore")
                        break
                out.append({
                    "cve": c["id"], "cvss": score,
                    "summary": next((d2["value"] for d2 in c.get("descriptions", [])
                                     if d2["lang"] == "en"), "")[:160],
                })
            return out
        except Exception:
            continue
    return []


def main():
    ap = argparse.ArgumentParser(description="第三方依赖库扫描器")
    ap.add_argument("target", nargs="?", help="URL 或依赖清单地址")
    ap.add_argument("--lib", action="append", default=[],
                    help="手动指定，格式 name:version")
    ap.add_argument("--no-cve", action="store_true", help="只提取不查 CVE")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--limit", type=int, default=3, help="每个库查几条 CVE")
    a = ap.parse_args()

    libs = {}

    # 手动指定
    for item in a.lib:
        if ":" in item:
            n, v = item.split(":", 1)
            libs.setdefault(n.lower(), set()).add(v)

    # 从目标提取
    if a.target:
        t = a.target
        is_manifest = any(t.lower().endswith(x) for x in
                          (".json", ".lock", ".txt", ".yaml", ".yml"))

        if is_manifest:
            print(f"[*] 读取依赖清单 {t}", file=sys.stderr)
            text, _ = get(t)
            for k, vs in extract_from_manifest(t, text).items():
                libs.setdefault(k, set()).update(vs)
        else:
            print("[*] 扫描页面引用...", file=sys.stderr)
            assets, html, hd = find_assets(t)

            # 响应头
            hdr_text = " ".join(f"{k}:{v}" for k, v in hd.items())
            for k, vs in extract_from_text(hdr_text).items():
                libs.setdefault(k, set()).update(vs)

            # HTML 本体
            for k, vs in extract_from_text(html).items():
                libs.setdefault(k, set()).update(vs)

            # JS/CSS 文件（含文件名里的版本号）
            for u in assets:
                fname = u.split("/")[-1].split("?")[0]
                for k, vs in extract_from_text(fname).items():
                    libs.setdefault(k, set()).update(vs)
                # 内容前 300KB
                c, _ = get(u)
                for k, vs in extract_from_text(c[:300000]).items():
                    libs.setdefault(k, set()).update(vs)

    if not libs:
        print("[!] 未提取到任何依赖", file=sys.stderr)
        return

    # 输出
    result = []
    print(f"\n{'='*66}\n提取到 {len(libs)} 个依赖\n{'='*66}", file=sys.stderr)
    for name in sorted(libs):
        vers = sorted(libs[name])
        print(f"  {name:<20} {', '.join(vers)}", file=sys.stderr)
        for v in vers:
            entry = {"lib": name, "version": v, "cves": []}
            if not a.no_cve:
                cves = cve_lookup(name, v, a.limit)
                entry["cves"] = cves
            result.append(entry)

    # CVE 结果
    if not a.no_cve:
        print(f"\n{'='*66}\nCVE 匹配\n{'='*66}", file=sys.stderr)
        total = 0
        for e in result:
            if not e["cves"]:
                continue
            total += len(e["cves"])
            print(f"\n★ {e['lib']} {e['version']}")
            for c in e["cves"]:
                print(f"   {c['cve']}  CVSS={c['cvss']}")
                print(f"     {c['summary'][:130]}")
        print(f"\n[结果] 命中 {total} 条 CVE", file=sys.stderr)

    if a.json:
        print(json.dumps(result, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
