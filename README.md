# 🤖 Agent Engine Playtime

A Python playground for experimenting with [Google Cloud Vertex AI Agent Engine](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/overview) using the **ADK** (Agent Development Kit).

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- A Google Cloud project with Vertex AI API enabled
- `gcloud` CLI authenticated (`gcloud auth application-default login`)

### Installation

1. **Clone and set up the environment:**

```bash
cd agent-engine-playtime

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -e ".[dev]"
```

2. **Configure your environment:**

```bash
# Copy the example env file
cp env.example .env

# Edit .env with your settings
# GOOGLE_CLOUD_PROJECT=your-project-id
# GOOGLE_CLOUD_LOCATION=us-central1
```

3. **Run the agent locally:**

```bash
python3 examples/run_adk_local.py
```

## 📁 Project Structure

```
agent-engine-playtime/
├── src/
│   ├── config.py          # Configuration management
│   ├── utils.py           # Utility functions
│   ├── deploy.py          # Deployment utilities
│   └── agents/
│       └── adk_agent.py   # ADK-based agent implementation
├── examples/
│   ├── run_adk_local.py       # Run agent locally
│   └── query_deployed_agent.py # Query a deployed agent
├── tests/
├── requirements.txt       # Dependencies
├── pyproject.toml        # Project configuration
├── env.example           # Environment variables template
└── README.md
```

## 🛠️ Usage

### Running the Agent Locally

Test your agent locally before deploying:

```bash
python3 examples/run_adk_local.py
```

### Deploying to Agent Engine

Deploy your agent to Google Cloud:

```bash
# Deploy agent
python3 -m src.deploy deploy --name "my-agent"

# List deployed agents
python3 -m src.deploy list

# Delete an agent
python3 -m src.deploy delete --name "projects/xxx/locations/xxx/agentEngines/xxx"
```

### Querying Deployed Agents

Interact with your deployed agents:

```bash
# Interactive mode
python3 examples/query_deployed_agent.py --resource-name "projects/xxx/locations/xxx/agentEngines/xxx"

# Single query
python3 examples/query_deployed_agent.py \
  --resource-name "projects/xxx/locations/xxx/agentEngines/xxx" \
  --query "What's the weather like today?"
```

## 🔧 Customization

### Adding Custom Tools

Edit `src/agents/adk_agent.py`:

```python
from google.adk.tools import FunctionTool

def my_custom_tool(param: str) -> str:
    """Description of what this tool does.
    
    Args:
        param: Description of the parameter.
    
    Returns:
        Description of the return value.
    """
    # Your implementation here
    return f"Result for {param}"

# Add to the agent's tools list
tools = [
    FunctionTool(my_custom_tool),
    # ... other tools
]
```

## 🔗 Resources

- [Agent Engine Documentation](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/overview)
- [ADK Python Repository](https://github.com/google/adk-python)
- [Vertex AI SDK](https://cloud.google.com/python/docs/reference/aiplatform/latest)

## 📝 License

MIT License - feel free to use this for your own experiments!
