#!/bin/sh

cd /usr/BB99
git pull
sudo /bin/systemctl restart bb99.service

