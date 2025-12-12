"""Configuration management for Agent Engine experiments."""

import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


@dataclass
class Config:
    """Application configuration."""

    # Google Cloud settings
    project_id: str
    location: str

    # Agent Engine settings
    staging_bucket: Optional[str] = None

    # Model settings
    model_name: str = "gemini-2.0-flash"

    @classmethod
    def from_env(cls) -> "Config":
        """Create config from environment variables."""
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        if not project_id:
            raise ValueError(
                "GOOGLE_CLOUD_PROJECT environment variable is required. "
                "Copy env.example to .env and set your project ID."
            )

        return cls(
            project_id=project_id,
            location=os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1"),
            staging_bucket=os.getenv("AGENT_ENGINE_STAGING_BUCKET"),
            model_name=os.getenv("MODEL_NAME", "gemini-2.0-flash"),
        )


def get_config() -> Config:
    """Get application configuration."""
    return Config.from_env()


