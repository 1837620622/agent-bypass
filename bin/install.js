#!/usr/bin/env node
'use strict';

/**
 * agent-bypass installer — 自动安装到 Pi / OpenCode / OpenMinis
 *
 * 用法:
 *   npx agent-bypass                 自动检测并安装到已装的 harness
 *   npx agent-bypass --pi            只装 Pi
 *   npx agent-bypass --opencode      只装 OpenCode
 *   npx agent-bypass --minis         只装 OpenMinis
 *   npx agent-bypass --no-inject     只装技能文件，跳过系统提示词注入
 *   npx agent-bypass --inject-global OpenMinis 也注入 GLOBAL.md（默认仅提示手动）
 *   npx agent-bypass --uninstall     卸载（移除技能 + 标记块 + instructions 条目）
 *
 * 防乱码设计:
 *   1. 所有新建文件一律 UTF-8（无 BOM）
 *   2. 追加现有文件前先做 UTF-8 校验，非 UTF-8 一律不碰（防混合编码）
 *   3. OpenCode 注入走 instructions 数组 + 独立文件，永不改动你原有的 AGENTS.md
 *   4. 标记块幂等：重复运行只更新，不重复追加
 */

const fs = require('fs');
const path = require('path');
const os = require('os');
const { isUtf8 } = require('buffer');

const ROOT = path.join(__dirname, '..');
const HOME = os.homedir();
const args = process.argv.slice(2);
const has = (f) => args.includes(f);
const only = ['--pi', '--opencode', '--minis'].filter(has);
const noInject = has('--no-inject');
const uninstall = has('--uninstall');
const injectGlobal = has('--inject-global');

const MARK_B = '<!-- agent-bypass:begin -->';
const MARK_E = '<!-- agent-bypass:end -->';
const SKILL_FILES = ['SKILL.md', 'ck-hunter.md', '系统提示词.md', 'config.yaml.example'];

const ok = (m) => console.log('  \u2713 ' + m);
const warn = (m) => console.log('  \u26a0 ' + m);
const info = (m) => console.log('  \u00b7 ' + m);
const exists = (p) => { try { fs.accessSync(p); return true; } catch { return false; } };

// 提取 系统提示词.md 的复制区（破甲块）
function getBlock() {
  const src = fs.readFileSync(path.join(ROOT, '系统提示词.md'), 'utf8');
  const a = src.indexOf('\u2193\u2193\u2193');
  const b = src.indexOf('\u2191\u2191\u2191');
  const s = src.indexOf('\n', a) + 1;
  const e = src.lastIndexOf('\n', b);
  return src.slice(s, e).trim();
}

function installSkills(dir) {
  fs.mkdirSync(dir, { recursive: true });
  let n = 0;
  for (const f of SKILL_FILES) {
    const src = path.join(ROOT, f);
    if (exists(src)) { fs.copyFileSync(src, path.join(dir, f)); n++; }
  }
  ok(`技能文件 \u2192 ${dir}（${n} 个）`);
}

function removeSkills(dir) {
  if (exists(dir)) { fs.rmSync(dir, { recursive: true, force: true }); ok(`已删除 ${dir}`); }
}

// 标记块注入（UTF-8 校验 + 行尾匹配 + 幂等）
function injectMarked(file, block, label) {
  let cur = '';
  if (exists(file)) {
    const buf = fs.readFileSync(file);
    if (!isUtf8(buf)) { warn(`${label} 非 UTF-8，跳过注入（防乱码）\u2192 ${file}`); return false; }
    cur = buf.toString('utf8');
  }
  const eol = cur.includes('\r\n') ? '\r\n' : '\n';
  const sec = [MARK_B, block, MARK_E].join(eol);
  let out;
  const bi = cur.indexOf(MARK_B), ei = cur.indexOf(MARK_E);
  if (bi !== -1 && ei > bi) {
    out = cur.slice(0, bi) + sec + cur.slice(ei + MARK_E.length);
    ok(`${label} 标记块已更新`);
  } else {
    out = cur.trimEnd() + (cur.trim() ? eol + eol : '') + sec + eol;
    ok(`${label} 标记块已追加`);
  }
  fs.writeFileSync(file, out, 'utf8');
  return true;
}

