"""文本表格和 JSON 输出。"""

import json


def to_json(result, *, pretty=True):
    return json.dumps(result, ensure_ascii=False, indent=2 if pretty else None)


def format_text(r):
    p = r['四柱']
    td = r['天干地支']
    ss = r['十神']
    cg = r['藏干']
    wx = r['五行']
    ny = r['纳音']
    dy = r['大运']
    ln = r['流年']
    ds = r['日主强弱']
    meta = r['原始数据']
    notes = r.get('注释', {})

    day_gan = td['日']['干']
    lines = []
    lines.append('=' * 54)
    lines.append('   四柱八字排盘（plus 版）')
    lines.append('=' * 54)
    lines.append(f"四柱：{p['年柱']} · {p['月柱']} · {p['日柱']} · {p['时柱']}")
    lines.append(f"阳历：{meta['阳历日期']} {meta['出生时辰']}  |  性别：{meta['性别']}  |  生肖：{r['生肖']}")
    if notes:
        note_strs = []
        for k, v in notes.items():
            note_strs.append(f"{k}={v}")
        lines.append('注释：' + '  '.join(note_strs))
    lines.append('')

    lines.append('【天干地支】')
    for col in ('年', '月', '日', '时'):
        c = td[col]
        lines.append(f"  {col}柱：天干[{c['干']}({c['干阴阳']})] 地支[{c['支']}]")

    lines.append('')
    lines.append(f'【十神】以日干[{day_gan}]为基准')
    for col, g_key, z_key in (('年', '年干', '年支'), ('月', '月干', '月支'), ('日', '日干', '日支'), ('时', '时干', '时支')):
        lines.append(f"  {col}柱：干[{ss[g_key] or '—'}] 支[{ss[z_key] or '—'}]")

    lines.append('')
    lines.append('【藏干】')
    for col in ('年支', '月支', '日支', '时支'):
        c = cg[col]
        lines.append(f"  {col}：本气[{c['本气'] or '—'}] 中气[{c['中气'] or '—'}] 余气[{c['余气'] or '—'}]")

    lines.append('')
    lines.append(f"【五行统计】日主五行={ds['日主五行']}")
    lines.append('  ' + '  '.join(f'{k}={v}' for k, v in wx.items()))

    lines.append('')
    lines.append('【日主强弱】')
    dl = ds['得令']
    lines.append(f"  得令：{'✓' if dl['判定'] else '✗'} ({dl['说明']})  分={dl['分数']}")
    lines.append(f"  得地：分={ds['得地']['分数']}  通根数={len(ds['得地']['通根'])}")
    lines.append(f"  得势：分={ds['得势']['分数']}  同党数={len(ds['得势']['同党'])}")
    lines.append(f"  总分={ds['总分']}  →  {ds['强弱判定']}   调候：{ds['调候倾向']}")

    lines.append('')
    lines.append(f"【纳音】年[{ny['年柱']}] 月[{ny['月柱']}] 日[{ny['日柱']}] 时[{ny['时柱']}]")
    lines.append(f"【节气】前[{r['节气']['前一节']}]  后[{r['节气']['后一节']}]")

    lines.append('')
    lines.append('─' * 54)
    lines.append(f"【大运】{dy['方向']}  起运={dy['起运年龄']}岁（约{dy['起运所需']}后）  起运日期≈{dy['起运日期']}")
    if dy.get('小运'):
        lines.append(f"  小运：{dy['小运']['起止年龄']}（{dy['小运']['起止年份']}）— {dy['小运']['说明']}")
    lines.append(f"  {'序号':<4}{'年龄':<14}{'年份':<14}{'干支':<6}")
    for d in dy['大运列表']:
        lines.append(f"  {d['序号']:<4}{d['起止年龄']:<14}{d['起止年份']:<14}{d['干支']:<6}")

    lines.append('')
    lines.append('─' * 54)
    lines.append('【近五年流年】')
    for y in ln:
        mark = ' ◀ 今年' if y['今年'] else ''
        lines.append(f"  {y['年份']}  {y['干支']}  ({y['五行']}){mark}")

    lines.append('')
    lines.append('=' * 54)
    lines.append('命理分析仅供参考，人生在于自身的努力和选择。')
    return '\n'.join(lines)
