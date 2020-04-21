#!/bin/bash

if [ -n "$(docker ps -aqf name=nanome-electrostatic-potential)" ]; then
    echo "removing exited container"
    docker rm -f nanome-electrostatic-potential
fi

docker run -d \
--name nanome-electrostatic-potential \
--restart unless-stopped \
-e ARGS="$*" \
nanome-electrostatic-potential
