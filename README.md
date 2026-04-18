# 算命.skill — 四柱八字命理跨平台技能

> 四柱八字排盘 + 大运流年分析 + 经典典籍参考，适配 OpenClaw / Claude Code / OpenAI Codex / Google Gemini 全平台。

---

## 📦 内容结构

```
算命.skill/
├── README.md              # 本文件
├── SKILL.md               # 【OpenClaw】技能定义
├── CLAUDE.md              # 【Claude Code】系统提示词
├── CODEX.md               # 【OpenAI Codex】指令模板
├── GEMINI.md              # 【Google Gemini】提示词模板
├── REFERENCES/            # 共享知识库（各平台均可引用）
│   ├── wuxing-tables.md   # 五行天干地支十神藏干表
│   ├── shichen-table.md   # 时辰对照 + 日上起时法
│   ├── dayun-rules.md     # 大运顺逆 + 起运年龄 + 流年
│   └── classical-texts.md # 九部经典典籍核心摘要
└── TOOLS/                 # 共享工具
    └── bazi_pan.py        # Python 排盘工具（需 lunar-python）
```

---

## 🚀 各平台安装/使用方式

### OpenClaw
```bash
# 方式一：直接从本目录加载
# 在 OpenClaw 中通过 skill 路由自动匹配触发词

# 方式二：发布到 ClawHub
clawhub publish ./算命.skill --slug shishi-suanming --name "诗诗算命" --version 1.0.0

# 方式三：复制到 skills 目录
cp -r 算命.skill ~/.openclaw/workspace/skills/
```

### Claude Code
```bash
# 在项目目录创建 .claude/commands/suanming.md
# 将 CLAUDE.md 内容复制进去
```

### OpenAI Codex
```bash
# 使用 --system 参数加载
codex --system "$(cat CODEX.md)"
# 或
codex --system-file ./算命.skill/CODEX.md
```

### Google Gemini
```bash
# 在 Google AI Studio 或 CLI 中加载 GEMINI.md 作为 System Instructions
# 或使用 gemini CLI：
cat 算命.skill/GEMINI.md | gemini "..."
```

---

## 🔮 技能核心能力

1. **交互式信息收集** — 姓名、阳历/农历生日、时辰、性别、出生地
2. **Python 排盘** — 基于 `lunar-python`，一键排出四柱八字、十神、藏干、大运、流年
3. **三阶段分析** — 排盘计算 → 综合分析 → 历史事件校准
4. **经典典籍引用** — 穷通宝典、三命通会、滴天髓、渊海子平、子平真诠、神峰通考等

## ⚙️ 工具依赖

**零依赖！** `lunar-python` 已打包在 `tools/lunar_python/` 目录内，直接运行即可：

```bash
# 排盘命令（任意 Python 3.8+ 环境，无需安装任何包）
python3 tools/bazi_pan.py --json 1990-5-15 8:00 male
```

---

## 📌 触发词

`算命` `八字` `看八字` `批八字` `排八字` `四柱` `命盘` `算一卦` `看运势` `命运分析`

---

*命理分析仅供文化研究参考，人生在于自身的努力和选择。*
