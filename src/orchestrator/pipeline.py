"""Pipeline orchestration for Multi-Agent Framework."""

import logging
import os
import uuid
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

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


class AgentPipeline:
    """
    Orchestrates the execution of all agents in the multi-agent framework
    with feedback loops and error handling.
    """

    def __init__(self, api_key: str = None, model: str = None):
        """
        Initialize the agent pipeline.

        Args:
            api_key: OpenAI API key (if None, uses config)
            model: Model name (if None, uses config)
        """
        self.api_key = api_key or config.openai_api_key
        self.model = model or config.model_name
        self.max_iterations = config.max_iterations

        # Initialize all agents
        logger.info("Initializing agents...")
        self.requirement_agent = RequirementAgent(self.api_key, self.model, temperature=0.3)
        self.coding_agent = CodingAgent(self.api_key, self.model, temperature=0.2)
        self.review_agent = ReviewAgent(self.api_key, self.model, temperature=0.4)
        self.documentation_agent = DocumentationAgent(self.api_key, self.model, temperature=0.3)
        self.test_agent = TestAgent(self.api_key, self.model, temperature=0.3)
        self.deployment_agent = DeploymentAgent(self.api_key, self.model, temperature=0.2)
        self.ui_agent = UIAgent(self.api_key, self.model, temperature=0.3)

        logger.info("All agents initialized successfully")

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
            directory: Directory to save to (e.g., 'documentation', 'generated_code', 'tests')
            run_id: Unique run identifier (UUID)

        Returns:
            Path to saved file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        run_id = run_id or str(uuid.uuid4())[:8]
        
        # Create run-specific directory at output root, then subdirectory
        run_dir = config.output_dir / f"run_{timestamp}_{run_id}" / directory.name
        run_dir.mkdir(parents=True, exist_ok=True)
        
        filepath = run_dir / filename

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        logger.info(f"Saved output to: {filepath}")
        return str(filepath)

    def execute_pipeline(
        self,
        user_requirement: str,
        save_outputs: bool = True
    ) -> Dict[str, Any]:
        """
        Execute the complete multi-agent pipeline.

        Args:
            user_requirement: Natural language requirement from user
            save_outputs: Whether to save outputs to files

        Returns:
            Dictionary containing all agent outputs and metadata
        """
        # Generate unique run ID for this execution
        run_id = str(uuid.uuid4())[:8]
        
        results = {
            'user_requirement': user_requirement,
            'timestamp': datetime.now().isoformat(),
            'run_id': run_id,
            'outputs': {},
            'metadata': {
                'iterations': 0,
                'status': 'in_progress'
            }
        }

        try:
            # Step 1: Requirement Analysis
            log_pipeline_step(logger, 1, "Requirement Analysis", "started")
            results['outputs']['requirements'] = self.requirement_agent.analyze_requirements(
                user_requirement
            )
            log_pipeline_step(logger, 1, "Requirement Analysis", "completed")

            if save_outputs:
                self._save_output(
                    results['outputs']['requirements'],
                    'requirements.md',
                    config.documentation_dir,
                    run_id
                )

            # Step 2-3: Coding with Review Loop
            log_pipeline_step(logger, 2, "Code Generation with Review Loop", "started")
            code_approved = False
            iteration = 0

            while not code_approved and iteration < self.max_iterations:
                iteration += 1
                logger.info(f"Code generation iteration {iteration}/{self.max_iterations}")

                # Generate code
                if iteration == 1:
                    code = self.coding_agent.generate_code(results['outputs']['requirements'])
                else:
                    # Pass review feedback for revision
                    code = self.coding_agent.generate_code(
                        results['outputs']['requirements'],
                        feedback=results['outputs']['review']
                    )

                # Review code
                review = self.review_agent.review_code(
                    code,
                    requirements=results['outputs']['requirements']
                )

                # Check if approved
                if self.review_agent.is_approved(review):
                    code_approved = True
                    results['outputs']['code'] = code
                    results['outputs']['review'] = review
                    results['metadata']['iterations'] = iteration
                    logger.info(f"Code approved after {iteration} iteration(s)")
                else:
                    logger.warning(f"Code needs revision (iteration {iteration})")
                    results['outputs']['review'] = review

                    # If max iterations reached, use the last code anyway
                    if iteration >= self.max_iterations:
                        logger.warning(f"Max iterations reached. Using last generated code.")
                        results['outputs']['code'] = code
                        results['metadata']['iterations'] = iteration
                        results['metadata']['max_iterations_reached'] = True
                        break

            log_pipeline_step(logger, 2, "Code Generation with Review Loop", "completed")

            if save_outputs:
                self._save_output(
                    results['outputs']['code'],
                    'generated_code.py',
                    config.generated_code_dir,
                    run_id
                )
                self._save_output(
                    results['outputs']['review'],
                    'code_review.md',
                    config.documentation_dir,
                    run_id
                )

            # Step 4: Documentation Generation
            log_pipeline_step(logger, 3, "Documentation Generation", "started")
            results['outputs']['documentation'] = self.documentation_agent.generate_documentation(
                results['outputs']['code'],
                requirements=results['outputs']['requirements']
            )
            log_pipeline_step(logger, 3, "Documentation Generation", "completed")

            if save_outputs:
                self._save_output(
                    results['outputs']['documentation'],
                    'documentation.md',
                    config.documentation_dir,
                    run_id
                )

            # Step 5: Test Case Generation
            log_pipeline_step(logger, 4, "Test Case Generation", "started")
            results['outputs']['tests'] = self.test_agent.generate_tests(
                results['outputs']['code'],
                requirements=results['outputs']['requirements']
            )
            log_pipeline_step(logger, 4, "Test Case Generation", "completed")

            if save_outputs:
                self._save_output(
                    results['outputs']['tests'],
                    'test_generated_code.py',
                    config.tests_dir,
                    run_id
                )

            # Step 6: Deployment Configuration
            log_pipeline_step(logger, 5, "Deployment Configuration", "started")
            results['outputs']['deployment'] = self.deployment_agent.generate_deployment_config(
                results['outputs']['code'],
                requirements=results['outputs']['requirements']
            )
            log_pipeline_step(logger, 5, "Deployment Configuration", "completed")

            if save_outputs:
                self._save_output(
                    results['outputs']['deployment'],
                    'deployment_config.md',
                    config.documentation_dir,
                    run_id
                )

            # Step 7: UI Generation (optional - for the project itself)
            log_pipeline_step(logger, 6, "UI Generation", "started")
            ui_context = f"""
Project Requirements: {results['outputs']['requirements']}

Generated Code: {results['outputs']['code'][:1000]}...

Documentation: {results['outputs']['documentation'][:500]}...
"""
            results['outputs']['ui'] = self.ui_agent.generate_ui(ui_context)
            log_pipeline_step(logger, 6, "UI Generation", "completed")

            if save_outputs:
                self._save_output(
                    results['outputs']['ui'],
                    'streamlit_ui.py',
                    config.output_dir,
                    run_id
                )

            results['metadata']['status'] = 'completed'
            logger.info("Pipeline execution completed successfully")

        except Exception as e:
            logger.error(f"Pipeline execution failed: {e}", exc_info=True)
            results['metadata']['status'] = 'failed'
            results['metadata']['error'] = str(e)
            raise

        return results

    def execute_step(self, step_name: str, **kwargs) -> str:
        """
        Execute a single pipeline step.

        Args:
            step_name: Name of the step to execute
            **kwargs: Arguments for the step

        Returns:
            Output from the step

        Raises:
            ValueError: If step_name is invalid
        """
        if step_name == 'requirements':
            return self.requirement_agent.analyze_requirements(kwargs['user_input'])
        elif step_name == 'code':
            return self.coding_agent.generate_code(kwargs['requirements'], kwargs.get('feedback'))
        elif step_name == 'review':
            return self.review_agent.review_code(kwargs['code'], kwargs.get('requirements'))
        elif step_name == 'documentation':
            return self.documentation_agent.generate_documentation(
                kwargs['code'],
                kwargs.get('requirements')
            )
        elif step_name == 'tests':
            return self.test_agent.generate_tests(kwargs['code'], kwargs.get('requirements'))
        elif step_name == 'deployment':
            return self.deployment_agent.generate_deployment_config(
                kwargs['code'],
                kwargs.get('requirements')
            )
        elif step_name == 'ui':
            return self.ui_agent.generate_ui(kwargs['project_description'])
        else:
            raise ValueError(f"Invalid step name: {step_name}")


def create_pipeline(api_key: str = None, model: str = None) -> AgentPipeline:
    """
    Factory function to create an agent pipeline.

    Args:
        api_key: OpenAI API key
        model: Model name

    Returns:
        AgentPipeline instance
    """
    return AgentPipeline(api_key=api_key, model=model)
