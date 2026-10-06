# -*- coding: utf-8 -*-
"""preflight：发布/PR 前门禁。全绿才算过。

步骤：
1. 五检查器全量（source/length/light/origin/sync_count）；
2. 死链检查：README + docs/**/*.md + book/*.md 中相对链接指向的本地文件必须存在
   （跳过 http/https/mailto/# 锚点）；
3. 必需文件清单（LICENSE / LICENSE-CODE / CONTRIBUTING / docs/价值观.md 等）。
用法：python tools/preflight.py
"""
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"

CHECKERS = ["check_source.py", "check_length.py", "check_light.py", "check_origin.py", "sync_count.py"]

REQUIRED = [
    "README.md",
    "CONTRIBUTING.md",
    "LICENSE",
    "LICENSE-CODE.md",
    "docs/价值观.md",
    # 社区标配（GitHub Community Standards）+ 承诺兑现：CONTRIBUTING 承诺了 CI 与 Issue 模板，缺了就是说谎
    "CODE_OF_CONDUCT.md",
    ".github/workflows/ci.yml",
    ".github/ISSUE_TEMPLATE/新内容投稿.md",
    ".github/ISSUE_TEMPLATE/纠错.md",
    ".github/PULL_REQUEST_TEMPLATE.md",
]

_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
_SKIP_PREFIX = ("http://", "https://", "mailto:", "#")


def dead_links():
    msgs = []
    targets = [ROOT / "README.md"]
    targets += sorted((ROOT / "docs").rglob("*.md"))
    targets += sorted((ROOT / "book").glob("*.md"))
    for f in targets:
        if not f.exists():
            continue
        text = f.read_text(encoding="utf-8")
        for m in _LINK_RE.finditer(text):
            link = m.group(1)
            if link.startswith(_SKIP_PREFIX):
                continue
            local = link.split("#")[0]
            if not local:
                continue
            if not (f.parent / local).exists():
                msgs.append(f"{f.relative_to(ROOT)}: 死链 -> {link}")
    return msgs


def main():
    failures = []

    for checker in CHECKERS:
        print(f"== {checker} ==")
        r = subprocess.run([sys.executable, str(TOOLS / checker)],
                           cwd=str(TOOLS), capture_output=True, text=True, encoding="utf-8")
        out = (r.stdout or "") + (r.stderr or "")
        print("\n".join("  " + ln for ln in out.strip().splitlines()))
        if r.returncode != 0:
            failures.append(checker)

    print("== 死链检查 ==")
    dl = dead_links()
    if dl:
        print("\n".join("  " + m for m in dl))
        failures.append("死链")
    else:
        print("  PASS")

    print("== 必需文件 ==")
    missing = [f for f in REQUIRED if not (ROOT / f).exists()]
    if missing:
        print("\n".join("  缺 " + f for f in missing))
        failures.append("必需文件")
    else:
        print(f"  PASS（{len(REQUIRED)} 项齐）")

    print()
    if failures:
        print(f"PREFLIGHT FAIL：{failures}")
        return 1
    print("PREFLIGHT PASS：全绿")
    return 0


if __name__ == "__main__":
    sys.exit(main())
