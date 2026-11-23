#!/usr/bin/env python3
"""Sube los reportes del pipeline a DefectDojo (API v2, endpoint reimport-scan).

Variables de entorno:
    DEFECTDOJO_URL      p. ej. https://defectdojo.midominio.com  (sin / final)
    DEFECTDOJO_TOKEN    API v2 key (Perfil de usuario > API v2 Key)
    DD_PRODUCT          nombre del producto      (default: Kiwi)
    DD_PRODUCT_TYPE     tipo de producto         (default: Proyecto UTEC DevOps)
    DD_ENGAGEMENT       nombre del engagement    (default: CI/CD <rama>)
    DD_BRANCH, DD_COMMIT, DD_BUILD_ID, DD_REPO_URL  metadatos opcionales

Uso:
    python security/scripts/defectdojo_upload.py <dir_reportes> [--dry-run]

reimport-scan + auto_create_context crea producto/engagement/test la primera vez y,
en las siguientes ejecuciones, actualiza el mismo test: los hallazgos que ya no
aparecen quedan como mitigados (permite medir antes vs después).
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

# prefijo de archivo -> (scan_type de DefectDojo, título del test)
SCAN_TYPES = [
    ("gitleaks", "Gitleaks Scan", "Secret scanning - Gitleaks"),
    ("semgrep", "Semgrep JSON Report", "SAST - Semgrep"),
    ("bandit", "Bandit Scan", "SAST - Bandit"),
    ("trivy-fs", "Trivy Scan", "SCA - Trivy filesystem"),
    ("trivy-image", "Trivy Scan", "Container - Trivy image"),
    ("trivy-config", "Trivy Scan", "IaC - Trivy config"),
    ("checkov", "Checkov Scan", "IaC - Checkov"),
    ("pip-audit", "pip-audit Scan", "SCA - pip-audit"),
    ("zap", "ZAP Scan", "DAST - OWASP ZAP"),
]


def classify(path: Path):
    name = path.name.lower()
    for prefix, scan_type, title in SCAN_TYPES:
        if name.startswith(prefix):
            if prefix == "zap" and path.suffix != ".xml":
                return None  # el parser "ZAP Scan" de DefectDojo usa el reporte XML
            if prefix != "zap" and path.suffix != ".json":
                return None
            suffix = path.stem[len(prefix):].strip("-_")
            return scan_type, f"{title} {suffix}".strip()
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("report_dir", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--minimum-severity", default="Info")
    args = parser.parse_args()

    url = os.getenv("DEFECTDOJO_URL", "").rstrip("/")
    token = os.getenv("DEFECTDOJO_TOKEN", "")
    branch = os.getenv("DD_BRANCH", "main")
    common = {
        "product_type_name": os.getenv("DD_PRODUCT_TYPE", "Proyecto UTEC DevOps"),
        "product_name": os.getenv("DD_PRODUCT", "Kiwi"),
        "engagement_name": os.getenv("DD_ENGAGEMENT", f"CI/CD {branch}"),
        "auto_create_context": "true",
        "deduplication_on_engagement": "true",
        "close_old_findings": "true",
        "active": "true",
        "verified": "false",
        "minimum_severity": args.minimum_severity,
        "branch_tag": branch,
        "commit_hash": os.getenv("DD_COMMIT", ""),
        "build_id": os.getenv("DD_BUILD_ID", ""),
        "source_code_management_uri": os.getenv("DD_REPO_URL", ""),
    }

    files = [(p, classify(p)) for p in sorted(args.report_dir.rglob("*")) if p.is_file()]
    files = [(p, c) for p, c in files if c]
    if not files:
        print("No se encontraron reportes compatibles", file=sys.stderr)
        return 1

    if args.dry_run:
        for p, (scan_type, title) in files:
            print(f"[DRY-RUN] {p.name:40s} -> {scan_type:22s} | {title}")
        return 0

    if not url or not token:
        print("DEFECTDOJO_URL / DEFECTDOJO_TOKEN no configurados; se omite la carga.", file=sys.stderr)
        return 0

    import requests

    session = requests.Session()
    session.headers["Authorization"] = f"Token {token}"
    errors = 0
    for path, (scan_type, title) in files:
        data = {**common, "scan_type": scan_type, "test_title": title}
        try:
            with path.open("rb") as fh:
                resp = session.post(f"{url}/api/v2/reimport-scan/", data=data,
                                    files={"file": (path.name, fh)}, timeout=300)
        except requests.RequestException as exc:
            errors += 1
            print(f"[ERROR] {path.name}: no se pudo conectar con DefectDojo ({exc.__class__.__name__})", file=sys.stderr)
            continue
        if resp.status_code in (200, 201):
            body = resp.json()
            stats = body.get("statistics", {}).get("after", {}).get("total", {})
            print(f"[OK] {path.name} -> test {body.get('test')} ({scan_type}) {stats}")
        else:
            errors += 1
            print(f"[ERROR {resp.status_code}] {path.name}: {resp.text[:300]}", file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
