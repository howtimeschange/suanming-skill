"""大运 + 流年：直接用 lunar_python 内置 Yun/DaYun/LiuNian，保证与经典排法一致。

流年按"出生月日"在各年取 Lunar → 年干支，避开立春陷阱（bug #9）。
"""

import sys
import os
from datetime import datetime

_TOOLS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _TOOLS_DIR not in sys.path:
    sys.path.insert(0, _TOOLS_DIR)
import lunar_python as lp

from .constants import GAN_WUXING, ZHI_WUXING, next_gan, next_zhi, prev_gan, prev_zhi


def build_dayun(birth):
    ec = birth.lunar.getEightChar()
    yun = ec.getYun(birth.gender_code)
    dayuns = yun.getDaYun()
    forward = yun.isForward()
    start_solar = yun.getStartSolar()

    items = []
    for d in dayuns[1:]:  # dayuns[0] 是起运前小运
        gz = d.getGanZhi()
        items.append({
            '序号': d.getIndex(),
            '起止年份': f"{d.getStartYear()}-{d.getEndYear()}",
            '起止年龄': f"{d.getStartAge()}-{d.getEndAge()}岁",
            '干支': gz,
            '天干': gz[0],
            '地支': gz[1],
        })
    # lunar_python 默认给 9 步，按月柱顺/逆补到 10 步以匹配传统排法
    if items:
        last = items[-1]
        last_age_end = int(last['起止年龄'].split('-')[1].rstrip('岁'))
        last_year_end = int(last['起止年份'].split('-')[1])
        g, z = last['天干'], last['地支']
        ng = next_gan(g) if forward else prev_gan(g)
        nz = next_zhi(z) if forward else prev_zhi(z)
        items.append({
            '序号': len(items) + 1 if items[0]['序号'] == 1 else last['序号'] + 1,
            '起止年份': f"{last_year_end + 1}-{last_year_end + 10}",
            '起止年龄': f"{last_age_end + 1}-{last_age_end + 10}岁",
            '干支': ng + nz,
            '天干': ng,
            '地支': nz,
        })

    pre = dayuns[0] if dayuns else None
    xiaoyun = None
    if pre is not None:
        xiaoyun = {
            '起止年龄': f'{pre.getStartAge()}-{pre.getEndAge()}岁',
            '起止年份': f'{pre.getStartYear()}-{pre.getEndYear()}',
            '说明': '未交大运，按月柱参看小运',
        }

    return {
        '方向': '顺排' if forward else '逆排',
        '起运所需': f'{yun.getStartYear()}年{yun.getStartMonth()}月{yun.getStartDay()}天',
        '起运日期': start_solar.toYmd() if start_solar else None,
        '起运年龄': dayuns[1].getStartAge() if len(dayuns) > 1 else None,
        '大运列表': items,
        '小运': xiaoyun,
    }


def build_liunian(birth, years_before=2, years_after=2):
    """按出生月日在每年的 Lunar 年干支；避开立春陷阱。"""
    solar = birth.solar
    today_year = datetime.now().year
    b_month, b_day = solar.getMonth(), solar.getDay()

    result = []
    for y in range(today_year - years_before, today_year + years_after + 1):
        try:
            s = lp.Solar.fromYmd(y, b_month, b_day)
        except Exception:
            s = lp.Solar.fromYmd(y, b_month, 28)
        gz = s.getLunar().getYearInGanZhi()
        gan, zhi = gz[0], gz[1]
        result.append({
            '年份': y,
            '干支': gz,
            '天干': gan,
            '地支': zhi,
            '五行': GAN_WUXING[gan] + ZHI_WUXING[zhi],
            '今年': y == today_year,
        })
    return result
