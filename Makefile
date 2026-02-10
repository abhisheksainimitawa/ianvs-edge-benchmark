# Docker build and push helper
.PHONY: build-all push-all deploy clean

IMAGE_REGISTRY ?= localhost:5000
IMAGE_TAG ?= latest

build-runner:
	docker build -t $(IMAGE_REGISTRY)/ianvs-runner:$(IMAGE_TAG) -f runner/docker/Dockerfile.runner runner/

build-dashboard:
	docker build -t $(IMAGE_REGISTRY)/ianvs-dashboard:$(IMAGE_TAG) -f dashboard/docker/Dockerfile.dashboard dashboard/

build-all: build-runner build-dashboard

push-runner:
	docker push $(IMAGE_REGISTRY)/ianvs-runner:$(IMAGE_TAG)

push-dashboard:
	docker push $(IMAGE_REGISTRY)/ianvs-dashboard:$(IMAGE_TAG)

push-all: push-runner push-dashboard

deploy:
	kubectl apply -f k8s/namespace.yaml
	kubectl apply -f k8s/configmap.yaml
	kubectl apply -f k8s/pvc.yaml
	kubectl apply -f k8s/cloud-deployment.yaml
	kubectl apply -f k8s/edge-deployment.yaml
	kubectl apply -f k8s/service.yaml
	kubectl apply -f k8s/kubeedge-edgeapp.yaml
	kubectl apply -f k8s/kubeedge-device.yaml

undeploy:
	kubectl delete -f k8s/ --ignore-not-found=true

clean:
	docker rmi $(IMAGE_REGISTRY)/ianvs-runner:$(IMAGE_TAG) || true
	docker rmi $(IMAGE_REGISTRY)/ianvs-dashboard:$(IMAGE_TAG) || true

doctor:
	cd runner && python doctor.py

dashboard-local:
	cd dashboard && streamlit run app.py
