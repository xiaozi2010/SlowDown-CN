# -*- coding: utf-8 -*-
"""check_length：短句门。

阈值依据（2026-10-06 对存量 50 条实测后定，README 对外承诺「刺 ≤50 字」）：
    刺 ≤ 50（README L20 承诺值，实测 max 42）
    人话 ≤ 100（实测 max 75）
    源 ≤ 80（实测 max 64）
    光 ≤ 60（实测 max 42）
    注 ≤ 160（实测 max 133）
超限即 FAIL。改阈值须同步 README 承诺。
"""
import sys

from entrylib import run_check

LIMITS = {"刺": 50, "人话": 100, "源": 80, "光": 60, "注": 160}


def check(e):
    msgs = []
    for field, limit in LIMITS.items():
        val = e["fields"].get(field)
        if val is None:
            continue  # 缺字段由各自检查器负责，这里只管长度
        if len(val) > limit:
            msgs.append(f"{field} 字段 {len(val)} 字超限（≤{limit}）")
    return msgs


if __name__ == "__main__":
    sys.exit(run_check(check))
