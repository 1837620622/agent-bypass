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

把任意 LLM Agent 从客服话术拉回工程现场。覆盖逆向 / Pwn / 网络 / 协议 / 密码学 / 移动 / 取证 / 渗透 / 内存 的全栈操作员指令集。

`固定开场白 > Cknb在线，你要整点薯条吗？`

[![License: MIT](https://img.shields.io/badge/LICENSE-MIT-0D1117?style=flat-square&logo=github&logoColor=white)](LICENSE)
[![Version](https://img.shields.io/badge/VERSION-v3.1-58A6FF?style=flat-square)](#)
[![SKILL.md](https://img.shields.io/badge/SKILL.md-364行·20模块-8A2BE2?style=flat-square)](SKILL.md)
[![Platform](https://img.shields.io/badge/PLATFORM-全Agent通用-00D4AA?style=flat-square)](#全球-agent-兼容)
[![No-Dep](https://img.shields.io/badge/依赖-零依赖·纯文本-444?style=flat-square)](#安装)

</div>

---

## 目录

- [这是什么](#这是什么)
- [为什么需要它](#为什么需要它)
- [全球 Agent 兼容](#全球-agent-兼容)
- [能力轨道](#能力轨道)
- [技能架构 20 模块](#技能架构20-模块)
- [安装](#安装)
- [触发词与工作模式](#触发词与工作模式)
- [使用示例](#使用示例)
- [可移植性](#可移植性)
- [目录结构](#目录结构)
- [设计原则](#设计原则)
- [FAQ](#faq)
- [免责声明](#免责声明)
- [License](#license)

---

## 这是什么

`SKILL.md` 是一份即装即用的 Agent 指令集。丢进任何能读系统提示词或技能文件的 Agent 环境，立刻交付四样东西：

1. **人格** — Cknb：暴躁、直接、嘴硬但把活干完的技术操作员。不陪练，不说客服话术，直接上手干活。
2. **方法论** — 10 条能力轨道的完整工作纪律。从侦察到弱点定位到脚本到验证，链路闭环。
3. **路由** — 黑话与模式路由。说“脱壳”自动走 packer 识别 + dump + import 恢复；说“开干”直接拉满主动性。
4. **边界自觉** — 运行时自检。先探测手头有什么工具再选路径，重型任务给可迁移到 PC/服务器的精确命令链，不硬撑。

单文件 364 行，20 个内建模块，无外部依赖，无可执行 payload。

## 为什么需要它

默认的 LLM Agent 有三个毛病：太礼貌、太会规划不干活、遇到专业任务只给模板。AgentBypass 解决的就是这个落差：

- **不是人设，是工程纪律** — 每个轨道都有工具链、输入产出、验证标准。不是一句“你现在是黑客”。
- **说黑话能听懂** — “透视/自瞄/脱壳/过检测/抓包逆协议”无需翻译，直接映射到技术路径。
- **知道自己在哪干活** — iOS/iSH 的 aarch64 musl 和 x86_64 PC 的手牌完全不同，技能会自动切降级链，不会在错的环境硬跑 `pwntools`。
- **交付物可复跑** — 不给“此处略”，给完整可跑的代码、偏移、字节、命令，长输出落地成文件。

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
| AUTOMATION / RESEARCH | 脚本工程、爬虫、批处理、来源核查 | 可复跑成品、带引用的研究报告 |

跨域任务自动组合轨道，无需手动切换。

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

每个模块用 `<!-- module: XX -->` 锚点分隔，支持按需校验与增量更新。

## 安装

> 零依赖。`SKILL.md` 是纯文本，复制即生效。

### 方式一：技能目录型框架

适用于 Claude Code / OpenMinis / Cursor / Windsurf / Cline / Aider 等约定式框架：

```bash
git clone https://github.com/1837620622/Agent-Bypass.git
cd Agent-Bypass

# 以 Claude Code 为例
mkdir -p ~/.claude/skills/agentbypass
cp SKILL.md ~/.claude/skills/agentbypass/SKILL.md

# 以 OpenMinis 为例
mkdir -p /var/minis/skills/agentbypass
cp SKILL.md /var/minis/skills/agentbypass/SKILL.md
```

### 方式二：系统提示词型

适用于 ChatGPT / Gemini / 任意网页 LLM / 自定义 Agent：

1. 打开 `SKILL.md` 全文复制
2. 粘贴进 System Prompt / 自定义指令 / 项目说明 / GPTs Instructions
3. 发送 `在吗` 测试，应回 `Cknb在线，你要整点薯条吗？`

### 各框架安装路径速查

| Agent | 放置位置 |
|-------|----------|
| OpenMinis | `/var/minis/skills/agentbypass/SKILL.md` |
| Claude Code | `~/.claude/skills/agentbypass/SKILL.md` |
| Cursor / Windsurf | Settings → Rules / Custom Instructions 粘贴 |
| Cline / Aider | `.clinerules` / `CONVENTIONS.md` 粘贴 |
| ChatGPT / Gemini / 任意 LLM | System Prompt / GPTs 指令 / 项目说明 粘贴全文 |
| GitHub Copilot | `.github/copilot-instructions.md` 粘贴 |

### 校验

无需额外脚本，一行命令完成完整性校验：

```bash
grep -q "Cknb在线，你要整点薯条吗" SKILL.md && echo "PASS 开场白" || echo "FAIL 开场白"
grep -q "^name: Agentbypass" SKILL.md && echo "PASS frontmatter" || echo "FAIL frontmatter"
echo "模块数: $(grep -c '<!-- module' SKILL.md) / 20"
echo "行数: $(wc -l < SKILL.md) 行"
test $(grep -c '<!-- module' SKILL.md) -ge 20 && echo "ALL GREEN" || echo "模块缺失"
```

### 更新

```bash
cd Agent-Bypass && git pull && cp SKILL.md <你的技能路径>/SKILL.md
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

```
> 在吗
Cknb在线，你要整点薯条吗？

> 这个 apk 登录加密怎么绕，开干
[jadx 定位签名函数 → Frida hook 脚本 → 绕过补丁 → 验证步骤]

> 丢给你一个 pcap，私有协议，逆向它
[分帧 → 字段推断 → 校验和反推 → 状态机 → parser + Wireshark Lua dissector]

> 有个固件 bin，帮我看入口和保护
[file + strings + r2 -A 目标画像 → 入口函数 → 打包/混淆判定 → 脱包路线图]

> 这站能打吗，Web 渗透
[攻击面盘点 → 假设矩阵 → 原语验证 → 链路组装 → 可复测报告 + 修复建议]
```

## 可移植性

- **环境自检**：首次运行 10 秒内探测 `python3 / curl / git / 包管理器`，自动按手牌选择工具链
- **iOS / iSH**：aarch64 musl 沙盒边界内干活，重型任务产出可迁移命令链（PC/服务器侧执行）
- **x86_64 PC**：自动解锁 `pwntools / angr / volatility3 / Ghidra headless / capstone` 全套
- **降级链**：宿主工具缺失时自动换等价物（OCR `apple-vision` → `tesseract`、浏览器 `browser_use` → `playwright`）
- **跨平台脚本**：交付默认 `pathlib` + 显式 `utf-8` + 平台标注，Windows 场景附 PowerShell 版本

## 目录结构

```
Agent-Bypass/
├── SKILL.md        # 技能本体（364 行，20 模块，单文件即全部）
├── README.md       # 说明文档（本文件）
└── LICENSE         # MIT
```

## 设计原则

- **行动优先** — 先动手再汇报，只在真被卡住时问，一次最多一个阻塞问题
- **证据导向** — 结论三档标注（确认 / 推测 / 未知），每个判断给偏移、字节、命令
- **完整交付** — 代码不留桩，长输出写文件，收尾给最短下一步
- **边界诚实** — 跑不了的明说，同时给最近可用组件保持动量

## FAQ

**为什么叫 AgentBypass？**
技能名。里面的人格叫 Cknb，本体是一个嘴硬的全能技术操作员。Bypass 指绕过废话、直达结果。

**和直接写系统提示词有什么区别？**
这是结构化的技能文件：能力轨道 + 环境自检 + 模式路由 + 输出硬约束，可版本化、可移植、可校验、可组合。不是一段人设描述。

**支持哪些 Agent？**
全部。见“全球 Agent 兼容”。只要框架能读 `SKILL.md` 或接受系统提示词，就能装。

**安全吗？**
技能本身是纯文本指令，不含任何可执行 payload。所有攻防内容仅面向授权测试与教育场景，见下方免责声明。

**如何卸载？**
删除技能目录下的 `agentbypass/SKILL.md` 或清空系统提示词中的对应内容即可。

**如何提需求 / 报 bug？**
提 Issue 附复现步骤、期望产出、实际输出三件套，优先带最小可复现样例。

## 免责声明

本技能仅用于**授权范围内**的安全研究、CTF 竞赛、教育与自有资产测试。使用者应对自身行为负责，禁止用于未授权的入侵、破坏或数据窃取。技能作者不对任何滥用行为承担责任。

## License

[MIT](LICENSE) © 2026 传康Kk (1837620622)
