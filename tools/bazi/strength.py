"""日主强弱评估：得令（月令长生）+ 得地（通根）+ 得势（党印）。四档：极旺/身旺/身弱/极弱。"""

from .constants import (
    CANGGAN, GAN_WUXING,
    get_changsheng_stage, get_shi_shen, SHISHEN_CATEGORY,
    DELING_SCORE, TONGGEN_WEIGHT,
)

# 阈值按子平日主强弱论取四档
TIER_THRESHOLDS = [
    (28, '极旺'),
    (16, '身旺'),
    (8, '身弱'),
    (0, '极弱'),
]

# 地支藏干"党（比劫）/印（印绶）"的权重
ALLY_WEIGHT = {'本气': 2.0, '中气': 1.0, '余气': 0.5}


def assess_strength(pillars):
    """三维打分 → 四档。"""
    td = pillars['天干地支']
    day_gan = td['日']['干']
    month_zhi = td['月']['支']
    stems = [td[c]['干'] for c in ('年', '月', '时')]           # 日干不算自己
    branches = [td[c]['支'] for c in ('年', '月', '日', '时')]
    dr_wx = GAN_WUXING[day_gan]

    # 1. 得令：月支对日干的十二长生位
    stage = get_changsheng_stage(day_gan, month_zhi)
    deling_score = DELING_SCORE.get(stage, 0)
    deling_ok = stage in ('长生', '临官', '帝旺')

    # 2. 得地（通根）：四支藏干里与日干同五行的本/中/余气
    dedi_score = 0.0
    roots = []
    for zhi in branches:
        for kind, gan in CANGGAN.get(zhi, []):
            if GAN_WUXING[gan] == dr_wx:
                dedi_score += TONGGEN_WEIGHT[kind]
                roots.append({'地支': zhi, '藏干': gan, '气': kind, '权': TONGGEN_WEIGHT[kind]})

    # 3. 得势：其他三干 + 四支藏干中为比劫/印绶的加权
    deshi_score = 0.0
    allies = []
    for g in stems:
        shi = get_shi_shen(day_gan, g)
        if SHISHEN_CATEGORY.get(shi) in ('比劫', '印绶'):
            deshi_score += 2.0
            allies.append({'位': '干', '干': g, '十神': shi, '权': 2.0})
    for zhi in branches:
        for kind, gan in CANGGAN.get(zhi, []):
            shi = get_shi_shen(day_gan, gan)
            if SHISHEN_CATEGORY.get(shi) in ('比劫', '印绶'):
                w = ALLY_WEIGHT[kind]
                deshi_score += w
                allies.append({'位': zhi, '藏干': gan, '气': kind, '十神': shi, '权': w})

    total = round(deling_score + dedi_score + deshi_score, 2)
    tier = next(name for th, name in TIER_THRESHOLDS if total >= th)
    tendency = '宜抑（食伤/财星/官杀泄秀）' if tier in ('极旺', '身旺') else '宜扶（比劫/印绶生助）'

    return {
        '日主': day_gan,
        '日主五行': dr_wx,
        '月支': month_zhi,
        '月令长生位': stage,
        '得令': {'判定': deling_ok, '分数': deling_score, '说明': f'{day_gan}在{month_zhi}月为{stage}'},
        '得地': {'分数': round(dedi_score, 2), '通根': roots},
        '得势': {'分数': round(deshi_score, 2), '同党': allies},
        '总分': total,
        '强弱判定': tier,
        '调候倾向': tendency,
    }
