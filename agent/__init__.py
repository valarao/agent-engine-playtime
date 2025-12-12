"""ADK Agent module for deployment to Agent Engine."""

from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from datetime import datetime


# Define custom tools
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


# Create the root agent - this is what ADK looks for
root_agent = Agent(
    name="assistant",
    model="gemini-2.0-flash",
    description="A helpful AI assistant that can answer questions and perform calculations.",
    instruction="""You are a helpful and knowledgeable AI assistant. 

Your capabilities include:
- Answering questions on a wide range of topics
- Performing mathematical calculations
- Providing the current date and time
- Helping users think through problems

Always be accurate, helpful, and concise.""",
    tools=[
        FunctionTool(get_current_time),
        FunctionTool(calculate),
    ],
)

