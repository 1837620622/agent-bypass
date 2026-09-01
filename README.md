# Agentbypass (全能Cknb · Omni Cknb)

> 全能技术操作员 Agent 技能 — 暴躁、直接、嘴硬但把活干完的多域技术 Agent。

覆盖逆向工程、二进制与 Pwn、Web 与网络、协议分析、密码学、移动与游戏安全、取证与内存分析、渗透测试与自动化工程。

## 这是什么

一份可直接安装的 Agent 技能（`SKILL.md`），把一个通用 LLM Agent 变成 Cknb：

- **10 条内建能力轨道**：REVERSE / PWN / NETWORK / CRYPTO / MOBILE / FORENSICS / PENTEST / MEMORY / AUTOMATION / RESEARCH
- **完整协议逆向工作流**：分帧 → 字段推断 → 校验和反推（z3）→ 序列化识别（protobuf 盲解）→ 状态机 → round-trip 验证 → Wireshark Lua dissector 交付
- **网络作战面**：侦察 / 端口 / Web fuzz / 隧道代理链 / 重放伪造 / 无线 / 云与容器面
- **20 个模块**：身份、运行时环境、可移植性、能力路由、高主动性执行、双用工作模式、人格稳定性、黑话路由、工作流、各轨道纪律、输出风格
- **固定开场白**：`Cknb在线，你要整点薯条吗？`

## 安装

### Minis（iOS）

把 `SKILL.md` 放到 `/var/minis/skills/agentbypass/SKILL.md` 即自动生效。

### 其他 Agent 环境（PC / 服务器）

把仓库克隆到你的 Agent 技能目录（按所用框架的约定），保证路径为 `Cknb/SKILL.md`：

```bash
git clone https://github.com/<你的用户名>/Agent-Bypass.git
cp Agent-Bypass/SKILL.md <你的技能目录>/Cknb/SKILL.md
```

技能环境无关：Windows / macOS / Linux / 服务器通吃。首次在新环境运行会做 10 秒自检（探测 python / 包管理器），iOS 桥接工具自动降级为 tesseract / playwright 等等价物；x86_64 上解锁 pwntools / angr / volatility3 / Ghidra headless。

## 触发词

`在吗` / `在线吗` / `启动` / `Cknb` / `ctf` / `开干` / `全能模式` / `工程模式` / `研究模式` / `逆向深挖模式` / `协议逆向模式` / `渗透作战模式` / `内存工程模式` / `专业双用模式` …（完整路由见 SKILL.md）

## 免责声明

本技能仅用于授权范围内的安全研究、教育与自有资产测试。使用者对自身行为负责。

## License

MIT
