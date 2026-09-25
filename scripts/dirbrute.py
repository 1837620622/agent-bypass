#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
并发目录/文件爆破

用法:
  python3 dirbrute.py https://target.com
  python3 dirbrute.py https://target.com --wordlist my.txt
  python3 dirbrute.py https://target.com --ext .php,.bak,.zip --mc 200,301,302,403
  python3 dirbrute.py https://target.com --conc 30 --delay 0.1

输出: jsonl
"""
import argparse, json, sys, ssl, time
from concurrent.futures import ThreadPoolExecutor, as_completed
import urllib.request, urllib.error

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"

# 内置字典（常用路径/文件）
DEFAULT = """admin
login
manage
manager
console
dashboard
api
api/v1
api/v2
v1
v2
user
users
account
accounts
config
config.php
config.js
settings
setup
install
test
tests
debug
dev
beta
backup
backups
bak
old
tmp
temp
log
logs
data
db
database
sql
private
secret
hidden
internal
portal
panel
cpanel
server
status
health
info
version
robots.txt
sitemap.xml
.git/config
.git/HEAD
.svn/entries
.env
.env.bak
.htaccess
web.config
phpinfo.php
info.php
test.php
shell.php
upload
uploads
files
download
downloads
static
assets
js
css
images
img
include
includes
src
lib
vendor
node_modules
composer.json
package.json
requirements.txt
Dockerfile
docker-compose.yml
readme.md
README.md
LICENSE
CHANGELOG.md
documentation.html
docs
docs/index.html
api.html
help.html
about.html
contact.html
index.html
home.html
main.html
default.html
error.html
404.html
403.html
login.html
register.html
admin.html
manage.html
dashboard.html
panel.html
console.html
phpinfo.html
info.html
test.html
demo.html
example.html
sample.html
temp.html
backup.html
old.html
legal.html
privacy.html
terms.html
service.html
agreement.html
faq.html
support.html
status.html
health.html
version.html
changelog.html
release.html
upgrade.html
install.html
setup.html
config.html
settings.html
profile.html
account.html
user.html
users.html
member.html
members.html
list.html
search.html
result.html
order
orders
order/search
order/list
order/detail
goods
goods/list
product
products
item
items
cart
pay
payment
wallet
balance
recharge
topup
withdraw
coupon
promo
notice
announce
message
messages
mail
email
sms
upload.html
download.html
file.html
files.html
image.html
video.html
media.html
static.html
public.html
assets.html
""".strip().split("\n")


def req(url, timeout=8, no_redirect=True):
    h = {"User-Agent": UA, "Accept": "*/*"}
    if no_redirect:
        class NoRedir(urllib.request.HTTPRedirectHandler):
            def redirect_request(self, *a, **k):
                return None
        op = urllib.request.build_opener(NoRedir)
    else:
        op = urllib.request.build_opener()
    # 关键：context 必须装在 opener 的 handler 上，不能传给 open()
    https = urllib.request.HTTPSHandler(context=CTX)
    op.add_handler(https)
    try:
        r = urllib.request.Request(url, headers=h)
        with op.open(r, timeout=timeout) as x:
            return x.status, len(x.read(200000)), dict(x.headers)
    except urllib.error.HTTPError as e:
        return e.code, 0, dict(e.headers)
    except Exception as e:
        # 不再静默吞掉，首次报错打到 stderr 便于排查
        if not req._warned:
            print(f"[req 错误] {url}: {type(e).__name__}: {str(e)[:80]}",
                  file=sys.stderr)
            req._warned = True
        return None, 0, {}


req._warned = False


def main():
    ap = argparse.ArgumentParser(description="并发目录爆破")
    ap.add_argument("base")
    ap.add_argument("--wordlist", help="字典文件（一行一条）")
    ap.add_argument("--ext", default="", help="附加扩展名，如 .php,.bak")
    ap.add_argument("--mc", default="200,204,301,302,307,401,403,405,500",
                    help="关注的状态码")
    ap.add_argument("--conc", type=int, default=20)
    ap.add_argument("--delay", type=float, default=0.0, help="每次请求间隔（秒）")
    ap.add_argument("--timeout", type=float, default=8)
    a = ap.parse_args()

    words = DEFAULT
    if a.wordlist:
        words = [l.strip() for l in open(a.wordlist) if l.strip()]

    exts = [e.strip() for e in a.ext.split(",") if e.strip()] if a.ext else [""]
    paths = []
    for w in words:
        for e in exts:
            paths.append(w + e)

    base = a.base.rstrip("/")
    mc = {int(x) for x in a.mc.split(",") if x.strip()}

    print(f"# {base} 共 {len(paths)} 条 (并发 {a.conc})", file=sys.stderr)

    hits = []

    def one(p):
        if a.delay:
            time.sleep(a.delay)
        url = f"{base}/{p}"
        st, ln, hd = req(url, a.timeout)
        if st in mc:
            return {"url": url, "status": st, "len": ln,
                    "location": hd.get("Location", ""),
                    "server": hd.get("Server", "")}
        return None

    done = 0
    with ThreadPoolExecutor(max_workers=a.conc) as ex:
        futs = {ex.submit(one, p): p for p in paths}
        for fu in as_completed(futs):
            done += 1
            try:
                r = fu.result()
            except Exception:
                r = None
            if r:
                hits.append(r)
                print(json.dumps(r, ensure_ascii=False))
            if done % 200 == 0:
                print(f"  ... {done}/{len(paths)}  命中 {len(hits)}", file=sys.stderr)

    print(f"# 完成: 命中 {len(hits)}", file=sys.stderr)


if __name__ == "__main__":
    main()
