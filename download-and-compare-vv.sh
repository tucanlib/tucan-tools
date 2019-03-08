#!/usr/bin/env bash

mv modules.json modules.old.json

./vv_exporter.py

cmp <(jq -cS . modules.json) <(jq -cS . modules.old.json) 
