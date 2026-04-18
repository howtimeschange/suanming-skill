# 算命.skill

> 四柱八字命理跨平台 skill。交互式收集生辰，调用 Python 排盘工具输出结构化 JSON，再由模型按《穷通宝典》《滴天髓》《渊海子平》《子平真诠》等经典做专业分析。
> 适配 OpenClaw / Claude Code / OpenAI Codex / Google Gemini，**零依赖**直接运行。

支持阳历/农历（含闰月）、真太阳时校正、夜子时进位、中文时辰与模糊时段（早上/中午/晚上）、日主三维强弱判定、十步大运、避立春陷阱的流年。

---

## 本次更新（v1.1.0）修复 14 项

| # | 问题 | 修复 |
|---|------|------|
| 1 | 阳历输入被 `lunar.Lunar.fromYmdHms` 当农历解析，**所有四柱都错** | 改为 `lunar.Solar.fromYmdHms(...).getLunar()`；`--lunar` 才走农历构造 |
| 2 | 夜子时（23:00–24:00）只在文档提及，CLI 未处理 | 自动进位次日日柱，时柱保留子时，JSON `注释.夜子时=True` |
| 3 | 不支持真太阳时 | 新增 `--longitude` 和 `--city`（内置 41 城经度表） |
| 4 | 不支持农历输入 | 新增 `--lunar` / `--leap` 双标志 |
| 5 | 性别只接受 `male/female`，文档却写"男/女" | 中文/英文/M/F 全收 |
| 6 | 模板大小写 `REFERENCES/` 与磁盘 `references/` 不一致 | 统一全小写 |
| 7 | 硬编码 `~/.openclaw/...` 与 `.venv/bin/python3` | 改为相对路径 + 系统 `python3` |
| 8 | CLAUDE/CODEX/GEMINI 三份内容 90% 重复 | 重构为单一权威源 `SKILL.md` + 四份 ≤50 行薄入口 |
| 9 | 流年用固定 7 月 1 日取干支，立春前后会错 | 按出生月日在目标年取 Lunar 年干支 |
| 10 | 日主强弱过粗 | 三维打分：得令（月令长生）+ 得地（通根本/中/余气加权）+ 得势（党印含藏干），四档判定 |
| 11 | 时辰无法模糊输入 | 支持 `子丑寅卯…亥` + `早上 上午 中午 下午 傍晚 晚上 夜里 深夜` |
| 12 | 无测试基准 | `tests/test_bazi.py` + 6 fixture（含立春/夜子时/闰月） |
| 13 | SKILL.md 缺 YAML frontmatter，Claude Code 可能识别失败 | 顶部加 `name` + `description` |
| 14 | CLI 错误用法直接 stack trace | argparse + 顶层 try/except + 友好错误提示 |

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
