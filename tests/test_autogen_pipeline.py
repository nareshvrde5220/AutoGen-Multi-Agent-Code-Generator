"""Tests for AutoGen-based Multi-Agent Framework Pipeline."""

import pytest
import os
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Add src to path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.orchestrator.autogen_pipeline import create_autogen_pipeline, AutoGenPipeline
from src.agents import (
    RequirementAgent,
    CodingAgent,
    ReviewAgent,
    DocumentationAgent,
    TestAgent,
    DeploymentAgent,
    UIAgent
)


@pytest.fixture
def mock_api_key():
    """Fixture providing a mock API key."""
    return "sk-test_api_key_12345"


@pytest.fixture
def mock_model():
    """Fixture providing a mock model name."""
    return "gpt-4o"


@pytest.fixture
def sample_requirement():
    """Fixture providing a sample requirement."""
    return "Create a Python function that calculates the factorial of a number"


@pytest.fixture
def sample_code():
    """Fixture providing sample Python code."""
    return """
def factorial(n: int) -> int:
    '''Calculate factorial of a number.'''
    if n < 0:
        raise ValueError("Number must be non-negative")
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)
"""


# Test RequirementAgent with AutoGen
class TestRequirementAgent:
    """Tests for RequirementAgent using AutoGen."""

    def test_requirement_agent_initialization(self, mock_api_key, mock_model):
        """Test RequirementAgent initialization with AutoGen."""
        agent = RequirementAgent(mock_api_key, mock_model)
        assert agent.name == "RequirementAnalyst"
        assert agent.model == mock_model
        assert agent.temperature == 0.3
        assert hasattr(agent, 'agent')  # Should have AutoGen ConversableAgent

    @patch('autogen.ConversableAgent.generate_reply')
    def test_analyze_requirements_success(
        self,
        mock_generate,
        mock_api_key,
        mock_model,
        sample_requirement
    ):
        """Test successful requirement analysis with AutoGen."""
        mock_generate.return_value = "## Structured Requirements\n\n### Functional Requirements\n- Calculate factorial"
        
        agent = RequirementAgent(mock_api_key, mock_model)
        result = agent.analyze_requirements(sample_requirement)

        assert "success" in result
        assert result["success"] == True


# Test CodingAgent with AutoGen
class TestCodingAgent:
    """Tests for CodingAgent using AutoGen."""

    def test_coding_agent_initialization(self, mock_api_key, mock_model):
        """Test CodingAgent initialization with AutoGen."""
        agent = CodingAgent(mock_api_key, mock_model)
        assert agent.name == "SeniorDeveloper"
        assert agent.model == mock_model
        assert hasattr(agent, 'agent')  # Should have AutoGen ConversableAgent

    @patch('autogen.ConversableAgent.generate_reply')
    def test_generate_code_success(
        self,
        mock_generate,
        mock_api_key,
        mock_model,
        sample_requirement
    ):
        """Test successful code generation with AutoGen."""
        mock_generate.return_value = "def factorial(n): return 1 if n <= 1 else n * factorial(n-1)"
        
        agent = CodingAgent(mock_api_key, mock_model)
        result = agent.generate_code(sample_requirement)

        assert "success" in result
        assert result["success"] == True


# Test ReviewAgent with AutoGen
class TestReviewAgent:
    """Tests for ReviewAgent using AutoGen."""

    def test_review_agent_initialization(self, mock_api_key, mock_model):
        """Test ReviewAgent initialization with AutoGen."""
        agent = ReviewAgent(mock_api_key, mock_model)
        assert agent.name == "CodeReviewer"
        assert agent.model == mock_model
        assert hasattr(agent, 'agent')  # Should have AutoGen ConversableAgent

    @patch('autogen.ConversableAgent.generate_reply')
    def test_review_code_approved(
        self,
        mock_generate,
        mock_api_key,
        mock_model,
        sample_code
    ):
        """Test code review approval with AutoGen."""
        mock_generate.return_value = "## Code Review\n\n**Status**: APPROVED\n\nCode looks good."
        
        agent = ReviewAgent(mock_api_key, mock_model)
        result = agent.review_code(sample_code, "Calculate factorial")

        assert "success" in result
        assert result["success"] == True


