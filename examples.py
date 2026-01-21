"""
Example usage scripts for the AutoGen Multi-Agent Code Generator.

This file demonstrates various ways to use the framework programmatically
with Microsoft AutoGen and OpenAI GPT-4o.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.orchestrator import create_pipeline
from src.utils import setup_logger


def example_1_simple_function():
    """Example 1: Generate a simple function."""
    print("=" * 60)
    print("EXAMPLE 1: Simple Function Generation with AutoGen")
    print("=" * 60)

    # Setup logging
    logger = setup_logger()

    # Create pipeline
    pipeline = create_pipeline()

    # Define requirement
    requirement = "Create a Python function that calculates the factorial of a number"

    # Execute pipeline
    results = pipeline.execute_pipeline(requirement, save_outputs=True)

    # Display results
    print(f"\nStatus: {results['metadata']['status']}")
    print(f"\nGenerated Code Preview:")
    print("-" * 60)
    print(results['outputs']['code'][:500])
    print("\n... (see output files for complete code)")


def example_2_rest_api():
    """Example 2: Generate a REST API."""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: REST API Generation with AutoGen")
    print("=" * 60)

    pipeline = create_pipeline()

    requirement = """
Create a REST API using FastAPI that:
- Manages a todo list with CRUD operations
- Stores data in SQLite database
- Includes authentication using JWT tokens
- Has input validation using Pydantic models
"""

    results = pipeline.execute_pipeline(requirement, save_outputs=True)

    print(f"\nStatus: {results['metadata']['status']}")
    print(f"Iterations: {results['metadata']['iterations']}")
    print(f"\nAll outputs saved to ./output/")


def example_3_individual_agents():
    """Example 3: Use individual agents separately."""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Using Individual Agents")
    print("=" * 60)

    from src.agents import (
        create_requirement_agent,
        create_coding_agent,
        create_review_agent
    )
    from src.utils import config

    # Create individual agents
    req_agent = create_requirement_agent(
        config.openai_api_key,
        config.model_name
    )

    # Analyze requirements
    requirement = "Create a CSV parser that validates data types"
    requirements = req_agent.analyze_requirements(requirement)

    print("\nRequirements generated:")
    print(requirements[:300])
    print("\n... (truncated)")

    # Generate code
    coding_agent = create_coding_agent(
        config.openai_api_key,
        config.model_name
    )

    code = coding_agent.generate_code(requirements)

    print("\nCode generated:")
    print(code[:300])
    print("\n... (truncated)")


def example_4_custom_configuration():
    """Example 4: Use custom configuration."""
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Custom Configuration")
    print("=" * 60)

    # Create pipeline with custom settings
    pipeline = create_pipeline(
        model="gpt-4o"
    )

    requirement = "Build a data validator for JSON schemas"

    results = pipeline.execute_pipeline(
        requirement,
        save_outputs=False  # Don't save to files
    )

    print(f"\nStatus: {results['metadata']['status']}")
    print("\nOutputs stored in memory (not saved to files)")


def example_5_error_handling():
    """Example 5: Error handling and edge cases."""
    print("\n" + "=" * 60)
    print("EXAMPLE 5: Error Handling")
    print("=" * 60)

    pipeline = create_pipeline()

    try:
        # Empty requirement
        results = pipeline.execute_pipeline("", save_outputs=False)
    except Exception as e:
        print(f"Expected error caught: {type(e).__name__}")

    # Valid requirement
    requirement = "Create a simple calculator"
    results = pipeline.execute_pipeline(requirement, save_outputs=False)

    print(f"\nSuccessful execution status: {results['metadata']['status']}")


def run_all_examples():
    """Run all examples."""
    print("\n" + "#" * 60)
    print("# AutoGen Multi-Agent Code Generator - Usage Examples")
    print("#" * 60)

    try:
        example_1_simple_function()
        example_2_rest_api()
        example_3_individual_agents()
        example_4_custom_configuration()
        example_5_error_handling()

        print("\n" + "#" * 60)
        print("# All AutoGen examples completed successfully!")
        print("#" * 60)

    except Exception as e:
        print(f"\nError running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # Note: This requires a valid OPENAI_API_KEY in config/.env
    print("WARNING: Running these examples will make API calls to OpenAI.")
    print("Ensure you have set OPENAI_API_KEY in config/.env")
    print()

    response = input("Continue? (y/n): ")
    if response.lower() == 'y':
        run_all_examples()
    else:
        print("Examples cancelled.")
