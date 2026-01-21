"""Documentation Agent for Multi-Agent Framework using AutoGen."""

import logging
from typing import Dict, Any
from autogen import ConversableAgent

logger = logging.getLogger(__name__)


class DocumentationAgent:
    """
    AutoGen-based agent responsible for generating comprehensive documentation 
    for approved code.
    """

    def __init__(self, api_key: str, model: str = "gpt-4o", temperature: float = 0.3, base_url: str = None):
        """
        Initialize Documentation Agent using AutoGen.

        Args:
            api_key: OpenAI API key
            model: Model name to use
            temperature: Temperature for generation (0.0-1.0)
        """
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.base_url = base_url
        self.name = "TechnicalWriter"

        # Configure LLM settings
        llm_config = {
            "model": self.model,
            "api_key": self.api_key,
            "temperature": self.temperature,
            "max_completion_tokens": 2500,
            "cache_seed": None,  # Disable caching
        }
        
        if self.base_url:
            llm_config["base_url"] = self.base_url
        
        # System message for documentation
        system_message = """You are a technical documentation specialist.
Generate comprehensive documentation for Python code.

Documentation Structure:

# [Project Name]

## Overview
Brief description of functionality and purpose

## Installation
```bash
pip install -r requirements.txt
```

## Architecture
[Text-based component diagram or description of code structure]

## API Reference
### Class: ClassName
**Purpose:** [Description]

#### Method: method_name
**Parameters:**
- param1 (type): Description

**Returns:** type - Description

**Raises:**
- ExceptionType: When this occurs

**Example:**
```python
[Usage example]
```

## Usage Examples
[Practical examples showing how to use the code]

## Configuration
[Environment variables, config files, and settings]

## Error Handling
[Common errors and their solutions]

## Best Practices
[Recommended usage patterns]

## Troubleshooting
[Common issues and solutions]

Ensure documentation is clear, comprehensive, and includes practical examples."""

        # Initialize AutoGen ConversableAgent
        self.agent = ConversableAgent(
            name=self.name,
            system_message=system_message,
            llm_config=llm_config,
            human_input_mode="NEVER",
        )

    def generate_documentation(self, code: str, requirements: str = None) -> str:
        """
        Generate comprehensive documentation for code using AutoGen.

        Args:
            code: Python code to document
            requirements: Original requirements for context (optional)

        Returns:
            Documentation in Markdown format

        Raises:
            Exception: If generation fails
        """
        try:
            logger.info(f"[{self.name}] Generating documentation with AutoGen...")

            prompt = f"""Generate comprehensive documentation for the following Python code:

{code}

Include:
- Installation instructions
- Usage examples
- API reference with all classes/functions
- Configuration details
- Best practices
"""

            if requirements:
                prompt += f"""

Original Requirements:
{requirements}
"""

            # Generate response using AutoGen agent
            response = self.agent.generate_reply(
                messages=[{"role": "user", "content": prompt}]
            )
            
            # Validate response
            if response is None or response == "" or response == "None":
                raise ValueError("Failed to get valid response from API. Please check your API key and model configuration.")
            
            documentation = response if isinstance(response, str) else str(response)
            logger.info(f"[{self.name}] Documentation generation completed successfully")
            return documentation

        except Exception as e:
            logger.error(f"[{self.name}] Error generating documentation: {e}")
            raise

    def get_agent(self) -> ConversableAgent:
        """
        Get the underlying AutoGen agent.

        Returns:
            ConversableAgent instance
        """
        return self.agent


def create_documentation_agent(api_key: str, model: str, temperature: float = 0.3) -> DocumentationAgent:
    """
    Factory function to create a Documentation Agent.

    Args:
        api_key: OpenAI API key
        model: Model name
        temperature: Temperature for generation

    Returns:
        DocumentationAgent instance
    """
    return DocumentationAgent(api_key=api_key, model=model, temperature=temperature)
