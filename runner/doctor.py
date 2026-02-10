#!/usr/bin/env python3
"""
Ianvs Environment Doctor - Validates K8s, KubeEdge, and Ianvs setup
Run this before benchmarking to ensure all dependencies are ready
"""

import os
import sys
import subprocess
import yaml
import json
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print as rprint

console = Console()

@dataclass
class CheckResult:
    name: str
    passed: bool
    message: str
    severity: str = "error"  # error, warning, info

class EnvironmentDoctor:
    def __init__(self):
        self.results: List[CheckResult] = []
        self.config_dir = Path(__file__).parent / "configs"
    
    def run_command(self, cmd: List[str]) -> Tuple[bool, str]:
        """Execute shell command and return success status and output"""
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0, result.stdout + result.stderr
        except Exception as e:
            return False, str(e)
    
    def check_python_version(self):
        """Check Python version compatibility"""
        version = sys.version_info
        if version.major == 3 and version.minor >= 8:
            self.results.append(CheckResult(
                "Python Version",
                True,
                f"Python {version.major}.{version.minor}.{version.micro} ✓"
            ))
        else:
            self.results.append(CheckResult(
                "Python Version",
                False,
                f"Python 3.8+ required, found {version.major}.{version.minor}",
                "error"
            ))
    
    def check_kubernetes_cluster(self):
        """Check if kubectl is available and cluster is accessible"""
        success, output = self.run_command(["kubectl", "cluster-info"])
        
        if success:
            self.results.append(CheckResult(
                "Kubernetes Cluster",
                True,
                "K8s cluster is accessible ✓"
            ))
            
            # Check nodes
            success, output = self.run_command(["kubectl", "get", "nodes", "-o", "json"])
            if success:
                try:
                    nodes = json.loads(output)
                    node_count = len(nodes.get("items", []))
                    self.results.append(CheckResult(
                        "Kubernetes Nodes",
                        True,
                        f"Found {node_count} node(s) ✓",
                        "info"
                    ))
                except:
                    pass
        else:
            self.results.append(CheckResult(
                "Kubernetes Cluster",
                False,
                "Cannot connect to K8s cluster. Run: kubectl cluster-info",
                "error"
            ))
    
    def check_kubeedge(self):
        """Check if KubeEdge is installed"""
        # Check for edge nodes (nodes with kubeedge label)
        success, output = self.run_command([
            "kubectl", "get", "nodes",
            "-l", "node-role.kubernetes.io/edge",
            "-o", "json"
        ])
        
        if success:
            try:
                nodes = json.loads(output)
                edge_nodes = nodes.get("items", [])
                if edge_nodes:
                    self.results.append(CheckResult(
                        "KubeEdge Nodes",
                        True,
                        f"Found {len(edge_nodes)} edge node(s) ✓"
                    ))
                else:
                    self.results.append(CheckResult(
                        "KubeEdge Nodes",
                        False,
                        "No edge nodes found. Label nodes: kubectl label nodes <node> node-role.kubernetes.io/edge=",
                        "warning"
                    ))
            except:
                self.results.append(CheckResult(
                    "KubeEdge",
                    False,
                    "Error parsing edge nodes",
                    "warning"
                ))
        else:
            self.results.append(CheckResult(
                "KubeEdge",
                False,
                "Cannot query edge nodes. Ensure KubeEdge is installed",
                "warning"
            ))
    
    def check_ianvs_configs(self):
        """Validate Ianvs configuration files"""
        required_configs = ["algorithm.yaml", "testenv.yaml", "benchmarkingjob.yaml"]
        
        for config_file in required_configs:
            config_path = self.config_dir / config_file
            
            if config_path.exists():
                try:
                    with open(config_path, 'r') as f:
                        config = yaml.safe_load(f)
                    
                    if config and len(str(config)) > 20:  # Not just empty dict
                        self.results.append(CheckResult(
                            f"Config: {config_file}",
                            True,
                            f"{config_file} is valid ✓",
                            "info"
                        ))
                    else:
                        self.results.append(CheckResult(
                            f"Config: {config_file}",
                            False,
                            f"{config_file} is empty or invalid",
                            "error"
                        ))
                except Exception as e:
                    self.results.append(CheckResult(
                        f"Config: {config_file}",
                        False,
                        f"{config_file} YAML parsing error: {str(e)}",
                        "error"
                    ))
            else:
                self.results.append(CheckResult(
                    f"Config: {config_file}",
                    False,
                    f"{config_file} not found in {self.config_dir}",
                    "error"
                ))
    
    def check_dependencies(self):
        """Check Python dependencies"""
        required_packages = {
            "yaml": "pyyaml",
            "rich": "rich",
            "pandas": "pandas",
            "numpy": "numpy",
        }
        
        for import_name, package_name in required_packages.items():
            try:
                __import__(import_name)
                self.results.append(CheckResult(
                    f"Package: {package_name}",
                    True,
                    f"{package_name} installed ✓",
                    "info"
                ))
            except ImportError:
                self.results.append(CheckResult(
                    f"Package: {package_name}",
                    False,
                    f"{package_name} not installed. Run: pip install {package_name}",
                    "error"
                ))
    
    def check_workspace(self):
        """Check workspace directory structure"""
        workspace_dir = Path(__file__).parent / "workspace"
        
        if workspace_dir.exists():
            self.results.append(CheckResult(
                "Workspace Directory",
                True,
                f"Workspace exists at {workspace_dir} ✓",
                "info"
            ))
        else:
            self.results.append(CheckResult(
                "Workspace Directory",
                False,
                f"Workspace directory not found. Creating at {workspace_dir}",
                "warning"
            ))
            workspace_dir.mkdir(parents=True, exist_ok=True)
    
    def check_docker(self):
        """Check if Docker is available"""
        success, output = self.run_command(["docker", "--version"])
        
        if success:
            version = output.strip()
            self.results.append(CheckResult(
                "Docker",
                True,
                f"{version} ✓",
                "info"
            ))
        else:
            self.results.append(CheckResult(
                "Docker",
                False,
                "Docker not found. Required for containerized benchmarking",
                "warning"
            ))
    
    def display_results(self):
        """Display check results in a formatted table"""
        console.print("\n")
        console.print(Panel.fit(
            "[bold cyan]Ianvs Environment Doctor[/bold cyan]\n"
            "[dim]Validating K8s + KubeEdge + Ianvs Setup[/dim]",
            border_style="cyan"
        ))
        console.print("\n")
        
        # Create results table
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Check", style="cyan", width=30)
        table.add_column("Status", justify="center", width=10)
        table.add_column("Details", style="dim")
        
        errors = 0
        warnings = 0
        
        for result in self.results:
            if result.passed:
                status = "[green]✓ PASS[/green]"
            else:
                status = "[red]✗ FAIL[/red]" if result.severity == "error" else "[yellow]⚠ WARN[/yellow]"
                if result.severity == "error":
                    errors += 1
                else:
                    warnings += 1
            
            table.add_row(result.name, status, result.message)
        
        console.print(table)
        console.print("\n")
        
        # Summary
        total = len(self.results)
        passed = sum(1 for r in self.results if r.passed)
        
        if errors == 0 and warnings == 0:
            console.print(Panel(
                f"[bold green]✓ All checks passed ({passed}/{total})[/bold green]\n"
                "[dim]Environment is ready for Ianvs benchmarking[/dim]",
                border_style="green"
            ))
            return 0
        elif errors == 0:
            console.print(Panel(
                f"[bold yellow]⚠ {warnings} warning(s) ({passed}/{total} passed)[/bold yellow]\n"
                "[dim]Environment is usable but some features may not work[/dim]",
                border_style="yellow"
            ))
            return 0
        else:
            console.print(Panel(
                f"[bold red]✗ {errors} error(s), {warnings} warning(s)[/bold red]\n"
                "[dim]Fix errors before running benchmarks[/dim]",
                border_style="red"
            ))
            return 1
    
    def run_all_checks(self):
        """Run all environment checks"""
        console.print("[bold]Running environment checks...[/bold]\n")
        
        self.check_python_version()
        self.check_dependencies()
        self.check_docker()
        self.check_kubernetes_cluster()
        self.check_kubeedge()
        self.check_ianvs_configs()
        self.check_workspace()
        
        return self.display_results()

def main():
    doctor = EnvironmentDoctor()
    exit_code = doctor.run_all_checks()
    sys.exit(exit_code)

if __name__ == "__main__":
    main()