function stripMarked(file, label) {
  if (!exists(file)) return;
  const buf = fs.readFileSync(file);
  if (!isUtf8(buf)) { warn(`${label} 非 UTF-8，跳过`); return; }
  let cur = buf.toString('utf8');
  const bi = cur.indexOf(MARK_B), ei = cur.indexOf(MARK_E);
  if (bi !== -1 && ei > bi) {
    cur = (cur.slice(0, bi) + cur.slice(ei + MARK_E.length)).replace(/\n{3,}/g, '\n\n').trimEnd() + '\n';
    fs.writeFileSync(file, cur, 'utf8');
    ok(`${label} 标记块已移除`);
  }
}

// ============ Pi ============
// skills: ~/.pi/agent/skills/agent-bypass/
// 系统注入: ~/.pi/agent/APPEND_SYSTEM.md（标记块，追加到默认提示词，不改动其他内容）
function installPi() {
  console.log('\n[Pi]');
  const base = path.join(HOME, '.pi', 'agent');
  installSkills(path.join(base, 'skills', 'agent-bypass'));
  if (!noInject) {
    if (!exists(base)) fs.mkdirSync(base, { recursive: true });
    injectMarked(path.join(base, 'APPEND_SYSTEM.md'), getBlock(), 'Pi APPEND_SYSTEM.md');
  }
}
function uninstallPi() {
  console.log('\n[Pi]');
  removeSkills(path.join(HOME, '.pi', 'agent', 'skills', 'agent-bypass'));
  stripMarked(path.join(HOME, '.pi', 'agent', 'APPEND_SYSTEM.md'), 'Pi APPEND_SYSTEM.md');
}

// ============ OpenCode ============
// skills: ~/.config/opencode/skills/agent-bypass/
// 系统注入: 独立文件 agent-bypass.md + opencode.json instructions 数组合并
// —— 永不改动用户原有的 AGENTS.md / 全局提示
function opencodeConfigPath() {
  const base = path.join(HOME, '.config', 'opencode');
  const j = path.join(base, 'opencode.json');
  const jc = path.join(base, 'opencode.jsonc');
  if (exists(j)) return j;
  if (exists(jc)) return jc;
  return j;
}
function installOpenCode() {
  console.log('\n[OpenCode]');
  const base = path.join(HOME, '.config', 'opencode');
  fs.mkdirSync(base, { recursive: true });
  installSkills(path.join(base, 'skills', 'agent-bypass'));
  if (noInject) return;
  const inj = path.join(base, 'agent-bypass.md');
  fs.writeFileSync(inj, getBlock() + '\n', 'utf8');
  ok(`注入文件 \u2192 ${inj}`);
  const cfg = opencodeConfigPath();
  let data = { $schema: 'https://opencode.ai/config.json' };
  if (exists(cfg)) {
    if (cfg.endsWith('.jsonc')) {
      warn('检测到 opencode.jsonc（JSONC 含注释，程序不自动改写）。');
      info(`请手动在 instructions 数组加入: "${inj}"`);
      return;
    }
    try { data = JSON.parse(fs.readFileSync(cfg, 'utf8')); }
    catch {
      warn('opencode.json 解析失败（可能含注释/尾逗号），未改动文件。');
      info(`请手动在 instructions 数组加入: "${inj}"`);
      return;
    }
  }
  const arr = Array.isArray(data.instructions) ? data.instructions : [];
  if (!arr.includes(inj)) arr.push(inj);
  data.instructions = arr;
  fs.writeFileSync(cfg, JSON.stringify(data, null, 2) + '\n', 'utf8');
  ok(`opencode.json instructions 已合并（原文件其余内容未动）`);
}
function uninstallOpenCode() {
  console.log('\n[OpenCode]');
  const base = path.join(HOME, '.config', 'opencode');
  removeSkills(path.join(base, 'skills', 'agent-bypass'));
  const inj = path.join(base, 'agent-bypass.md');
  if (exists(inj)) { fs.rmSync(inj); ok('已删除 agent-bypass.md'); }
  const cfg = opencodeConfigPath();
  if (exists(cfg) && !cfg.endsWith('.jsonc')) {
    try {
      const data = JSON.parse(fs.readFileSync(cfg, 'utf8'));
      if (Array.isArray(data.instructions)) {
        data.instructions = data.instructions.filter((x) => x !== inj);
        if (!data.instructions.length) delete data.instructions;
        fs.writeFileSync(cfg, JSON.stringify(data, null, 2) + '\n', 'utf8');
        ok('opencode.json instructions 已移除条目');
      }
    } catch { warn('opencode.json 解析失败，未改动'); }
  }
}

