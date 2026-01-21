"""Pipeline orchestration for Multi-Agent Framework using AutoGen GroupChat."""

import logging
import os
import uuid
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime

from autogen import ConversableAgent, GroupChat, GroupChatManager

from ..agents import (
    RequirementAgent,
    CodingAgent,
    ReviewAgent,
    DocumentationAgent,
    TestAgent,
    DeploymentAgent,
    UIAgent
)
from ..utils import config, log_pipeline_step

logger = logging.getLogger(__name__)


class AutoGenPipeline:
    """
    Orchestrates the execution of all agents using AutoGen GroupChat
    with proper agent-to-agent communication and orchestration.
    """

    def __init__(self, api_key: str = None, model: str = None):
        """
        Initialize the AutoGen pipeline.

        Args:
            api_key: OpenAI API key (if None, uses config)
            model: Model name (if None, uses config)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model or config.get("api", "model_id", default="gpt-4o")
        self.base_url = os.getenv("OPENAI_BASE_URL") or config.get("api", "base_url", default=None)
        self.max_iterations = config.get("pipeline", "max_iterations", default=3)
        self.max_rounds = config.get("pipeline", "max_rounds", default=10)

        # Initialize all agents
        logger.info("Initializing AutoGen agents...")
        self.requirement_agent = RequirementAgent(self.api_key, self.model, temperature=0.3, base_url=self.base_url)
        self.coding_agent = CodingAgent(self.api_key, self.model, temperature=0.2, base_url=self.base_url)
        self.review_agent = ReviewAgent(self.api_key, self.model, temperature=0.4, base_url=self.base_url)
        self.documentation_agent = DocumentationAgent(self.api_key, self.model, temperature=0.3, base_url=self.base_url)
        self.test_agent = TestAgent(self.api_key, self.model, temperature=0.3, base_url=self.base_url)
        self.deployment_agent = DeploymentAgent(self.api_key, self.model, temperature=0.2, base_url=self.base_url)
        self.ui_agent = UIAgent(self.api_key, self.model, temperature=0.3, base_url=self.base_url)

        logger.info("All AutoGen agents initialized successfully")

        # Ensure output directories exist
        self._setup_output_directories()

    def _setup_output_directories(self):
        """Create output directories if they don't exist."""
        config.generated_code_dir.mkdir(parents=True, exist_ok=True)
        config.documentation_dir.mkdir(parents=True, exist_ok=True)
        config.tests_dir.mkdir(parents=True, exist_ok=True)

    def _save_output(self, content: str, filename: str, directory: Path, run_id: str = None) -> str:
        """
        Save output to file with UUID and timestamp.

        Args:
            content: Content to save
            filename: Base filename
            directory: Directory to save to
            run_id: Unique run identifier (UUID)

        Returns:
            Path to saved file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        run_id = run_id or str(uuid.uuid4())[:8]
        
        # Create run-specific directory
        run_dir = config.output_dir / f"run_{timestamp}_{run_id}" / directory.name
        run_dir.mkdir(parents=True, exist_ok=True)
        
        filepath = run_dir / filename

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        logger.info(f"Saved output to: {filepath}")
        return str(filepath)

    def create_user_proxy(self) -> ConversableAgent:
        """
        Create a user proxy agent for AutoGen GroupChat.

        Returns:
            ConversableAgent configured as user proxy
        """
        return ConversableAgent(
            name="UserProxy",
            system_message="You are a user proxy representing the human user's requirements.",
            llm_config=False,  # No LLM needed for user proxy
            human_input_mode="NEVER",
            is_termination_msg=lambda x: "TERMINATE" in x.get("content", "").upper(),
        )

    def create_orchestrator_agent(self) -> ConversableAgent:
        """
        Create an orchestrator agent to manage the workflow.

        Returns:
            ConversableAgent configured as orchestrator
        """
        llm_config = {
            "model": self.model,
            "api_key": self.api_key,
            "temperature": 0.1,
            "max_completion_tokens": 1000,
        }

        system_message = """You are the Orchestrator managing a multi-agent software development pipeline.

Your role is to coordinate the agents in this sequence:
1. RequirementAnalyst - Analyzes user requirements and creates structured specifications
2. SeniorDeveloper - Generates production-ready Python code
3. CodeReviewer - Reviews code for quality, security, and best practices
4. TechnicalWriter - Creates comprehensive documentation
5. QAEngineer - Generates pytest test cases
6. DevOpsEngineer - Creates deployment configurations
7. UIDesigner - Generates Streamlit UI

Workflow:
- Start by asking RequirementAnalyst to analyze the user's requirements
- Once requirements are ready, ask SeniorDeveloper to generate code
- Have CodeReviewer review the code. If NEEDS_REVISION, ask SeniorDeveloper to revise
- When code is APPROVED, proceed to parallel tasks:
  * TechnicalWriter creates documentation
  * QAEngineer creates tests
  * DevOpsEngineer creates deployment config
  * UIDesigner creates Streamlit UI
- When all artifacts are complete, say TERMINATE

