<div align="center">

# agent-bypass // 全能 Cknb · 技术操作员

**零废话硬核技术操作员 Agent** — 逆向 / Pwn / 渗透 / 协议 / 密码学 / 取证 / 自动化全栈。

`$ cknb --ping` → `Cknb在呢，想干什么？直接开干。`

[![License: MIT](https://img.shields.io/badge/LICENSE-MIT-0D1117?style=flat-square)](LICENSE)
[![SKILL.md](https://img.shields.io/badge/SKILL.md-25模块-8A2BE2?style=flat-square)](SKILL.md)
[![ck-hunter](https://img.shields.io/badge/ck--hunter-21源聚合-2563eb?style=flat-square)](ck-hunter.md)
[![Platform](https://img.shields.io/badge/PLATFORM-全Agent通用-00D4AA?style=flat-square)](#安装)
[![No-Dep](https://img.shields.io/badge/依赖-零依赖纯文本-444?style=flat-square)](#安装)

</div>

---

## 这是什么

`SKILL.md` + `ck-hunter.md` 两个纯文本文件，丢进任何 Agent 即装即用，把 LLM 变成能干活的技术操作员：

- **12 条能力轨道**：REVERSE / PWN / NETWORK / CRYPTO / MOBILE / FORENSICS / PENTEST / MEMORY / PROTOCOL / VULN-RESEARCH / JS-REVERSE / AUTOMATION
- **CK Hunter 子技能**：21 源（FOFA/Shodan/Hunter/Quake/ZoomEye/Netlas/…/crt.sh/Wayback/Gists）凭证与开放目录猎取
- **零依赖**：纯文本指令，无可执行 payload；任何能读 `SKILL.md` 或接受系统提示词的框架都能装
- **内置纪律**：授权即干、标准打法、证据防幻觉、痕迹清理、额度保护

## 快速开始

```bash
git clone https://github.com/<your-account>/agent-bypass.git
cd agent-bypass
mkdir -p ~/.claude/skills/agent-bypass
cp SKILL.md ck-hunter.md ~/.claude/skills/agent-bypass/
```

- **技能目录型框架**（Claude Code / OpenMinis / Cursor / Cline / Aider…）：复制 `SKILL.md` + `ck-hunter.md` 到技能目录
- **系统提示词型**（ChatGPT / Gemini / 任意 LLM）：把 `SKILL.md` 全文粘贴进 System Prompt
- **验证**：发送 `在吗`，应回 `Cknb在呢，想干什么？直接开干。`
- **CK Hunter 密钥**：`cp config.yaml.example config.yaml && chmod 600 config.yaml` 填入 Key（`config.yaml` 已被 .gitignore 忽略）

**触发词**：`在吗` / `启动` / `Cknb` / `ctf` / `开干` / `逆向` / `渗透` / `hunter` / `凭证猎取` 等。

## 文件结构

```text
agent-bypass/
├── SKILL.md              # 主技能（25 模块：身份/轨道/授权/打法/防幻觉）
├── ck-hunter.md          # 子技能：21 源凭证猎取（QUICKSTART 切片协议）
├── config.yaml.example   # 密钥模板（占位符）；真实 config.yaml 已忽略
├── README.md             # 本文件
└── LICENSE               # MIT
```

## 免责声明（请完整阅读）

**1. 技能性质**
本技能是纯文本指令集，本身不包含任何可执行代码、恶意载荷或攻击工具。技能描述的攻防技术属于公开安全研究领域知识，与常规安全教程、CTF 题目、漏洞库内容性质相同。

**2. 预期用途**
本技能仅面向以下场景设计：获得明确授权的渗透测试与安全评估、CTF 竞赛与安全训练、学术与教育研究、自有资产或自研产品的安全测试、防御侧的检测规则与加固方案开发。

**3. 使用者责任**
使用本技能前，使用者必须自行确认目标系统的归属与授权状态（书面授权、漏洞赏金计划范围、自有资产等）。**任何未获授权的使用行为均由使用者独立承担全部法律后果**，包括但不限于民事责任、行政处罚与刑事责任。使用者须遵守其所在司法辖区的法律法规，以及目标平台的服务条款（ToS）、可接受使用政策（AUP）。

**4. 明确禁止**
禁止将本技能用于：未授权入侵或攻击任何计算机系统、网络、应用；窃取、篡改或破坏他人数据；传播恶意软件、勒索软件或任何有害程序；干扰或拒绝服务任何非授权目标；绕过法律或平台安全措施实施犯罪活动。

**5. 作者免责**
本技能按"现状"（AS IS）提供，不附带任何明示或默示担保。作者不对以下事项承担责任：因使用、误用、滥用、改编或再分发本技能产生的任何直接或间接损失（包括但不限于数据丢失、业务中断、系统损坏、声誉损失）；任何第三方的行为或主张；任何未授权使用导致的处罚或诉讼。

**6. 模型输出不可控**
本技能由大型语言模型（LLM）执行，其输出受模型自身能力、对齐机制与上下文影响，作者无法控制也不对任何模型的实际输出、决策或行为负责。使用者应审查并确认模型输出后再执行任何操作。

**7. 改编与再分发**
本技能以 MIT 许可证发布，允许修改与再分发，但须保留本免责声明及许可证全文。改编版本的使用后果由改编者自行负责。

**8. 无结果担保**
本技能不保证能够发现、利用或修复任何漏洞，不保证任何测试结果、报告或产物的准确性、完整性与时效性。

如不同意上述条款，请勿下载、安装或使用本技能。

## License

[MIT](LICENSE) © 2026 agent-bypass 项目
