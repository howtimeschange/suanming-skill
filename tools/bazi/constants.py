"""常量表：天干地支、藏干、十二长生、五行关系、十神映射。"""

TIANGAN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
DIZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']


def next_gan(g, n=1):
    return TIANGAN[(TIANGAN.index(g) + n) % 10]


def prev_gan(g, n=1):
    return TIANGAN[(TIANGAN.index(g) - n) % 10]


def next_zhi(z, n=1):
    return DIZHI[(DIZHI.index(z) + n) % 12]


def prev_zhi(z, n=1):
    return DIZHI[(DIZHI.index(z) - n) % 12]

GAN_WUXING = {
    '甲': '木', '乙': '木', '丙': '火', '丁': '火',
    '戊': '土', '己': '土', '庚': '金', '辛': '金',
    '壬': '水', '癸': '水',
}
ZHI_WUXING = {
    '子': '水', '丑': '土', '寅': '木', '卯': '木',
    '辰': '土', '巳': '火', '午': '火', '未': '土',
    '申': '金', '酉': '金', '戌': '土', '亥': '水',
}
GAN_YIN_YANG = {g: ('阳' if i % 2 == 0 else '阴') for i, g in enumerate(TIANGAN)}

# 藏干（本气/中气/余气）
CANGGAN = {
    '子': [('本气', '癸')],
    '丑': [('本气', '己'), ('中气', '癸'), ('余气', '辛')],
    '寅': [('本气', '甲'), ('中气', '丙'), ('余气', '戊')],
    '卯': [('本气', '乙')],
    '辰': [('本气', '戊'), ('中气', '乙'), ('余气', '癸')],
    '巳': [('本气', '丙'), ('中气', '庚'), ('余气', '戊')],
    '午': [('本气', '丁'), ('中气', '己')],
    '未': [('本气', '己'), ('中气', '丁'), ('余气', '乙')],
    '申': [('本气', '庚'), ('中气', '壬'), ('余气', '戊')],
    '酉': [('本气', '辛')],
    '戌': [('本气', '戊'), ('中气', '辛'), ('余气', '丁')],
    '亥': [('本气', '壬'), ('中气', '甲')],
}

# 十二长生阶段
CHANG_SHENG_STAGES = ['长生', '沐浴', '冠带', '临官', '帝旺', '衰', '病', '死', '墓', '绝', '胎', '养']

# 各天干的"长生位"起始地支（阳干顺行、阴干逆行）
CHANG_SHENG_START = {
    '甲': '亥', '丙': '寅', '戊': '寅', '庚': '巳', '壬': '申',
    '乙': '午', '丁': '酉', '己': '酉', '辛': '子', '癸': '卯',
}

# 得令分数：日干 vs 月支所处十二长生位
DELING_SCORE = {
    '帝旺': 10, '临官': 9, '长生': 8,
    '冠带': 6, '沐浴': 4, '养': 3,
    '衰': 3, '墓': 3,
    '病': 2, '死': 1, '绝': 1, '胎': 2,
}

# 得地（通根）权重
TONGGEN_WEIGHT = {'本气': 3.0, '中气': 1.5, '余气': 1.0}

# 五行相生相克：生者为印、同者为比劫
WUXING_SHENG = {'木': '火', '火': '土', '土': '金', '金': '水', '水': '木'}
WUXING_KE = {'木': '土', '土': '水', '水': '火', '火': '金', '金': '木'}


def get_shi_shen(day_gan, other_gan):
    """根据日干求 other_gan 的十神（比肩/劫财/食神/伤官/偏财/正财/七杀/正官/偏印/正印）。"""
    if other_gan is None:
        return None
    dr_wx = GAN_WUXING[day_gan]
    o_wx = GAN_WUXING[other_gan]
    dr_yy = GAN_YIN_YANG[day_gan]
    o_yy = GAN_YIN_YANG[other_gan]
    same_yy = dr_yy == o_yy
    if o_wx == dr_wx:
        return '比肩' if same_yy else '劫财'
    if WUXING_SHENG[dr_wx] == o_wx:
        return '食神' if same_yy else '伤官'
    if WUXING_KE[dr_wx] == o_wx:
        return '偏财' if same_yy else '正财'
    if WUXING_KE[o_wx] == dr_wx:
        return '七杀' if same_yy else '正官'
    if WUXING_SHENG[o_wx] == dr_wx:
        return '偏印' if same_yy else '正印'
    return None


SHISHEN_CATEGORY = {
    '比肩': '比劫', '劫财': '比劫',
    '正印': '印绶', '偏印': '印绶',
    '食神': '食伤', '伤官': '食伤',
    '正财': '财星', '偏财': '财星',
    '正官': '官杀', '七杀': '官杀',
}


def get_changsheng_stage(day_gan, zhi):
    """求 day_gan 在 zhi 的十二长生位阶段。"""
    start_zhi = CHANG_SHENG_START[day_gan]
    start_idx = DIZHI.index(start_zhi)
    zhi_idx = DIZHI.index(zhi)
    if GAN_YIN_YANG[day_gan] == '阳':
        offset = (zhi_idx - start_idx) % 12
    else:
        offset = (start_idx - zhi_idx) % 12
    return CHANG_SHENG_STAGES[offset]