# Test AutoGenPipeline
class TestAutoGenPipeline:
    """Tests for AutoGen Pipeline orchestration."""

    def test_pipeline_creation(self, mock_api_key, mock_model):
        """Test AutoGen pipeline creation."""
        pipeline = create_autogen_pipeline(mock_api_key, mock_model)
        assert isinstance(pipeline, AutoGenPipeline)
        assert len(pipeline.agents) == 7

    def test_pipeline_initialization(self, mock_api_key, mock_model):
        """Test AutoGen pipeline has all agents."""
        pipeline = AutoGenPipeline(mock_api_key, mock_model)
        
        # Check all agents are initialized
        assert hasattr(pipeline, 'requirement_agent')
        assert hasattr(pipeline, 'coding_agent')
        assert hasattr(pipeline, 'review_agent')
        assert hasattr(pipeline, 'documentation_agent')
        assert hasattr(pipeline, 'test_agent')
        assert hasattr(pipeline, 'deployment_agent')
        assert hasattr(pipeline, 'ui_agent')


# Test DocumentationAgent
class TestDocumentationAgent:
    """Tests for DocumentationAgent using AutoGen."""

    def test_documentation_agent_initialization(self, mock_api_key, mock_model):
        """Test DocumentationAgent initialization."""
        agent = DocumentationAgent(mock_api_key, mock_model)
        assert agent.name == "TechnicalWriter"
        assert hasattr(agent, 'agent')


# Test TestAgent
class TestTestAgent:
    """Tests for TestAgent using AutoGen."""

    def test_test_agent_initialization(self, mock_api_key, mock_model):
        """Test TestAgent initialization."""
        agent = TestAgent(mock_api_key, mock_model)
        assert agent.name == "QAEngineer"
        assert hasattr(agent, 'agent')


# Test DeploymentAgent
class TestDeploymentAgent:
    """Tests for DeploymentAgent using AutoGen."""

    def test_deployment_agent_initialization(self, mock_api_key, mock_model):
        """Test DeploymentAgent initialization."""
        agent = DeploymentAgent(mock_api_key, mock_model)
        assert agent.name == "DevOpsEngineer"
        assert hasattr(agent, 'agent')


# Test UIAgent
class TestUIAgent:
    """Tests for UIAgent using AutoGen."""

    def test_ui_agent_initialization(self, mock_api_key, mock_model):
        """Test UIAgent initialization."""
        agent = UIAgent(mock_api_key, mock_model)
        assert agent.name == "UIDesigner"
        assert hasattr(agent, 'agent')


# Integration Tests
class TestIntegration:
    """Integration tests for the complete AutoGen pipeline."""

    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    def test_pipeline_from_env(self):
        """Test pipeline creation from environment variables."""
        pipeline = create_autogen_pipeline()
        assert pipeline is not None

    def test_all_agents_have_autogen(self, mock_api_key, mock_model):
        """Test that all agents use AutoGen ConversableAgent."""
        agents = [
            RequirementAgent(mock_api_key, mock_model),
            CodingAgent(mock_api_key, mock_model),
            ReviewAgent(mock_api_key, mock_model),
            DocumentationAgent(mock_api_key, mock_model),
            TestAgent(mock_api_key, mock_model),
            DeploymentAgent(mock_api_key, mock_model),
            UIAgent(mock_api_key, mock_model)
        ]
        
        for agent in agents:
            assert hasattr(agent, 'agent'), f"{agent.name} missing AutoGen agent"
            assert hasattr(agent, 'name'), f"{agent.name} missing name attribute"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
