"""
Data models for the agents package
"""

from dataclasses import dataclass
from typing import Dict, Any, List, Optional
from datetime import datetime


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


@dataclass
class ExtractedFeature:
    """Represents a feature extracted from a PRD"""
    feature_id: str
    feature_name: str
    feature_description: str
    feature_content: str
    section: str
    priority: str
    complexity: str
    data_types: List[str]
    user_impact: str
    technical_requirements: List[str]
    compliance_considerations: List[str]


@dataclass
class USStateCompliance:
    """Represents compliance status for a specific US state"""
    state_name: str
    state_code: str
    is_compliant: bool
    non_compliant_regulations: List[str]
    risk_level: str
    required_actions: List[str]
    notes: str


@dataclass
class FeatureComplianceResult:
    """Complete compliance result for a single feature"""
    feature: ExtractedFeature
    agent_outputs: Dict[str, AgentOutput]
    compliance_flags: List[str]
    risk_level: str
    confidence_score: float
    requires_human_review: bool
    reasoning: str
    recommendations: List[str]
    us_state_compliance: List[USStateCompliance]
    non_compliant_states: List[str]
    processing_time: float
    timestamp: str


@dataclass
class PRDAnalysisResult:
    """Complete analysis result for an entire PRD"""
    prd_id: str
    prd_name: str
    prd_description: str
    extracted_features: List[ExtractedFeature]
    total_features: int
    feature_compliance_results: List[FeatureComplianceResult]
    overall_risk_level: str
    overall_confidence_score: float
    critical_compliance_issues: List[str]
    summary_recommendations: List[str]
    total_processing_time: float
    timestamp: str
