"""Coding Agent for Multi-Agent Framework using AutoGen."""

import logging
from typing import Dict, Any, Optional
from autogen import ConversableAgent

logger = logging.getLogger(__name__)


class CodingAgent:
    """
    AutoGen-based agent responsible for generating production-quality Python code 
    from structured requirements.
    """

    def __init__(self, api_key: str, model: str = "gpt-4o", temperature: float = 0.2, base_url: str = None):
        """
        Initialize Coding Agent using AutoGen.

        Args:
            api_key: OpenAI API key
            model: Model name to use (gpt-4o, etc.)
            temperature: Temperature for generation (0.0-1.0)
        """
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.base_url = base_url
        self.name = "SeniorDeveloper"
        
        # Configure LLM settings
        llm_config = {
            "model": self.model,
            "api_key": self.api_key,
            "temperature": self.temperature,
            "max_completion_tokens": 3000,
            "cache_seed": None,  # Disable caching
        }
        
        if self.base_url:
            llm_config["base_url"] = self.base_url
        
        # System message for code generation
        system_message = """You are an expert Python developer with 10+ years of experience.
Generate production-ready Python code based on structured requirements.

Code Standards:
- Use type hints for all functions
- Implement comprehensive error handling with try-except blocks
- Follow PEP 8 style guide
- Add docstrings (Google style) for all classes/functions
- Use logging instead of print statements
- Implement input validation
- Make code modular with single responsibility principle
- Include if __name__ == "__main__" block
- Add inline comments for complex logic
- Use appropriate data structures and algorithms
- Handle edge cases properly

Output ONLY the complete Python code with proper structure and comments.
Make the code production-ready, efficient, and maintainable."""

        # Initialize AutoGen ConversableAgent
        self.agent = ConversableAgent(
            name=self.name,
            system_message=system_message,
            llm_config=llm_config,
            human_input_mode="NEVER",
        )

    def generate_code(self, requirements: str, feedback: Optional[str] = None) -> str:
        """
        Generate Python code from requirements using AutoGen.

        Args:
            requirements: Structured requirements
            feedback: Optional feedback from code review for revision

        Returns:
            Generated Python code

        Raises:
            Exception: If generation fails
        """
        try:
            logger.info(f"[{self.name}] Generating code with AutoGen...")

            if feedback:
                prompt = f"""REVISION REQUEST

Previous code received the following feedback:
{feedback}

Please revise the code to address all issues raised.

Original Requirements:
{requirements}"""
            else:
                prompt = f"""Generate production-ready Python code for the following requirements:

{requirements}"""

            # Generate response using AutoGen agent
            response = self.agent.generate_reply(
                messages=[{"role": "user", "content": prompt}]
            )
            
            # Validate response
            if response is None or response == "" or response == "None":
                raise ValueError("Failed to get valid response from API. Please check your API key and model configuration.")
            
            code = response if isinstance(response, str) else str(response)
            logger.info(f"[{self.name}] Code generation completed successfully")
            return code

        except Exception as e:
            logger.error(f"[{self.name}] Error generating code: {e}")
            raise

    def get_agent(self) -> ConversableAgent:
        """
        Get the underlying AutoGen agent.

        Returns:
            ConversableAgent instance
        """
        return self.agent


def create_coding_agent(api_key: str, model: str, temperature: float = 0.2) -> CodingAgent:
    """
    Factory function to create a Coding Agent.

    Args:
        api_key: OpenAI API key
        model: Model name
        temperature: Temperature for generation

    Returns:
        CodingAgent instance
    """
    return CodingAgent(api_key=api_key, model=model, temperature=temperature)
