"""Utility functions for Agent Engine experiments."""

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

console = Console()


def print_header(title: str) -> None:
    """Print a styled header."""
    console.print(Panel(f"[bold cyan]{title}[/bold cyan]", expand=False))


def print_response(response: str, title: str = "Agent Response") -> None:
    """Print an agent response with formatting."""
    console.print(Panel(Markdown(response), title=title, border_style="green"))


def print_error(message: str) -> None:
    """Print an error message."""
    console.print(f"[bold red]Error:[/bold red] {message}")


def print_success(message: str) -> None:
    """Print a success message."""
    console.print(f"[bold green]✓[/bold green] {message}")


def print_info(message: str) -> None:
    """Print an info message."""
    console.print(f"[bold blue]ℹ[/bold blue] {message}")

