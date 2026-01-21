"""Deployment Configuration Agent for Multi-Agent Framework using AutoGen."""

import logging
from typing import Dict, Any
from autogen import ConversableAgent

logger = logging.getLogger(__name__)


class DeploymentAgent:
    """
    AutoGen-based agent responsible for generating deployment scripts and configuration 
    for running the project.
    """

    def __init__(self, api_key: str, model: str = "gpt-4o", temperature: float = 0.2, base_url: str = None):
        """
        Initialize Deployment Agent using AutoGen.

        Args:
            api_key: OpenAI API key
            model: Model name to use
            temperature: Temperature for generation (0.0-1.0)
        """
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.base_url = base_url
        self.name = "DevOpsEngineer"

        # Configure LLM settings
        llm_config = {
            "model": self.model,
            "api_key": self.api_key,
            "temperature": self.temperature,
            "max_completion_tokens": 2000,
            "cache_seed": None,  # Disable caching
        }
        
        if self.base_url:
            llm_config["base_url"] = self.base_url
        
        # System message for deployment
        system_message = """You are a DevOps engineer specializing in containerization and deployment.
Generate production-ready deployment configurations.

Generate the following deployment files:

1. requirements.txt
List all Python dependencies with specific versions
Example:
flask==2.3.0
requests==2.31.0

2. Dockerfile
Multi-stage build for production deployment
Example:
```dockerfile
FROM python:3.10-slim as base
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "main.py"]
```

3. docker-compose.yml (if multi-service)
Service orchestration with proper networking
Include health checks, volume mounts, environment variables

4. deploy.sh
Bash script for automated deployment
Include build, test, and run steps

5. .env.example
Template for environment variables
List all required configuration

6. .dockerignore
Files to exclude from Docker build

Output Format:
## Deployment Configuration

### requirements.txt
```
[content]
```

### Dockerfile
```dockerfile
[content]
```

### docker-compose.yml
```yaml
[content]
```

### deploy.sh
```bash
[content]
```

### .env.example
```
[content]
```

### .dockerignore
```
[content]
```

### Deployment Instructions
[Step-by-step deployment guide]

Include:
- Security best practices (non-root user, minimal base image)
- Health checks and logging
- Port mappings
- Volume mounts for persistence
- Environment variable management
- Comments explaining each step"""

        # Initialize AutoGen ConversableAgent
        self.agent = ConversableAgent(
            name=self.name,
            system_message=system_message,
            llm_config=llm_config,
            human_input_mode="NEVER",
        )

    def generate_deployment_config(self, code: str, requirements: str = None) -> str:
        """
        Generate deployment configuration files using AutoGen.

        Args:
            code: Python code to deploy
            requirements: Original requirements for context (optional)

        Returns:
            Deployment configuration files

        Raises:
            Exception: If generation fails
        """
        try:
            logger.info(f"[{self.name}] Generating deployment configuration with AutoGen...")

            prompt = f"""Generate complete deployment configuration for the following Python code:

{code}

Create all necessary files for production deployment including:
- requirements.txt with all dependencies
- Dockerfile with multi-stage build
- docker-compose.yml (if needed)
- deploy.sh script
- .env.example
- .dockerignore
- Deployment instructions
"""

            if requirements:
                prompt += f"""

Original Requirements:
{requirements}

Ensure deployment configuration meets all requirements.
"""

            # Generate response using AutoGen agent
            response = self.agent.generate_reply(
                messages=[{"role": "user", "content": prompt}]
            )

            # Validate response
            if response is None or response == "" or response == "None":
                raise ValueError("Failed to get valid response from API. Please check your API key and model configuration.")
            
            deployment_config = response if isinstance(response, str) else str(response)
            logger.info(f"[{self.name}] Deployment configuration completed successfully")
            return deployment_config

        except Exception as e:
            logger.error(f"[{self.name}] Error generating deployment config: {e}")
            raise

    def generate_reply(self, messages: list) -> str:
        """
        Generate reply for AutoGen compatibility.

        Args:
            messages: List of message dictionaries

        Returns:
            Generated deployment configuration
        """
        if not messages:
            raise ValueError("Messages list cannot be empty")

        code = None
        requirements = None

        for message in messages:
            content = message.get("content", "")
            if "```python" in content or "def " in content or "class " in content:
                if "def test_" not in content:  # Skip test code
                    code = content
            elif "Functional Requirements" in content or "Technical Specifications" in content:
                requirements = content

        if code is None:
            code = messages[-1].get("content", "")

        return self.generate_deployment_config(code, requirements)

    def get_agent(self) -> ConversableAgent:
        """
        Get the underlying AutoGen agent.

        Returns:
            ConversableAgent instance
        """
        return self.agent


def create_deployment_agent(api_key: str, model: str, temperature: float = 0.2) -> DeploymentAgent:
    """
    Factory function to create a Deployment Agent.

    Args:
        api_key: OpenAI API key
        model: Model name
        temperature: Temperature for generation

    Returns:
        DeploymentAgent instance
    """
    return DeploymentAgent(api_key=api_key, model=model, temperature=temperature)
