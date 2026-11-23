#!/usr/bin/env python3
"""Impide promover un resultado incompleto como un escaneo sin hallazgos."""
import argparse
import json
from pathlib import Path

EXPECTED = {
    'gitleaks.json': list,
    'semgrep.json': dict,
    'bandit.json': dict,
    'trivy-fs.json': dict,
    'trivy-config.json': dict,
    'checkov.json': (list, dict),
    'pip-audit-ms-orchestrator.json': dict,
    'pip-audit-ms-quiz.json': dict,
    'zap-api.json': dict,
    'zap-frontend.json': dict,
    **{f'trivy-image-{name}.json': dict for name in (
        'microservice-users', 'microservice-classroom', 'microservice-quiz', 'orchestrator', 'frontend')},
}

def verify(root):
    errors = []
    for name, kind in EXPECTED.items():
        paths = list(root.rglob(name))
        if len(paths) != 1:
            errors.append(f'{name}: esperado 1 reporte, encontrados {len(paths)}')
            continue
        try:
            data = json.loads(paths[0].read_text())
            if not isinstance(data, kind):
                raise ValueError('estructura JSON inválida')
            if name.startswith('zap-') and not data.get('site'):
                raise ValueError('no hay sitios escaneados')
            if name.startswith('trivy-') and 'Results' not in data:
                raise ValueError('falta Results')
            if name in ('semgrep.json', 'bandit.json') and 'results' not in data:
                raise ValueError('falta results')
            if name.startswith('pip-audit') and 'dependencies' not in data:
                raise ValueError('falta dependencies')
        except (ValueError, OSError) as exc:
            errors.append(f'{name}: {exc}')
    return errors

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('report_dir', type=Path)
    args = parser.parse_args()
    errors = verify(args.report_dir)
    for error in errors:
        print('[ERROR]', error)
    print(f'Reportes requeridos: {len(EXPECTED)}. Errores: {len(errors)}.')
    raise SystemExit(bool(errors))
