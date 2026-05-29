"""Post-process hyperfine markdown report to add vs-builtin column."""

import re
import sys

REPORT = "benches/report.md"

with open(REPORT, encoding="utf-8") as f:
    text = f.read()

lines = text.splitlines()

builtin_mean = None
for line in lines:
    if "builtin" not in line:
        continue
    m = re.search(r"\|\s*([\d.]+)\s*±", line)
    if m:
        builtin_mean = float(m.group(1))
        break

if builtin_mean is None:
    sys.exit(0)

out = []
for i, line in enumerate(lines):
    parts = [p.strip() for p in line.split("|")]
    parts = [p for p in parts if p]
    if i == 0:
        parts.append("vs builtin")
    elif i == 1:
        parts.append("---:")
    else:
        if "builtin" in line:
            parts.append("1.00 (baseline)")
        else:
            m = re.search(r"([\d.]+)\s*±", parts[1])
            if m:
                mean = float(m.group(1))
                ratio = builtin_mean / mean
                parts.append(f"{ratio:.2f}x")
            else:
                parts.append("")
    out.append("| " + " | ".join(parts) + " |")

with open(REPORT, "w", encoding="utf-8") as f:
    f.write("\n".join(out) + "\n")
