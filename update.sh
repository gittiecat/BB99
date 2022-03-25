#!/bin/sh

cd /home/misha/dev/BB99
git pull
sudo /bin/systemctl restart bb99.service

if (systemctl -q is-active bb99.service)
then
	echo "BB99 daemon has been successfully restarted" >> bot.log
else
	echo "BB99 daemon failed to restart :(" >> bot_error.log
fi
