#!/usr/bin/env python3
"""Normaliza los reportes de las herramientas DevSecOps en un solo inventario.

Uso:
    python security/scripts/security_summary.py <dir_reportes> \
        --csv findings.csv --markdown summary.md [--fail-on CRITICAL]

Archivos reconocidos (por nombre):
    gitleaks*.json, semgrep*.json, bandit*.json, trivy*.json, checkov*.json,
    zap*.json, npm-audit*.json, pip-audit*.json
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path

SEVERITIES = ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"]


@dataclass
class Finding:
    tool: str
    category: str
    severity: str
    rule: str
    title: str
    location: str
    detail: str = ""


def _sev(value: str | None, default: str = "MEDIUM") -> str:
    if not value:
        return default
    v = str(value).upper()
    aliases = {
        "ERROR": "HIGH",
        "WARNING": "MEDIUM",
        "MODERATE": "MEDIUM",
        "INFORMATIONAL": "INFO",
        "UNKNOWN": "INFO",
        "NOTE": "LOW",
    }
    v = aliases.get(v, v)
    return v if v in SEVERITIES else default


def parse_gitleaks(data) -> list[Finding]:
    return [
        Finding("Gitleaks", "Secret scanning", "HIGH", x["RuleID"], x.get("Description", x["RuleID"]),
                f'{x["File"]}:{x["StartLine"]}', f'commit {x.get("Commit", "")[:7]}')
        for x in data or []
    ]


def parse_semgrep(data) -> list[Finding]:
    out = []
    for x in data.get("results", []):
        out.append(Finding("Semgrep", "SAST", _sev(x["extra"].get("severity")), x["check_id"].split(".")[-1],
                           x["extra"].get("message", "").strip().split("\n")[0][:160],
                           f'{x["path"]}:{x["start"]["line"]}'))
    return out


def parse_bandit(data) -> list[Finding]:
    return [
        Finding("Bandit", "SAST", _sev(x["issue_severity"]), x["test_id"], x["issue_text"],
                f'{x["filename"]}:{x["line_number"]}', f'confidence {x["issue_confidence"]}')
        for x in data.get("results", [])
    ]


def parse_trivy(data) -> list[Finding]:
    out = []
    for r in data.get("Results", []) or []:
        target = r.get("Target", "")
        for v in r.get("Vulnerabilities", []) or []:
            category = "Container scan" if data.get("ArtifactType") == "container_image" else "SCA"
            out.append(Finding("Trivy", category, _sev(v.get("Severity")), v["VulnerabilityID"],
                               f'{v["PkgName"]} {v.get("InstalledVersion", "")}: {v.get("Title", "")}'[:160],
                               target, f'fixed: {v.get("FixedVersion", "-")}'))
        for m in r.get("Misconfigurations", []) or []:
            out.append(Finding("Trivy", "IaC", _sev(m.get("Severity")), m["ID"], m.get("Title", ""), target))
        for s in r.get("Secrets", []) or []:
            out.append(Finding("Trivy", "Secret scanning", _sev(s.get("Severity")), s["RuleID"], s.get("Title", ""),
                               f'{target}:{s.get("StartLine", "")}'))
    return out


def parse_checkov(data) -> list[Finding]:
    reports = data if isinstance(data, list) else [data]
    out = []
    for r in reports:
        for c in r.get("results", {}).get("failed_checks", []):
            out.append(Finding("Checkov", "IaC", _sev(c.get("severity")), c["check_id"], c["check_name"],
                               c["file_path"].lstrip("/")))
    return out


def parse_zap(data) -> list[Finding]:
    risk = {"3": "HIGH", "2": "MEDIUM", "1": "LOW", "0": "INFO"}
    out = []
    for site in data.get("site", []):
        for a in site.get("alerts", []):
            out.append(Finding("OWASP ZAP", "DAST", risk.get(str(a.get("riskcode")), "INFO"),
                               str(a.get("pluginid")), a.get("name", a.get("alert", "")),
                               site.get("@name", ""), f'{a.get("count", "")} instancias'))
    return out


def parse_npm_audit(data, source: str) -> list[Finding]:
    out, seen = [], set()
    for name, v in data.get("vulnerabilities", {}).items():
        for via in v.get("via", []):
            if isinstance(via, dict) and (name, via.get("url")) not in seen:
                seen.add((name, via.get("url")))
                out.append(Finding("npm audit", "SCA", _sev(via.get("severity")), via.get("url", "").split("/")[-1],
                                   f'{name}: {via.get("title", "")}'[:160], source,
                                   "directa" if v.get("isDirect") else "transitiva"))
    return out


def parse_pip_audit(data, source: str) -> list[Finding]:
    out = []
    for dep in data.get("dependencies", []):
        for v in dep.get("vulns", []):
            out.append(Finding("pip-audit", "SCA", "MEDIUM", v["id"],
                               f'{dep["name"]} {dep["version"]}: {", ".join(v.get("aliases", []))}', source,
                               f'fix: {",".join(v.get("fix_versions", [])) or "-"}'))
    return out


def collect(report_dir: Path) -> list[Finding]:
    findings: list[Finding] = []
    for path in sorted(report_dir.rglob("*.json")):
        name = path.name.lower()
        try:
            data = json.loads(path.read_text(encoding="utf-8") or "null")
        except json.JSONDecodeError:
            print(f"[WARN] JSON inválido: {path}", file=sys.stderr)
            continue
        if data is None:
            data = []
        source = path.stem
        if name.startswith("gitleaks"):
            findings += parse_gitleaks(data)
        elif name.startswith("semgrep"):
            findings += parse_semgrep(data)
        elif name.startswith("bandit"):
            findings += parse_bandit(data)
        elif name.startswith("trivy"):
            findings += parse_trivy(data)
        elif name.startswith("checkov"):
            findings += parse_checkov(data)
        elif name.startswith("zap"):
            findings += parse_zap(data)
        elif name.startswith("npm-audit"):
            findings += parse_npm_audit(data, source)
        elif name.startswith("pip-audit"):
            findings += parse_pip_audit(data, source)
    return findings


def to_markdown(findings: list[Finding], min_detail: str = "MEDIUM") -> str:
    by_tool: dict[str, Counter] = {}
    for f in findings:
        by_tool.setdefault(f.tool, Counter())[f.severity] += 1
    total = Counter(f.severity for f in findings)
    lines = ["## Resumen de seguridad", "", "| Herramienta | " + " | ".join(SEVERITIES) + " | Total |",
             "|---|" + "---:|" * (len(SEVERITIES) + 1)]
    for tool, c in sorted(by_tool.items()):
        lines.append(f"| {tool} | " + " | ".join(str(c[s]) for s in SEVERITIES) + f" | {sum(c.values())} |")
    lines.append("| **Total** | " + " | ".join(f"**{total[s]}**" for s in SEVERITIES) + f" | **{len(findings)}** |")
    limit = SEVERITIES.index(min_detail)
    top = [f for f in findings if SEVERITIES.index(f.severity) <= min(limit, 1)]
    if top:
        lines += ["", "### Hallazgos CRITICAL / HIGH", "", "| Severidad | Herramienta | Regla | Hallazgo | Ubicación |",
                  "|---|---|---|---|---|"]
        for f in sorted(top, key=lambda x: SEVERITIES.index(x.severity))[:60]:
            title = f.title.replace("|", "/")
            lines.append(f"| {f.severity} | {f.tool} | {f.rule} | {title} | {f.location} |")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("report_dir", type=Path)
    parser.add_argument("--csv", type=Path)
    parser.add_argument("--markdown", type=Path)
    parser.add_argument("--fail-on", choices=SEVERITIES, help="Termina con código 1 si hay hallazgos de esta severidad o mayor")
    args = parser.parse_args()

    findings = collect(args.report_dir)
    md = to_markdown(findings)
    print(md)
    if args.markdown:
        args.markdown.write_text(md, encoding="utf-8")
    if args.csv:
        with args.csv.open("w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=list(Finding.__dataclass_fields__))
            writer.writeheader()
            writer.writerows(asdict(f) for f in findings)
    if args.fail_on:
        threshold = SEVERITIES.index(args.fail_on)
        blocking = [f for f in findings if SEVERITIES.index(f.severity) <= threshold]
        if blocking:
            print(f"[GATE] {len(blocking)} hallazgos con severidad >= {args.fail_on}", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
