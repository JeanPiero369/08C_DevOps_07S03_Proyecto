#!/usr/bin/env bash
# Instala Trivy desde el release oficial verificando el checksum SHA-256.
set -euo pipefail
version="${TRIVY_VERSION:?TRIVY_VERSION no definido}"
base="https://github.com/aquasecurity/trivy/releases/download/v${version}"
tmp=$(mktemp -d)
curl -sSfL -o "$tmp/trivy.tgz" "$base/trivy_${version}_Linux-64bit.tar.gz"
curl -sSfL "$base/trivy_${version}_checksums.txt" | grep "Linux-64bit.tar.gz$" | awk -v f="$tmp/trivy.tgz" '{print $1"  "f}' | sha256sum -c -
tar xzf "$tmp/trivy.tgz" -C "$tmp" trivy
sudo mv "$tmp/trivy" /usr/local/bin/trivy
trivy --version | head -1
