"""Orchestrator package for Multi-Agent Framework."""

from .pipeline import AgentPipeline, create_pipeline
from .autogen_pipeline import AutoGenPipeline, create_pipeline as create_autogen_pipeline

__all__ = ['AgentPipeline', 'create_pipeline', 'AutoGenPipeline', 'create_autogen_pipeline']
