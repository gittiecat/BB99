#!/bin/sh

cd /home/misha/dev/BB99
git pull
sudo systemctl restart bb99.service

