"""从 BirthInfo 构建四柱、藏干、十神、纳音。"""

from .constants import (
    CANGGAN, GAN_WUXING, ZHI_WUXING, GAN_YIN_YANG,
    get_shi_shen,
)


def _canggan_dict(zhi):
    items = CANGGAN.get(zhi, [])
    d = {'本气': None, '中气': None, '余气': None}
    for kind, gan in items:
        d[kind] = f"{gan}{GAN_WUXING[gan]}"
    return d


def build_pillars(birth):
    """返回排盘 dict（四柱/天干地支/十神/藏干/五行统计/纳音/节气/生肖）。"""
    lunar = birth.lunar
    ec = lunar.getEightChar()

    year_gz = ec.getYear()
    month_gz = ec.getMonth()
    day_gz = ec.getDay()
    time_gz = ec.getTime()

    year_gan, year_zhi = year_gz[0], year_gz[1]
    month_gan, month_zhi = month_gz[0], month_gz[1]
    day_gan, day_zhi = day_gz[0], day_gz[1]
    time_gan, time_zhi = time_gz[0], time_gz[1]

    # 十神（天干用 get_shi_shen 自算，地支用藏干本气）
    def zhi_shi_shen(zhi):
        bengi = next((g for k, g in CANGGAN.get(zhi, []) if k == '本气'), None)
        return get_shi_shen(day_gan, bengi) if bengi else None

    # 五行统计（天干 + 地支本气 + 中气 + 余气，权重 3/1.5/1）
    wx_cnt = {'金': 0, '木': 0, '水': 0, '火': 0, '土': 0}
    for g in (year_gan, month_gan, day_gan, time_gan):
        wx_cnt[GAN_WUXING[g]] += 1
    for z in (year_zhi, month_zhi, day_zhi, time_zhi):
        wx_cnt[ZHI_WUXING[z]] += 1
    # 便于 JSON 查看

    return {
        '四柱': {'年柱': year_gz, '月柱': month_gz, '日柱': day_gz, '时柱': time_gz},
        '天干地支': {
            '年': {'干': year_gan, '支': year_zhi, '干阴阳': GAN_YIN_YANG[year_gan]},
            '月': {'干': month_gan, '支': month_zhi, '干阴阳': GAN_YIN_YANG[month_gan]},
            '日': {'干': day_gan, '支': day_zhi, '干阴阳': GAN_YIN_YANG[day_gan]},
            '时': {'干': time_gan, '支': time_zhi, '干阴阳': GAN_YIN_YANG[time_gan]},
        },
        '十神': {
            '年干': get_shi_shen(day_gan, year_gan),
            '年支': zhi_shi_shen(year_zhi),
            '月干': get_shi_shen(day_gan, month_gan),
            '月支': zhi_shi_shen(month_zhi),
            '日干': '日主',
            '日支': zhi_shi_shen(day_zhi),
            '时干': get_shi_shen(day_gan, time_gan),
            '时支': zhi_shi_shen(time_zhi),
        },
        '藏干': {
            '年支': _canggan_dict(year_zhi),
            '月支': _canggan_dict(month_zhi),
            '日支': _canggan_dict(day_zhi),
            '时支': _canggan_dict(time_zhi),
        },
        '五行': wx_cnt,
        '纳音': {
            '年柱': ec.getYearNaYin(), '月柱': ec.getMonthNaYin(),
            '日柱': ec.getDayNaYin(), '时柱': ec.getTimeNaYin(),
        },
        '节气': {
            '前一节': str(lunar.getPrevJie()),
            '后一节': str(lunar.getNextJie()),
        },
        '生肖': lunar.getYearShengXiao(),
    }
