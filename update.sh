#!/bin/sh

cd /usr/BB99
git pull
# /bin/su -c "systemctl restart bb99.service" - bb99bot
systemctl restart bb99.service

