"""日期/时辰解析与归一化：修复 bug #1 #2 #3 #4 #5 #11。

- 阳历默认，`lunar=True` 走农历（`leap=True` 表示闰月）
- 支持 HH:MM、中文时辰（子/丑/…/亥）、模糊时段（早上/中午/晚上…）
- 真太阳时：`longitude` 或 `city` 决定 Δmin，写回 Solar
- 23:00-23:59 → 夜子时：日柱进位到次日 0:00，时柱仍取子时，保留 `ye_zi=True`
- 性别：男/女/male/female/M/F → 'male'/'female'
"""

import sys
import os
from datetime import datetime, timedelta

_TOOLS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _TOOLS_DIR not in sys.path:
    sys.path.insert(0, _TOOLS_DIR)
import lunar_python as lp


GENDER_MAP = {
    '男': 'male', '女': 'female',
    'male': 'male', 'female': 'female',
    'M': 'male', 'F': 'female',
    'm': 'male', 'f': 'female',
}
GENDER_CODE = {'male': 1, 'female': 0}

SHICHEN_TO_HOUR = {
    '子': 0, '丑': 2, '寅': 4, '卯': 6, '辰': 8, '巳': 10,
    '午': 12, '未': 14, '申': 16, '酉': 18, '戌': 20, '亥': 22,
}
# 模糊时段：取区间中点
FUZZY_TIME = {
    '凌晨': (2, 0), '夜里': (2, 0), '深夜': (2, 0),
    '早上': (7, 0), '上午': (10, 0), '早晨': (7, 0),
    '中午': (12, 0), '正午': (12, 0),
    '下午': (15, 0), '傍晚': (18, 0), '黄昏': (18, 0),
    '晚上': (20, 0), '夜晚': (20, 0),
}

CITY_LONGITUDE = {
    '北京': 116.41, '上海': 121.47, '广州': 113.27, '深圳': 114.06,
    '天津': 117.20, '重庆': 106.55, '成都': 104.07, '西安': 108.95,
    '杭州': 120.15, '南京': 118.78, '武汉': 114.30, '长沙': 112.94,
    '苏州': 120.58, '郑州': 113.62, '济南': 117.00, '合肥': 117.27,
    '福州': 119.30, '厦门': 118.08, '南昌': 115.89, '南宁': 108.37,
    '昆明': 102.71, '贵阳': 106.71, '兰州': 103.82, '西宁': 101.78,
    '银川': 106.27, '呼和浩特': 111.67, '太原': 112.55, '石家庄': 114.51,
    '沈阳': 123.43, '长春': 125.32, '哈尔滨': 126.53, '大连': 121.62,
    '青岛': 120.38, '乌鲁木齐': 87.62, '拉萨': 91.10,
    '台北': 121.56, '香港': 114.17, '澳门': 113.55,
    '海口': 110.33, '三亚': 109.51, '韶山': 112.52,
}


class BirthInfo:
    def __init__(self, solar, gender, notes):
        self.solar = solar           # lunar_python Solar (已含真太阳时校正 + 夜子时进位)
        self.lunar = solar.getLunar()
        self.gender = gender         # 'male' | 'female'
        self.gender_code = GENDER_CODE[gender]
        self.notes = notes           # 用于 JSON 回传：真太阳时偏移、夜子时、农历闰月等

    def __repr__(self):
        return f"BirthInfo(solar={self.solar.toYmdHms()}, gender={self.gender}, notes={self.notes})"


def _parse_date(date_str):
    """支持 1990-5-15 / 1990年5月15日 / 1990/5/15 → (y, m, d)。负月份支持闰月。"""
    s = date_str.replace('年', '-').replace('月', '-').replace('日', '').replace('/', '-').strip()
    parts = [p for p in s.split('-') if p]
    if len(parts) != 3:
        raise ValueError(f"无法解析日期：{date_str!r}（期望 1990-5-15 或 1990年5月15日）")
    y, m, d = int(parts[0]), int(parts[1]), int(parts[2])
    return y, m, d


