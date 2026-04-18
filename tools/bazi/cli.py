"""argparse 入口 + 顶层错误处理（bug #14）。"""

import argparse
import sys

from .calendar import parse_birth, CITY_LONGITUDE
from .pillars import build_pillars
from .strength import assess_strength
from .fortune import build_dayun, build_liunian
from .formatting import format_text, to_json

VERSION = '1.0.0'
PROG = 'bazi_pan.py'


def build_parser():
    p = argparse.ArgumentParser(
        prog=PROG,
        description='四柱八字排盘 CLI — 支持阳历/农历、真太阳时、中文时辰、夜子时、闰月。',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
示例：
  {PROG} 1990-5-15 8:00 男
  {PROG} --lunar 1990-4-21 辰时 女
  {PROG} --lunar --leap 2020-4-15 早上 male
  {PROG} --city 北京 1990-5-15 23:30 male
  {PROG} --longitude 116.4 --json 1990-5-15 8:00 男

时辰：HH:MM / 子丑寅卯辰巳午未申酉戌亥 / 早上 上午 中午 下午 傍晚 晚上 夜里
性别：男 / 女 / male / female / M / F
""",
    )
    p.add_argument('date', nargs='?', help='日期，例 1990-5-15 或 1990年5月15日')
    p.add_argument('time', nargs='?', help='时辰，例 8:00 / 辰时 / 早上')
    p.add_argument('gender', nargs='?', help='性别')
    p.add_argument('--lunar', action='store_true', help='按农历解析日期')
    p.add_argument('--leap', action='store_true', help='农历闰月（须配合 --lunar）')
    p.add_argument('--longitude', type=float, help='出生地经度，用于真太阳时校正（°E）')
    p.add_argument(
        '--city', type=str,
        help=f'内置城市经度表（{len(CITY_LONGITUDE)} 个：北京/上海/广州/…）',
    )
    p.add_argument('--json', dest='as_json', action='store_true', help='JSON 输出')
    p.add_argument('--pretty', action='store_true', help='JSON 格式化（默认已格式化）')
    p.add_argument('--version', action='version', version=f'{PROG} {VERSION}')
    return p


def run(args):
    if not args.date or not args.time or not args.gender:
        raise SystemExit(
            '缺少位置参数：需要 <日期> <时辰> <性别>。用 --help 查看示例。'
        )
    birth = parse_birth(
        args.date, args.time, args.gender,
        lunar=args.lunar, leap=args.leap,
        longitude=args.longitude, city=args.city,
    )
    pillars = build_pillars(birth)
    strength = assess_strength(pillars)
    dayun = build_dayun(birth)
    liunian = build_liunian(birth)

    result = {
        **pillars,
        '日主强弱': strength,
        '大运': dayun,
        '流年': liunian,
        '原始数据': {
            '阳历日期': birth.solar.toYmd(),
            '出生时辰': f'{birth.solar.getHour():02d}:{birth.solar.getMinute():02d}',
            '性别': birth.gender,
        },
        '注释': birth.notes,
        '版本': VERSION,
    }

    if args.as_json:
        print(to_json(result, pretty=True))
    else:
        print(format_text(result))
    return 0


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return run(args)
    except ValueError as e:
        print(f'❌ 输入错误：{e}', file=sys.stderr)
        print('   用 `python3 tools/bazi_pan.py --help` 查看用法。', file=sys.stderr)
        return 2
    except SystemExit:
        raise
    except Exception as e:  # noqa: BLE001
        print(f'❌ 计算失败：{type(e).__name__}: {e}', file=sys.stderr)
        print('   若问题稳定复现，请贴 issue 附带完整命令。', file=sys.stderr)
        return 3
