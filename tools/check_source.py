# -*- coding: utf-8 -*-
"""check_source：每条必须有可追溯的源。

规则：
1. 标签注释必须含 出处类型=，且取值在已知集合内；
2. 源 字段必须存在且非空；
3. 抖音视频类来源必须含「抖音」或「同上」字样
   （「同上」为延续引用惯例，指向上一条完整源，可追溯性成立）。
"""
import sys

from entrylib import run_check

SOURCE_TYPES = {"抖音视频", "访谈", "文献", "书籍", "书", "播客", "文章", "其他"}


def check(e):
    msgs = []
    st = e["tags"].get("出处类型")
    if not st:
        msgs.append("标签缺少 出处类型=")
    elif st not in SOURCE_TYPES:
        msgs.append(f"出处类型={st} 不在已知集合 {sorted(SOURCE_TYPES)}")
    src = e["fields"].get("源")
    if not src:
        msgs.append("缺 源 字段")
    else:
        if st == "抖音视频" and "抖音" not in src and "同上" not in src:
            msgs.append("出处类型=抖音视频 但 源 字段未写明抖音或同上")
        if len(src) < 6:
            msgs.append("源 字段过短，无法追溯")
    return msgs


if __name__ == "__main__":
    sys.exit(run_check(check))
