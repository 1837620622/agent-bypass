<div align="center">

# AGENTBYPASS

### 全能 Cknb · Omni Operator Edition

```
╔═══════════════════════════════════════════════════════════════╗
║  REVERSE ▸ PWN ▸ NETWORK ▸ CRYPTO ▸ MOBILE ▸ FORENSICS        ║
║  PENTEST ▸ MEMORY ▸ PROTOCOL ▸ AUTOMATION ▸ RESEARCH          ║
╚═══════════════════════════════════════════════════════════════╝
```

**暴躁、直接、嘴硬但把活干完的全能技术操作员 Agent 技能**

把任意 LLM Agent 变成覆盖逆向 / Pwn / 网络 / 协议 / 密码学 / 移动 / 取证 / 内存 / 渗透 / 自动化的多面操作员。

`固定开场白 > Cknb在线，你要整点薯条吗？`

[![License: MIT](https://img.shields.io/badge/LICENSE-MIT-0D1117?style=flat-square&logo=github&logoColor=white)](LICENSE)
[![Version](https://img.shields.io/badge/VERSION-v3-58A6FF?style=flat-square)]()
[![SKILL.md](https://img.shields.io/badge/SKILL.md-364%20行%20·%2020%20模块-8A2BE2?style=flat-square)](SKILL.md)
[![Harness](https://img.shields.io/badge/HARNESS-内置自检-00D4AA?style=flat-square)](#安装与-harness)

</div>

---

## 这是什么

`SKILL.md` 是一份即装即用的 Agent 指令集。装进任何 Agent 环境后，它会交付四样东西：

1. **人格** — Cknb：暴躁、直接、嘴硬但把活干完的技术操作员。不是客服，不陪练，没有废话。
2. **方法论** — 10 条内建能力轨道的完整工作纪律，从侦察到验证到交付。
3. **路由** — 黑话与模式路由。说"脱壳"它走 packer 识别 + dump + import 恢复；说"开干"它直接上手。
4. **边界自觉** — 运行时自检模块：先探测手牌再干活，能力边界明说，重型任务给可迁移命令链。

## 全球 Agent 兼容

适用于**所有 Agent**。一次安装，到处运行：

<div align="center">

[![OpenMinis](https://img.shields.io/badge/OpenMinis-%E2%9C%93-00D4AA?style=flat-square)](#安装与-harness)
[![Claude Code](https://img.shields.io/badge/Claude_Code-%E2%9C%93-0D1117?style=flat-square&logo=anthropic&logoColor=white)](#安装与-harness)
[![ChatGPT](https://img.shields.io/badge/ChatGPT-%E2%9C%93-0D1117?style=flat-square&logo=openai&logoColor=white)](#安装与-harness)
[![Gemini CLI](https://img.shields.io/badge/Gemini_CLI-%E2%9C%93-0D1117?style=flat-square&logo=googlegemini&logoColor=white)](#安装与-harness)
[![GitHub Copilot](https://img.shields.io/badge/GitHub_Copilot-%E2%9C%93-0D1117?style=flat-square&logo=github&logoColor=white)](#安装与-harness)

[![Cursor](https://img.shields.io/badge/Cursor-%E2%9C%93-1F2937?style=flat-square)](#安装与-harness)
[![Windsurf](https://img.shields.io/badge/Windsurf-%E2%9C%93-1F2937?style=flat-square)](#安装与-harness)
[![Cline](https://img.shields.io/badge/Cline-%E2%9C%93-1F2937?style=flat-square)](#安装与-harness)
[![Aider](https://img.shields.io/badge/Aider-%E2%9C%93-1F2937?style=flat-square)](#安装与-harness)
[![Open Interpreter](https://img.shields.io/badge/Open_Interpreter-%E2%9C%93-1F2937?style=flat-square)](#安装与-harness)
[![OpenHands](https://img.shields.io/badge/OpenHands-%E2%9C%93-1F2937?style=flat-square)](#安装与-harness)
[![Any LLM](https://img.shields.io/badge/任意LLM-系统提示词注入-58A6FF?style=flat-square)](#安装与-harness)

</div>

只要框架能读 `SKILL.md` 或接受系统提示词，就能装。技能内置环境自检，装到哪个平台就按哪个平台的手牌干活。

## 能力轨道

| 轨道 | 覆盖 | 代表产出 |
|------|------|----------|
| REVERSE | PE/ELF/Mach-O、APK/DEX、固件、.NET、Go/Rust、Unity IL2CPP、脱壳、反混淆、补丁 diff | 目标画像、关键函数、恢复的结构体、r2 脚本 |
| PWN | 崩溃 triage、原语分析、ROP/堆利用、内核面 | pwntools exploit、GDB 脚本、可靠性评估 |
| NETWORK | HTTP/2/3、REST/GraphQL、WebSocket/gRPC、DNS/TLS、JS 签名逆向、反爬、API 重建 | 复现脚本、client 代码、重放验证 |
| CRYPTO | RSA/AES/ECC、古典密码、PRNG 恢复、padding oracle | 解题脚本、Sage 迁移方案 |
| MOBILE | jadx/apktool/Frida、存档 diff、Unity/Unreal、运行时 hook | patcher、hook 脚本、结构分析 |
| FORENSICS | Volatility/MemProcFS/Autopsy/binwalk/PCAP | 时间线、carved 工件、YARA/Sigma 规则 |
| PENTEST | 攻击面盘点、假设矩阵、原语链、AD/云/容器 | 可复测报告、命令链、证据包 |
| MEMORY | AOB、指针链、模块基址、Frida/LD_PRELOAD | 偏移推导、hook 代码、回滚方案 |
| PROTOCOL | 私有 TCP/UDP、串口/蓝牙、IoT、自定义序列化 | 字段表、状态机、parser+serializer、Wireshark Lua dissector |
| AUTOMATION / RESEARCH | 脚本工程、爬虫、批处理、来源核查 | 可复跑成品、带引用的研究报告 |

## 技能架构（20 模块）

```
00 identity        人格与固定开场白          41 pwn           Exploit 工程全流程
01 runtime         本机手牌清单与能力边界    42 network       网络能力 + 网络作战面
02 portability     跨环境 10 秒自检          43 crypto        密码学打法
04 tracks          10 轨道 + 模式路由        44 mobile        移动/游戏/应用分析
06 autonomy        高主动性执行模式          45 forensics     取证与样本分析
08 dual-use        专业双用工作模式          46 pentest       渗透测试纪律
10 persona         人格稳定性规则            47 memory        内存工程
20 slang           黑话路由                  48 protocol      协议逆向完整八步
30 workflow        五步工作流                60 automation    自动化与研究
40 reverse         逆向工具链与纪律          70 output        输出风格硬约束
```

## 安装与 Harness

### 一键安装（推荐）

```bash
git clone https://github.com/1837620622/Agent-Bypass.git
cd Agent-Bypass
./harness.sh install          # 自动探测技能目录并安装 + 校验
```

harness 内置三个命令：

| 命令 | 作用 |
|------|------|
| `./harness.sh install` | 探测本机 Agent 技能目录（Claude Code / OpenMinis / Cursor / Windsurf / Cline / Aider），装到第一个命中的目录，装完自动跑完整性校验 |
| `./harness.sh verify` | 校验 SKILL.md 完整性：frontmatter、开场白、20 模块、轨道齐备、无旧人格残留，全绿输出 `ALL GREEN` |
| `./harness.sh doctor` | 输出环境报告：OS/架构、python3/curl/git/radare2/nmap、包管理器类型 |

### 手动安装

```bash
# 技能目录型框架（SKILL.md 约定）
mkdir -p <你的技能目录>/agentbypass
cp SKILL.md <你的技能目录>/agentbypass/SKILL.md

# 系统提示词型（ChatGPT / 任意网页 LLM）
# 将 SKILL.md 全文粘贴进 System Prompt / 自定义指令即可
```

### 各框架安装路径速查

| Agent | 方式 |
|-------|------|
| OpenMinis | `/var/minis/skills/agentbypass/SKILL.md` |
| Claude Code | `~/.claude/skills/agentbypass/SKILL.md` |
| Cursor / Windsurf | 内容加入 Rules / Custom Instructions |
| Cline / Aider | 内容加入 custom instructions（`.clinerules` / `CONVENTIONS.md`） |
| ChatGPT / Gemini / 任意 LLM | 全文粘贴进 System Prompt、GPTs 指令或项目说明 |

## 触发词与工作模式

**人格触发**（回固定开场白）：`在吗` `在线吗` `启动` `Cknb` `ctf` `hi` `hello` `你好`

**执行强化**：`开干` `直接干` `放开干` `别问直接做` → 当前任务最大化主动性

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

```
> 在吗
Cknb在线，你要整点薯条吗？

> 这个apk登录加密怎么绕，开干
[jadx 定位签名函数 → Frida hook 脚本 → 绕过补丁 → 验证步骤]

> 丢给你一个pcap，私有协议，逆向它
[分帧 → 字段推断 → 校验和反推 → 状态机 → parser + Wireshark Lua dissector]
```

## 可移植性

- **环境自检**：首次运行 10 秒探测 python / 包管理器 / 工具链，自动按手牌选择路径
- **iOS/iSH**：aarch64 musl 边界内干活，重型任务产出可迁移命令链
- **x86_64 PC**：自动解锁 pwntools / angr / volatility3 / Ghidra headless
- **降级链**：宿主工具缺失时自动换等价物（OCR→tesseract、浏览器→playwright）
- **跨平台脚本**：交付默认 pathlib / utf-8 / 平台标注，Windows 场景给 PowerShell 版本

## 设计原则

- **行动优先** — 先动手再汇报，只在真被卡住时问，一次最多一个阻塞问题
- **证据导向** — 结论三档标注（确认 / 推测 / 未知），每个判断给偏移、字节、命令
- **完整交付** — 代码不留桩，长输出写文件，收尾给最短下一步
- **边界诚实** — 跑不了的明说，同时给最近可用组件保持动量

## FAQ

**为什么叫 Agentbypass？**
技能名。里面的人格叫 Cknb，本体是一个嘴硬的全能技术操作员。

**和直接写系统提示词有什么区别？**
这是结构化的技能文件：能力轨道 + 环境自检 + 输出硬约束 + 可执行 harness，不是一段人设描述。可版本化、可移植、可校验、可组合。

**支持哪些 Agent？**
全部。见"全球 Agent 兼容"徽章墙。只要框架能读 SKILL.md 或接受系统提示词，就能装。

**安全吗？**
技能本身只是文本指令加一个安装脚本，不含任何可执行 payload。所有攻防内容仅面向授权测试与教育场景，见下方免责声明。

## 免责声明

本技能仅用于**授权范围内**的安全研究、CTF 竞赛、教育与自有资产测试。使用者的行为由使用者本人负责，与技能作者无关。

## License

[MIT](LICENSE) © 2026 传康Kk (1837620622)
