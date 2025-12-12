"""Deployment utilities for Agent Engine.

This module provides functions to deploy agents to Google Cloud's
Vertex AI Agent Engine for production use.
"""

import os
import vertexai
from vertexai import agent_engines
from rich.console import Console
from rich.panel import Panel

from dotenv import load_dotenv

load_dotenv()

console = Console()


def print_header(title: str) -> None:
    console.print(Panel(f"[bold cyan]{title}[/bold cyan]", expand=False))


def print_success(message: str) -> None:
    console.print(f"[bold green]✓[/bold green] {message}")


def print_error(message: str) -> None:
    console.print(f"[bold red]Error:[/bold red] {message}")


def print_info(message: str) -> None:
    console.print(f"[bold blue]ℹ[/bold blue] {message}")


def get_config():
    """Get configuration from environment."""
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable is required.")
    return {
        "project_id": project_id,
        "location": os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1"),
        "staging_bucket": os.getenv("AGENT_ENGINE_STAGING_BUCKET"),
        "model_name": os.getenv("MODEL_NAME", "gemini-2.0-flash"),
    }


def initialize_vertexai():
    """Initialize the Vertex AI SDK."""
    config = get_config()
    vertexai.init(
        project=config["project_id"],
        location=config["location"],
        staging_bucket=config["staging_bucket"],
    )
    print_success(
        f"Initialized Vertex AI for project '{config['project_id']}' in '{config['location']}'"
    )


def create_agent_for_deployment(model_name: str = "gemini-2.0-flash"):
    """Create an ADK agent for deployment.
    
    This function creates the agent inline to avoid import issues
    when deployed to Agent Engine.
    """
    from google.adk.agents import Agent
    from google.adk.tools import FunctionTool
    from datetime import datetime

    # Define tools inline (no external imports)
    def get_current_time() -> str:
        """Get the current date and time.

        Returns:
            A string with the current date and time.
        """
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def calculate(expression: str) -> str:
        """Evaluate a mathematical expression safely.

        Args:
            expression: A mathematical expression to evaluate (e.g., "2 + 2 * 3").

        Returns:
            The result of the calculation as a string.
        """
        allowed_chars = set("0123456789+-*/(). ")
        if not all(c in allowed_chars for c in expression):
            return "Error: Invalid characters in expression."
        try:
            result = eval(expression)
            return str(result)
        except Exception as e:
            return f"Error: {str(e)}"

    # Create tools
    tools = [
        FunctionTool(get_current_time),
        FunctionTool(calculate),
    ]

    # Create the agent
    agent = Agent(
        name="assistant",
        model=model_name,
        description="A helpful AI assistant that can answer questions and perform calculations.",
        instruction="""You are a helpful and knowledgeable AI assistant. 

Your capabilities include:
- Answering questions on a wide range of topics
- Performing mathematical calculations
- Providing the current date and time
- Helping users think through problems

Always be accurate, helpful, and concise.""",
        tools=tools,
    )

    return agent


def deploy_agent(
    display_name: str = "adk-playground-agent",
    description: str = "An ADK-based agent for experimentation",
) -> agent_engines.AgentEngine:
    """Deploy an ADK agent to Agent Engine.

    Args:
        display_name: Display name for the deployed agent.
        description: Description of the agent.

    Returns:
        The deployed AgentEngine instance.
    """
    print_header("Deploying ADK Agent to Agent Engine")

    # Initialize Vertex AI
    initialize_vertexai()

    config = get_config()
    
    # Check staging bucket
    if not config["staging_bucket"]:
        print_error(
            "AGENT_ENGINE_STAGING_BUCKET is required for deployment. "
            "Create a GCS bucket and add it to your .env file."
        )
        raise ValueError("Staging bucket not configured")

    # Create the agent inline (no external module imports)
    print_info("Creating ADK agent...")
    agent = create_agent_for_deployment(model_name=config["model_name"])

    # Deploy to Agent Engine
    print_info("Deploying to Agent Engine (this may take a few minutes)...")

    # Requirements needed in the cloud environment
    requirements = [
        "google-cloud-aiplatform[adk,agent_engines]>=1.87.0",
        "google-adk",
        "google-genai",
    ]

    try:
        remote_agent = agent_engines.create(
            agent_engine=agent,
            display_name=display_name,
            description=description,
            requirements=requirements,
        )

        print_success(f"Agent deployed successfully!")
        print_info(f"Resource name: {remote_agent.resource_name}")

        return remote_agent

    except Exception as e:
        print_error(f"Deployment failed: {str(e)}")
        raise


def list_deployed_agents() -> list:
    """List all deployed agents in the project.

    Returns:
        List of deployed AgentEngine instances.
    """
    print_header("Deployed Agents")

    initialize_vertexai()

    agents = agent_engines.list()

    if not agents:
        print_info("No agents deployed yet.")
        return []

    for agent in agents:
        console.print(f"  • [cyan]{agent.display_name}[/cyan]")
        console.print(f"    Resource: {agent.resource_name}")
        console.print()

    return list(agents)


def delete_agent(resource_name: str) -> None:
    """Delete a deployed agent.

    Args:
        resource_name: The resource name of the agent to delete.
    """
    print_header("Deleting Agent")

    initialize_vertexai()

    try:
        agent_engines.delete(resource_name)
        print_success(f"Agent '{resource_name}' deleted successfully!")
    except Exception as e:
        print_error(f"Failed to delete agent: {str(e)}")
        raise


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Deploy agents to Agent Engine")
    parser.add_argument(
        "action",
        choices=["deploy", "list", "delete"],
        help="Action to perform",
    )
    parser.add_argument(
        "--name",
        help="Display name for deployment or resource name for deletion",
    )
    parser.add_argument(
        "--description",
        default="Agent Engine playground agent",
        help="Description for the agent",
    )

    args = parser.parse_args()

    if args.action == "deploy":
        deploy_agent(
            display_name=args.name or "adk-playground-agent",
            description=args.description,
        )
    elif args.action == "list":
        list_deployed_agents()
    elif args.action == "delete":
        if not args.name:
            print_error("--name (resource name) is required for deletion")
        else:
            delete_agent(args.name)
