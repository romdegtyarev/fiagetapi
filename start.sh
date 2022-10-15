#!/bin/bash

MODE=$1
MODE_START="START"
MODE_STOP="STOP"
DOCKER_IMAGE_NAME="fia"
DOCKER_CONATAINER_NAME="fia_bot"
TG_BOT_START_COMMAND="/home/fia/pyvenv/bin/python3 /home/fia/fia_get/main.py"
USER_ID="1000"
GROUP_ID="985"
HOST_DIR="/home/rom/apps/fia/"
DOCKER_DIR="/home/fia/fia_get"

#Start
if [[ $# -lt 1 ]]
	then
		echo "Enter mode type"
		exit 0
fi

echo "Docker mode $MODE"
if [[ $MODE == $MODE_START ]]
	then
		echo "Start docker"
		docker run --rm \
			--user 1000:985 \
			--name $DOCKER_IMAGE_NAME \
			-v $HOST_DIR:$DOCKER_DIR \
			-i $DOCKER_IMAGE_NAME $TG_BOT_START_COMMAND &
elif [[ $MODE == $MODE_STOP ]]
	then
		echo "Stop docker"
		docker stop $DOCKER_IMAGE_NAME
else
		echo "Unknown mode"
fi


