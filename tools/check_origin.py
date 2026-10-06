# -*- coding: utf-8 -*-
"""check_origin：防错误归属（对标 dwyl 的 misattribution 门，K-622 护城河机器侧）。

规则：注 字段必须存在且写明与原话的关系，即包含以下归属词之一：
    直引 / 原话 / 转述 / 意译 / 整理 / 摘引 / 微调 / 改写 / 编译 / 自察
裸条目（无归属说明）一律 FAIL，防止把转述当原话传播。
"""
import sys

from entrylib import run_check

ORIGIN_WORDS = ("直引", "原话", "转述", "意译", "整理", "摘引", "微调", "改写", "编译", "自察")


def check(e):
    msgs = []
    note = e["fields"].get("注")
    if not note:
        msgs.append("缺 注 字段（归属说明）")
    elif not any(w in note for w in ORIGIN_WORDS):
        msgs.append(f"注 字段未写明与原话的关系（需含 {ORIGIN_WORDS[0]}~{ORIGIN_WORDS[4]} 等归属词）")
    return msgs


if __name__ == "__main__":
    sys.exit(run_check(check))
