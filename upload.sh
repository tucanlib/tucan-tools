#!/usr/bin/env bash

SERVER="$FTP_SERVER"
DIR="$FTP_FOLDER"

# Defaults
if [ -z "$SERVER" ]; then
    SERVER='davidgengenbach.de'
fi

if [ -z "$DIR" ]; then
    DIR='/sites/davidgengenbach/informatik-vv/ws1718/assets'
fi

TMP=$(mktemp)
DATE=$(date +%d.%m.%y)
SEMESTER="WiSe 17/18"

cat > constants.json <<EOF
(function(angular) {
    'use strict';
    angular
        .module('informatikModulesConstants', [])
        .constant('SEMESTER', '$SEMESTER')
        .constant('LAST_UPDATED', '$DATE');
})(angular);
EOF

if [ -z "$FTP_LOGIN" ]; then
ftp $SERVER <<EOF
    binary
    cd $DIR
    put modules.json
    put $TMP constants.js
    bye
EOF
else
    # Credentials are in .netrc
    curl -T {modules.json,constants.json} -u $FTP_LOGIN:$FTP_PASSWORD ftp://$FTP_SERVER$FTP_FOLDER/
fi

rm constants.json