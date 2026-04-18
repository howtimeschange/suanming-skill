#!/usr/bin/env python3
"""八字排盘回归测试（纯 stdlib）。

运行方式：
  cd suanming-skill-plus
  python3 tests/test_bazi.py
"""

import json
import os
import sys
import traceback

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
sys.path.insert(0, os.path.join(_ROOT, 'tools'))

from bazi.calendar import parse_birth
from bazi.pillars import build_pillars
from bazi.fortune import build_dayun

FIX_DIR = os.path.join(_HERE, 'fixtures')


def dotted_get(d, dotted):
    for k in dotted.split('.'):
        if not isinstance(d, dict) or k not in d:
            return None
        d = d[k]
    return d


def compute(inp):
    kw = {}
    for k in ('lunar', 'leap', 'longitude', 'city'):
        if k in inp:
            kw[k] = inp[k]
    birth = parse_birth(inp['date'], inp['time'], inp['gender'], **kw)
    pillars = build_pillars(birth)
    result = {**pillars}
    result['原始数据'] = {
        '阳历日期': birth.solar.toYmd(),
        '出生时辰': f'{birth.solar.getHour():02d}:{birth.solar.getMinute():02d}',
        '性别': birth.gender,
    }
    result['注释'] = birth.notes
    return result, birth


def _subset_match(actual, want):
    """字典期望值按"子集包含"比对；非字典直接等值比较。"""
    if isinstance(want, dict):
        if not isinstance(actual, dict):
            return False
        return all(_subset_match(actual.get(k), v) for k, v in want.items())
    return actual == want


def check_expected(actual, expected, label):
    errors = []
    for key, want in expected.items():
        got = dotted_get(actual, key)
        if not _subset_match(got, want):
            errors.append(f'  ✗ [{label}] {key}: 期望 {want!r}，实际 {got!r}')
    return errors


def run_case(path):
    name = os.path.basename(path)
    data = json.load(open(path, encoding='utf-8'))

    cases = data.get('cases') or [{'input': data['input'], 'expected': data['expected']}]
    all_errors = []
    for i, case in enumerate(cases):
        label = f'{name}#{i}' if len(cases) > 1 else name
        try:
            actual, birth = compute(case['input'])
            all_errors.extend(check_expected(actual, case['expected'], label))
            # 大运额外测一下，确保能跑完（10 步 + 小运）
            dayun = build_dayun(birth)
            if len(dayun['大运列表']) != 10:
                all_errors.append(f'  ✗ [{label}] 大运列表应为 10 步，实际 {len(dayun["大运列表"])} 步')
        except Exception as e:
            tb = traceback.format_exc()
            all_errors.append(f'  ✗ [{label}] 抛异常：{e}\n{tb}')
    return all_errors


def main():
    fixtures = sorted(f for f in os.listdir(FIX_DIR) if f.endswith('.json'))
    total = len(fixtures)
    passed = 0
    all_failures = []

    for f in fixtures:
        errors = run_case(os.path.join(FIX_DIR, f))
        if errors:
            all_failures.extend(errors)
        else:
            passed += 1
            print(f'  ✓ {f}')

    print()
    print(f'结果：{passed}/{total} 通过')
    if all_failures:
        print()
        print('失败明细：')
        for e in all_failures:
            print(e)
        sys.exit(1)


if __name__ == '__main__':
    main()
