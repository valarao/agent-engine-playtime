#!/usr/bin/env python3
"""Query a deployed agent on Agent Engine.

This script demonstrates how to interact with an agent that has been
deployed to Agent Engine.

Usage:
    python examples/query_deployed_agent.py --resource-name "projects/xxx/locations/xxx/agentEngines/xxx"
"""

import sys
import argparse
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import vertexai
from vertexai import agent_engines

from src.config import get_config
from src.utils import print_header, print_response, print_info, print_error


def main():
    """Query a deployed agent."""
    parser = argparse.ArgumentParser(description="Query a deployed agent")
    parser.add_argument(
        "--resource-name",
        required=True,
        help="The resource name of the deployed agent",
    )
    parser.add_argument(
        "--query",
        help="Single query to send (interactive mode if not provided)",
    )

    args = parser.parse_args()

    print_header("Query Deployed Agent")

    config = get_config()

    # Initialize Vertex AI
    vertexai.init(
        project=config.project_id,
        location=config.location,
    )

    # Get the deployed agent
    print_info(f"Connecting to agent: {args.resource_name}")

    try:
        remote_agent = agent_engines.get(args.resource_name)
    except Exception as e:
        print_error(f"Failed to get agent: {str(e)}")
        return

    # Create a session for the conversation
    session = remote_agent.create_session(user_id="user-1")
    print_info(f"Session created: {session['id']}")
    print()

    if args.query:
        # Single query mode
        response = remote_agent.stream_query(
            user_id="user-1",
            session_id=session["id"],
            message=args.query,
        )

        full_response = ""
        for chunk in response:
            if hasattr(chunk, "content") and chunk.content:
                full_response += chunk.content

        print_response(full_response)
    else:
        # Interactive mode
        print_info("Interactive mode. Type 'quit' or 'exit' to stop.\n")

        while True:
            try:
                user_input = input("You: ").strip()

                if user_input.lower() in ["quit", "exit", "q"]:
                    print_info("Goodbye!")
                    break

                if not user_input:
                    continue

                response = remote_agent.stream_query(
                    user_id="user-1",
                    session_id=session["id"],
                    message=user_input,
                )

                full_response = ""
                for chunk in response:
                    if hasattr(chunk, "content") and chunk.content:
                        full_response += chunk.content

                if full_response:
                    print_response(full_response)
                print()

            except KeyboardInterrupt:
                print("\n")
                print_info("Interrupted. Goodbye!")
                break


if __name__ == "__main__":
    main()

