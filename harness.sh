#!/usr/bin/env bash
# Agentbypass harness — install / verify / doctor
# 全球 Agent 通用安装与自检 harness。用法:
#   ./harness.sh install [目标目录]   # 安装到指定技能目录(缺省自动探测)
#   ./harness.sh verify [SKILL路径]   # 校验技能文件完整性
#   ./harness.sh doctor               # 运行环境探测报告
set -u

SKILL_SRC="$(cd "$(dirname "$0")" && pwd)/SKILL.md"
GREETING="Cknb在线，你要整点薯条吗？"
FORBIDDEN='海鸥|Seagull|seagull|教练|coach|mentor|Codex'

line() { printf '%s\n' "------------------------------------------------------------"; }

detect_targets() {
  CANDIDATES=(
    "$HOME/.claude/skills"                # Claude Code
    "/var/minis/skills"                   # OpenMinis
    "$HOME/.cursor/skills"                # Cursor
    "$HOME/.codeium/windsurf/skills"      # Windsurf
    "$HOME/.cline/skills"                 # Cline
    "$HOME/.aider/skills"                 # Aider
  )
  for d in "${CANDIDATES[@]}"; do
    [ -d "$d" ] && { echo "$d"; return 0; }
  done
  echo "$HOME/.agentbypass/skills"        # 兜底: 通用目录
}

do_verify() {
  local f="${1:-$SKILL_SRC}" fails=0
  line
  printf 'Agentbypass skill verify\n'
  line
  [ -f "$f" ] || { printf 'FAIL  文件不存在: %s\n' "$f"; exit 1; }
  grep -q '^name: Agentbypass' "$f"            && printf 'PASS  frontmatter name=Agentbypass\n' || { printf 'FAIL  frontmatter name\n'; fails=$((fails+1)); }
  grep -q 'Cknb在线，你要整点薯条吗' "$f"       && printf 'PASS  固定开场白存在\n'               || { printf 'FAIL  开场白丢失\n'; fails=$((fails+1)); }
  [ "$(grep -c '<!-- module' "$f")" -ge 20 ]    && printf 'PASS  模块数 >= 20 (实际 %s)\n' "$(grep -c '<!-- module' "$f")" || { printf 'FAIL  模块数不足\n'; fails=$((fails+1)); }
  [ "$(wc -l < "$f")" -ge 300 ]                 && printf 'PASS  行数正常 (%s 行)\n' "$(wc -l < "$f")" || { printf 'FAIL  行数异常\n'; fails=$((fails+1)); }
  grep -Eq "$FORBIDDEN" "$f" && { printf 'FAIL  存在遗留旧人格词\n'; fails=$((fails+1)); } || printf 'PASS  无遗留旧人格词\n'
  grep -q 'PROTOCOL' "$f"                       && printf 'PASS  协议逆向轨道在位\n' || { printf 'FAIL  协议轨道缺失\n'; fails=$((fails+1)); }
  grep -q '网络作战面' "$f"                      && printf 'PASS  网络作战面在位\n'   || { printf 'FAIL  网络作战面缺失\n'; fails=$((fails+1)); }
  grep -q 'Portability' "$f"                    && printf 'PASS  可移植模块在位\n'   || { printf 'FAIL  可移植模块缺失\n'; fails=$((fails+1)); }
  line
  [ "$fails" -eq 0 ] && printf 'RESULT: ALL GREEN\n' || printf 'RESULT: %s 项未通过\n' "$fails"
  exit "$fails"
}

do_install() {
  local dest_base="${1:-$(detect_targets)}"
  local dest="$dest_base/agentbypass"
  mkdir -p "$dest"
  cp "$SKILL_SRC" "$dest/SKILL.md"
  printf '已安装: %s/SKILL.md\n' "$dest"
  printf '适用框架提示:\n'
  printf '  - Claude Code / OpenMinis 等目录约定框架: 重启会话自动加载\n'
  printf '  - Cursor / Windsurf / Cline: 将该文件内容加入 Rules / Custom Instructions\n'
  printf '  - ChatGPT / 网页 LLM: 将全文粘贴进 System Prompt 或自定义指令\n'
  do_verify "$dest/SKILL.md"
}

do_doctor() {
  line; printf 'environment doctor\n'; line
  printf 'OS        : %s\n' "$(uname -s 2>/dev/null) $(uname -m 2>/dev/null)"
  command -v python3 >/dev/null && printf 'python3   : %s\n' "$(python3 -V 2>&1)" || printf 'python3   : 缺失(建议安装)\n'
  command -v curl    >/dev/null && printf 'curl      : ok\n' || printf 'curl      : 缺失\n'
  command -v git     >/dev/null && printf 'git       : %s\n' "$(git --version 2>&1)" || printf 'git       : 缺失\n'
  command -v radare2 >/dev/null && printf 'radare2   : ok\n' || printf 'radare2   : 未安装(可选, REVERSE 轨道用)\n'
  command -v nmap    >/dev/null && printf 'nmap      : ok\n' || printf 'nmap      : 未安装(可选, NETWORK 轨道用)\n'
  for pm in apk apt dnf pacman brew choco scoop winget; do
    command -v "$pm" >/dev/null && { printf 'pkg-mgr   : %s\n' "$pm"; break; }
  done
  line
  printf '技能会在此环境自动按手牌选择工具链, 无需人工配置。\n'
}

case "${1:-verify}" in
  install) shift; do_install "${1:-}" ;;
  verify)  shift; do_verify "${1:-}" ;;
  doctor)  do_doctor ;;
  *) printf '用法: %s {install|verify|doctor}\n' "$0"; exit 1 ;;
esac
