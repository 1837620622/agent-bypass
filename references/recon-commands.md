# 情报收集命令集

## 一、被动收集（不触碰目标）

### 域名与 DNS
```bash
whois target.com
dig +short target.com A
dig +short target.com MX
dig +short target.com TXT          # 常含 SPF/验证信息
dig +short target.com NS
dig +short -x 1.2.3.4              # 反查

# DNS 历史（找已废弃但可能仍在用的IP）
# securitytrails.com / viewdns.info / dnsdumpster.com
```

### 证书透明度（子域金矿）
```bash
curl -s "https://crt.sh/?q=%25.target.com&output=json" | jq -r '.[].name_value' | tr ',' '\n' | sort -u
```
> 证书日志会暴露**所有签发过证书的子域**，包括测试环境、内部系统。
> 常能发现几十个子域，每个都可能是独立攻击面。

### ★ GitHub / 代码仓库搜索（最高价值）

```bash
# 网页搜索语法
"target.com" password
"target.com" api_key
"target.com" secret
"target.com" token
org:TargetOrg filename:.env
org:TargetOrg filename:application.yml
org:TargetOrg filename:config.php
path:**/config/*.yml
filename:.env DB_PASSWORD
filename:docker-compose.yml password
"BEGIN RSA PRIVATE KEY"
"BEGIN OPENSSH PRIVATE KEY"
```

```bash
# 工具
trufflehog git https://github.com/org/repo --only-verified
gitleaks detect --source . -v
# grep.app 可在所有公开仓库中搜字符串
```

**重点文件类型**：
```
.env  .env.bak  config.php  database.yml  application-prod.yml
settings.py  wp-config.php  docker-compose.yml  .git-credentials
*.pem  *.key  id_rsa  *.p12  *.jks  keystore
```

**中文项目常搜**：
```
搜索：目标公司名 + 数据库 / 支付 / 后台
搜索：目标系统名 + 源码 / 破解版 / 开心版
```

### 资产测绘平台
```
FOFA      fofa.info
Quake      quake.360.cn
Hunter     hunter.how
Shodan     shodan.io
Censys     censys.io
ZoomEye    zoomeye.org
```

```bash
# FOFA 核心语法
domain="target.com"
cert="target.com"                  # ★ 证书反查，挖关联资产
ip="1.2.3.4"                       # ★ 同IP所有站点，攻击面翻倍
body="特征字符串"                   # 找同款系统
title="系统名"
header="Server: nginx/1.18.0"
icon_hash="-1234567890"            # ★ favicon指纹，找同源系统
port="8080" && country="CN"
org="公司名"
```

**多资产关联技巧**：
1. `domain=` 找目标全部资产
2. `cert=` 找同一证书下的其他域名（同一个人/公司）
3. `ip=` 找同机部署的所有站点
4. `icon_hash=` 找使用同款系统的其他实例（可能有更早的版本漏洞）
5. `body="报错字符串"` 找同款系统

### 历史与快照
```
web.archive.org                    # 历史页面
urlscan.io                         # 历史扫描记录
github.com/search                  # 泄露的源码
```

### 商务信息
```
ICP备案：beian.miit.gov.cn
工商：天眼查 / 企查查 / 国家企业信用信息公示系统
域名注册：whois（注意隐私保护，可用历史whois）
```

## 二、主动收集（需授权，会留日志）

### 端口与服务
```bash
# 快速全端口
nmap -sS -p- --min-rate 2000 -T4 target
masscan -p1-65535 --rate=5000 target

# 服务识别
nmap -sV -sC -p 22,80,443,3306,6379,8080,8089,9000 target
nmap -sV --script http-title,http-headers,http-enum target

# UDP（别忘）
nmap -sU --top-ports 100 target
```

### 指纹识别
```bash
whatweb -a 3 https://target
wafw00f https://target
curl -sI https://target                          # 看 Server / X-Powered-By
curl -s https://target/favicon.ico | md5sum     # favicon hash
```

### 目录与文件爆破
```bash
# 目录
ffuf -u https://target/FUZZ -w /usr/share/seclists/Discovery/Web-Content/common.txt -mc 200,301,302,401,403
dirsearch -u https://target -e php,asp,aspx,jsp,html,js

# 敏感文件（手工必试清单）
/.git/config
/.env
/.env.bak
/backup.zip
/www.zip
/database.sql
/phpinfo.php
/robots.txt
/sitemap.xml
/swagger-ui.html
/actuator
/openapi.json
/Dockerfile
/package.json
/composer.json

# 备份文件后缀
index.php.bak  index.php~  index.php.swp  index.php.save
config.php.old  config.php.orig  index.php.1
```

### 子域爆破
```bash
subfinder -d target -silent | httpx -silent -title -sc
amass enum -passive -d target
dnsx -d target -w subdomains.txt
```

### 从文档拿接口清单（★ 高性价比）
```bash
curl -s https://target/openapi.json | jq '.paths | keys'
curl -s https://target/v2/api-docs | jq '.paths | keys'
curl -s https://target/actuator/mappings | jq
curl -s https://target/swagger-ui.html

# 提取所有接口路径
curl -s https://target/openapi.json | jq -r '.paths | keys[]' | sort
```

## 三、协议分析（★ 别跳过）

**在做任何利用之前，先用浏览器看真实请求长什么样：**

```
1. 打开目标页面
2. F12 → Network → 勾选 Preserve log
3. 执行目标操作（登录/提交订单/查询）
4. 找到对应的 XHR/Fetch 请求
5. 右键 → Copy as cURL
6. 对着这个 curl 分析：请求头、参数格式、是否加密、是否有签名字段
```

**必查项**：
```
- 是否有 signature / sign / nonce / timestamp 字段
- 请求体是明文还是加密（base64 / hex / RSA）
- Content-Type 是 json 还是 form-urlencoded
- 有没有自定义 Header（token / X-Api-Key / appid）
- 前端 JS 里有没有加密函数（grep encrypt / JSEncrypt / AES / RSA）
```

```bash
# 从 JS 中找加密逻辑和密钥
curl -s https://target/static/js/main.js | grep -oE "(publicKey|privateKey|secretKey|aesKey|iv)\s*[:=]\s*['\"][^'\"]{8,}"
curl -s https://target/static/js/main.js | grep -oE "MFww[A-Za-z0-9+/=]{20,}"
curl -s https://target/static/js/main.js | grep -oE "BEGIN (PUBLIC|RSA)[A-Z ]*KEY"
```

> **教训**：如果登录接口总是返回"请完成验证"/"参数错误"，先怀疑**请求格式不对**，
> 而不是急着归因给验证码或WAF。多数"卡死"是因为没按协议发请求。

## 四、代理与抓包

```bash
# Burp Suite 常用
# 拦截 → 改包 → 重放（Repeater）→ 爆破（Intruder）

# 命令行代理
curl -x http://127.0.0.1:8080 -k https://target

# mitmproxy 脚本化改包
mitmproxy -s script.py
```

## 五、协作与记录

```bash
# 保持目录结构
recon/
  subdomains.txt
  ports.txt
  screenshots/
  requests/          # 保存原始请求响应
  findings.md

# 每个发现都记录：时间、命令、完整响应
```
