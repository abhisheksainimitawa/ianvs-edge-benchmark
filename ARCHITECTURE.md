# Architecture Diagram

```
                    ┌─────────────────────────────────────────┐
                    │     Kubernetes Cluster (Cloud)          │
                    │                                          │
                    │  ┌────────────────────────────────────┐ │
                    │  │  Namespace: ianvs-benchmark        │ │
                    │  │                                    │ │
                    │  │  ┌──────────────────────────────┐ │ │
                    │  │  │  Cloud Master Deployment     │ │ │
                    │  │  │  ┌────────────────────────┐  │ │ │
                    │  │  │  │  Container: Runner     │  │ │ │
                    │  │  │  │  - FedAvg Aggregation │  │ │ │
                    │  │  │  │  - Model Distribution │  │ │ │
                    │  │  │  └────────────────────────┘  │ │ │
                    │  │  │  ┌────────────────────────┐  │ │ │
                    │  │  │  │  Container: Dashboard  │  │ │ │
                    │  │  │  │  - Streamlit UI       │  │ │ │
                    │  │  │  │  - Metrics Viz        │  │ │ │
                    │  │  │  └────────────────────────┘  │ │ │
                    │  │  └──────────────┬───────────────┘ │ │
                    │  │                 │                  │ │
                    │  │       ┌─────────┴─────────┐        │ │
                    │  │       │                   │        │ │
                    │  │       ▼                   ▼        │ │
                    │  │  ConfigMap           PersistentVC  │ │
                    │  │  (Ianvs Configs)     (Results)     │ │
                    │  └────────────────────────────────────┘ │
                    └──────────────┬───────────────────────────┘
                                   │
                                   │ KubeEdge Cloud-Edge Channel
                                   │
                    ┌──────────────┴───────────────────────────┐
                    │                                          │
          ┌─────────▼──────────┐                  ┌───────────▼─────────┐
          │   Edge Node 1      │                  │   Edge Node 2       │
          │  ┌──────────────┐  │                  │  ┌──────────────┐   │
          │  │  DaemonSet   │  │      ...         │  │  DaemonSet   │   │
          │  │  Pod         │  │                  │  │  Pod         │   │
          │  │              │  │                  │  │              │   │
          │  │ - Local      │  │                  │  │ - Local      │   │
          │  │   Training   │  │                  │  │   Training   │   │
          │  │ - Edge       │  │                  │  │ - Edge       │   │
          │  │   Inference  │  │                  │  │   Inference  │   │
          │  └──────────────┘  │                  │  └──────────────┘   │
          └────────────────────┘                  └─────────────────────┘

                    Data Flow:
                    ──────────
    1. Cloud distributes global model to edge nodes
    2. Edge nodes train on local data
    3. Edge nodes send model updates to cloud
    4. Cloud aggregates updates (FedAvg)
    5. Repeat for N rounds
    6. Dashboard visualizes metrics in real-time
```

## Component Interactions

### Federated Learning Workflow

1. **Initialization**
   - Cloud master loads initial model
   - Distributes to all edge nodes via KubeEdge

2. **Local Training (Edge)**
   - Each edge node trains on local dataset
   - Computes model gradients/weights
   - No raw data leaves edge

3. **Aggregation (Cloud)**
   - Collects model updates from all edges
   - Applies FedAvg algorithm
   - Computes global model

4. **Distribution (Cloud → Edge)**
   - Sends updated global model to edges
   - Repeats for configured rounds

5. **Evaluation**
   - Measures accuracy, F1, latency
   - Dashboard displays real-time metrics

### Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **UI** | Streamlit + Plotly | Dashboard visualization |
| **Orchestration** | Kubernetes | Container management |
| **Edge Runtime** | KubeEdge | Cloud-edge synchronization |
| **Framework** | Ianvs | Benchmarking engine |
| **CI/CD** | GitHub Actions | Automation |
| **Storage** | PersistentVolume | Results persistence |
