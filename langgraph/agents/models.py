"""
Data models for the agents package
"""

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class AgentOutput:
    """Structured output from the agent"""
    agent_name: str
    input_data: Dict[str, Any]
    thought_process: str
    analysis_result: Dict[str, Any]
    confidence_score: float
    processing_time: float
    timestamp: str
