#!/usr/bin/env bash

SERVER="${FTP_SERVER:-davidgengenbach.de}"
DIR="${FTP_FOLDER:-/sites/davidgengenbach/informatik-vv/sose19/assets}"
SEMESTER="${SEMESTER:-SoSe 19}"

DATE=$(date +%d.%m.%y)

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
    put constants.json constants.js
    bye
EOF
else
    # Credentials are in .netrc
    curl -T {modules.json,constants.json} -u $FTP_LOGIN:$FTP_PASSWORD ftp://$FTP_SERVER$FTP_FOLDER/
fi

rm constants.json