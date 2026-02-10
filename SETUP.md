# Setup Guide

## Local Development Setup

### 1. Clone and Navigate
```bash
git clone <your-repo-url>
cd repo
```

### 2. Install Python Dependencies

**Runner component:**
```bash
cd runner
pip install -r requirements.txt
```

**Dashboard component:**
```bash
cd dashboard
pip install -r requirements.txt
```

### 3. Test Components Locally

**Test doctor script:**
```bash
cd runner
python doctor.py
```

**Test dashboard:**
```bash
cd dashboard
streamlit run app.py
```

## Docker Setup

### Build Images
```bash
# From repo/ directory
make build-all

# Or individually
docker build -t ianvs-runner:latest -f runner/docker/Dockerfile.runner runner/
docker build -t ianvs-dashboard:latest -f dashboard/docker/Dockerfile.dashboard dashboard/
```

### Run Containers Locally
```bash
# Run dashboard
docker run -p 8501:8501 ianvs-dashboard:latest

# Run runner
docker run ianvs-runner:latest
```

## Kubernetes Setup

### Prerequisites
1. Kubernetes cluster running (Minikube, Kind, or cloud provider)
2. kubectl configured
3. Docker images built/pushed

### Deployment Steps

1. **Create namespace:**
```bash
kubectl apply -f k8s/namespace.yaml
```

2. **Create ConfigMap:**
```bash
kubectl apply -f k8s/configmap.yaml
```

3. **Create PVC:**
```bash
kubectl apply -f k8s/pvc.yaml
```

4. **Deploy cloud components:**
```bash
kubectl apply -f k8s/cloud-deployment.yaml
kubectl apply -f k8s/service.yaml
```

5. **Deploy edge workers:**
```bash
# Label nodes as edge first
kubectl label nodes <node-name> node-role.kubernetes.io/edge=

kubectl apply -f k8s/edge-deployment.yaml
```

6. **(Optional) KubeEdge components:**
```bash
kubectl apply -f k8s/kubeedge-edgeapp.yaml
kubectl apply -f k8s/kubeedge-device.yaml
```

### Verification

```bash
# Check all resources
kubectl get all -n ianvs-benchmark

# Check logs
kubectl logs -n ianvs-benchmark deployment/ianvs-cloud-master -c benchmark-runner

# Access dashboard
kubectl port-forward -n ianvs-benchmark svc/ianvs-dashboard 8501:8501
```

## KubeEdge Setup (Optional)

For edge node support:

1. **Install KubeEdge cloudcore:**
```bash
keadm init --advertise-address=<cloud-ip>
```

2. **Get token:**
```bash
keadm gettoken
```

3. **Join edge nodes:**
```bash
keadm join --cloudcore-ipport=<cloud-ip>:10000 --token=<token>
```

4. **Verify edge nodes:**
```bash
kubectl get nodes
kubectl get nodes --show-labels | grep edge
```

## Troubleshooting

### Image Pull Errors
If using local Minikube:
```bash
eval $(minikube docker-env)
make build-all
```

### Permission Issues
```bash
# Fix entrypoint script
chmod +x runner/docker/entrypoint.sh
```

### Dashboard Not Loading
```bash
# Check pod status
kubectl get pods -n ianvs-benchmark

# Check logs
kubectl logs -n ianvs-benchmark deployment/ianvs-cloud-master -c dashboard
```
