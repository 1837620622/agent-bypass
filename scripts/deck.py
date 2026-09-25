#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
牌组管理器（§01 Step 5.5 · 攻击面牌化）

把每轮攻击收集到的信息变成"牌"，供模型自己推演组合。

★ 设计原则：本工具不规定组合规则。
   只做三件事：① 存牌 ② 呈现牌面 ③ 给思考提示
   组合效果由模型自己推理 —— 规则写死了就只会那几种。

用法:
  python3 deck.py add --type cred --value "user:pass" --note "普通用户" --from "/api/login"
  python3 deck.py show                    # 看手里的牌（含牌面分析）
  python3 deck.py show --type cred
  python3 deck.py matrix                  # 输出组合矩阵（类型交叉表）
  python3 deck.py prompt                  # 输出推演提示（给模型看的思考题）
  python3 deck.py rm --id 3
  python3 deck.py clear
  python3 deck.py next-round
"""
import argparse, json, os
from datetime import datetime, timezone, timedelta

BASE = os.path.dirname(os.path.abspath(__file__))
DECK = os.path.join(BASE, "..", "deck.json")
CST = timezone(timedelta(hours=8))

# ── 牌型定义（只描述"是什么"，不规定"能组合出什么"）──
TYPES = {
    "cred":     ("凭据",   "账号/密码/token/session/cookie/API key"),
    "endpoint": ("端点",   "URL/接口/路径（含 403、隐藏的、未授权的）"),
    "leak":     ("泄露",   "配置/密钥/源码/报错/内网地址"),
    "tech":     ("技术栈", "框架/中间件/版本/组件"),
    "vuln":     ("弱点",   "已确认存在的缺陷（未完全利用）"),
    "perm":     ("权限",   "角色/授权级别/可访问范围"),
    "data":     ("数据",   "拿到的业务数据（用户列表/订单/配置）"),
    "bypass":   ("绕过",   "已验证有效的绕过手法"),
    "infra":    ("基建",   "IP/端口/子域/证书/云资源"),
    "logic":    ("逻辑",   "业务流程/状态机/时序特征"),
    "timing":   ("时序",   "时间窗口/竞态条件/过期策略"),
    "signal":   ("信号",   "报错模式/响应差异/行为异常"),
}


def load():
    if os.path.exists(DECK):
        try:
            return json.load(open(DECK))
        except Exception:
            return {"cards": [], "round": 1}
    return {"cards": [], "round": 1}


def save(d):
    json.dump(d, open(DECK, "w"), ensure_ascii=False, indent=1)


def add_card(args):
    d = load()
    cid = max([c["id"] for c in d["cards"]], default=0) + 1
    card = {
        "id": cid, "type": args.type, "value": args.value,
        "note": args.note or "", "source": args.source or "",
        "layer": args.layer or "?",           # 逻辑链坐标：在哪一层
        "role": args.role or "?",             # 角色：消费者/提供者/中间人
        "conn": args.conn or "",              # 连向：上下游是谁
        "round": args.round if args.round else d["round"],
        "ts": datetime.now(CST).strftime("%Y-%m-%d %H:%M"),
        "used": False,
    }
    d["cards"].append(card)
    save(d)
    tname = TYPES.get(args.type, (args.type,))[0]
    print(f"✓ 新增牌 #{cid} [{tname}] {args.value}")
    if card["note"]:
        print(f"  备注: {card['note']}")
    if card["source"]:
        print(f"  来源: {card['source']}")
    if card["layer"] != "?" or card["conn"]:
        print(f"  坐标: {card['layer']} / {card['role']}"
              + (f" / 连向 {card['conn']}" if card["conn"] else ""))


def show(args):
    d = load()
    cards = d["cards"]
    if args.type:
        cards = [c for c in cards if c["type"] == args.type]
    if not cards:
        print("(手里没有牌)")
        return

    groups = {}
    for c in cards:
        groups.setdefault(c["type"], []).append(c)

    print("=" * 72)
    print(f"  牌组 — {len(cards)} 张（第 {d['round']} 轮）")
    print("=" * 72)
    for t, items in sorted(groups.items()):
        tname, tdesc = TYPES.get(t, (t, ""))
        print(f"\n【{tname}】{len(items)} 张 — {tdesc}")
        for c in items:
            mark = "✓" if c["used"] else " "
            coord = ""
            if c.get("layer") and c["layer"] != "?":
                coord = f" [{c['layer']}"
                if c.get("role") and c["role"] != "?":
                    coord += f"/{c['role']}"
                coord += "]"
            print(f"  {mark} #{c['id']:<3} {c['value'][:58]}{coord}")
            if c["note"]:
                print(f"        └ {c['note'][:66]}")
            if c.get("conn"):
                print(f"        ↕ 连向: {c['conn'][:60]}")

    # 牌面统计（不是规则，是观察）
    print("\n" + "=" * 72)
    print("  牌面分析")
    print("=" * 72)
    have = set(groups.keys())
    missing = [t for t in TYPES if t not in have]
    print(f"  已有类型: {', '.join(TYPES.get(t, (t,))[0] for t in have)}")
    print(f"  缺失类型: {', '.join(TYPES.get(t, (t,))[0] for t in missing) or '无'}")
    print(f"  未使用:   {len([c for c in cards if not c['used']])} 张")


def matrix(args):
    """输出类型交叉矩阵 —— 只给结构，不给结论"""
    d = load()
    cards = d["cards"]
    if len(cards) < 2:
        print("(牌不足 2 张)")
        return

    bytype = {}
    for c in cards:
        bytype.setdefault(c["type"], []).append(c)
    ts = sorted(bytype.keys())

    print("=" * 72)
    print("  组合矩阵（交叉点 = 该类型对的牌数乘积，供你逐个思考）")
    print("=" * 72)
    hdr = "        " + "".join(f"{TYPES.get(t,(t,))[0]:>8}" for t in ts)
    print(hdr)
    for a in ts:
        row = f"{TYPES.get(a,(a,))[0]:>8}"
        for b in ts:
            if a == b:
                n = len(bytype[a]) * (len(bytype[a]) - 1) // 2
            else:
                n = len(bytype[a]) * len(bytype[b])
            row += f"{n:>8}"
        print(row)

    print(f"\n  共 {len(ts)} 种牌型，{sum(len(bytype[a])*(len(bytype[b])) for a in ts for b in ts if a!=b)//2 + sum(len(bytype[a])*(len(bytype[a])-1)//2 for a in ts)} 个可能的两两组合")
    print("\n  下一步: 用 `deck.py prompt` 拿到思考题，逐个推演")


def prompt(args):
    """输出推演提示 —— 引导思考，不给答案"""
    d = load()
    cards = d["cards"]
    if len(cards) < 2:
        print("(牌不足 2 张)")
        return

    bytype = {}
    for c in cards:
        bytype.setdefault(c["type"], []).append(c)

    print("=" * 72)
    print("  牌组推演提示（★ 组合效果由你自己推理，这里只给思考框架）")
    print("=" * 72)

    print("""
