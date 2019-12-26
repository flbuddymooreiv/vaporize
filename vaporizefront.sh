#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
notify-send "Scanning Sectors"
./vaporize.py > vaporize.sh
notify-send "Firing!"
./vaporize.sh
