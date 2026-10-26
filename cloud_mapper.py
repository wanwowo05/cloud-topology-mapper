import json
from rich.console import Console
from rich.tree import Tree

console = Console()

cloud_architecture = {
    "VPC-Prod (vpc-0abcd1234) | 10.0.0.0/16": {
        "Public Subnet 1 (subnet-111) | 10.0.1.0/24": [
            "Internet Gateway (igw-01)",
            "Application Load Balancer (alb-web-prod)",
            "NAT Gateway (nat-0987)"
        ],
        "Private App Subnet (subnet-222) | 10.0.2.0/24": [
            "Web Server EC2 (i-0123) - [Running]",
            "Web Server EC2 (i-0456) - [Running]",
            "App Server EC2 (i-0789) - [Stopped]"
        ],
        "Secure DB Subnet (subnet-333) | 10.0.3.0/24": [
            "Amazon RDS PostgreSQL (db-prod-primary)",
            "Amazon RDS Standby (db-prod-replica)",
            "ElastiCache Redis Cluster (cache-prod)"
        ]
    }
}

def build_tree(data, tree):
    for key, value in data.items():
        if isinstance(value, dict):
            branch = tree.add(f"[bold cyan] {key}[/bold cyan]")
            build_tree(value, branch)
        elif isinstance(value, list):
            branch = tree.add(f"[bold magenta] {key}[/bold magenta]")
            for item in value:
                if "Running" in item:
                    branch.add(f"[bold green] {item}[/bold green]")
                elif "Stopped" in item:
                    branch.add(f"[bold red] {item}[/bold red]")
                elif "Gateway" in item or "Balancer" in item:
                    branch.add(f"[bold blue] {item}[/bold blue]")
                else:
                    branch.add(f"[bold yellow] {item}[/bold yellow]")
        else:
            tree.add(f"[white]{value}[/white]")

if __name__ == '__main__':
    root = Tree("[bold bright_blue] AWS Cloud Environment Topology[/bold bright_blue]")
    build_tree(cloud_architecture, root)
    console.print("\n")
    console.print(root)
    console.print("\n[dim]Audit complete: 3 Subnets, 9 Resources mapped successfully.[/dim]\n")