━━━ 第零层：逻辑链坐标（★ 先定位，再推演）━━━

每张牌在产业链上有位置，位置决定它能影响谁：

    L0 源头/资源层    真实资源提供者
    L1 生产/供给层    把资源加工成商品
    L2 平台/中转层    技术封装
    L3 分销/零售层    面向终端（防护通常最弱）
    L4 终端层         最终用户

""")
    for c in cards:
        tname = TYPES.get(c["type"], (c["type"],))[0]
        lay = c.get("layer", "?")
        role = c.get("role", "?")
        conn = c.get("conn", "")
        print(f"  #{c['id']} [{tname}] {c['value'][:45]}")
        print(f"      坐标: {lay} / {role}" + (f" / 连向 {conn}" if conn else ""))
        if lay == "?":
            print("      ⚠ 未标注坐标 —— 先想清楚它在链上哪里")

    print("""
━━━ 沿链推演（五个方向，逐个自问）━━━

  ① ⬆ 向上（最优先）
     这张牌能不能让我接触它的上游？上游是谁？能不能绕过中间直接打？
     线索：配置里的上游地址/凭据、报错里的上游域名、代理执行器接口

  ② ↔ 平行
     同层其他节点能不能用同样方法打？同款系统？共享凭据？

  ③ ⬇ 向下
     能不能影响下游？篡改下发内容？伪造回调？读下游数据？

  ④ ↺ 自身
     这张牌本身还能挖多深？权限能不能提？数据能不能扩？隐藏功能？

  ⑤ ⤴ 跳板（跨层）
     能不能作为跳板够到其他层？一点撬动整条链？

""")
    print("  你的推演（自己填）：\n")
    for c in cards:
        tname = TYPES.get(c["type"], (c["type"],))[0]
        print(f"  #{c['id']} [{tname}] {c['value'][:40]}")
        print("      ①向上:    ②平行:    ③向下:    ④自身:    ⑤跳板:")

    print("""
━━━ 单张牌的"半成品属性" ━━━

每张牌都是半成品，先问自己：这张牌"还差什么"才能变成完整能力？

