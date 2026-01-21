"""Test Case Generation Agent for Multi-Agent Framework using AutoGen."""

import logging
from typing import Dict, Any
from autogen import ConversableAgent

logger = logging.getLogger(__name__)


class TestAgent:
    """
    AutoGen-based agent responsible for creating comprehensive unit and integration tests 
    for code modules.
    """

    def __init__(self, api_key: str, model: str = "gpt-4o", temperature: float = 0.3, base_url: str = None):
        """
        Initialize Test Case Generation Agent using AutoGen.

        Args:
            api_key: OpenAI API key
            model: Model name to use
            temperature: Temperature for generation (0.0-1.0)
        """
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.base_url = base_url
        self.name = "QAEngineer"

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
        
        # System message for test generation
        system_message = """You are a Quality Assurance engineer specializing in test automation.
Generate comprehensive pytest test cases for Python code.

Test Structure:
```python
import pytest
from unittest.mock import Mock, patch, MagicMock

# Fixtures for test setup
@pytest.fixture
def sample_data():
    '''Fixture providing sample test data.'''
    return {...}

# Happy path tests - normal expected behavior
def test_function_name_success(sample_data):
    '''Test function with valid input.'''
    result = function_name(sample_data)
    assert result == expected_value
    assert isinstance(result, ExpectedType)

# Edge case tests - boundary values, empty data
def test_function_name_empty_input():
    '''Test function with empty input.'''
    with pytest.raises(ValueError) as exc_info:
        function_name(None)
    assert "expected error message" in str(exc_info.value)

def test_function_name_boundary_values():
    '''Test function with boundary values.'''
    assert function_name(0) == expected
    assert function_name(sys.maxsize) == expected

# Error handling tests - invalid inputs, exceptions
def test_function_name_invalid_type():
    '''Test function with invalid input type.'''
    with pytest.raises(TypeError):
        function_name("invalid")

# Integration tests - multi-function workflows
def test_integration_workflow():
    '''Test multiple functions working together.'''
    step1 = function_one()
    step2 = function_two(step1)
    assert step2 == expected_final_result

# Mock external dependencies
@patch('module.external_dependency')
def test_with_mocked_dependency(mock_dep):
    '''Test function with mocked external dependency.'''
    mock_dep.return_value = "mocked_value"
    result = function_using_dependency()
    assert result == expected
    mock_dep.assert_called_once()
```

Requirements:
- At least 3 tests per function (happy path, edge case, error case)
- Cover all public functions and methods
- Use descriptive test names following test_<function>_<scenario> pattern
- Include docstrings for complex tests
- Mock external dependencies (APIs, databases, file systems)
- Aim for >80% code coverage
- Test both positive and negative scenarios
- Include parametrized tests where appropriate

Generate complete, runnable pytest test files."""

        # Initialize AutoGen ConversableAgent
        self.agent = ConversableAgent(
            name=self.name,
            system_message=system_message,
            llm_config=llm_config,
            human_input_mode="NEVER",
        )

    def generate_tests(self, code: str, requirements: str = None) -> str:
        """
        Generate pytest test cases for code using AutoGen.

        Args:
            code: Python code to test
            requirements: Original requirements for context (optional)

        Returns:
            Pytest test code

        Raises:
            Exception: If generation fails
        """
        try:
            logger.info(f"[{self.name}] Generating test cases with AutoGen...")

            prompt = f"""Generate comprehensive pytest test cases for the following Python code:

{code}

Include:
- Unit tests for all functions
- Edge case tests
- Error handling tests
- Integration tests if multiple functions work together
- Mock external dependencies appropriately
"""

            if requirements:
                prompt += f"""

Original Requirements:
{requirements}

Ensure tests verify all requirements are met.
"""

            # Generate response using AutoGen agent
            response = self.agent.generate_reply(
                messages=[{"role": "user", "content": prompt}]
            )
            
            # Validate response
            if response is None or response == "" or response == "None":
                raise ValueError("Failed to get valid response from API. Please check your API key and model configuration.")
            
            tests = response if isinstance(response, str) else str(response)
            logger.info(f"[{self.name}] Test generation completed successfully")
            return tests

        except Exception as e:
            logger.error(f"[{self.name}] Error generating tests: {e}")
            raise

    def get_agent(self) -> ConversableAgent:
        """
        Get the underlying AutoGen agent.

        Returns:
            ConversableAgent instance
        """
        return self.agent


def create_test_agent(api_key: str, model: str, temperature: float = 0.3) -> TestAgent:
    """
    Factory function to create a Test Agent.

    Args:
        api_key: OpenAI API key
        model: Model name
        temperature: Temperature for generation

    Returns:
        TestAgent instance
    """
    return TestAgent(api_key=api_key, model=model, temperature=temperature)
