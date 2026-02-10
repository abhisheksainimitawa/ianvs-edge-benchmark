#!/bin/bash
set -e

echo "================================================"
echo "Ianvs Edge AI Benchmarking Runner"
echo "================================================"

# Determine node type
NODE_TYPE=${NODE_TYPE:-"cloud"}
echo "Node Type: $NODE_TYPE"

# Setup workspace
WORKSPACE_DIR=${IANVS_WORKSPACE:-"/app/workspace"}
mkdir -p "$WORKSPACE_DIR/results"
mkdir -p "$WORKSPACE_DIR/logs"

echo "Workspace: $WORKSPACE_DIR"

# Run environment doctor
echo ""
echo "Running environment validation..."
python3 /app/doctor.py

DOCTOR_EXIT_CODE=$?

if [ $DOCTOR_EXIT_CODE -eq 0 ]; then
    echo ""
    echo "✓ Environment validation passed"
    echo ""
    
    if [ "$NODE_TYPE" = "cloud" ]; then
        echo "Starting cloud master node..."
        # Cloud node: run benchmarking orchestrator
        python3 -c "
import time
import json
from datetime import datetime
from pathlib import Path

print('Cloud master orchestrating federated learning...')

workspace = Path('$WORKSPACE_DIR')
results_dir = workspace / 'results'
results_dir.mkdir(exist_ok=True)

# Simulate benchmark orchestration
for round_num in range(1, 11):
    print(f'Round {round_num}/10: Aggregating edge model updates...')
    
    result = {
        'round': round_num,
        'timestamp': datetime.now().isoformat(),
        'accuracy': 0.78 + (round_num * 0.015),
        'loss': 0.45 - (round_num * 0.025)
    }
    
    result_file = results_dir / f'round_{round_num}.json'
    with open(result_file, 'w') as f:
        json.dump(result, f, indent=2)
    
    time.sleep(10)

print('Benchmarking complete!')
"
    else
        echo "Starting edge worker node..."
        # Edge node: run local training
        python3 -c "
import time
import os

node_name = os.getenv('NODE_NAME', 'edge-unknown')
print(f'Edge worker {node_name} ready for federated learning...')

while True:
    print(f'[{node_name}] Training local model on edge data...')
    time.sleep(30)
"
    fi
else
    echo ""
    echo "✗ Environment validation failed (exit code: $DOCTOR_EXIT_CODE)"
    echo "Please fix errors before running benchmarks"
    exit $DOCTOR_EXIT_CODE
fi