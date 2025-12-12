"""Deployment utilities for Agent Engine.

This module provides functions to deploy agents to Google Cloud's
Vertex AI Agent Engine for production use.
"""

import vertexai
from vertexai import agent_engines
from rich.console import Console

from src.config import get_config
from src.utils import print_header, print_success, print_error, print_info

console = Console()


def initialize_vertexai():
    """Initialize the Vertex AI SDK."""
    config = get_config()
    vertexai.init(
        project=config.project_id,
        location=config.location,
        staging_bucket=config.staging_bucket,
    )
    print_success(
        f"Initialized Vertex AI for project '{config.project_id}' in '{config.location}'"
    )


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
    from src.agents.adk_agent import create_adk_agent

    print_header("Deploying ADK Agent to Agent Engine")

    # Initialize Vertex AI
    initialize_vertexai()

    # Create the agent
    print_info("Creating ADK agent...")
    config = get_config()
    agent = create_adk_agent(model_name=config.model_name)

    # Deploy to Agent Engine
    print_info("Deploying to Agent Engine (this may take a few minutes)...")

    try:
        remote_agent = agent_engines.create(
            agent_engine=agent,
            display_name=display_name,
            description=description,
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