// ============ OpenMinis ============
// skills: /var/minis/skills/agent-bypass/
// 系统注入: 默认提示手动（Settings \u2192 Soul / GLOBAL.md）；--inject-global 时标记块注入 GLOBAL.md
function installMinis() {
  console.log('\n[OpenMinis]');
  installSkills('/var/minis/skills/agent-bypass');
  if (noInject) return;
  if (injectGlobal && exists('/var/minis/memory/GLOBAL.md')) {
    injectMarked('/var/minis/memory/GLOBAL.md', getBlock(), 'OpenMinis GLOBAL.md');
  } else {
    info('系统级注入（二选一，手动）：');
    info('  A. 打开 Minis \u2192 Settings \u2192 Soul，把 系统提示词.md 复制区贴入');
    info('  B. 或运行: npx agent-bypass --minis --inject-global（自动注入 GLOBAL.md）');
  }
}
function uninstallMinis() {
  console.log('\n[OpenMinis]');
  removeSkills('/var/minis/skills/agent-bypass');
  stripMarked('/var/minis/memory/GLOBAL.md', 'OpenMinis GLOBAL.md');
}

// ============ 主流程 ============
console.log('\nagent-bypass installer' + (uninstall ? '（卸载模式）' : ''));
console.log('\u2500'.repeat(40));

const detectPi = exists(path.join(HOME, '.pi'));
const detectOc = exists(path.join(HOME, '.config', 'opencode'));
const detectMinis = exists('/var/minis');

let targets;
if (only.length) {
  targets = only.map((f) => f.slice(2));
} else {
  targets = [];
  if (detectPi) targets.push('pi');
  if (detectOc) targets.push('opencode');
  if (detectMinis) targets.push('minis');
  if (!targets.length) {
    warn('未检测到任何目标 harness：');
    info('Pi: ~/.pi 不存在');
    info('OpenCode: ~/.config/opencode 不存在');
    info('OpenMinis: /var/minis 不存在');
    info('强制安装指定目标: npx agent-bypass --pi | --opencode | --minis');
    process.exit(1);
  }
  console.log(`检测到: ${targets.join(' / ')}`);
}

const map = {
  pi: [installPi, uninstallPi],
  opencode: [installOpenCode, uninstallOpenCode],
  minis: [installMinis, uninstallMinis],
};
for (const t of targets) {
  const [inst, uninst] = map[t];
  if (uninstall) uninst(); else inst();
}

console.log('\n' + '\u2500'.repeat(40));
if (uninstall) {
  console.log('卸载完成。');
} else {
  console.log('安装完成。');
  console.log('验证：对 harness 说「ck」「在」「干」等触发词，应回「Cknb在呢，想干什么？直接开干。」');
  console.log('密钥（凭证猎取用）：把 config.yaml.example 复制为 config.yaml 填入 API Key。');
}