Keep coordination brief and direct. Use agent names to address them."""

        return ConversableAgent(
            name="Orchestrator",
            system_message=system_message,
            llm_config=llm_config,
            human_input_mode="NEVER",
        )

    def execute_pipeline(
        self,
        user_requirement: str,
        save_outputs: bool = True
    ) -> Dict[str, Any]:
        """
        Execute the complete multi-agent pipeline using AutoGen GroupChat.

        Args:
            user_requirement: Natural language requirement from user
            save_outputs: Whether to save outputs to files

        Returns:
            Dictionary containing all agent outputs and metadata
        """
        # Generate unique run ID
        run_id = str(uuid.uuid4())[:8]
        
        results = {
            'user_requirement': user_requirement,
            'timestamp': datetime.now().isoformat(),
            'run_id': run_id,
            'outputs': {},
            'metadata': {
                'status': 'in_progress',
                'model': self.model
            }
        }

        try:
            logger.info("=== Starting AutoGen Pipeline Execution ===")

            # Create orchestrator and user proxy
            orchestrator = self.create_orchestrator_agent()
            user_proxy = self.create_user_proxy()

            # Get AutoGen agents from wrapper classes
            agents = [
                user_proxy,
                orchestrator,
                self.requirement_agent.get_agent(),
                self.coding_agent.get_agent(),
                self.review_agent.get_agent(),
                self.documentation_agent.get_agent(),
                self.test_agent.get_agent(),
                self.deployment_agent.get_agent(),
                self.ui_agent.get_agent(),
            ]

            # Create GroupChat
            groupchat = GroupChat(
                agents=agents,
                messages=[],
                max_round=self.max_rounds,
                speaker_selection_method="auto",  # Let AutoGen handle speaker selection
            )

            # Create GroupChat Manager
            manager = GroupChatManager(
                groupchat=groupchat,
                llm_config={
                    "model": self.model,
                    "api_key": self.api_key,
                    "temperature": 0.1,
                }
            )

            # Start the conversation
            logger.info("Initiating GroupChat conversation...")
            initial_message = f"""Please process the following software development requirement:

{user_requirement}

Follow the complete pipeline: requirements analysis -> code generation -> code review (with revisions if needed) -> documentation, tests, deployment config, and UI generation.

When all artifacts are complete, respond with TERMINATE."""

            # Execute the group chat
            chat_result = user_proxy.initiate_chat(
                manager,
                message=initial_message,
            )

            logger.info("GroupChat conversation completed")

            # Extract outputs from conversation history
            results['outputs'] = self._extract_outputs_from_chat(groupchat.messages)
            results['metadata']['status'] = 'completed'
            results['metadata']['total_messages'] = len(groupchat.messages)

            # Save outputs if requested
            if save_outputs:
                self._save_all_outputs(results['outputs'], run_id)

            logger.info("=== Pipeline Execution Completed Successfully ===")
            return results

        except Exception as e:
            logger.error(f"Pipeline execution failed: {e}", exc_info=True)
            results['metadata']['status'] = 'failed'
            results['metadata']['error'] = str(e)
            raise

    def _extract_outputs_from_chat(self, messages: List[Dict]) -> Dict[str, Any]:
        """
        Extract agent outputs from chat conversation.

        Args:
            messages: List of chat messages

        Returns:
            Dictionary of outputs by agent type
        """
        outputs = {}
        
        for msg in messages:
            sender = msg.get('name', '')
            content = msg.get('content', '')
            
            # Map agent names to output types
            if sender == 'RequirementAnalyst' and 'Functional Requirements' in content:
                outputs['requirements'] = content
            elif sender == 'SeniorDeveloper' and ('def ' in content or 'class ' in content):
                if 'def test_' not in content:  # Not test code
                    outputs['code'] = content
            elif sender == 'CodeReviewer' and ('APPROVED' in content or 'NEEDS_REVISION' in content):
                outputs['review'] = content
            elif sender == 'TechnicalWriter' and ('##' in content or '# ' in content):
                outputs['documentation'] = content
            elif sender == 'QAEngineer' and 'def test_' in content:
                outputs['tests'] = content
            elif sender == 'DevOpsEngineer' and ('Dockerfile' in content or 'requirements.txt' in content):
                outputs['deployment'] = content
            elif sender == 'UIDesigner' and 'streamlit' in content.lower():
                outputs['ui'] = content
        
        return outputs

    def _save_all_outputs(self, outputs: Dict[str, Any], run_id: str):
        """
        Save all pipeline outputs to files.

        Args:
            outputs: Dictionary of outputs
            run_id: Unique run identifier
        """
        output_mapping = {
            'requirements': ('requirements.md', config.documentation_dir),
            'code': ('generated_code.py', config.generated_code_dir),
            'review': ('code_review.md', config.documentation_dir),
            'documentation': ('documentation.md', config.documentation_dir),
            'tests': ('test_generated.py', config.tests_dir),
            'deployment': ('deployment_config.md', config.documentation_dir),
            'ui': ('streamlit_ui.py', config.generated_code_dir),
        }

        for key, (filename, directory) in output_mapping.items():
            if key in outputs and outputs[key]:
                try:
                    self._save_output(outputs[key], filename, directory, run_id)
                except Exception as e:
                    logger.warning(f"Failed to save {key}: {e}")


def create_pipeline(api_key: str = None, model: str = None) -> AutoGenPipeline:
    """
    Factory function to create an AutoGen Pipeline.

    Args:
        api_key: OpenAI API key
        model: Model name

    Returns:
        AutoGenPipeline instance
    """
    return AutoGenPipeline(api_key=api_key, model=model)
