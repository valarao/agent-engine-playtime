"""Tests for configuration management."""

import os
import pytest
from unittest.mock import patch


def test_config_from_env():
    """Test creating config from environment variables."""
    with patch.dict(
        os.environ,
        {
            "GOOGLE_CLOUD_PROJECT": "test-project",
            "GOOGLE_CLOUD_LOCATION": "us-west1",
            "MODEL_NAME": "gemini-pro",
        },
    ):
        from src.config import Config

        config = Config.from_env()

        assert config.project_id == "test-project"
        assert config.location == "us-west1"
        assert config.model_name == "gemini-pro"


def test_config_defaults():
    """Test config uses defaults when optional vars not set."""
    with patch.dict(
        os.environ,
        {"GOOGLE_CLOUD_PROJECT": "test-project"},
        clear=True,
    ):
        from src.config import Config

        config = Config.from_env()

        assert config.project_id == "test-project"
        assert config.location == "us-central1"  # default
        assert config.model_name == "gemini-2.0-flash"  # default


def test_config_missing_project():
    """Test that missing project ID raises an error."""
    with patch.dict(os.environ, {}, clear=True):
        from src.config import Config

        with pytest.raises(ValueError, match="GOOGLE_CLOUD_PROJECT"):
            Config.from_env()


