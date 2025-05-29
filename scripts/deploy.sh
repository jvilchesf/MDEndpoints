#!/bin/bash

# This script is used to deploy a given service to the the given Kubernetes environment

service=$1

if [ -z "$service" ]; then
    echo "Usage: $0 <service> <env>"
    exit 1
fi

cd deployments/${service}

# hook the direnv tool here
# we add this line here so that direnv can load the right KUBECONFIG environment variable
# from the deployments/${env}/.env.local file

echo "Deploying ${service} with kustomize"
# delete the service
# TODO: add the ignore-not-found flag to avoid errors the first time you deploy something
kustomize build . | kubectl delete -f - --ignore-not-found=true
# deploy the service
kustomize build . | kubectl apply -f -
