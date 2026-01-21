"""Configuration management for Multi-Agent Framework."""

import os
import yaml
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration manager for the multi-agent framework."""

    def __init__(self, config_path: str = None):
        """
        Initialize configuration manager.

        Args:
            config_path: Path to config.yaml file. If None, uses default path.
        """
        if config_path is None:
            # Get the project root directory
            project_root = Path(__file__).parent.parent.parent
            config_path = project_root / "config" / "config.yaml"

        self.config_path = Path(config_path)
        self.config_data = self._load_config()
        self._validate_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        try:
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing YAML configuration: {e}")

    def _validate_config(self):
        """Validate that required configuration keys exist."""
        required_keys = ['agents', 'pipeline']
        for key in required_keys:
            if key not in self.config_data:
                raise ValueError(f"Missing required configuration key: {key}")

    def get(self, *keys, default=None):
        """
        Get nested configuration value.

        Args:
            *keys: Sequence of keys for nested access
            default: Default value if key not found

        Returns:
            Configuration value or default
        """
        value = self.config_data
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        return value

    @property
    def openai_api_key(self) -> str:
        """Get OpenAI API key from environment variables."""
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        return api_key

    @property
    def model_name(self) -> str:
        """Get model name from config or environment variables."""
        return os.getenv('MODEL_NAME') or self.get('api', 'model_id', default='gpt-4o')

    @property
    def temperature(self) -> float:
        """Get default temperature from environment variables."""
        return float(os.getenv('TEMPERATURE', '0.3'))

    @property
    def max_iterations(self) -> int:
        """Get maximum iterations for feedback loop."""
        return int(os.getenv('MAX_ITERATIONS', '3'))

    @property
    def max_round(self) -> int:
        """Get maximum rounds for group chat."""
        return int(os.getenv('MAX_ROUND', '20'))

    def get_agent_config(self, agent_name: str) -> Dict[str, Any]:
        """
        Get configuration for a specific agent.

        Args:
            agent_name: Name of the agent (e.g., 'requirement_analyst')

        Returns:
            Dictionary containing agent configuration
        """
        agents = self.config_data.get('agents', {})
        if agent_name not in agents:
            raise ValueError(f"Agent configuration not found: {agent_name}")
        return agents[agent_name]

    def get_pipeline_config(self) -> Dict[str, Any]:
        """Get pipeline configuration."""
        return self.config_data.get('pipeline', {})

    def get_output_config(self) -> Dict[str, Any]:
        """Get output configuration."""
        return self.config_data.get('output', {})

    @property
    def output_dir(self) -> Path:
        """Get output directory path."""
        project_root = Path(__file__).parent.parent.parent
        return project_root / os.getenv('OUTPUT_DIR', 'output')

    @property
    def generated_code_dir(self) -> Path:
        """Get generated code directory path."""
        project_root = Path(__file__).parent.parent.parent
        return project_root / os.getenv('GENERATED_CODE_DIR', 'output/generated_code')

    @property
    def documentation_dir(self) -> Path:
        """Get documentation directory path."""
        project_root = Path(__file__).parent.parent.parent
        return project_root / os.getenv('DOCUMENTATION_DIR', 'output/documentation')

    @property
    def tests_dir(self) -> Path:
        """Get tests directory path."""
        project_root = Path(__file__).parent.parent.parent
        return project_root / os.getenv('TESTS_DIR', 'output/tests')

    def get_llm_config(self, temperature: float = None) -> Dict[str, Any]:
        """
        Get LLM configuration for AutoGen agents.

        Args:
            temperature: Temperature override. If None, uses default.

        Returns:
            Dictionary containing LLM configuration
        """
        return {
            "config_list": [{
                "model": self.model_name,
                "api_key": self.openai_api_key,
                "api_type": "openai"
            }],
            "temperature": temperature if temperature is not None else self.temperature
        }


# Global configuration instance
config = Config()
