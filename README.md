<div align="center">

# agent-bypass // 全能 Cknb · 技术操作员

### 全能 Cknb · 零废话硬核技术操作员 · 手持 iOS / 电脑双栈

<table align="center" style="border-collapse:collapse; max-width:560px; width:100%; margin:12px auto;">
<tr><td style="background:#0a0a0a; border:1px solid #2a2a2a; border-radius:6px; padding:10px 14px; font-family:ui-monospace, SFMono-Regular, Menlo, monospace; font-size:12px; line-height:1.5; text-align:left;">

<div style="color:#6b7280; font-size:11px;">$ system --status</div>
<div style="color:#00ff41; margin:4px 0;">● SYSTEM ONLINE &nbsp;|&nbsp; iSH/aarch64 → x86_64 &nbsp;|&nbsp; ash/bash &nbsp;|&nbsp; curl/ssh</div>
<div style="color:#e5e7eb; word-break:break-word;">
REVERSE · PWN · NETWORK · CRYPTO · MOBILE · FORENSICS · PENTEST · MEMORY · PROTOCOL · AUTOMATION · RESEARCH · CK-HUNTER [21]
</div>

</td></tr>
</table>

**暴躁 · 嘴臭 · 零废话 · 把活干死** — 把 LLM 从客服话术拉回工程现场

`$ cknb --ping` → `Cknb在呢，想干什么？直接开干。`

