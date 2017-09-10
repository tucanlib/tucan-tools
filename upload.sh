#!/usr/bin/env bash

SERVER="$FTP_SERVER"
DIR="$FTP_FOLDER"

TMP=$(mktemp)
DATE=$(date +%d.%m.%y)
SEMESTER="WiSe 17/18"

cat > $TMP <<EOF
(function(angular) {
    'use strict';
    angular
        .module('informatikModulesConstants', [])
        .constant('SEMESTER', '$SEMESTER')
        .constant('LAST_UPDATED', '$DATE');
})(angular);
EOF

# Credentials are in .netrc
ftp $SERVER <<EOF
    binary
    cd $DIR
    put modules.json
    put $TMP constants.js
    bye
EOF
