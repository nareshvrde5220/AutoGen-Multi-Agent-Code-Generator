"""Requirement Analysis Agent for Multi-Agent Framework using AutoGen."""

import logging
from typing import Dict, Any, Optional
from autogen import ConversableAgent

logger = logging.getLogger(__name__)


class RequirementAgent:
    """
    AutoGen-based agent responsible for transforming natural language input 
    into structured software requirements.
    """

    def __init__(self, api_key: str, model: str = "gpt-4o", temperature: float = 0.3, base_url: str = None):
        """
        Initialize Requirement Analysis Agent using AutoGen.

        Args:
            api_key: OpenAI API key
            model: Model name to use
            temperature: Temperature for generation (0.0-1.0)
            base_url: Custom API base URL (optional)
        """
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.base_url = base_url
        self.name = "RequirementAnalyst"
        
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
        
        # System message for requirement analysis
        system_message = """You are a senior Business Analyst specializing in software requirements.
Your task is to convert natural language descriptions into structured requirements.

Output Format:
## Project Title

### Functional Requirements
- [List each requirement clearly and concisely]

### Technical Specifications
- Programming Language: Python 3.10+
- Dependencies: [List required libraries]
- Input Format: [Specify expected input format]
- Output Format: [Specify expected output format]

### Acceptance Criteria
- [List testable conditions for each requirement]

### Constraints & Assumptions
- [List any constraints or assumptions]

### Data Structures & Models
- [Describe any data structures needed]

Be specific, clear, and ensure all requirements are testable and unambiguous."""

        # Initialize AutoGen ConversableAgent
        self.agent = ConversableAgent(
            name=self.name,
            system_message=system_message,
            llm_config=llm_config,
            human_input_mode="NEVER",
        )

    def analyze_requirements(self, user_input: str) -> str:
        """
        Analyze natural language input and generate structured requirements using AutoGen.

        Args:
            user_input: Natural language description of the requirements

        Returns:
            Structured requirements in Markdown format

        Raises:
            Exception: If agent interaction fails
        """
        try:
            logger.info(f"[{self.name}] Analyzing requirements with AutoGen...")

            prompt = f"""Convert the following natural language requirement into structured requirements:

{user_input}"""

            # Generate response using AutoGen agent
            logger.info(f"[{self.name}] Sending request to {self.model} (base_url: {self.base_url or 'default'})")
            response = self.agent.generate_reply(
                messages=[{"role": "user", "content": prompt}]
            )
            
            logger.info(f"[{self.name}] Raw response type: {type(response)}, value: {response}")
            
            # Validate response
            if response is None or response == "" or response == "None":
                raise ValueError(f"Failed to get valid response from API. Response was: {response}. Check if your custom API at {self.base_url} is running and returning proper responses.")
            
            requirements = response if isinstance(response, str) else str(response)
            logger.info(f"[{self.name}] Requirements analysis completed successfully")
            return requirements

        except Exception as e:
            logger.error(f"[{self.name}] Error analyzing requirements: {e}")
            raise

    def get_agent(self) -> ConversableAgent:
        """
        Get the underlying AutoGen agent.

        Returns:
            ConversableAgent instance
        """
        return self.agent


def create_requirement_agent(api_key: str, model: str, temperature: float = 0.3) -> RequirementAgent:
    """
    Factory function to create a Requirement Agent.

    Args:
        api_key: OpenAI API key
        model: Model name
        temperature: Temperature for generation

    Returns:
        RequirementAgent instance
    """
    return RequirementAgent(api_key=api_key, model=model, temperature=temperature)
