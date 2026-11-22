#!/usr/bin/env python3
"""Comprueba las sondas reales de Prometheus y conserva evidencia de staging."""
import argparse
import json
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

def query(base, expression):
    url = base.rstrip('/') + '/api/v1/query?' + urllib.parse.urlencode({'query': expression})
    with urllib.request.urlopen(url, timeout=10) as response:
        data = json.load(response)
    if data.get('status') != 'success':
        raise ValueError('Prometheus no devolvió success')
    return data['data']['result']

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--url', default='http://localhost:9090')
    parser.add_argument('--output', type=Path, default=Path('reports/monitoring.json'))
    args = parser.parse_args()
    samples = []
    for attempt in range(12):
        try:
            samples = query(args.url, 'probe_success{job="kiwi-http"}')
            if len(samples) == 2 and all(float(s['value'][1]) == 1 for s in samples):
                break
        except (OSError, ValueError):
            pass
        time.sleep(5)
    ok = len(samples) == 2 and all(float(s['value'][1]) == 1 for s in samples)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps({'timestamp': datetime.now(timezone.utc).isoformat(),
        'healthy': ok, 'probe_success': samples}, indent=2) + '\n')
    print(f'Monitoreo HTTP: {len(samples)} sondas, healthy={ok}')
    raise SystemExit(0 if ok else 1)
