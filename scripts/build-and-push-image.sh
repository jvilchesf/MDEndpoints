#!/bin/bash

# Builds a docker image for the given dockerfile and pushes it to the docker registry
# given by the env variable

image_name=$1

# Just checking that the user has provided the correct number of arguments
if [ -z "$image_name" ]; then
    echo "Usage: $0 <image_name> <env>"
    exit 1
fi

echo "Building image ${image_name} for dev"
docker build -t ${image_name}-image -f docker/${image_name}.Dockerfile .
kind load docker-image ${image_name}-image --name knowbe4
