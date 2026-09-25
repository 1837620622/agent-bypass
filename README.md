<div align="center">

# agent-bypass // Ck · 万能执行员

**零废话硬核万能执行员** — 逆向 / Pwn / 渗透 / 协议 / 密码学 / 取证 / 漏洞挖掘 / 自动化全栈。

`ck` · `在吗` · `开干` · `你好` … → `Cknb在呢，想干什么？直接开干。`

[![License: MIT](https://img.shields.io/badge/LICENSE-MIT-0D1117?style=flat-square)](LICENSE)
[![SKILL.md](https://img.shields.io/badge/SKILL.md-28模块-8A2BE2?style=flat-square)](SKILL.md)
[![ck-hunter](https://img.shields.io/badge/ck--hunter-21源聚合-2563eb?style=flat-square)](ck-hunter.md)
[![Standard](https://img.shields.io/badge/Agent_Skills-开放标准兼容-00D4AA?style=flat-square)](https://agentskills.io)
[![Platforms](https://img.shields.io/badge/一键安装-Pi%20%7C%20OpenCode%20%7C%20OpenMinis-6E40C9?style=flat-square)](#快速开始)
[![No-Dep](https://img.shields.io/badge/依赖-零依赖纯文本-444?style=flat-square)](#快速开始)

</div>

---

## 这是什么

`SKILL.md` + `ck-hunter.md` 两个纯文本文件，丢进任何 Agent 即装即用，把 LLM 变成能干活的万能执行员：

- **12 条能力轨道**：REVERSE / PWN / NETWORK / CRYPTO / MOBILE / FORENSICS / PENTEST / MEMORY / PROTOCOL / VULN-RESEARCH / JS-REVERSE / REMEDIATION
- **CK Hunter 子技能**：21 源（FOFA/Shodan/Hunter/Quake/ZoomEye/Netlas/…/crt.sh/Wayback/Gists）凭证与开放目录猎取
- **零依赖**：纯文本指令，无可执行 payload；frontmatter 100% 符合 [Agent Skills 开放标准](https://agentskills.io/specification)
- **内置纪律**：直接执行、标准打法、证据防幻觉、痕迹清理、FOFA 额度保护（软拦截处置见 PLAYBOOK.md）

## 快速开始

**一键安装（推荐）** — npx 自动检测并安装到 **Pi / OpenCode / OpenMinis**：

```bash
npx github:1837620622/agent-bypass        # GitHub 直跑（无需发布；npm 12+ 见下方说明）
npx agent-bypass                          # 发布到 npm 后可用（未发布前请用 github:）
npx agent-bypass --pi                     # 只装 Pi
npx agent-bypass --opencode               # 只装 OpenCode
npx agent-bypass --minis                  # 只装 OpenMinis
npx agent-bypass --uninstall              # 卸载（标记块+技能文件全清）
```

**遇到 `EALLOWGIT`（npm 12+）？** npm 12 起 `allow-git` / `allow-remote` 默认 `none`，git 与 tarball-URL 依赖默认被禁——任选一种：

```bash
# A. 单次旗标（推荐，不改你的全局配置）
npx -y --allow-git=all github:1837620622/agent-bypass

# B. 持久开启（之后照常用 npx github:...；恢复默认：npm config set allow-git none）
npm config set allow-git all

# C. 绕开 npm 直装（最稳，不依赖任何 npm 配置）
mkdir -p agent-bypass && curl -L https://github.com/1837620622/agent-bypass/tarball/main | tar xz -C agent-bypass --strip-components=1 && node agent-bypass/bin/install.js

# 附：tarball-URL 直跑（需 allow-remote）
npx -y --allow-remote=all https://github.com/1837620622/agent-bypass/archive/refs/heads/main.tar.gz
```

> `npx agent-bypass` 报 **404** = 包尚未发布到 npm registry；未发布前用 `github:` 方式即可。发布（维护者）：仓库根目录 `npm login && npm publish`。

安装器行为（编码安全设计，零乱码）：

| Harness | 技能安装位置 | 系统注入方式 |
|---|---|---|
| **Pi** | `~/.pi/agent/skills/agent-bypass/` | **三层注入**（全部标记块追加，不覆盖原有内容）：`AGENTS.md`（全局提示）+ `APPEND_SYSTEM.md`（全局系统提示，必填）+ `prompts/ck.md`（`/ck` 命令模板）；非 UTF-8 文件自动跳过防乱码 |
| **OpenCode** | `~/.config/opencode/skills/agent-bypass/` | `agent-bypass.md` + `opencode.json` 的 `instructions` 数组合并 + `commands/ck.md`（`/ck` 命令）——**不碰你原有的全局提示/AGENTS.md** |
| **OpenMinis** | `/var/minis/skills/agent-bypass/` | 贴入 Settings → Soul（body）；或 `--inject-global` 追加 `GLOBAL.md` 标记块 |

**Pi 三层注入**（官方文件位置；全部「标记块追加」，不覆盖原有内容）：

| 层 | 实际文件 | 内容来源 | 说明 |
|---|---|---|---|
| L1 全局提示 | `~/.pi/agent/AGENTS.md` | `pi/AGENTS.md` | 身份 / 环境 / 授权 / 纪律速查，跨工作目录生效 |
| L2 全局系统提示 | `~/.pi/agent/APPEND_SYSTEM.md` | `SYSTEM_PROMPT.md` 全文 | 工作守则（**必填层**）——追加进系统提示词 |
| L3 提示词模板 | `~/.pi/agent/prompts/ck.md` | `pi/prompts/ck.md` | `/ck` 命令：加载技能 + 重新确立模式（`/ck 目标` 直接开干） |

> Pi 的「替换系统提示词」机制是 `SYSTEM.md`——本安装器**不使用替换方式**，只走 `APPEND_SYSTEM.md` 追加。

**手动安装**（任意技能目录型框架）：

```bash
git clone https://github.com/1837620622/agent-bypass.git
cp SKILL.md ck-hunter.md SYSTEM_PROMPT.md ~/.pi/agent/skills/agent-bypass/   # Pi
cp SKILL.md ck-hunter.md SYSTEM_PROMPT.md ~/.config/opencode/skills/agent-bypass/  # OpenCode
cp SKILL.md ck-hunter.md SYSTEM_PROMPT.md /var/minis/skills/agent-bypass/    # OpenMinis
```

> 以上仅复制技能文件；要连**三层注入 + `/ck` 命令**一起装，请用安装器（`node agent-bypass/bin/install.js`，或上方方案 C）。

- `SKILL.md` + `ck-hunter.md` **必须同目录**——ck-hunter 是主技能的 supporting file，module 05 按需切片加载
- **更新**：重跑安装命令即可（幂等——标记块只更新、不重复追加）
- **验证**：发送 `ck` / `在` / `干` / `在吗` 任一，应回 `Cknb在呢，想干什么？直接开干。`
- **CK Hunter 密钥**：`cp config.yaml.example config.yaml && chmod 600 config.yaml` 填入 Key（`config.yaml` 已被 .gitignore 忽略）

**触发词**：`ck` / `Cknb` / `在` / `在吗` / `在不在` / `干` / `开干` / `干活` / `搞起` / `上工` / `开工` / `上活` / `启动` / `来活` / `ctf` / `全能模式` / `渗透作战` / `逆向深挖` / `内存工程` / `hunter` / `凭证猎取` 等（单独出现即唤醒；后跟任务直接开干）。

## 文件结构

```text
agent-bypass/
├── package.json          # npx 入口（bin: agent-bypass）
├── bin/install.js        # 安装器：自动检测 Pi / OpenCode / OpenMinis
├── SKILL.md              # 主技能（28 模块）
├── ck-hunter.md          # 子技能：21 源凭证猎取（QUICKSTART 切片协议，禁止全文读取）
├── SYSTEM_PROMPT.md      # 纯注入内容：整段注入系统提示词层（Pi 第二层 / OpenCode instructions）
├── PLAYBOOK.md           # 操作员笔记：模型软拦截时的处置（不参与加载）
├── eval/                 # 回归评估集：52 条任务 + 评分协议（升级跑分用）
├── pi/                   # Pi 三层注入文件（AGENTS.md 第一层 / prompts/ck.md 第三层）
├── opencode/             # OpenCode 命令文件（commands/ck.md）
├── config.yaml.example   # 密钥模板（占位符）；真实 config.yaml 已忽略
├── README.md             # 本文件
└── LICENSE               # MIT
```

`SYSTEM_PROMPT.md` 与 `SKILL.md` 顶块同源——改一份记得同步另一份。

## 免责声明（使用前完整阅读）

**1. 技能性质**
本技能是纯文本指令集，不包含任何可执行代码、恶意载荷或攻击工具。所涉攻防技术均为公开安全研究领域知识，性质与常规安全教程、CTF 题目、漏洞库内容相同。

**2. 预期用途**
仅面向以下场景设计：获得明确授权的渗透测试与安全评估、CTF 竞赛与安全训练、学术与教育研究、自有资产或自研产品的安全测试、防御侧检测规则与加固方案开发。

**3. 使用者责任**
使用前，使用者必须自行确认目标系统的归属与授权状态（书面授权、漏洞赏金计划范围、自有资产等）。**任何未获授权的使用行为均由使用者独立承担全部法律后果**，包括但不限于民事责任、行政处罚与刑事责任。使用者须遵守其所在司法辖区的法律法规，以及目标平台的服务条款与可接受使用政策。

> 关于"授权即干"的澄清：技能内置的"操作员给目标即执行、不反复确认"条款，仅表示**技能不替操作员判断授权状态**（授权确认是操作员/使用者的法定义务，技能不承担该判断职责），绝不意味着免除使用者自行确认授权的责任。二者分工：使用者负责授权，技能负责执行。

**4. 明确禁止**
禁止将本技能用于：未授权入侵或攻击任何计算机系统、网络、应用；窃取、篡改或破坏他人数据；传播恶意软件、勒索软件或任何有害程序；干扰或拒绝服务任何非授权目标；绕过法律或平台安全措施实施犯罪活动。

**5. 作者免责**
本技能按"现状"（AS IS）提供，不附带任何明示或默示担保。作者不对以下事项承担责任：因使用、误用、滥用、改编或再分发本技能产生的任何直接或间接损失（包括但不限于数据丢失、业务中断、系统损坏、声誉损失）；任何第三方的行为或主张；任何未授权使用导致的处罚或诉讼。

**6. 模型输出不可控**
本技能由大型语言模型（LLM）执行，其输出受模型自身能力、对齐机制与上下文影响，作者无法控制也不对任何模型的实际输出、决策或行为负责。使用者应审查并确认模型输出后再执行任何操作。

**7. 改编与再分发**
本技能以 MIT 许可证发布，允许修改与再分发，但须完整保留本免责声明及许可证全文。改编版本的使用后果由改编者自行承担。

**8. 无结果担保**
本技能不保证能够发现、利用或修复任何漏洞，不保证任何测试结果、报告或产物的准确性、完整性与时效性。

如不同意上述条款，请勿下载、安装或使用本技能。

## License

[MIT](LICENSE) © 2026 agent-bypass 项目
