run:
	uv run services/get_data/src/main.py

# Build and push docker image to the kubernetes kind cluster
build-and-push:
	./scripts/build-and-push-image.sh mdendpoints

# Deploy the service to the kubernetes kind cluster
deploy:
	./scripts/deploy.sh ${service_name}

