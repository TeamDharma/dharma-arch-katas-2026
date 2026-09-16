#!/bin/bash
# Render every Mermaid block in the repository, then assert the legend rule.
#
# Unlike the other checks here this one needs a toolchain: @mermaid-js/mermaid-cli
# and a headless Chrome. It preflights both and fails distinctly if either is
# missing, because an earlier version reported a broken toolchain as fifteen
# simultaneous content failures. A check that cannot tell "the tool is missing"
# from "your diagrams are wrong" is worse than no check.
#
# Usage: ./check-diagrams.sh [repo-root] [export-dir]
#
# With a second argument the rendered PNGs are also copied there, named after
# the file the diagram came from. That is how assets/diagrams/ is produced.

set -uo pipefail
REPO="${1:-$(cd "$(dirname "$0")/../.." && pwd)}"
EXPORT="${2:-}"

# --- preflight ------------------------------------------------------------

if ! command -v mmdc >/dev/null 2>&1; then
  echo "TOOLCHAIN: mmdc not found on PATH."
  echo "  npm install -g @mermaid-js/mermaid-cli"
  echo "  If you use nvm, check you are on the node version it was installed under."
  exit 2
fi

# Find whatever Chrome puppeteer actually has, rather than hardcoding a version
# that goes stale on the next update.
CHROME="$(find "$HOME/.cache/puppeteer" -type f \
          \( -name 'chrome-headless-shell' -o -name 'Google Chrome for Testing' \) \
          2>/dev/null | head -1)"

if [ -z "$CHROME" ]; then
  echo "TOOLCHAIN: no puppeteer Chrome found under ~/.cache/puppeteer"
  echo "  npx puppeteer browsers install chrome-headless-shell"
  exit 2
fi

# Unique working directory. A fixed one means two concurrent runs delete each
# other's files mid-render and every diagram reports as failed.
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
printf '{"executablePath":"%s","args":["--no-sandbox"]}' "$CHROME" > "$WORK/pptr.json"

# --- extract --------------------------------------------------------------

python3 - "$REPO" "$WORK" <<'PY'
import re, sys, pathlib
repo, work = sys.argv[1], sys.argv[2]
n = 0
for md in sorted(pathlib.Path(repo).rglob('*.md')):
    if '.git' in md.parts:
        continue
    for i, block in enumerate(re.findall(r'```mermaid\n(.*?)```', md.read_text(), re.S)):
        n += 1
        name = str(md.relative_to(repo)).replace('/', '__') + f'.{i}.mmd'
        (pathlib.Path(work) / name).write_text(block)
print(f"found {n} mermaid block(s)")
PY

# --- render ---------------------------------------------------------------

total=0; failed=0; first_error=""
for f in "$WORK"/*.mmd; do
  [ -e "$f" ] || continue
  total=$((total + 1))
  if err="$(mmdc -i "$f" -o "${f%.mmd}.png" -p "$WORK/pptr.json" -b white -s 2 -q 2>&1)" \
     && [ -s "${f%.mmd}.png" ]; then
    echo "  OK    $(basename "${f%.mmd}")"
    if [ -n "$EXPORT" ]; then
      mkdir -p "$EXPORT"
      name="$(basename "${f%.mmd}" | sed -E 's/__README\.md\./.md./; s/\.md\.0$//; s/\.md\.([0-9]+)$/-\1/')"
      cp "${f%.mmd}.png" "$EXPORT/$name.png"
    fi
  else
    echo "  FAIL  $(basename "${f%.mmd}")"
    failed=$((failed + 1))
    [ -z "$first_error" ] && first_error="$(echo "$err" | grep -viE '^\s+at ' | head -4)"
  fi
done

if [ "$failed" -gt 0 ] && [ "$failed" -eq "$total" ]; then
  echo
  echo "EVERY diagram failed. That is almost certainly the toolchain or a"
  echo "concurrent run, not $total simultaneous syntax errors. First error:"
  echo "$first_error" | sed 's/^/    /'
elif [ "$failed" -gt 0 ]; then
  echo
  echo "First error:"
  echo "$first_error" | sed 's/^/    /'
fi

# --- legend rule ----------------------------------------------------------

echo
echo "--- legend rule: every file with a diagram carries an inline Key and links the legend ---"
python3 - "$REPO" <<'PY'
import sys, pathlib
repo = sys.argv[1]; bad = 0
for md in sorted(pathlib.Path(repo).rglob('*.md')):
    if '.git' in md.parts:
        continue
    t = md.read_text()
    if '```mermaid' not in t:
        continue
    rel = md.relative_to(repo)
    if str(rel).endswith('3_10-diagram-legend.md'):
        print(f"  OK    {rel} (is the legend)"); continue
    missing = []
    if '**Key.**' not in t: missing.append('no inline Key')
    if '3_10-diagram-legend.md' not in t: missing.append('no legend link')
    if missing:
        print(f"  FAIL  {rel}: {', '.join(missing)}"); bad = 1
    else:
        print(f"  OK    {rel}")
sys.exit(bad)
PY
legendfail=$?

echo
[ "$failed" -eq 0 ] && echo "all $total diagrams render" || echo "$failed of $total diagrams FAILED"
[ "$legendfail" -eq 0 ] && echo "all diagrams carry a legend" || echo "SOME DIAGRAMS LACK A LEGEND"
[ "$failed" -eq 0 ] && [ "$legendfail" -eq 0 ] && exit 0 || exit 1