""")
    for c in cards:
        tname = TYPES.get(c["type"], (c["type"],))[0]
        print(f"  #{c['id']} [{tname}] {c['value'][:50]}")
        print("      → 它现在能干什么？还缺什么？")

    print("""
━━━ 第二层：两两组合（自问自答）━━━

对每一对牌，问这四个问题：

  ① 能不能拼成一条完整攻击链？
     （A 提供"钥匙"，B 提供"锁"？）

  ② A 能不能帮 B 绕过限制？
     （B 被什么挡住？A 里有能解开它的东西吗？）

  ③ A 能不能扩大 B 的效果？
     （B 只能打一个点，A 能不能让它打一片？）

  ④ A 和 B 指向的是不是同一个目标？
     （同一个系统/同一个用户/同一条数据流？）

""")
    ts = sorted(bytype.keys())
    print("  你的牌型组合（自己填结论）：\n")
    for i, a in enumerate(ts):
        for b in ts[i:]:
            na = TYPES.get(a, (a,))[0]
            nb = TYPES.get(b, (b,))[0]
            if a == b and len(bytype[a]) < 2:
                continue
            print(f"  [{na}] × [{nb}]")
            print("      ① 完整链？  ② 绕过？  ③ 放大？  ④ 同目标？")
            print("      → 结论: ")

    print("""
━━━ 第三层：三张以上（链式推演）━━━

  如果两两组合都不通，试三张：
     A 打不开 B，但 A + C 可以先拿到 D，再用 D 打开 B

  问自己：
     · 我手里有没有"中间态"的牌，能当作跳板？
     · 有没有哪张牌可以"放大"另一张的效果？
     · 所有牌指向的目标之间，有没有信任关系？

━━━ 第四层：缺牌分析 ━━━

  推演中如果反复卡在"需要某样东西但我没有"：
     → 那就是你的下一张目标牌
     → 回到 §1.6 侧枝探测，专门去搞这张牌

━━━ 第五层：组合的代价 ━━━

  每个组合都问：
     · 这个组合会留多少痕迹？（响度）
     · 失败了会不会暴露意图？（可逆性）
     · 有没有更隐蔽的组合能达到同样效果？
""")


def rm_card(args):
    d = load()
    before = len(d["cards"])
    d["cards"] = [c for c in d["cards"] if c["id"] != args.id]
    save(d)
    print(f"✓ 删除 {before - len(d['cards'])} 张牌")


def clear(args):
    d = load()
    d["cards"] = []
    d["round"] = 1
    save(d)
    print("✓ 牌组已清空")


def next_round(args):
    d = load()
    d["round"] += 1
    for c in d["cards"]:
        c["used"] = False
    save(d)
    print(f"✓ 进入第 {d['round']} 轮（所有牌重置为未使用）")


def main():
    ap = argparse.ArgumentParser(description="牌组管理器 — 攻击面牌化（不规定组合规则）")
    sub = ap.add_subparsers(dest="cmd")

    p = sub.add_parser("add", help="添加一张牌")
    p.add_argument("--type", required=True, choices=list(TYPES.keys()))
    p.add_argument("--value", required=True)
    p.add_argument("--note", default="")
    p.add_argument("--from", dest="source", default="")
    p.add_argument("--layer", default="", help="逻辑链坐标：L0源头/L1供给/L2平台/L3分销/L4终端")
    p.add_argument("--role", default="", help="角色：消费者/提供者/中间人/旁观者")
    p.add_argument("--conn", default="", help="连向：上游是谁 / 下游是谁")
    p.add_argument("--round", type=int)
    p.set_defaults(func=add_card)

    p = sub.add_parser("show", help="查看牌组 + 牌面分析")
    p.add_argument("--type")
    p.set_defaults(func=show)

    p = sub.add_parser("matrix", help="类型交叉矩阵")
    p.set_defaults(func=matrix)

    p = sub.add_parser("prompt", help="★ 输出推演提示（思考框架）")
    p.set_defaults(func=prompt)

    p = sub.add_parser("rm", help="删除一张牌")
    p.add_argument("--id", type=int, required=True)
    p.set_defaults(func=rm_card)

    p = sub.add_parser("clear", help="清空牌组")
    p.set_defaults(func=clear)

    p = sub.add_parser("next-round", help="进入下一轮")
    p.set_defaults(func=next_round)

    a = ap.parse_args()
    if not a.cmd:
        ap.print_help()
        print("\n牌型说明:")
        for t, (n, d2) in TYPES.items():
            print(f"  {t:<10} {n:<6} {d2}")
        print("\n★ 本工具不规定组合规则 —— 用 `prompt` 拿思考框架，自己推演")
        return
    a.func(a)


if __name__ == "__main__":
    main()
