"""Centralized logging configuration for Multi-Agent Framework."""

import os
import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional


class LoggerSetup:
    """Setup and manage logging for the multi-agent framework."""

    def __init__(
        self,
        log_level: str = None,
        log_file: str = None,
        log_dir: str = "logs"
    ):
        """
        Initialize logger setup.

        Args:
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_file: Log file name. If None, uses default with timestamp
            log_dir: Directory to store log files
        """
        self.log_level = log_level or os.getenv('LOG_LEVEL', 'INFO')
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)

        if log_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_file = f"multi_agent_framework_{timestamp}.log"

        self.log_file = self.log_dir / log_file
        self._setup_logging()

    def _setup_logging(self):
        """Configure logging with both file and console handlers."""
        # Get the root logger
        logger = logging.getLogger()
        logger.setLevel(getattr(logging, self.log_level.upper()))

        # Remove existing handlers to avoid duplicates
        logger.handlers.clear()

        # Create formatters
        detailed_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        console_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )

        # File handler (detailed logging)
        file_handler = logging.FileHandler(self.log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(detailed_formatter)
        logger.addHandler(file_handler)

        # Console handler (less verbose)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        """
        Get a logger instance for a specific module.

        Args:
            name: Name of the logger (typically __name__)

        Returns:
            Logger instance
        """
        return logging.getLogger(name)


def setup_logger(
    log_level: str = None,
    log_file: str = None,
    log_dir: str = "logs"
) -> logging.Logger:
    """
    Setup logging and return a logger instance.

    Args:
        log_level: Logging level
        log_file: Log file name
        log_dir: Directory for log files

    Returns:
        Logger instance
    """
    LoggerSetup(log_level=log_level, log_file=log_file, log_dir=log_dir)
    return logging.getLogger(__name__)


def log_agent_interaction(
    logger: logging.Logger,
    agent_name: str,
    action: str,
    details: Optional[str] = None
):
    """
    Log agent interactions with consistent format.

    Args:
        logger: Logger instance
        agent_name: Name of the agent
        action: Action being performed
        details: Additional details about the action
    """
    message = f"[{agent_name}] {action}"
    if details:
        message += f" - {details}"
    logger.info(message)


def log_pipeline_step(
    logger: logging.Logger,
    step_number: int,
    step_name: str,
    status: str = "started"
):
    """
    Log pipeline execution steps.

    Args:
        logger: Logger instance
        step_number: Step number in the pipeline
        step_name: Name of the step
        status: Status of the step (started, completed, failed)
    """
    logger.info(f"Pipeline Step {step_number}: {step_name} - {status.upper()}")


# Initialize default logger
default_logger = setup_logger()
