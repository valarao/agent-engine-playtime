#!/usr/bin/env python3
"""Run an ADK agent locally for testing.

This script demonstrates how to run an ADK agent locally before deploying
to Agent Engine. Great for rapid iteration and testing.

Usage:
    python examples/run_adk_local.py
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from src.agents.adk_agent import create_adk_agent
from src.config import get_config
from src.utils import print_header, print_response, print_info


def main():
    """Run the ADK agent in an interactive loop."""
    print_header("ADK Agent - Local Testing")

    config = get_config()
    print_info(f"Project: {config.project_id}")
    print_info(f"Model: {config.model_name}")
    print()

    # Create the agent
    agent = create_adk_agent(model_name=config.model_name)

    # Create a session service for conversation memory
    session_service = InMemorySessionService()

    # Create a runner
    runner = Runner(
        agent=agent,
        app_name="agent-engine-playtime",
        session_service=session_service,
    )

    # Create a session
    session = session_service.create_session(
        app_name="agent-engine-playtime",
        user_id="local-user",
    )

    print_info("Agent ready! Type 'quit' or 'exit' to stop.\n")

    while True:
        try:
            user_input = input("You: ").strip()

            if user_input.lower() in ["quit", "exit", "q"]:
                print_info("Goodbye!")
                break

            if not user_input:
                continue

            # Create the content for the agent
            content = types.Content(
                role="user",
                parts=[types.Part(text=user_input)],
            )

            # Run the agent
            response_text = ""
            for event in runner.run(
                user_id="local-user",
                session_id=session.id,
                new_message=content,
            ):
                if hasattr(event, "content") and event.content:
                    for part in event.content.parts:
                        if hasattr(part, "text") and part.text:
                            response_text += part.text

            if response_text:
                print_response(response_text)
            print()

        except KeyboardInterrupt:
            print("\n")
            print_info("Interrupted. Goodbye!")
            break


if __name__ == "__main__":
    main()


