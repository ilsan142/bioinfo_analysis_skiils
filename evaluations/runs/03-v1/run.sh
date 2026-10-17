#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "$0")"
{
  printf 'Command: python analyze.py\n'
  python analyze.py
} 2>&1 | tee execution.log
