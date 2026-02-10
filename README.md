# 🚀 Ianvs Edge AI Benchmarking Platform

[![CI/CD Pipeline](https://github.com/yourusername/ianvs-benchmark/actions/workflows/ci.yaml/badge.svg)](https://github.com/yourusername/ianvs-benchmark/actions)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![KubeEdge](https://img.shields.io/badge/KubeEdge-Compatible-green.svg)](https://kubeedge.io)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-1.25+-blue.svg)](https://kubernetes.io)

> **A production-ready cloud-edge collaborative AI benchmarking system built with Ianvs, Kubernetes, and KubeEdge for distributed federated learning workloads.**

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Deployment](#deployment)
- [Usage](#usage)
- [CI/CD Pipeline](#cicd-pipeline)
- [Monitoring](#monitoring)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

This project implements a **cloud-edge collaborative AI benchmarking framework** using the [Ianvs distributed synergy AI benchmarking system](https://github.com/kubeedge/ianvs). It demonstrates real-world federated learning workflows across Kubernetes clusters with KubeEdge-managed edge nodes.

### Why This Project?

- **LFX Mentorship Ready**: Directly aligned with Ianvs restoration and enhancement goals
- **Production Architecture**: Multi-stage Docker builds, K8s best practices, CI/CD automation
- **Resume-Worthy**: Demonstrates cloud-native, edge computing, and distributed AI expertise
- **Hands-On Learning**: Real implementation of federated learning benchmarking

### Key Technologies

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Orchestration** | Kubernetes 1.25+ | Container orchestration and workload management |
| **Edge Computing** | KubeEdge 1.12+ | Cloud-edge collaborative infrastructure |
| **AI Framework** | Ianvs | Distributed AI benchmarking and evaluation |
| **Dashboard** | Streamlit + Plotly | Real-time metrics visualization |
| **CI/CD** | GitHub Actions | Automated testing and deployment |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Cloud Control Plane                      │
│  ┌────────────────┐           ┌─────────────────────────┐   │
│  │  Ianvs Master  │◄─────────►│  Dashboard (Streamlit)  │   │
│  │  (Benchmark    │           │  - Metrics Visualization │   │
│  │   Orchestrator)│           │  - Job Monitoring        │   │
│  └────────┬───────┘           └─────────────────────────┘   │
│           │                                                  │
│           │ FedAvg Aggregation                               │
└───────────┼──────────────────────────────────────────────────┘
            │
            ├─────────────┬─────────────┬─────────────┐
            ▼             ▼             ▼             ▼
    ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐
    │Edge Node 1│ │Edge Node 2│ │Edge Node 3│ │Edge Node N│
    │           │ │           │ │           │ │           │
    │ Local     │ │ Local     │ │ Local     │ │ Local     │
    │ Training  │ │ Training  │ │ Training  │ │ Training  │
    │           │ │           │ │           │ │           │
    │ Inference │ │ Inference │ │ Inference │ │ Inference │
    └───────────┘ └───────────┘ └───────────┘ └───────────┘
```

### Component Breakdown

#### 🌩️ Cloud Components
- **Ianvs Master**: Federated learning orchestrator, aggregates edge model updates
- **Dashboard**: Real-time visualization of benchmarking metrics (accuracy, latency, bandwidth)
- **Persistent Storage**: Benchmark results, model checkpoints, configuration

#### 🌐 Edge Components
- **Edge Workers**: Local training on distributed datasets
- **Inference Engines**: Low-latency edge inference
- **Device Managers**: IoT device integration via KubeEdge

---

## ✨ Features

### ✅ Core Functionality
- [x] **Federated Learning Benchmark** - FedAvg algorithm with 3+ edge clients
- [x] **Multi-Metric Evaluation** - Accuracy, F1, precision, recall, latency, bandwidth
- [x] **Cloud-Edge Synchronization** - Model aggregation and distribution
- [x] **Environment Validation** - Doctor script checks K8s, KubeEdge, dependencies
- [x] **Interactive Dashboard** - Streamlit-based real-time metrics visualization

### 🔧 DevOps & Infrastructure
- [x] **Kubernetes Native** - Deployments, Services, ConfigMaps, PVCs
- [x] **KubeEdge Integration** - EdgeApplications, DeviceModels
- [x] **Multi-Stage Docker Builds** - Optimized image sizes (<200MB)
- [x] **CI/CD Pipeline** - GitHub Actions for testing, building, security scanning
- [x] **Makefile Automation** - One-command build/deploy/test

### 📊 Benchmarking Capabilities
- [x] Algorithm comparison (FedAvg, FedProx extensible)
- [x] Training convergence visualization
- [x] Edge node performance profiling
- [x] Radar chart metrics comparison
- [x] Configurable ranking criteria

---

## 📦 Prerequisites

### Required
- **Kubernetes cluster** (v1.25+) - [Install Minikube](https://minikube.sigs.k8s.io/docs/start/) or use cloud provider
- **kubectl** (v1.25+) - [Installation guide](https://kubernetes.io/docs/tasks/tools/)
- **Docker** (v20.10+) - [Get Docker](https://docs.docker.com/get-docker/)
- **Python** (3.8+) - For local development

### Optional (for KubeEdge features)
- **KubeEdge** (v1.12+) - [KubeEdge Installation](https://kubeedge.io/en/docs/setup/install-with-keadm/)
- **Edge nodes** - Raspberry Pi, NUC, or VM with KubeEdge runtime

### Development Tools
```bash
# Clone repository
git clone https://github.com/yourusername/ianvs-benchmark.git
cd ianvs-benchmark/repo

# Install Python dependencies (local testing)
pip install -r runner/requirements.txt
pip install -r dashboard/requirements.txt
```

---

## 🚀 Quick Start

### Option 1: Local Kubernetes (Minikube)

```bash
# Start Minikube cluster
minikube start --cpus=4 --memory=8192

# Enable necessary addons
minikube addons enable metrics-server

# Build Docker images (uses Minikube's Docker daemon)
eval $(minikube docker-env)
make build-all

# Deploy to Kubernetes
make deploy

# Access dashboard
kubectl port-forward -n ianvs-benchmark svc/ianvs-dashboard 8501:8501
# Open http://localhost:8501
```

### Option 2: Cloud Kubernetes (GKE, EKS, AKS)

```bash
# Configure kubectl for your cluster
# (Refer to cloud provider docs)

# Build and push images to registry
export IMAGE_REGISTRY=ghcr.io/yourusername
make build-all
make push-all

# Update k8s/cloud-deployment.yaml and k8s/edge-deployment.yaml
# Change image references to your registry

# Deploy
kubectl apply -f k8s/

# Get dashboard URL
kubectl get svc -n ianvs-benchmark ianvs-dashboard
# Access via NodePort or LoadBalancer IP
```

### Validate Environment

```bash
# Run environment doctor
cd runner
python doctor.py

# Expected output:
# ✓ Python Version: 3.10.x
# ✓ Kubernetes Cluster: accessible
# ✓ Config files: valid
```

---

## 📂 Project Structure

```
repo/
├── dashboard/                      # Streamlit dashboard
│   ├── app.py                     # Main dashboard application
│   ├── requirements.txt           # Python dependencies
│   └── docker/
│       └── Dockerfile.dashboard   # Multi-stage Docker build
│
├── runner/                        # Benchmarking runner
│   ├── doctor.py                  # Environment validation script
│   ├── requirements.txt           # Python dependencies
│   ├── configs/                   # Ianvs configuration files
│   │   ├── algorithm.yaml         # FedAvg algorithm config
│   │   ├── testenv.yaml           # Test environment (dataset, metrics)
│   │   └── benchmarkingjob.yaml   # Benchmark job specification
│   ├── docker/
│   │   ├── Dockerfile.runner      # Multi-stage Docker build
│   │   └── entrypoint.sh          # Container entrypoint script
│   └── workspace/                 # Runtime workspace (gitignored)
│       └── results/               # Benchmark results output
│
├── k8s/                           # Kubernetes manifests
│   ├── namespace.yaml             # ianvs-benchmark namespace
│   ├── configmap.yaml             # Ianvs configs as ConfigMap
│   ├── pvc.yaml                   # Persistent volume claim
│   ├── cloud-deployment.yaml      # Cloud master deployment
│   ├── edge-deployment.yaml       # Edge worker DaemonSet
│   ├── service.yaml               # K8s services (dashboard, master)
│   ├── kubeedge-edgeapp.yaml      # KubeEdge EdgeApplication
│   └── kubeedge-device.yaml       # KubeEdge DeviceModel
│
├── .github/
│   └── workflows/
│       └── ci.yaml                # GitHub Actions CI/CD pipeline
│
├── Makefile                       # Build and deployment automation
├── .gitignore                     # Git ignore patterns
└── README.md                      # This file
```

---

## ⚙️ Configuration

### Ianvs Configuration Files

#### `algorithm.yaml` - Federated Learning Algorithm
```yaml
algorithm:
  paradigm_type: "federatedlearning"
  modules:
    - type: "basemodel"
      hyperparameters:
        learning_rate: 0.001
        batch_size: 32
    - type: "aggregation"
      name: "FedAvg"  # Federated Averaging
```

#### `testenv.yaml` - Test Environment
```yaml
testenv:
  dataset:
    name: "MNIST"
  metrics:
    - accuracy
    - f1_score
    - inference_latency
  edge_nodes:
    - name: "edge-node-1"
      resources: { cpu: "2", memory: "4Gi" }
```

#### `benchmarkingjob.yaml` - Benchmark Job
```yaml
benchmarkingjob:
  name: "federated_learning_edge_benchmark"
  execution:
    mode: "distributed"
    parallelism: 3  # 3 edge nodes
  rank:
    sort_by:
      - name: "accuracy"
        weight: 0.4
```

### Customization

**Change dataset**: Edit `testenv.yaml` → `dataset.name`  
**Add algorithms**: Add new algorithm config in `algorithm.yaml`  
**Adjust resources**: Modify `k8s/cloud-deployment.yaml` resource limits  
**Change metrics**: Add custom metrics in `testenv.yaml` → `metrics`

---

## 🚀 Deployment

### Step-by-Step Deployment

#### 1. Build Docker Images
```bash
# Local registry (Minikube)
eval $(minikube docker-env)
make build-all

# Remote registry (GitHub Container Registry)
export IMAGE_REGISTRY=ghcr.io/yourusername
docker login ghcr.io
make build-all
make push-all
```

#### 2. Deploy to Kubernetes
```bash
# Create namespace and resources
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/pvc.yaml

# Deploy cloud and edge components
kubectl apply -f k8s/cloud-deployment.yaml
kubectl apply -f k8s/edge-deployment.yaml
kubectl apply -f k8s/service.yaml

# (Optional) KubeEdge components
kubectl apply -f k8s/kubeedge-edgeapp.yaml
kubectl apply -f k8s/kubeedge-device.yaml
```

#### 3. Verify Deployment
```bash
# Check pods
kubectl get pods -n ianvs-benchmark

# Expected output:
# NAME                                   READY   STATUS    RESTARTS   AGE
# ianvs-cloud-master-xxxx-yyyy           2/2     Running   0          2m
# ianvs-edge-worker-aaaa                 1/1     Running   0          2m
# ianvs-edge-worker-bbbb                 1/1     Running   0          2m

# Check logs
kubectl logs -n ianvs-benchmark deployment/ianvs-cloud-master -c benchmark-runner
```

#### 4. Access Dashboard
```bash
# Port forward
kubectl port-forward -n ianvs-benchmark svc/ianvs-dashboard 8501:8501

# Open browser
open http://localhost:8501
```

---

## 📊 Usage

### Running Benchmarks

#### Via Dashboard
1. Access dashboard at `http://localhost:8501`
2. View real-time metrics: accuracy, loss, latency
3. Compare edge node performance
4. Download benchmark reports

#### Via Command Line
```bash
# Execute benchmark job
kubectl exec -n ianvs-benchmark deployment/ianvs-cloud-master -c benchmark-runner -- \
  python3 /app/doctor.py

# View results
kubectl exec -n ianvs-benchmark deployment/ianvs-cloud-master -c benchmark-runner -- \
  cat /app/workspace/results/round_10.json
```

### Monitoring Logs

```bash
# Cloud master logs
kubectl logs -n ianvs-benchmark deployment/ianvs-cloud-master -c benchmark-runner -f

# Edge worker logs
kubectl logs -n ianvs-benchmark daemonset/ianvs-edge-worker -f

# Dashboard logs
kubectl logs -n ianvs-benchmark deployment/ianvs-cloud-master -c dashboard -f
```

---

## 🔄 CI/CD Pipeline

GitHub Actions workflow ([`.github/workflows/ci.yaml`](.github/workflows/ci.yaml)):

### Pipeline Stages

1. **Test Runner** - Validate Python code, config files
2. **Test Dashboard** - Check Streamlit app imports
3. **Build Docker Images** - Multi-arch builds (amd64, arm64)
4. **Validate K8s Manifests** - Kubeconform syntax checking
5. **Security Scan** - Trivy vulnerability scanning
6. **Deploy to Staging** - (Optional) Auto-deploy on `main` branch

### Triggering CI

```bash
# Push to main branch
git push origin main

# Create pull request
gh pr create --title "Feature: XYZ"

# Manual trigger
gh workflow run ci.yaml
```

---

## 📈 Monitoring

### Dashboard Features

| View | Description |
|------|-------------|
| **Overview** | Key metrics: accuracy, F1, latency, bandwidth |
| **Training Progress** | Line charts showing convergence over rounds |
| **Edge Nodes** | Per-node accuracy, latency, sample counts |
| **Radar Chart** | Multi-metric algorithm comparison |
| **Config Viewer** | Live view of YAML configurations |

### Metrics Collected

- **Accuracy**: Model prediction accuracy (%)
- **F1 Score**: Harmonic mean of precision/recall
- **Precision/Recall**: Classification metrics
- **Inference Latency**: Time per prediction (ms)
- **Bandwidth Usage**: Network data transfer (MB)

---

## 🛠️ Troubleshooting

### Common Issues

#### Pod CrashLoopBackOff
```bash
# Check logs
kubectl logs -n ianvs-benchmark <pod-name>

# Verify image exists
docker images | grep ianvs

# Rebuild and redeploy
make build-all deploy
```

#### Dashboard Not Accessible
```bash
# Check service
kubectl get svc -n ianvs-benchmark ianvs-dashboard

# Port forward directly to pod
kubectl port-forward -n ianvs-benchmark pod/<dashboard-pod> 8501:8501
```

#### KubeEdge Nodes Not Showing
```bash
# Label nodes as edge
kubectl label nodes <node-name> node-role.kubernetes.io/edge=

# Verify labels
kubectl get nodes --show-labels | grep edge
```

#### Doctor Script Failures
```bash
# Run locally
cd runner
python doctor.py

# Check specific component
python -c "
from doctor import EnvironmentDoctor
d = EnvironmentDoctor()
d.check_kubernetes_cluster()
d.display_results()
"
```

---

## 🤝 Contributing

Contributions welcome! This project aligns with [Ianvs LFX mentorship goals](https://github.com/kubeedge/ianvs/issues).

### Development Workflow

1. Fork repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Make changes
4. Run tests: `python -m pytest` (if tests exist)
5. Commit: `git commit -m 'Add amazing feature'`
6. Push: `git push origin feature/amazing-feature`
7. Open Pull Request

### Code Style

- Python: Follow PEP 8
- YAML: 2-space indentation
- Commits: Conventional Commits format

---

## 📄 License

This project is licensed under the **Apache License 2.0** - see [LICENSE](LICENSE) file.

---

## 🙏 Acknowledgments

- **[Ianvs Project](https://github.com/kubeedge/ianvs)** - Distributed AI benchmarking framework
- **[KubeEdge](https://kubeedge.io)** - Kubernetes edge computing platform
- **[CNCF](https://www.cncf.io)** - Cloud Native Computing Foundation

---

## 📞 Contact & Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/ianvs-benchmark/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/ianvs-benchmark/discussions)
- **Ianvs Slack**: [Join #ianvs channel](https://kubeedge.io/community/)

---

## 🎓 Learning Resources

- [Ianvs Documentation](https://ianvs.readthedocs.io)
- [KubeEdge Getting Started](https://kubeedge.io/en/docs/)
- [Federated Learning Guide](https://federated.withgoogle.com/)
- [Kubernetes Best Practices](https://kubernetes.io/docs/concepts/)

---

**Built with ❤️ for edge AI and cloud-native computing**

*Star ⭐ this repo if it helped you learn about edge AI benchmarking!*
