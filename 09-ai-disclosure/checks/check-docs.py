#!/usr/bin/env python3
"""Documentation checks for this repository. Standard library only.

Each check exists because the corresponding mistake was made. See
../README.md for which was which.

Usage:
    python3 09-ai-disclosure/checks/check-docs.py
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
ALLOWED_NON_ASCII = set("ÄÖÜäöüß·→−ṛ")   # German, our notation, the team name


# Verbatim third-party text. Editing a quoted review to match our own house
# style would defeat the point of quoting it, so these files are exempt from
# the style checks and only the structural ones apply.
VERBATIM = {"09-ai-disclosure/reviews/round-1-raw.md",
            "09-ai-disclosure/reviews/round-2-raw.md",
            "09-ai-disclosure/reviews/round-3-raw.md"}


def markdown_files(include_verbatim=True):
    files = [p for p in ROOT.rglob("*.md") if ".git" not in p.parts]
    if include_verbatim:
        return files
    return [p for p in files
            if str(p.relative_to(ROOT)) not in VERBATIM]


def check_em_dashes():
    hits = []
    for p in markdown_files(include_verbatim=False):
        for i, line in enumerate(p.read_text().splitlines(), 1):
            if "—" in line:
                hits.append(f"{p.relative_to(ROOT)}:{i}")
    return "em-dashes", hits


def check_non_ascii():
    hits = []
    for p in markdown_files(include_verbatim=False):
        for i, line in enumerate(p.read_text().splitlines(), 1):
            for ch in line:
                if ord(ch) > 127 and ch not in ALLOWED_NON_ASCII:
                    hits.append(f"{p.relative_to(ROOT)}:{i} unexpected {ch!r}")
    return "unexpected non-ASCII", hits


def check_links():
    hits = []
    for p in markdown_files():
        for m in re.finditer(r"\[[^\]]*\]\(([^)#][^)]*)\)", p.read_text()):
            target = m.group(1).split("#")[0]
            if target.startswith("http") or not target:
                continue
            if not (p.parent / target).resolve().exists():
                hits.append(f"{p.relative_to(ROOT)} -> {target}")
    return "broken relative links", hits


def check_diagram_keys():
    """Every file with a Mermaid block carries an inline Key and links the legend.

    The brief asks for a key where shapes carry meaning, so this is scored.
    """
    hits = []
    for p in markdown_files():
        text = p.read_text()
        if "```mermaid" not in text:
            continue
        if p.name == "3_10-diagram-legend.md":
            continue
        if "**Key.**" not in text:
            hits.append(f"{p.relative_to(ROOT)} has a diagram but no inline Key")
        if "3_10-diagram-legend.md" not in text:
            hits.append(f"{p.relative_to(ROOT)} has a diagram but no legend link")
    return "diagram keys", hits


def check_requirement_counts():
    """Verify the counts the requirements document claims about itself.

    This check exists because that document once claimed 46 requirements when
    it contained 48, with a provenance breakdown that was also wrong. The
    claim had been written from memory rather than from the table.
    """
    p = ROOT / "02-requirements" / "2_1-functional-requirements.md"
    text = p.read_text()
    rows = re.findall(r"^\| (FR-\d+) \|([^|]*)\|([^|]*)\|", text, re.M)
    total = len(rows)
    sources = {}
    for _, _, src in rows:
        sources[src.strip()] = sources.get(src.strip(), 0) + 1

    hits = []
    claimed = re.search(r"Forty eight functional requirements", text)
    if not claimed:
        hits.append("document no longer claims forty eight requirements")
    if total != 48:
        hits.append(f"table contains {total} requirements, prose says forty eight")

    for label, expected in [("Brief", 7), ("Derived", 23), ("Regulatory", 16)]:
        actual = sources.get(label, 0)
        if actual != expected:
            hits.append(f"{label}: table has {actual}, summary claims {expected}")
    return f"requirement counts ({total} rows)", hits


CHECKS = [check_em_dashes, check_non_ascii, check_links,
          check_diagram_keys, check_requirement_counts]


def main():
    print(f"documentation checks over {len(markdown_files())} markdown files")
    print("-" * 68)
    failed = 0
    for check in CHECKS:
        name, hits = check()
        if hits:
            failed += 1
            print(f"[FAIL] {name}: {len(hits)}")
            for h in hits[:10]:
                print(f"         {h}")
        else:
            print(f"[PASS] {name}")
    print("-" * 68)
    print("all documentation checks passed" if not failed
          else f"{failed} check(s) failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
