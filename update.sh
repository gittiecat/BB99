#!/bin/sh

cd /usr/BB99
git pull
systemctl restart bb99.service
