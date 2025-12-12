"""ADK (Agent Development Kit) based agent implementation.

This module demonstrates how to build agents using Google's ADK framework.
ADK provides a clean interface for building AI agents with tools, memory,
and conversation management.
"""

from google.adk.agents import Agent
from google.adk.tools import FunctionTool


# Define custom tools that the agent can use
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
    # Only allow safe mathematical operations
    allowed_chars = set("0123456789+-*/(). ")
    if not all(c in allowed_chars for c in expression):
        return "Error: Invalid characters in expression. Only numbers and basic operators allowed."

    try:
        result = eval(expression)  # Safe because we validated the input
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"


def search_web(query: str) -> str:
    """Simulate a web search (placeholder for actual implementation).

    Args:
        query: The search query.

    Returns:
        Search results (simulated).
    """
    # In a real implementation, you'd integrate with a search API
    return f"Search results for '{query}': [This is a placeholder. Integrate with a real search API for production use.]"


def create_adk_agent(model_name: str = "gemini-2.0-flash") -> Agent:
    """Create an ADK-based agent with custom tools.

    Args:
        model_name: The name of the model to use (default: gemini-2.0-flash).

    Returns:
        A configured ADK Agent instance.
    """
    # Create tool instances
    tools = [
        FunctionTool(get_current_time),
        FunctionTool(calculate),
        FunctionTool(search_web),
    ]

    # Create the agent with a system instruction
    agent = Agent(
        name="assistant",
        model=model_name,
        description="A helpful AI assistant that can answer questions, perform calculations, and help with various tasks.",
        instruction="""You are a helpful and knowledgeable AI assistant. 

Your capabilities include:
- Answering questions on a wide range of topics
- Performing mathematical calculations
- Providing the current date and time
- Helping users think through problems

Always be:
- Accurate and helpful
- Clear and concise in your responses
- Honest about your limitations

When using tools, explain what you're doing and why.""",
        tools=tools,
    )

    return agent


# Example of a more specialized agent
def create_code_assistant(model_name: str = "gemini-2.0-flash") -> Agent:
    """Create a specialized coding assistant agent.

    Args:
        model_name: The name of the model to use.

    Returns:
        A configured ADK Agent for coding tasks.
    """

    def analyze_code(code: str, language: str = "python") -> str:
        """Analyze code for potential issues.

        Args:
            code: The code to analyze.
            language: The programming language.

        Returns:
            Analysis results.
        """
        # Placeholder - in production, integrate with a linter or static analyzer
        return f"Analyzed {language} code ({len(code)} characters). [Integrate with real analysis tools for production.]"

    tools = [
        FunctionTool(analyze_code),
        FunctionTool(get_current_time),
    ]

    agent = Agent(
        name="code_assistant",
        model=model_name,
        description="A specialized assistant for software development and coding tasks.",
        instruction="""You are an expert software developer and coding assistant.

Your expertise includes:
- Writing clean, efficient, and well-documented code
- Debugging and troubleshooting issues
- Explaining programming concepts clearly
- Reviewing code and suggesting improvements
- Best practices for software development

When helping with code:
1. Always explain your reasoning
2. Provide complete, working examples when possible
3. Consider edge cases and error handling
4. Follow language-specific conventions and best practices""",
        tools=tools,
    )

    return agent


