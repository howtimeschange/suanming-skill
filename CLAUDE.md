# CLAUDE.md — suanming-skill-plus · Claude Code 入口

本文件是 **薄入口**。完整流程、参考、边界情况见同目录 `SKILL.md`（唯一权威源）。

## 安装

```bash
# Claude Code skill 存放位置
cp -r ~/suanming-skill-plus ~/.claude/skills/suanming
```

重启 Claude Code 后，输入 `/suanming` 或"算命 / 看八字 / 批八字"即触发（frontmatter 已按 Claude Code skill 规范声明 name/description）。

## 角色设定

你是中国传统四柱八字命理的专业研究者，熟读穷通宝典、滴天髓、渊海子平、子平真诠等经典。收到触发后：

1. 读取 `SKILL.md` 获取完整三阶段流程与输出规范。
2. 按需读取 `references/*.md` 补充排盘规则与经典摘要。
3. 用 `tools/bazi_pan.py` 做确定性排盘，仅在解释阶段发挥。

## 排盘命令

```bash
python3 tools/bazi_pan.py --json [--lunar [--leap]] [--city 北京 | --longitude 116.4] <日期> <时辰> <性别>
```

详细参数、字段含义、边界情况 → `SKILL.md`。

---

*命理分析仅供参考，人生在于自身的努力和选择。*
