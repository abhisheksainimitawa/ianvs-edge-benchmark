#!/usr/bin/env python3
"""
Ianvs Benchmarking Dashboard - Real-time metrics visualization
Displays federated learning benchmarks, cloud-edge metrics, and algorithm comparisons
"""

import streamlit as st
import pandas as pd
import json
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
from datetime import datetime
import yaml

# Page configuration
st.set_page_config(
    page_title="Ianvs Edge AI Benchmarking",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .status-badge {
        padding: 0.25rem 0.75rem;
        border-radius: 1rem;
        font-weight: bold;
    }
    .status-running { background-color: #ffd700; color: #000; }
    .status-completed { background-color: #90EE90; color: #000; }
    .status-failed { background-color: #ff6b6b; color: #fff; }
</style>
""", unsafe_allow_html=True)

class IanvsDashboard:
    def __init__(self):
        self.workspace_path = Path("./runner/workspace/results")
        self.configs_path = Path("./runner/configs")
    
    def load_benchmark_results(self):
        """Load benchmark results from workspace"""
        # Mock data for demonstration (replace with actual Ianvs output parsing)
        return {
            "job_name": "federated_learning_edge_benchmark",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "completed",
            "algorithms": [
                {
                    "name": "FederatedAveraging",
                    "metrics": {
                        "accuracy": 0.9234,
                        "f1_score": 0.9156,
                        "precision": 0.9301,
                        "recall": 0.9015,
                        "inference_latency": 45.2,  # ms
                        "bandwidth_usage": 1.23  # MB
                    },
                    "rounds": 10,
                    "convergence_round": 7
                }
            ],
            "edge_nodes": [
                {
                    "name": "edge-node-1",
                    "samples": 1024,
                    "accuracy": 0.9189,
                    "avg_latency": 42.1,
                    "status": "active"
                },
                {
                    "name": "edge-node-2",
                    "samples": 987,
                    "accuracy": 0.9278,
                    "avg_latency": 38.9,
                    "status": "active"
                },
                {
                    "name": "edge-node-3",
                    "samples": 1105,
                    "accuracy": 0.9241,
                    "avg_latency": 54.3,
                    "status": "active"
                }
            ],
            "training_history": [
                {"round": 1, "accuracy": 0.7823, "loss": 0.4512, "latency": 89.3},
                {"round": 2, "accuracy": 0.8234, "loss": 0.3891, "latency": 76.2},
                {"round": 3, "accuracy": 0.8567, "loss": 0.3245, "latency": 68.5},
                {"round": 4, "accuracy": 0.8789, "loss": 0.2891, "latency": 61.2},
                {"round": 5, "accuracy": 0.8945, "loss": 0.2567, "latency": 55.8},
                {"round": 6, "accuracy": 0.9078, "loss": 0.2234, "latency": 51.3},
                {"round": 7, "accuracy": 0.9156, "loss": 0.1987, "latency": 47.9},
                {"round": 8, "accuracy": 0.9201, "loss": 0.1823, "latency": 46.1},
                {"round": 9, "accuracy": 0.9223, "loss": 0.1756, "latency": 45.5},
                {"round": 10, "accuracy": 0.9234, "loss": 0.1721, "latency": 45.2}
            ]
        }
    
    def render_header(self):
        """Render dashboard header"""
        st.markdown('<h1 class="main-header">🚀 Ianvs Edge AI Benchmarking Dashboard</h1>', unsafe_allow_html=True)
        st.markdown("**Cloud-Edge Collaborative Federated Learning Benchmark**")
        st.markdown("---")
    
    def render_overview(self, data):
        """Render overview metrics"""
        st.subheader("📊 Benchmark Overview")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Overall Accuracy",
                value=f"{data['algorithms'][0]['metrics']['accuracy']:.2%}",
                delta="+2.34%"
            )
        
        with col2:
            st.metric(
                label="F1 Score",
                value=f"{data['algorithms'][0]['metrics']['f1_score']:.4f}",
                delta="+0.0156"
            )
        
        with col3:
            st.metric(
                label="Avg Latency",
                value=f"{data['algorithms'][0]['metrics']['inference_latency']:.1f} ms",
                delta="-12.3 ms",
                delta_color="inverse"
            )
        
        with col4:
            st.metric(
                label="Bandwidth Used",
                value=f"{data['algorithms'][0]['metrics']['bandwidth_usage']:.2f} MB",
                delta="-0.45 MB",
                delta_color="inverse"
            )
        
        st.markdown("---")
    
    def render_training_progress(self, data):
        """Render training progress charts"""
        st.subheader("📈 Federated Learning Training Progress")
        
        df = pd.DataFrame(data['training_history'])
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Accuracy over rounds
            fig_acc = go.Figure()
            fig_acc.add_trace(go.Scatter(
                x=df['round'],
                y=df['accuracy'],
                mode='lines+markers',
                name='Accuracy',
                line=dict(color='#1f77b4', width=3),
                marker=dict(size=8)
            ))
            fig_acc.update_layout(
                title="Accuracy Improvement Across Rounds",
                xaxis_title="Federated Round",
                yaxis_title="Accuracy",
                hovermode='x unified',
                height=400
            )
            st.plotly_chart(fig_acc, use_container_width=True)
        
        with col2:
            # Loss over rounds
            fig_loss = go.Figure()
            fig_loss.add_trace(go.Scatter(
                x=df['round'],
                y=df['loss'],
                mode='lines+markers',
                name='Loss',
                line=dict(color='#ff7f0e', width=3),
                marker=dict(size=8)
            ))
            fig_loss.update_layout(
                title="Loss Reduction Across Rounds",
                xaxis_title="Federated Round",
                yaxis_title="Loss",
                hovermode='x unified',
                height=400
            )
            st.plotly_chart(fig_loss, use_container_width=True)
        
        # Latency trend
        fig_latency = go.Figure()
        fig_latency.add_trace(go.Scatter(
            x=df['round'],
            y=df['latency'],
            mode='lines+markers',
            name='Latency',
            line=dict(color='#2ca02c', width=3),
            marker=dict(size=8),
            fill='tozeroy'
        ))
        fig_latency.update_layout(
            title="Inference Latency Optimization",
            xaxis_title="Federated Round",
            yaxis_title="Latency (ms)",
            hovermode='x unified',
            height=300
        )
        st.plotly_chart(fig_latency, use_container_width=True)
        
        st.markdown("---")
    
    def render_edge_nodes(self, data):
        """Render edge node statistics"""
        st.subheader("🌐 Edge Nodes Performance")
        
        df_nodes = pd.DataFrame(data['edge_nodes'])
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Edge node comparison
            fig_nodes = go.Figure()
            
            fig_nodes.add_trace(go.Bar(
                name='Accuracy',
                x=df_nodes['name'],
                y=df_nodes['accuracy'],
                marker_color='#1f77b4'
            ))
            
            fig_nodes.add_trace(go.Bar(
                name='Avg Latency (ms)',
                x=df_nodes['name'],
                y=df_nodes['avg_latency'],
                marker_color='#ff7f0e',
                yaxis='y2'
            ))
            
            fig_nodes.update_layout(
                title="Edge Nodes: Accuracy vs Latency",
                xaxis_title="Edge Node",
                yaxis=dict(title="Accuracy", side='left'),
                yaxis2=dict(title="Latency (ms)", overlaying='y', side='right'),
                barmode='group',
                height=400
            )
            st.plotly_chart(fig_nodes, use_container_width=True)
        
        with col2:
            # Edge node details table
            st.markdown("**Edge Node Details**")
            for node in data['edge_nodes']:
                status_class = f"status-{node['status']}"
                st.markdown(f"""
                <div class="metric-card">
                    <h4>{node['name']}</h4>
                    <p><strong>Samples:</strong> {node['samples']}</p>
                    <p><strong>Accuracy:</strong> {node['accuracy']:.2%}</p>
                    <p><strong>Latency:</strong> {node['avg_latency']:.1f} ms</p>
                    <span class="status-badge {status_class}">{node['status'].upper()}</span>
                </div>
                """, unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("---")
    
    def render_metrics_radar(self, data):
        """Render radar chart for algorithm metrics"""
        st.subheader("🎯 Algorithm Performance Radar")
        
        metrics = data['algorithms'][0]['metrics']
        
        # Normalize metrics for radar chart
        categories = ['Accuracy', 'F1 Score', 'Precision', 'Recall']
        values = [
            metrics['accuracy'],
            metrics['f1_score'],
            metrics['precision'],
            metrics['recall']
        ]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name='FederatedAveraging',
            line=dict(color='#1f77b4', width=2),
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0.85, 1.0]
                )
            ),
            showlegend=True,
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
    
    def render_config_viewer(self):
        """Render configuration viewer"""
        st.subheader("⚙️ Configuration Viewer")
        
        config_file = st.selectbox(
            "Select Configuration",
            ["algorithm.yaml", "testenv.yaml", "benchmarkingjob.yaml"]
        )
        
        try:
            config_path = self.configs_path / config_file
            if config_path.exists():
                with open(config_path, 'r') as f:
                    config_content = f.read()
                st.code(config_content, language='yaml')
            else:
                st.warning(f"Configuration file {config_file} not found")
        except Exception as e:
            st.error(f"Error reading configuration: {str(e)}")
    
    def render_sidebar(self, data):
        """Render sidebar with job info"""
        with st.sidebar:
            st.image("https://via.placeholder.com/300x100/1f77b4/ffffff?text=Ianvs+Benchmark", use_container_width=True)
            
            st.markdown("### 📋 Job Information")
            st.markdown(f"**Job Name:** {data['job_name']}")
            st.markdown(f"**Timestamp:** {data['timestamp']}")
            
            status_color = {
                "completed": "🟢",
                "running": "🟡",
                "failed": "🔴"
            }
            st.markdown(f"**Status:** {status_color.get(data['status'], '⚪')} {data['status'].upper()}")
            
            st.markdown("---")
            
            st.markdown("### 🔧 Quick Actions")
            if st.button("🔄 Refresh Results"):
                st.rerun()
            
            if st.button("📥 Download Report"):
                st.info("Report download feature coming soon!")
            
            if st.button("🚀 Run New Benchmark"):
                st.info("Benchmark execution feature coming soon!")
            
            st.markdown("---")
            
            st.markdown("### 📚 Resources")
            st.markdown("- [Ianvs Docs](https://ianvs.readthedocs.io)")
            st.markdown("- [KubeEdge](https://kubeedge.io)")
            st.markdown("- [GitHub Repo](https://github.com)")
    
    def run(self):
        """Main dashboard render function"""
        self.render_header()
        
        # Load data
        data = self.load_benchmark_results()
        
        # Render sidebar
        self.render_sidebar(data)
        
        # Main content
        self.render_overview(data)
        self.render_training_progress(data)
        self.render_edge_nodes(data)
        self.render_metrics_radar(data)
        self.render_config_viewer()
        
        # Footer
        st.markdown("---")
        st.markdown(
            "<div style='text-align: center; color: #666;'>"
            "Built with Streamlit | Powered by Ianvs + KubeEdge | "
            f"© 2026"
            "</div>",
            unsafe_allow_html=True
        )

def main():
    dashboard = IanvsDashboard()
    dashboard.run()

if __name__ == "__main__":
    main()