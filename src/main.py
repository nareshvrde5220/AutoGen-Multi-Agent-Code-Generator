"""Main entry point for Multi-Agent Framework CLI."""

import argparse
import sys
import logging
from pathlib import Path

from src.orchestrator import create_autogen_pipeline
from src.utils import setup_logger, config

logger = logging.getLogger(__name__)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Multi-Agentic Coding Framework - Transform requirements into production-ready code"
    )

    # Subcommands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Run command
    run_parser = subparsers.add_parser('run', help='Run the agent pipeline')
    run_parser.add_argument(
        'requirement',
        type=str,
        help='Natural language requirement (or path to file with @)'
    )
    run_parser.add_argument(
        '--api-key',
        type=str,
        help='OpenAI API key (or set OPENAI_API_KEY env var)'
    )
    run_parser.add_argument(
        '--model',
        type=str,
        default='gpt-4o',
        help='Model to use (default: gpt-4o)'
    )
    run_parser.add_argument(
        '--no-save',
        action='store_true',
        help='Do not save outputs to files'
    )
    run_parser.add_argument(
        '--output-dir',
        type=str,
        help='Custom output directory'
    )

    # UI command
    ui_parser = subparsers.add_parser('ui', help='Launch Streamlit UI')
    ui_parser.add_argument(
        '--port',
        type=int,
        default=8501,
        help='Port to run Streamlit on'
    )

    # Test command
    test_parser = subparsers.add_parser('test', help='Run tests')
    test_parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Verbose output'
    )

    # Version command
    parser.add_argument(
        '--version',
        action='version',
        version='Multi-Agent Framework 1.0.0'
    )

    args = parser.parse_args()

    # Setup logging
    setup_logger()

    if args.command == 'run':
        run_pipeline(args)
    elif args.command == 'ui':
        launch_ui(args)
    elif args.command == 'test':
        run_tests(args)
    else:
        parser.print_help()


def run_pipeline(args):
    """Run the agent pipeline."""
    try:
        # Get requirement
        requirement = args.requirement
        if requirement.startswith('@'):
            # Read from file
            file_path = requirement[1:]
            with open(file_path, 'r', encoding='utf-8') as f:
                requirement = f.read()

        logger.info("Starting AutoGen agent pipeline...")
        logger.info(f"Requirement: {requirement[:100]}...")

        # Create AutoGen pipeline
        pipeline = create_autogen_pipeline(
            api_key=args.api_key,
            model=args.model
        )

        # Execute
        results = pipeline.execute_pipeline(
            user_requirement=requirement,
            save_outputs=not args.no_save
        )

        # Print summary
        print("\n" + "="*60)
        print("PIPELINE EXECUTION COMPLETED")
        print("="*60)
        print(f"Status: {results['metadata']['status']}")
        print(f"Iterations: {results['metadata']['iterations']}")
        print(f"Timestamp: {results['timestamp']}")

        if not args.no_save:
            print(f"\nOutputs saved to: {config.output_dir}")

        print("\n" + "="*60)
        print("GENERATED ARTIFACTS")
        print("="*60)

        for key, value in results['outputs'].items():
            preview = value[:200] if len(value) > 200 else value
            print(f"\n{key.upper()}:")
            print("-" * 60)
            print(preview)
            if len(value) > 200:
                print("... (truncated)")

        logger.info("Pipeline completed successfully")

    except Exception as e:
        logger.error(f"Pipeline execution failed: {e}", exc_info=True)
        print(f"\nError: {e}")
        sys.exit(1)


def launch_ui(args):
    """Launch Streamlit UI."""
    try:
        import streamlit.web.cli as stcli
        import sys

        sys.argv = [
            "streamlit",
            "run",
            "ui/streamlit_app.py",
            f"--server.port={args.port}",
            "--server.address=0.0.0.0"
        ]

        logger.info(f"Launching Streamlit UI on port {args.port}...")
        sys.exit(stcli.main())

    except Exception as e:
        logger.error(f"Failed to launch UI: {e}", exc_info=True)
        print(f"\nError launching UI: {e}")
        sys.exit(1)


def run_tests(args):
    """Run tests."""
    try:
        import pytest

        pytest_args = ['tests/']
        if args.verbose:
            pytest_args.append('-v')

        logger.info("Running tests...")
        exit_code = pytest.main(pytest_args)
        sys.exit(exit_code)

    except ImportError:
        print("pytest not installed. Install with: pip install pytest")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Test execution failed: {e}", exc_info=True)
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
