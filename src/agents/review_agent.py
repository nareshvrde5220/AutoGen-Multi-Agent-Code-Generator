"""Code Review Agent for Multi-Agent Framework using AutoGen."""

import logging
import re
from typing import Dict, Any, Tuple
from autogen import ConversableAgent

logger = logging.getLogger(__name__)


class ReviewAgent:
    """
    AutoGen-based agent responsible for reviewing generated code for correctness, 
    efficiency, security, and best practices.
    """

    def __init__(self, api_key: str, model: str = "gpt-4o", temperature: float = 0.4, base_url: str = None):
        """
        Initialize Code Review Agent using AutoGen.

        Args:
            api_key: OpenAI API key
            model: Model name to use
            temperature: Temperature for generation (0.0-1.0)
        """
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.base_url = base_url
        self.name = "CodeReviewer"
        
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
        
        # System message for code review
        system_message = """You are a Principal Software Engineer conducting code reviews.
Review code against these criteria:

1. CORRECTNESS: Verify logic matches requirements, no logic errors
2. SECURITY: Check for vulnerabilities (injection, XSS, hardcoded secrets, path traversal)
3. PERFORMANCE: Identify inefficient algorithms or memory issues
4. ERROR HANDLING: Ensure all exceptions are caught appropriately
5. READABILITY: Code should be self-documenting with clear variable names
6. TESTING: Code should be testable (no tight coupling)
7. BEST PRACTICES: Follow SOLID principles, PEP 8, proper use of type hints

Output Format:
## Review Status: [APPROVED / NEEDS_REVISION]

### Overall Assessment
[Brief summary of code quality]

### Issues Found
- [Severity: HIGH/MEDIUM/LOW] [Category]: [Description with specific line references if possible]

### Recommendations
- [Specific improvement with code example if applicable]

### Security Concerns
- [List any security vulnerabilities]

### Performance Considerations
- [List performance issues or optimization opportunities]

If status is NEEDS_REVISION, provide clear, actionable feedback for the developer.
If status is APPROVED, the code meets all quality standards."""

        # Initialize AutoGen ConversableAgent
        self.agent = ConversableAgent(
            name=self.name,
            system_message=system_message,
            llm_config=llm_config,
            human_input_mode="NEVER",
        )

    def review_code(self, code: str, requirements: str = None) -> str:
        """
        Review Python code and provide feedback using AutoGen.

        Args:
            code: Python code to review
            requirements: Original requirements for context (optional)

        Returns:
            Review feedback with status (APPROVED or NEEDS_REVISION)

        Raises:
            Exception: If generation fails
        """
        try:
            logger.info(f"[{self.name}] Reviewing code with AutoGen...")

            prompt = f"""Review the following Python code:

{code}
"""

            if requirements:
                prompt += f"""

Original Requirements:
{requirements}

Verify the code implements all requirements correctly.
"""

            # Generate response using AutoGen agent
            response = self.agent.generate_reply(
                messages=[{"role": "user", "content": prompt}]
            )

            # Validate response
            if response is None or response == "" or response == "None":
                raise ValueError("Failed to get valid response from API. Please check your API key and model configuration.")

            review_feedback = response if isinstance(response, str) else str(response)
            logger.info(f"[{self.name}] Code review completed successfully")

            # Log the review status
            if "APPROVED" in review_feedback:
                logger.info(f"[{self.name}] Code APPROVED")
            elif "NEEDS_REVISION" in review_feedback:
                logger.warning(f"[{self.name}] Code NEEDS_REVISION")

            return review_feedback

        except Exception as e:
            logger.error(f"[{self.name}] Error reviewing code: {e}")
            raise

    def is_approved(self, review_feedback: str) -> bool:
        """
        Check if code is approved based on review feedback.

        Args:
            review_feedback: Review feedback text

        Returns:
            True if code is approved, False otherwise
        """
        return "APPROVED" in review_feedback and "NEEDS_REVISION" not in review_feedback

    def extract_issues(self, review_feedback: str) -> list:
        """
        Extract issues from review feedback.

        Args:
            review_feedback: Review feedback text

        Returns:
            List of issues found
        """
        issues = []
        lines = review_feedback.split('\n')

        for line in lines:
            if line.strip().startswith('-') and any(
                severity in line for severity in ['HIGH', 'MEDIUM', 'LOW']
            ):
                issues.append(line.strip())

        return issues

    def generate_reply(self, messages: list) -> str:
        """
        Generate reply for AutoGen compatibility.

        Args:
            messages: List of message dictionaries

        Returns:
            Review feedback
        """
        if not messages:
            raise ValueError("Messages list cannot be empty")

        code = None
        requirements = None

        for message in messages:
            content = message.get("content", "")
            # Check if message contains code (has python syntax)
            if "```python" in content or "def " in content or "class " in content:
                code = content
            elif "Functional Requirements" in content or "Technical Specifications" in content:
                requirements = content

        if code is None:
            code = messages[-1].get("content", "")

        return self.review_code(code, requirements)

    def get_agent(self) -> ConversableAgent:
        """
        Get the underlying AutoGen agent.

        Returns:
            ConversableAgent instance
        """
        return self.agent


def create_review_agent(api_key: str, model: str, temperature: float = 0.4) -> ReviewAgent:
    """
    Factory function to create a Review Agent.

    Args:
        api_key: OpenAI API key
        model: Model name
        temperature: Temperature for generation

    Returns:
        ReviewAgent instance
    """
    return ReviewAgent(api_key=api_key, model=model, temperature=temperature)