def _parse_time(time_str):
    """返回 (hour, minute)。支持 HH:MM / 8点 / 子时 / 早上 等。"""
    if time_str is None:
        return 12, 0
    t = time_str.strip().replace('点', ':').replace('时', '')
    # 中文单字时辰：子/丑/…/亥（可后跟"时"字，前面已剥离）
    if t in SHICHEN_TO_HOUR:
        return SHICHEN_TO_HOUR[t], 0
    # 模糊时段
    if t in FUZZY_TIME:
        return FUZZY_TIME[t]
    # HH:MM
    if ':' in t:
        hh, *rest = t.split(':')
        mm = int(rest[0]) if rest and rest[0] else 0
        return int(hh), mm
    # 纯数字小时
    if t.isdigit():
        return int(t), 0
    raise ValueError(f"无法解析时辰：{time_str!r}（支持 HH:MM / 辰时 / 早上）")


def _parse_gender(gender_str):
    if gender_str is None:
        raise ValueError("缺少性别参数（男/女/male/female）")
    key = gender_str.strip()
    if key not in GENDER_MAP:
        raise ValueError(f"无法识别性别：{gender_str!r}（支持 男/女/male/female）")
    return GENDER_MAP[key]


def _longitude_offset_minutes(lon):
    """真太阳时：与东八区经度 120° 的差，每 1° ≈ 4 分钟。"""
    return (lon - 120.0) * 4.0


def parse_birth(
    date_str,
    time_str,
    gender_str,
    *,
    lunar=False,
    leap=False,
    longitude=None,
    city=None,
):
    """主入口：解析所有输入，返回 BirthInfo。"""
    gender = _parse_gender(gender_str)
    y, m, d = _parse_date(date_str)
    hour, minute = _parse_time(time_str) if time_str else (12, 0)
    notes = {}

    if leap and not lunar:
        raise ValueError("--leap 必须和 --lunar 一起用")

    # 1. 构造基础 Solar
    if lunar:
        lunar_month = -m if leap else m
        lun = lp.Lunar.fromYmdHms(y, lunar_month, d, hour, minute, 0)
        solar = lun.getSolar()
        notes['输入历法'] = '农历'
        if leap:
            notes['闰月'] = True
    else:
        solar = lp.Solar.fromYmdHms(y, m, d, hour, minute, 0)
        notes['输入历法'] = '阳历'

    # 2. 真太阳时校正
    lon = None
    if city is not None:
        if city not in CITY_LONGITUDE:
            raise ValueError(f"未内置城市经度：{city!r}（可改用 --longitude）")
        lon = CITY_LONGITUDE[city]
        notes['城市'] = city
    elif longitude is not None:
        lon = float(longitude)
    if lon is not None:
        offset_min = _longitude_offset_minutes(lon)
        notes['真太阳时'] = {
            '经度': round(lon, 3),
            '偏移分钟': round(offset_min, 2),
        }
        dt = datetime(solar.getYear(), solar.getMonth(), solar.getDay(),
                      solar.getHour(), solar.getMinute(), solar.getSecond())
        dt = dt + timedelta(minutes=offset_min)
        solar = lp.Solar.fromYmdHms(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)

    # 3. 夜子时处理：23:00-23:59 → 次日子时
    if solar.getHour() == 23:
        notes['夜子时'] = True
        next_solar = solar.next(1)  # 次日同时刻
        # 次日 0:00 给日柱；时柱仍落在"子"，由 EightChar 天然覆盖
        dt_next = datetime(next_solar.getYear(), next_solar.getMonth(), next_solar.getDay(), 0, 0, 0)
        solar = lp.Solar.fromYmdHms(dt_next.year, dt_next.month, dt_next.day, 0, 0, 0)

    return BirthInfo(solar, gender, notes)
