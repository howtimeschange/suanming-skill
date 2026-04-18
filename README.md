# 算命.skill

> 四柱八字命理跨平台 skill。交互式收集生辰，调用 Python 排盘工具输出结构化 JSON，再由模型按《穷通宝典》《滴天髓》《渊海子平》《子平真诠》等经典做专业分析。
> 适配 OpenClaw / Claude Code / OpenAI Codex / Google Gemini，**零依赖**直接运行。

支持阳历/农历（含闰月）、真太阳时校正、夜子时进位、中文时辰与模糊时段（早上/中午/晚上）、日主三维强弱判定、十步大运、避立春陷阱的流年。

---

## 功能

- **排盘**：根据阳历或农历生辰推出年/月/日/时四柱，含藏干（本/中/余气）、十神、纳音、五行统计、生肖、节气所在
- **日主强弱**：三维打分（得令 / 得地 / 得势），分「极旺 / 身旺 / 身弱 / 极弱」四档，并给出调候倾向
- **大运**：按阴阳年 + 性别顺逆排列十步，含起运年龄、起运日期、每步起止年份
- **流年**：近五年干支与五行，按出生月日取年干支，避开立春前后误判
- **真太阳时**：按 `--city`（内置 41 个中国主要城市）或 `--longitude` 经度校正出生时间
- **夜子时**：23:00–24:00 自动进位次日日柱，时柱仍落子时
- **输入宽容**：性别「男/女/male/female」都认，时辰「8:00 / 辰时 / 早上 / 晚上」都认，日期「1990-5-15 / 1990年5月15日」都认
- **输出灵活**：默认带表格的文本报告，`--json` 输出结构化 JSON 便于程序处理
- **经典论命**：模型按《穷通宝典》《滴天髓》《渊海子平》《子平真诠》等九部经典做日主 / 十神 / 五行 / 格局 / 大运 / 流年综合分析，并含「历史事件校准」让分析可被反馈修正

---

## 目录结构

```
算命.skill/
├── SKILL.md                 # ★ 唯一权威源（含 YAML frontmatter）
├── CLAUDE.md / CODEX.md / GEMINI.md / OPENCLAW.md   # 四平台薄入口
├── README.md  LICENSE
├── references/              # 知识库（全小写）
│   ├── wuxing-tables.md
│   ├── shichen-table.md
│   ├── changsheng-table.md  # 新增
│   ├── dayun-rules.md
│   ├── shensha-common.md    # 新增
│   └── classical-texts.md
├── tools/
│   ├── bazi_pan.py          # CLI 薄入口
│   ├── bazi/                # 模块化排盘核心
│   │   ├── calendar.py      # 阳/农历、真太阳时、夜子时、模糊时辰
│   │   ├── pillars.py       # 四柱、藏干、十神、纳音
│   │   ├── strength.py      # 三维打分日主强弱
│   │   ├── fortune.py       # 大运、流年（避立春陷阱）
│   │   ├── formatting.py    # 文本/JSON 输出
│   │   ├── cli.py           # argparse + 错误处理
│   │   └── constants.py
│   └── lunar_python/        # 内嵌（Apache-2.0），零依赖
└── tests/
    ├── test_bazi.py
    └── fixtures/            # 毛蒋王 + 夜子时 + 立春 + 闰月
```

---

## 快速开始

```bash
git clone https://github.com/howtimeschange/suanming-skill.git
cd suanming-skill

# 阳历
python3 tools/bazi_pan.py 1990-5-15 8:00 男

# JSON
python3 tools/bazi_pan.py --json 1990-5-15 8:00 男

# 农历
python3 tools/bazi_pan.py --lunar 1990-4-21 辰时 女

# 农历闰月
python3 tools/bazi_pan.py --lunar --leap 2020-4-15 早上 male

# 真太阳时（按城市）
python3 tools/bazi_pan.py --city 北京 1990-5-15 8:00 男

# 真太阳时（按经度）
python3 tools/bazi_pan.py --longitude 116.4 1990-5-15 8:00 男

# 夜子时（自动进位）
python3 tools/bazi_pan.py 1990-5-15 23:30 male

# 帮助 / 版本
python3 tools/bazi_pan.py --help
python3 tools/bazi_pan.py --version
```

支持 Python 3.8+；除 Python 标准库外**无其他依赖**。

---

## 跑测试

```bash
python3 tests/test_bazi.py
# 期望输出：6/6 通过
```

---

## 各平台安装

### Claude Code

```bash
cp -r suanming-skill ~/.claude/skills/suanming
```

重启 Claude Code，输入 `/suanming` 或"算命 / 看八字 / 批八字"即触发。

### OpenClaw

```bash
cp -r suanming-skill ~/.openclaw/workspace/skills/suanming
```

触发词：算命 / 八字 / 看八字 / 批八字 / 排八字 / 四柱 / 命盘 / 算一卦 / 看运势 / 命运分析。

### OpenAI Codex

```bash
codex --system-file ./SKILL.md
```

### Google Gemini

将 `SKILL.md` 全文粘贴到 System Instructions。

---

## 设计原则

1. **计算与解释分离**：Python 做确定性排盘，LLM 仅在第三阶段做经典论命。
2. **零依赖**：`tools/lunar_python/` 完整内嵌，避免 `pip install`。
3. **单一权威源**：所有流程细节只在 `SKILL.md`，平台入口仅 ≤50 行。
4. **可证伪**：第三阶段必有"历史事件校准"，让分析可被反馈修正。
5. **可回归**：`tests/` 提供 fixture，边界条件不会被未来改动悄悄破坏。

---

## 致谢

- 排盘内核：[6tail/lunar-python](https://github.com/6tail/lunar-python)（Apache-2.0，已内嵌）

---

*命理分析仅供文化研究参考，人生在于自身的努力和选择。*
