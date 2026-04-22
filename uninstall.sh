#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(dirname "$(realpath "${0}")")"
TMP_SCRIPT="/tmp/quick-dns-switcher-uninstall-$$.sh"
cp "${SCRIPT_DIR}/qds/resources/bin/quick-dns-switcher-uninstall.sh" "${TMP_SCRIPT}"
chmod 755 "${TMP_SCRIPT}"
exec bash "${TMP_SCRIPT}" "${@}"
