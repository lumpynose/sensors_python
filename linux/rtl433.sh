#! /bin/sh

passwd=$(cat /usr/local/etc/passwd)

logger -i --tag rtl_433 "Starting rtl_433 to mqtt"

rtl_433 \
    -C customary \
    -F \
    "mqtt://localhost:1883,events=rtl_433[/model]" > /dev/null
