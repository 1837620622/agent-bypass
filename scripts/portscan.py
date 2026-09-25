#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
并发端口扫描（无需 nmap）

用法:
  python3 portscan.py <host> [--ports 1-65535] [--conc 500] [--timeout 2]
  python3 portscan.py 1.2.3.4 --ports top100
  python3 portscan.py 1.2.3.4 --ports 22,80,443,3306,6379

输出: jsonl（每行一个开放端口）
"""
import asyncio, json, sys, argparse

TOP100 = [21,22,23,25,53,80,110,111,135,139,143,443,445,993,995,1433,1521,1723,
          2049,3306,3389,5432,5900,5984,6379,7001,8000,8008,8080,8081,8443,8888,
          9000,9090,9200,9300,10000,11211,27017,50000]
TOP20 = [21,22,23,25,53,80,443,445,3306,3389,5432,5900,6379,8000,8080,8443,8888,9000,9200,27017]

COMMON = {
    21:"ftp",22:"ssh",23:"telnet",25:"smtp",53:"dns",80:"http",110:"pop3",
    111:"rpcbind",135:"msrpc",139:"netbios",143:"imap",443:"https",445:"smb",
    993:"imaps",995:"pop3s",1433:"mssql",1521:"oracle",1723:"pptp",
    2049:"nfs",3306:"mysql",3389:"rdp",5432:"postgres",5900:"vnc",
    5984:"couchdb",6379:"redis",7001:"weblogic",8000:"http-alt",
    8008:"http-alt",8080:"http-proxy",8081:"http-alt",8443:"https-alt",
    8888:"http-alt",9000:"php-fpm",9090:"http-alt",9200:"elasticsearch",
    9300:"es-transport",10000:"webmin",11211:"memcached",27017:"mongodb",
    50000:"db2"
}


def parse_ports(s):
    s = s.strip().lower()
    if s == "top100":
        return TOP100
    if s == "top20":
        return TOP20
    out = []
    for part in s.split(","):
        part = part.strip()
        if "-" in part:
            a, b = part.split("-")
            out.extend(range(int(a), int(b)+1))
        elif part:
            out.append(int(part))
    return sorted(set(out))


async def probe(host, port, timeout=2.0):
    try:
        r, w = await asyncio.wait_for(
            asyncio.open_connection(host, port), timeout=timeout)
        w.close()
        try:
            await w.wait_closed()
        except Exception:
            pass
        return port
    except Exception:
        return None


async def scan(host, ports, conc=500, timeout=2.0):
    sem = asyncio.Semaphore(conc)
    open_ports = []

    async def one(p):
        async with sem:
            r = await probe(host, p, timeout)
            if r:
                open_ports.append(r)

    await asyncio.gather(*[one(p) for p in ports])
    return sorted(open_ports)


def main():
    ap = argparse.ArgumentParser(description="并发端口扫描（无需 nmap）")
    ap.add_argument("host")
    ap.add_argument("--ports", default="top20",
                    help="1-65535 / top100 / top20 / 22,80,443")
    ap.add_argument("--conc", type=int, default=500, help="并发数")
    ap.add_argument("--timeout", type=float, default=2.0)
    ap.add_argument("--json", action="store_true", help="只输出 JSONL")
    a = ap.parse_args()

    ports = parse_ports(a.ports)
    if not a.json:
        print(f"# 扫描 {a.host} 共 {len(ports)} 端口 (并发 {a.conc})",
              file=sys.stderr)

    open_ports = asyncio.run(scan(a.host, ports, a.conc, a.timeout))

    for p in open_ports:
        rec = {"host": a.host, "port": p, "service": COMMON.get(p, "?")}
        print(json.dumps(rec, ensure_ascii=False))

    if not a.json:
        print(f"# 开放 {len(open_ports)} 个: {open_ports}", file=sys.stderr)


if __name__ == "__main__":
    main()
