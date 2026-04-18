#!/usr/bin/env python3
"""四柱八字排盘 CLI 入口（薄包装，实际逻辑在 tools/bazi/）。"""

import os
import sys

_TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
if _TOOLS_DIR not in sys.path:
    sys.path.insert(0, _TOOLS_DIR)

from bazi.cli import main

if __name__ == '__main__':
    sys.exit(main())
