# -*- coding: utf-8 -*-
"""check_light：光栏三档口径（K-624 定案）。

规则：
1. 标签 光= 取值必须 ∈ {有, 无, 一分钟, 一小时, 一整天}；
   存量条目为过渡值「有」，新条目按三档强度标注；
2. 光=无 时允许没有 光 字段；其余取值必须有非空 光 字段。
"""
import sys

from entrylib import run_check

LIGHT_LEVELS = {"有", "无", "一分钟", "一小时", "一整天"}


def check(e):
    msgs = []
    lv = e["tags"].get("光")
    if not lv:
        msgs.append("标签缺少 光=")
    elif lv not in LIGHT_LEVELS:
        msgs.append(f"光={lv} 不在合法集合 {sorted(LIGHT_LEVELS)}")
    act = e["fields"].get("光")
    if lv != "无" and not act:
        msgs.append("缺 光 字段（行动项）")
    return msgs


if __name__ == "__main__":
    sys.exit(run_check(check))
