#!/bin/bash
if [ -n "$(docker ps -aqf name=esp)" ]; then
    echo "removing exited container"
    docker rm -f esp
fi

docker run -d \
--name esp \
--restart unless-stopped \
-e ARGS="$*" \
esp
