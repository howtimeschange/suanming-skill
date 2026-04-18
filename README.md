# 算命.skill — 四柱八字命理跨平台技能

> 四柱八字排盘 + 大运流年分析 + 经典典籍参考，适配 OpenClaw / Claude Code / OpenAI Codex / Google Gemini 全平台。**零依赖**，直接运行。

---

## 📦 内容结构

```
算命.skill/
├── README.md              # 本文件
├── SKILL.md               # 【OpenClaw】技能定义（触发词 + 完整流程）
├── CLAUDE.md              # 【Claude Code】自定义命令（/suanming）
├── CODEX.md               # 【OpenAI Codex】指令模板
├── GEMINI.md              # 【Google Gemini】提示词模板
├── REFERENCES/            # 共享知识库
│   ├── wuxing-tables.md   # 五行天干地支、十神、藏干表
│   ├── shichen-table.md   # 时辰对照、日上起时法
│   ├── dayun-rules.md     # 大运顺逆、起运年龄、流年规则
│   └── classical-texts.md # 九部经典典籍核心摘要
└── TOOLS/
    ├── bazi_pan.py        # Python 排盘工具
    └── lunar_python/      # 内嵌 lunar-python（已打包，零依赖）
```

---

## ⚙️ 快速开始（排盘验证）

```bash
# 克隆后无需安装任何依赖，直接运行
python3 tools/bazi_pan.py --json 1990-5-15 8:00 male
```

支持 Python 3.8+。

---

## 🚀 各平台安装方式

### OpenClaw

```bash
# 复制到 skills 目录，触发词自动生效
cp -r 算命.skill ~/.openclaw/workspace/skills/
```

说出触发词（"算命"、"看八字"等）即可自动调用。

---

### Claude Code

**方式一：复制到 skills 目录（推荐）**
```bash
cp -r 算命.skill ~/.claude/skills/suanming
```

然后在 Claude Code 中输入 `/suanming` 即可开始分析。

---

### OpenAI Codex

```bash
# 直接用 --system-file 指定提示词文件
codex --system-file ./算命.skill/CODEX.md
```

每次启动时指定即可，无需额外安装。

---

### Google Gemini

在 Google AI Studio 或 Gemini CLI 中，将 `GEMINI.md` 的全部内容复制到 **System Instructions** 框中，加载后每次对话自动生效。

---

## 🔮 技能核心能力

1. **交互式信息收集** — 姓名、阳历/农历生日、时辰、性别、出生地
2. **Python 排盘** — 一键输出四柱八字、十神、藏干、大运、流年（JSON格式）
3. **三阶段分析** — 信息收集 → 排盘计算 → 综合分析（含历史事件校准）
4. **经典典籍引用** — 穷通宝典调候用神、滴天髓旺衰、子平真诠格局论

---

## 📌 触发词

`算命` `八字` `看八字` `批八字` `排八字` `四柱` `命盘` `算一卦` `看运势` `命运分析`

---

*命理分析仅供文化研究参考，人生在于自身的努力和选择。*
