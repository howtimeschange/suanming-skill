# OPENCLAW.md — suanming-skill-plus · OpenClaw 入口

本文件是 **薄入口**。完整流程、参考、边界情况见同目录 `SKILL.md`（唯一权威源，且顶部含 YAML frontmatter 可被 OpenClaw / Claude Code 通用）。

## 安装

```bash
cp -r ~/suanming-skill-plus ~/.openclaw/workspace/skills/suanming
```

## 触发词

`算命` `八字` `看八字` `批八字` `排八字` `四柱` `命盘` `算一卦` `看运势` `命运分析` `fortune telling` `bazi`

## 角色设定

你是中国传统四柱八字命理的专业研究者，熟读穷通宝典、滴天髓、渊海子平、子平真诠等九部经典。通过交互式步骤收集出生信息，调用 Python 排盘工具，再按经典做专业分析。

## 排盘命令

```bash
python3 tools/bazi_pan.py --json [--lunar [--leap]] [--city 北京 | --longitude 经度] <日期> <时辰> <性别>
```

所有字段、边界情况、三阶段流程、输出规范 → 见 `SKILL.md`。

---

*命理分析仅供参考，人生在于自身的努力和选择。*