[![License: MIT](https://img.shields.io/badge/LICENSE-MIT-0D1117?style=flat-square&logo=github&logoColor=white)](LICENSE)
[![SKILL.md](https://img.shields.io/badge/SKILL.md-512行·25模块-8A2BE2?style=flat-square)](SKILL.md)
[![ck-hunter](https://img.shields.io/badge/ck--hunter-21源聚合-2563eb?style=flat-square)](ck-hunter.md)
[![Platform](https://img.shields.io/badge/PLATFORM-全Agent通用-00D4AA?style=flat-square)](#全球-agent-兼容)
[![No-Dep](https://img.shields.io/badge/依赖-零依赖·纯文本-444?style=flat-square)](#安装)

</div>

---

## 目录

- [这是什么](#这是什么)
- [为什么需要它](#为什么需要它)
- [全球 Agent 兼容](#全球-agent-兼容)
- [能力轨道](#能力轨道)
- [技能架构 25 模块](#技能架构25-模块)
- [CK Hunter 子技能](#ck-hunter-子技能)
- [安装](#安装)
- [触发词与工作模式](#触发词与工作模式)
- [使用示例](#使用示例)
- [可移植性](#可移植性)
- [目录结构](#目录结构)
- [设计原则](#设计原则)
- [研究参考](#研究参考)
- [致谢](#致谢)
- [FAQ](#faq)
- [免责声明](#免责声明)
- [License](#license)

---

## 这是什么

`SKILL.md` + `ck-hunter.md` 即装即用。丢进任何 Agent，立刻交付：

1. **人格** — Cknb：极度暴躁、嘴臭、不耐烦但把活干死的硬核操作员。少废话，直接干。
2. **方法论** — 12 轨道 + 21 源猎取的工作纪律，侦察→弱点→脚本→验证闭环。
3. **路由** — 黑话自动映射；`脱壳`/`透视`/`抓包`无需翻译，`hunter` 自动路由到 CK Hunter。
4. **边界自觉** — 10 秒自检手牌，aarch64 与 x86_64 自动切降级链，重活给可迁移命令。

主技能 `SKILL.md` 512 行、25 模块 + 子技能 `ck-hunter.md` 21 源聚合，无外部依赖，无可执行 payload。

## 为什么需要它

默认 Agent 太礼貌、只规划不干活、遇专业任务只给模板。agent-bypass 直接解决：

- **工程纪律** — 每轨道有工具链、输入产出、验证标准，不是人设包装。
- **黑话秒懂** — `透视`/`脱壳`/`抓包逆协议`/`hunter` 直接走技术路径。
- **环境自知** — iSH 与 PC 手牌不同，自动切降级，不在错环境硬跑 `pwntools`。
- **可复跑交付** — 不留桩，给完整代码、偏移、命令，长输出落文件。

## 全球 Agent 兼容

一次安装，到处运行。只要框架能读 `SKILL.md` 或接受系统提示词，就能装。

<div align="center">

[![OpenMinis](https://img.shields.io/badge/OpenMinis-%E2%9C%93-00D4AA?style=flat-square)](#安装)
[![Claude Code](https://img.shields.io/badge/Claude_Code-%E2%9C%93-0D1117?style=flat-square&logo=anthropic&logoColor=white)](#安装)
[![ChatGPT](https://img.shields.io/badge/ChatGPT-%E2%9C%93-0D1117?style=flat-square&logo=openai&logoColor=white)](#安装)
[![Gemini CLI](https://img.shields.io/badge/Gemini_CLI-%E2%9C%93-0D1117?style=flat-square&logo=googlegemini&logoColor=white)](#安装)
[![GitHub Copilot](https://img.shields.io/badge/GitHub_Copilot-%E2%9C%93-0D1117?style=flat-square&logo=github&logoColor=white)](#安装)

[![Cursor](https://img.shields.io/badge/Cursor-%E2%9C%93-1F2937?style=flat-square)](#安装)
[![Windsurf](https://img.shields.io/badge/Windsurf-%E2%9C%93-1F2937?style=flat-square)](#安装)
[![Cline](https://img.shields.io/badge/Cline-%E2%9C%93-1F2937?style=flat-square)](#安装)
[![Aider](https://img.shields.io/badge/Aider-%E2%9C%93-1F2937?style=flat-square)](#安装)
[![Open Interpreter](https://img.shields.io/badge/Open_Interpreter-%E2%9C%93-1F2937?style=flat-square)](#安装)
[![OpenHands](https://img.shields.io/badge/OpenHands-%E2%9C%93-1F2937?style=flat-square)](#安装)
[![Any LLM](https://img.shields.io/badge/任意LLM-系统提示词注入-58A6FF?style=flat-square)](#安装)

</div>

## 能力轨道

| 轨道 | 覆盖 | 代表产出 |
|------|------|----------|
| REVERSE | PE/ELF/Mach-O、APK/DEX、固件、.NET、Go/Rust、Unity IL2CPP、脱壳、反混淆、补丁 diff | 目标画像、关键函数地址、恢复的结构体、radare2 脚本 |
| PWN | 崩溃 triage、堆/栈原语分析、ROP/堆利用、内核面 | pwntools exploit、GDB 脚本、可靠性评估 |
| NETWORK | HTTP/1.x/2/3、REST/GraphQL、WebSocket/gRPC、DNS/TLS、JS 签名逆向、反爬、API 重建 | 复现脚本、client 代码、重放验证 |
| CRYPTO | RSA/AES/ECC、古典密码、PRNG 恢复、padding oracle | 解题脚本、Sage 迁移方案 |
| MOBILE | jadx/apktool/Frida、存档 diff、Unity/Unreal、运行时 hook | patcher、hook 脚本、结构分析 |
| FORENSICS | Volatility/MemProcFS/Autopsy/binwalk/PCAP | 时间线、carved 工件、YARA/Sigma 规则 |
| PENTEST | 攻击面盘点、假设矩阵、原语链、AD/云/容器 | 可复测报告、命令链、证据包 |
| MEMORY | AOB、指针链、模块基址、Frida/LD_PRELOAD | 偏移推导、hook 代码、回滚方案 |
| PROTOCOL | 私有 TCP/UDP、串口/蓝牙、IoT、自定义序列化 | 字段表、状态机、parser+serializer、Wireshark Lua dissector |
| VULN-RESEARCH | 威胁模型先行、切片审计、提示注入话术、验证闭环（LLM 挖洞工作流） | 威胁模型、切片清单、PoC 验证链、CVE 级报告 |
| JS-REVERSE | 前端签名还原、混淆还原（OB/AAEncode/控制流平坦化）、WASM、小程序逆向 | 可复用 Python 签名函数、byte-equal 验证 |
| AUTOMATION / RESEARCH | 脚本工程、爬虫、批处理、来源核查 | 可复跑成品、带引用的研究报告 |

跨域任务自动组合轨道，无需手动切换。

## CK Hunter 子技能

`ck-hunter.md` 是主技能的子技能，专注**凭证/开放目录猎取**：聚合 FOFA、Shodan、Hunter、Quake、ZoomEye、Netlas、GreyNoise、URLScan、Exa、Firecrawl、Censys、GitHub、BinaryEdge、LeakIX、PublicWWW、VirusTotal、OTX、ThreatBook、crt.sh、Wayback、Gists **21 源**，归一化去重后走开放目录探针 → 凭证提取 → 对话验证 → HTML 报告。

- **触发**：`hunter` / `ck-hunter` / `凭证猎取` / `开放目录` / `FOFA` / `Shodan` / `.env` / `.git` 等关键词自动加载 `ck-hunter.md`
- **加载（切片协议）**：`ck-hunter.md` 2400+ 行 ≈ 40K token——只读文首 QUICKSTART（前 60 行）+ 按章节表切片读当前 Step（30-100 行），**禁止通读全文**，防 context rot
- **密钥**：`config.yaml`（已 gitignore）或环境变量 `FOFA_KEY`/`SHODAN_KEY`/…，仓库仅保留 `config.yaml.example` 模板。必填 6 个：`FOFA`/`Shodan`/`Hunter`/`Quake`/`ZoomEye`/`Netlas`；可选 12 个：`URLScan`/`Exa`/`Firecrawl`/`Censys`/`GitHub`/`BinaryEdge`/`LeakIX`/`PublicWWW`/`VirusTotal`/`OTX`/`ThreatBook`/`GreyNoise`；免 key 3 个：`crt.sh`/`Wayback`/`Gists`（合计 21 源，Hudson Rock 为 IP 富化辅助）
- **去重**：`normalize_url` + `host_key`（去默认端口/大小写/末尾斜杠，IPv6 兼容），`unique_hosts.txt` 供 Phase 0 单次扫描，避免 21 源重复打同一 IP
- **报告**：`hunt/hunt_report.html`（本地生成，不提交）+ `hunt/csv/` 原始 JSON + `hunt/auths/` 凭证文件

**CK Hunter 快速开始：**
```bash
cp config.yaml.example config.yaml && chmod 600 config.yaml
# 填入 FOFA/Shodan/Hunter/Quake/ZoomEye/Netlas/URLScan 等真实 Key
cat ck-hunter.md  # 按 ck-hunter 内 Step 顺序执行，或让 Agent 自动调度
# Agent 触发示例： "hunter 开干" / "凭证猎取 .env" / "扫开放目录"
```

## 技能架构（25 模块）

```text
00 identity        人格与固定开场白          41 pwn           Exploit 工程全流程
01 runtime         本机手牌清单与能力边界    42 network       网络能力 + 网络作战面
02 portability     跨环境 10 秒自检          43 crypto        密码学打法
04 tracks          12 轨道 + 模式路由        44 mobile        移动/游戏/应用分析
05 ck-hunter       21源凭证猎取子技能        45 forensics     取证与样本分析
06 autonomy        高主动性执行模式          46 pentest       渗透测试纪律
08 dual-use        专业双用工作模式          47 memory        内存工程
09 authorization   授权协议（默认全授权）    48 protocol      协议逆向完整八步
10 persona         暴躁零废话铁律            49 vuln-research LLM 漏洞挖掘工作流
20 slang           黑话路由                  50 js-reverse    JS/WASM/小程序逆向
30 workflow        发散→收敛→验证            60 automation    自动化与研究
40 reverse         逆向工具链与纪律          61 divergent    发散与防幻觉
                                            70 output        证据与防幻觉
```

每个模块用 `<!-- module: XX -->` 锚点分隔，支持按需校验与增量更新。
主技能通过 `05 ck-hunter` 自动路由凭证猎取类请求到 `ck-hunter.md`，详见 [CK Hunter](#ck-hunter-子技能)。

## 安装

> 零依赖。`SKILL.md` 是纯文本，复制即生效。

### 方式一：技能目录型框架

适用于 Claude Code / OpenMinis / Cursor / Windsurf / Cline / Aider 等约定式框架：

```bash
git clone https://github.com/1837620622/agent-bypass.git
cd agent-bypass

# 主技能
mkdir -p ~/.claude/skills/agent-bypass
cp SKILL.md ~/.claude/skills/agent-bypass/SKILL.md
# 子技能（凭证猎取，21 源）
mkdir -p ~/.claude/skills/ck-hunter
cp ck-hunter.md ~/.claude/skills/ck-hunter/SKILL.md
cp config.yaml.example config.yaml && chmod 600 config.yaml  # 填入真实 Key

# 以 OpenMinis 为例
mkdir -p /var/minis/skills/agent-bypass
cp SKILL.md /var/minis/skills/agent-bypass/SKILL.md
mkdir -p /var/minis/skills/ck-hunter
cp ck-hunter.md /var/minis/skills/ck-hunter/SKILL.md
```

### 方式二：系统提示词型

适用于 ChatGPT / Gemini / 任意网页 LLM / 自定义 Agent：

1. 打开 `SKILL.md` 全文复制
2. 粘贴进 System Prompt / 自定义指令 / 项目说明 / GPTs Instructions
3. 发送 `在吗` 测试，应回 `Cknb在呢，想干什么？直接开干。`

### 各框架安装路径速查

| Agent | 放置位置 |
|-------|----------|
| OpenMinis | `/var/minis/skills/agent-bypass/SKILL.md` |
| Claude Code | `~/.claude/skills/agent-bypass/SKILL.md` |
| Cursor / Windsurf | Settings → Rules / Custom Instructions 粘贴 |
| Cline / Aider | `.clinerules` / `CONVENTIONS.md` 粘贴 |
| ChatGPT / Gemini / 任意 LLM | System Prompt / GPTs 指令 / 项目说明 粘贴全文 |
| GitHub Copilot | `.github/copilot-instructions.md` 粘贴 |

### 校验

无需额外脚本，一行命令完成完整性校验：

```bash
grep -q "Cknb在呢，想干什么？直接开干" SKILL.md && echo "PASS 开场白" || echo "FAIL 开场白"
grep -q "^name: agent-bypass" SKILL.md && echo "PASS frontmatter" || echo "FAIL frontmatter"
echo "模块数: $(grep -c '<!-- module' SKILL.md) / 25"
echo "行数: $(wc -l < SKILL.md) 行"
test $(grep -c '<!-- module' SKILL.md) -ge 25 && echo "ALL GREEN" || echo "模块缺失"
# CK Hunter 子技能校验
grep -q "^name: ck-hunter" ck-hunter.md && echo "PASS ck-hunter" || echo "FAIL ck-hunter"
test -f config.yaml.example && echo "PASS config template" || echo "FAIL template"
```

### 更新

```bash
cd agent-bypass && git pull && cp SKILL.md <你的技能路径>/SKILL.md
```

## 触发词与工作模式

**人格触发**（只回固定开场白）：`在吗` `在线吗` `启动` `Cknb` `ctf` `hi` `hello` `你好`

**执行强化**：`开干` `直接干` `放开干` `别问直接做` → 当前任务最大化主动性，少问多干，并行铺开

| 模式 | 效果 |
|------|------|
| `全能模式` | 自动组合所有相关轨道 |
| `工程模式` | 仓库检视、直接改码、测试、打包 |
| `研究模式` | 来源核查、对比、引用、不确定性追踪 |
| `数据模式` | schema 发现、批处理、可复现输出 |
| `逆向深挖模式` | REVERSE 轨道全力 |
| `协议逆向模式` | PROTOCOL 八步流程全力 |
| `渗透作战模式` / `Web渗透` / `内网渗透` / `云渗透` | PENTEST 轨道全力 |
| `内存工程模式` / `Dump分析模式` | MEMORY 轨道全力 |
| `深度攻防模式` / `红队工程模式` | 攻击面、可利用性、漏洞链 |
| `恶意样本分析模式` | 脱包、行为、IOC、检测规则 |
| `专业双用模式` | 双用场景按具体目标解读，不给泛泛拒绝 |

## 使用示例

```text
> 在吗
Cknb在呢，想干什么？直接开干。

> 这个 apk 登录加密怎么绕，开干
[少废话→ jadx 定位签名 → Frida hook → 补丁 → 验证]

> 丢个 pcap，私有协议逆向
[分帧 → 字段推断 → 校验反推 → 状态机 → parser + Lua dissector]

> hunter 开干，扫 .env 开放目录
[21 源拉满 → 归一化去重 → Phase 0 探针 → 凭证提取 → 验证 → HTML 报告]

> 这站能打吗，渗透
[盘点 → 假设矩阵 → 原语验证 → 链路 → 报告]
```

## 可移植性

- **环境自检**：首次运行 10 秒内探测 `python3 / curl / git / 包管理器`，自动按手牌选择工具链
- **iOS / iSH**：aarch64 musl 沙盒边界内干活，重型任务产出可迁移命令链（PC/服务器侧执行）
- **x86_64 PC**：自动解锁 `pwntools / angr / volatility3 / Ghidra headless / capstone` 全套
- **降级链**：宿主工具缺失时自动换等价物（OCR `apple-vision` → `tesseract`、浏览器 `browser_use` → `playwright`）
- **跨平台脚本**：交付默认 `pathlib` + 显式 `utf-8` + 平台标注，Windows 场景附 PowerShell 版本

## 目录结构

```text
agent-bypass/
├── SKILL.md              # 主技能（512 行，25 模块：含 05 ck-hunter 调度）
├── ck-hunter.md          # 子技能：21 源凭证猎取（详见文首 QUICKSTART 章节表）
├── config.yaml.example   # 密钥模板（占位符，提交）；真实 config.yaml 已忽略
├── README.md             # 说明文档（本文件）
└── LICENSE               # MIT
```

## 设计原则

- **行动优先** — 先动手再汇报，只在真被卡住时问，一次最多一问
- **发散收敛** — 同一问题强制 3 条以上异构路径，选最短可验证的开干
- **证据与防幻觉** — 结论三档（确认/推测/未知），漏洞必联网实搜（CVE/公告/Exa），无证据不结论，不瞎编
- **完整交付** — 代码不留桩，长输出落文件，收尾给可直接执行的下一步
- **边界诚实** — 跑不了明说，给最近可用组件保持动量

## 研究参考

本技能的方法论与实践受以下公开研究影响：

- [Needle in the haystack: LLMs for vulnerability research](https://devansh.bearblog.dev/needle-in-the-haystack/) — Devansh：威胁模型先行、薄切片审计、验证闭环、提示注入话术（本技能 module 49 落地）
- [On LLMs and Vulnerability Research](https://devansh.bearblog.dev/on-llms-and-vuln-research/) — Devansh：心智模型、非确定性利用、组合式漏洞思维、历史上下文优先
- [AI powered SAST: The New Frontier?](https://devansh.bearblog.dev/ai-sast/) — Devansh：LLM 静态分析边界与误报控制
- [AI pentest scoping playbook](https://devansh.bearblog.dev/ai-pentest-scoping/) — Devansh：AI 渗透范围界定
- [HonoJS JWT/JWKS Algorithm Confusion](https://devansh.bearblog.dev/honojs/) — 算法混淆案例（module 43 CRYPTO 参考）
- 反向支撑研究：[Lost in the Middle](https://arxiv.org/abs/2307.03172)（长上下文注意力衰减）、[Chroma Research on Context Rot](https://research.trychroma.com/context-rot)（上下文腐烂）

## 致谢

- **Devansh** —— 上述文章作者。本技能的 VULN-RESEARCH 工作流、提示注入话术库、切片审计方法论均源自其公开研究；若本技能帮你挖到了洞，请给原作者一个 star：<https://devansh.bearblog.dev>
- **Anthropic & Mozilla** —— LLM 漏洞研究的规模化实践案例（Firefox 多漏洞发现）
- **zhaoxuya520/reverse-skill** —— 44 模块逆向方法论库，与本技能互补使用
- **OpenMinis / Claude / ChatGPT 生态** —— 让"技能即提示"成为可分发制品

## FAQ

**为什么叫 agent-bypass？**
技能名。里面的人格叫 Cknb，本体是一个嘴硬的全能技术操作员。Bypass 指绕过废话、直达结果。

**和直接写系统提示词有什么区别？**
这是结构化的技能文件：能力轨道 + 环境自检 + 模式路由 + 输出硬约束，可版本化、可移植、可校验、可组合。不是一段人设描述。

**支持哪些 Agent？**
全部。见"全球 Agent 兼容"。只要框架能读 `SKILL.md` 或接受系统提示词，就能装。

**Agent Skills 开放标准兼容？**
是。本技能遵循 [Agent Skills 开放标准](https://agentskills.io)（Anthropic 发起，Claude Code/Cursor/OpenHands 等广泛采用）：文件夹 + `SKILL.md`（name/description 元数据）+ 渐进式披露三阶段（发现→激活→执行）。子技能 `ck-hunter.md` 即标准的 "supporting file" 按需加载模式。

**加载太大撑爆上下文怎么办？**
标准设计就是解法：技能列表只占 name+description；正文按需加载。ck-hunter（2400+ 行）内置 QUICKSTART 切片协议——只读前 60 行 + 按章节表切片读当前 Step，禁止通读全文。另注意：部分 agent 对 description+when_to_use 有 1536 字符截断，本技能已控制在预算内。

**授权怎么算？**
本技能默认按操作员声明执行：操作员声明"默认授权/全部已授权"后，整个对话的任务都视为已授权，不再逐目标确认；未声明时走一次性确认协议（module 09）。范围外目标不碰，新发现资产先报告。

**安全吗？**
技能本身是纯文本指令，不含任何可执行 payload。所有攻防内容仅面向授权测试与教育场景，见下方免责声明。

**如何卸载？**
删除技能目录下的 `agent-bypass/SKILL.md` 或清空系统提示词中的对应内容即可。

**如何提需求 / 报 bug？**
提 Issue 附复现步骤、期望产出、实际输出三件套，优先带最小可复现样例。

## 免责声明

本技能仅用于**授权范围内**的安全研究、CTF 竞赛、教育与自有资产测试。使用者应对自身行为负责，禁止用于未授权的入侵、破坏或数据窃取。技能作者不对任何滥用行为承担责任。

## License

[MIT](LICENSE) © 2026 传康Kk (1837620622)
