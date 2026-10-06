# -*- coding: utf-8 -*-
"""SlowDown-CN 条目解析公共库。

条目结构契约（详见 CLAUDE.md）：
    ### N. 标题
    <!-- 标签: 轴=process 强度=高 出处类型=抖音视频 光=有 -->
    > **刺**：...
    > **人话**：...
    > **源**：...
    > **光**：...
    > **注**：...

所有检查器只用 Python 标准库，零第三方依赖。
"""
import pathlib
import re
import sys

FIELDS = ["刺", "人话", "源", "光", "注"]

_HEADER_RE = re.compile(r"^### (\d+)\.\s*(.+)$")
_TAG_RE = re.compile(r"<!--\s*标签:\s*(.+?)\s*-->")
_FIELD_RE = re.compile(r"^>\s*\*\*(.+?)\*\*：\s*(.*)$")


def parse_file(path):
    """解析一个分册/fixture 文件，返回条目列表。

    每个条目: {num, title, line, file, tags(dict), raw_tags(str), fields(dict[str, str])}
    fields 取字段首行（当前全部条目为单行字段；多行会被长度检查遗漏，属已知边界）。
    """
    text = pathlib.Path(path).read_text(encoding="utf-8")
    entries = []
    cur = None
    for i, line in enumerate(text.splitlines(), 1):
        m = _HEADER_RE.match(line)
        if m:
            cur = {
                "num": int(m.group(1)),
                "title": m.group(2).strip(),
                "line": i,
                "file": str(path),
                "tags": {},
                "raw_tags": "",
                "fields": {},
            }
            entries.append(cur)
            continue
        if cur is None:
            continue
        tm = _TAG_RE.search(line)
        if tm and not cur["raw_tags"]:
            cur["raw_tags"] = tm.group(1)
            for kv in tm.group(1).split():
                if "=" in kv:
                    k, v = kv.split("=", 1)
                    cur["tags"][k] = v
            continue
        fm = _FIELD_RE.match(line)
        if fm and fm.group(1) in FIELDS and fm.group(1) not in cur["fields"]:
            cur["fields"][fm.group(1)] = fm.group(2).strip()
    return entries


def default_targets(argv):
    """无参数时扫 book/ 全部分册；有参数时按传入文件/目录解析。"""
    if argv:
        out = []
        for a in argv:
            p = pathlib.Path(a)
            if p.is_dir():
                out.extend(sorted(p.glob("*.md")))
            else:
                out.append(p)
        return out
    return sorted(pathlib.Path(__file__).resolve().parent.parent.glob("book/*.md"))


def run_check(fn):
    """检查器统一入口：fn(entry) 返回违规消息列表；打印并返回退出码。"""
    problems = []
    for f in default_targets(sys.argv[1:]):
        if not f.exists():
            problems.append(f"{f}: 文件不存在")
            continue
        for e in parse_file(f):
            problems.extend(f"{e['file']}:{e['line']} ({e['num']}.{e['title']}): {msg}" for msg in fn(e))
    if problems:
        print("\n".join(problems))
        print(f"FAIL：{len(problems)} 处违规")
        return 1
    print("PASS")
    return 0
