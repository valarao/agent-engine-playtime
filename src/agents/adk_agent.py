"""ADK (Agent Development Kit) based agent implementation.

This module demonstrates how to build agents using Google's ADK framework.
ADK provides a clean interface for building AI agents with tools, memory,
and conversation management.

Includes MCP (Model Context Protocol) integration for Google Cloud Storage.
"""

from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters


# ============== Basic Tools ==============

def get_current_time() -> str:
    """Get the current date and time.

    Returns:
        A string with the current date and time.
    """
    from datetime import datetime
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
        return "Error: Invalid characters in expression. Only numbers and basic operators allowed."

    try:
        result = eval(expression)  # Safe because we validated the input
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"


# ============== Agent Creation ==============

def create_adk_agent(model_name: str = "gemini-2.0-flash") -> Agent:
    """Create an ADK-based agent with custom tools (without MCP).

    Args:
        model_name: The name of the model to use (default: gemini-2.0-flash).

    Returns:
        A configured ADK Agent instance.
    """
    tools = [
        FunctionTool(get_current_time),
        FunctionTool(calculate),
    ]

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


async def create_adk_agent_with_gcs_mcp(model_name: str = "gemini-2.0-flash") -> Agent:
    """Create an ADK agent with Google Cloud Storage via MCP.

    This function creates an agent that can interact with GCS using the
    @google-cloud/storage-mcp Node.js MCP server.

    Args:
        model_name: The name of the model to use (default: gemini-2.0-flash).

    Returns:
        A configured ADK Agent instance with GCS tools.
    """
    # Basic tools
    basic_tools = [
        FunctionTool(get_current_time),
        FunctionTool(calculate),
    ]

    # Connect to the GCS MCP server using npx (auto-downloads if needed)
    gcs_mcp_tools, exit_stack = await MCPToolset.from_server(
        connection_params=StdioServerParameters(
            command="npx",
            args=["-y", "@google-cloud/storage-mcp"],
        )
    )

    # Combine basic tools with MCP tools
    all_tools = basic_tools + gcs_mcp_tools

    agent = Agent(
        name="gcs_assistant",
        model=model_name,
        description="A helpful AI assistant with Google Cloud Storage capabilities.",
        instruction="""You are a helpful AI assistant with access to Google Cloud Storage.

Your capabilities include:
- Managing files in Google Cloud Storage (list, read, write, delete)
- Answering questions on a wide range of topics
- Performing mathematical calculations
- Providing the current date and time

When working with GCS:
- Always confirm bucket and file names with the user before making changes
- Be careful with delete operations - ask for confirmation
- Explain what you're doing when accessing storage

Always be accurate, helpful, and concise.""",
        tools=all_tools,
    )

    # Return both agent and exit_stack for proper cleanup
    return agent, exit_stack


# ============== Agent for ADK folder structure ==============
# This is used by `adk web` command

root_agent = create_adk_agent()
