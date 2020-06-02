#!/bin/bash
export OASIS_MODEL_DATA_DIR=<..path to piwind ..>
export API_TAG=local-ver

docker rmi coreoasis/api_server:$API_TAG
docker rmi coreoasis/model_worker:$API_TAG

set -e 
docker build -f Dockerfile.api_server -t coreoasis/api_server:$API_TAG .
docker build -f Dockerfile.model_worker -t coreoasis/model_worker:$API_TAG .

docker-compose -f tag.docker-compose.yml up -d --no-build worker-monitor channel-layer celery-beat task-controller server worker
