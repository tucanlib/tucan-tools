#!/usr/bin/env bash

SERVER='davidgengenbach.de'
DIR='/sites/davidgengenbach/informatik-vv/sose17/assets'

# Credentials are in .netrc
ftp $SERVER <<EOF
binary
cd $DIR
put modules.json
bye
EOF