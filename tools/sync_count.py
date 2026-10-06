# -*- coding: utf-8 -*-
"""sync_count：数量与轴一致性对账。

规则：
1. 每个分册：### 条目数 == <!-- 标签: --> 注释数（一一条一标签）；
2. 每条标签 轴= 必须与文件名轴一致（01-process.md 的条目轴必须全为 process）；
3. README 分册表引用的 book/*.md 文件必须存在（防改名后死表）。
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent


def check_file(path):
    msgs = []
    text = path.read_text(encoding="utf-8")
    n_head = len(re.findall(r"^### \d+\.", text, flags=re.M))
    n_tags = len(re.findall(r"<!--\s*标签:", text))
    if n_head != n_tags:
        msgs.append(f"条目数 {n_head} != 标签注释数 {n_tags}")
    axis_expected = re.sub(r"^\d+-", "", path.stem)
    for m in re.finditer(r"<!--\s*标签:[^>]*轴=([\w-]+)", text):
        if m.group(1) != axis_expected:
            msgs.append(f"标签 轴={m.group(1)} 与文件名轴 {axis_expected} 不一致")
    return msgs


def main():
    msgs = []
    books = sorted((ROOT / "book").glob("*.md"))
    if not books:
        msgs.append("book/ 下没有分册文件")
    for f in books:
        msgs.extend(f"{f.relative_to(ROOT)}: {m}" for m in check_file(f))
    readme = ROOT / "README.md"
    if readme.exists():
        for link in re.findall(r"\((book/[\w-]+\.md)\)", readme.read_text(encoding="utf-8")):
            if not (ROOT / link).exists():
                msgs.append(f"README 引用的 {link} 不存在")
    else:
        msgs.append("README.md 不存在")
    if msgs:
        print("\n".join(msgs))
        print(f"FAIL：{len(msgs)} 处违规")
        return 1
    n_total = sum(len(re.findall(r"^### \d+\.", f.read_text(encoding="utf-8"), flags=re.M)) for f in books)
    print(f"PASS：{len(books)} 册共 {n_total} 条，条目=标签，轴名一致")
    return 0


if __name__ == "__main__":
    sys.exit(main())
