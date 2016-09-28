#!/usr/bin/env sh

set -x

mv modules.json modules.old.json
./vv_exporter.py
diff modules.json modules.old.json
