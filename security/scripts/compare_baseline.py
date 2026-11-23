#!/usr/bin/env python3
"""Compara dos findings.csv de security_summary.py (antes vs después).

Uso:
    python security/scripts/compare_baseline.py ANTES.csv DESPUES.csv [--markdown salida.md]

Genera tablas por severidad y por herramienta con la reducción porcentual, y
la lista de reglas/paquetes que desaparecieron o aparecieron. Solo cuenta lo
que está en los CSV: no interpreta ni corrige cifras.
"""
import argparse
import csv
from collections import Counter

SEVERITIES = ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"]


def load(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def pct(before, after):
    if before == 0:
        return "—" if after == 0 else "nuevo"
    return f"{(before - after) / before * 100:.1f} %"


def table_by_severity(a, b):
    ca, cb = Counter(r["severity"] for r in a), Counter(r["severity"] for r in b)
    lines = ["| Severidad | Antes | Después | Reducción |", "|---|---:|---:|---:|"]
    for s in SEVERITIES:
        lines.append(f"| {s} | {ca[s]} | {cb[s]} | {pct(ca[s], cb[s])} |")
    lines.append(f"| **Total** | **{len(a)}** | **{len(b)}** | **{pct(len(a), len(b))}** |")
    crit_a = ca["CRITICAL"] + ca["HIGH"]
    crit_b = cb["CRITICAL"] + cb["HIGH"]
    lines.append(f"| **CRITICAL + HIGH** | **{crit_a}** | **{crit_b}** | **{pct(crit_a, crit_b)}** |")
    return "\n".join(lines)


def table_by_tool(a, b):
    tools = sorted({r["tool"] for r in a} | {r["tool"] for r in b})
    head = "| Herramienta | " + " | ".join(f"{s[:4]} antes→después" for s in SEVERITIES[:3]) + " | Total antes | Total después | Reducción |"
    lines = [head, "|---|" + "---:|" * 6]
    for t in tools:
        ta = [r for r in a if r["tool"] == t]
        tb = [r for r in b if r["tool"] == t]
        ca, cb = Counter(r["severity"] for r in ta), Counter(r["severity"] for r in tb)
        cells = " | ".join(f"{ca[s]}→{cb[s]}" for s in SEVERITIES[:3])
        lines.append(f"| {t} | {cells} | {len(ta)} | {len(tb)} | {pct(len(ta), len(tb))} |")
    return "\n".join(lines)


def key(r):
    return (r["tool"], r["rule"], r["title"][:80])


def diff_rules(a, b, sev=("CRITICAL", "HIGH")):
    ka = Counter(key(r) for r in a if r["severity"] in sev)
    kb = Counter(key(r) for r in b if r["severity"] in sev)
    gone = sorted(k for k in ka if k not in kb)
    new = sorted(k for k in kb if k not in ka)
    return gone, new


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("before")
    ap.add_argument("after")
    ap.add_argument("--markdown")
    args = ap.parse_args()
    a, b = load(args.before), load(args.after)
    gone, new = diff_rules(a, b)
    out = [
        "## Antes vs después (findings.csv de security_summary.py)",
        "",
        f"- Antes: `{args.before}` · Después: `{args.after}`",
        "",
        "### Por severidad",
        "",
        table_by_severity(a, b),
        "",
        "### Por herramienta",
        "",
        table_by_tool(a, b),
        "",
        f"### Hallazgos CRITICAL/HIGH distintos: {len(gone)} desaparecen, {len(new)} aparecen",
        "",
    ]
    if new:
        out += ["Aparecen (revisar):", ""] + [f"- {t} · {r} · {ti}" for t, r, ti in new] + [""]
    text = "\n".join(out)
    print(text)
    if args.markdown:
        with open(args.markdown, "w", encoding="utf-8") as f:
            f.write(text + "\n")


if __name__ == "__main__":
    main()
