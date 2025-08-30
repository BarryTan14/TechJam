"""
Executive Report Generator Agent
Generates comprehensive executive summaries from PRD analysis results
"""

from __future__ import annotations

import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

# WorkflowState is defined in langgraph_workflow.py, so we'll import it when needed


@dataclass
class ExecutiveReport:
    """Executive report data structure"""
    report_id: str
    prd_name: str
    generated_at: str
    executive_summary: str
    key_findings: List[str]
    risk_assessment: Dict[str, Any]
    compliance_overview: Dict[str, Any]
    recommendations: List[str]
    next_steps: List[str]


class ExecutiveReportGenerator:
    """Agent for generating executive reports from PRD analysis results"""
    
    def __init__(self, llm=None):
        self.llm = llm
        self.agent_name = "Executive Report Generator"
    
    def generate_executive_report(self, workflow_state: 'WorkflowState') -> ExecutiveReport:
        """
        Generate a comprehensive executive report from workflow analysis results
        
        Args:
            workflow_state: Complete workflow state with analysis results
            
        Returns:
            ExecutiveReport object containing the executive summary and detailed findings
        """
        print(f"📊 Generating Executive Report for: {workflow_state.prd_name}")
        
        # Generate report ID
        report_id = f"exec_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Extract key metrics and findings
        key_findings = self._extract_key_findings(workflow_state)
        risk_assessment = self._generate_risk_assessment(workflow_state)
        compliance_overview = self._generate_compliance_overview(workflow_state)
        recommendations = self._extract_recommendations(workflow_state)
        next_steps = self._generate_next_steps(workflow_state)
        
        # Generate executive summary
        executive_summary = self._generate_executive_summary(
            workflow_state, key_findings, risk_assessment, compliance_overview
        )
        
        return ExecutiveReport(
            report_id=report_id,
            prd_name=workflow_state.prd_name,
            generated_at=datetime.now().isoformat(),
            executive_summary=executive_summary,
            key_findings=key_findings,
            risk_assessment=risk_assessment,
            compliance_overview=compliance_overview,
            recommendations=recommendations,
            next_steps=next_steps
        )
    
    def _extract_key_findings(self, workflow_state: 'WorkflowState') -> List[str]:
        """Extract key findings from the analysis"""
        findings = []
        
        # Overall risk assessment
        findings.append(f"Overall Risk Level: {workflow_state.overall_risk_level.upper()}")
        findings.append(f"Overall Confidence Score: {workflow_state.overall_confidence_score:.2f}")
        
        # Feature analysis summary
        total_features = len(workflow_state.feature_compliance_results)
        high_risk_features = sum(1 for f in workflow_state.feature_compliance_results if f.risk_level == "high")
        low_risk_features = total_features - high_risk_features
        
        findings.append(f"Total Features Analyzed: {total_features}")
        findings.append(f"High-Risk Features: {high_risk_features}")
        findings.append(f"Low-Risk Features: {low_risk_features}")
        
        # State compliance summary
        if hasattr(workflow_state, 'non_compliant_states_dict') and workflow_state.non_compliant_states_dict:
            non_compliant_states = len(workflow_state.non_compliant_states_dict)
            findings.append(f"States with Compliance Issues: {non_compliant_states}")
        
        # Critical issues
        if workflow_state.critical_compliance_issues:
            findings.append(f"Critical Compliance Issues Identified: {len(workflow_state.critical_compliance_issues)}")
        
        return findings
    
    def _generate_risk_assessment(self, workflow_state: 'WorkflowState') -> Dict[str, Any]:
        """Generate comprehensive risk assessment"""
        risk_assessment = {
            "overall_risk_level": workflow_state.overall_risk_level,
            "overall_confidence_score": workflow_state.overall_confidence_score,
            "feature_risk_distribution": {},
            "state_risk_analysis": {},
            "critical_issues": workflow_state.critical_compliance_issues
        }
        
        # Feature risk distribution
        risk_counts = {}
        for feature in workflow_state.feature_compliance_results:
            risk_level = feature.risk_level
            risk_counts[risk_level] = risk_counts.get(risk_level, 0) + 1
        risk_assessment["feature_risk_distribution"] = risk_counts
        
        # State risk analysis
        if hasattr(workflow_state, 'non_compliant_states_dict') and workflow_state.non_compliant_states_dict:
            state_risks = {}
            for state_code, state_data in workflow_state.non_compliant_states_dict.items():
                state_risks[state_code] = {
                    "state_name": state_data.get("state_name", ""),
                    "risk_level": state_data.get("risk_level", "unknown"),
                    "risk_score": state_data.get("risk_score", 0.0),
                    "non_compliant_features": state_data.get("non_compliant_features", 0),
                    "compliance_rate": state_data.get("compliance_rate", 0.0)
                }
            risk_assessment["state_risk_analysis"] = state_risks
        
        return risk_assessment
    
    def _generate_compliance_overview(self, workflow_state: 'WorkflowState') -> Dict[str, Any]:
        """Generate compliance overview"""
        compliance_overview = {
            "total_features": len(workflow_state.feature_compliance_results),
            "compliance_by_feature": {},
            "compliance_by_state": {},
            "overall_compliance_rate": 0.0
        }
        
        # Feature compliance analysis
        feature_compliance = {}
        total_compliance_score = 0.0
        
        for feature in workflow_state.feature_compliance_results:
            # Calculate average compliance score across states
            if feature.state_compliance_scores:
                avg_compliance = sum(score.compliance_score for score in feature.state_compliance_scores.values()) / len(feature.state_compliance_scores)
                total_compliance_score += avg_compliance
                
                feature_compliance[feature.feature.feature_name] = {
                    "risk_level": feature.risk_level,
                    "avg_compliance_score": avg_compliance,
                    "non_compliant_states": len(feature.non_compliant_states),
                    "total_states": len(feature.state_compliance_scores)
                }
        
        compliance_overview["compliance_by_feature"] = feature_compliance
        
        # Calculate overall compliance rate
        if workflow_state.feature_compliance_results:
            compliance_overview["overall_compliance_rate"] = total_compliance_score / len(workflow_state.feature_compliance_results)
        
        return compliance_overview
    
    def _extract_recommendations(self, workflow_state: 'WorkflowState') -> List[str]:
        """Extract and prioritize recommendations"""
        all_recommendations = []
        
        # Collect recommendations from all features
        for feature in workflow_state.feature_compliance_results:
            all_recommendations.extend(feature.recommendations)
        
        # Add summary recommendations
        if hasattr(workflow_state, 'summary_recommendations') and workflow_state.summary_recommendations:
            all_recommendations.extend(workflow_state.summary_recommendations)
        
        # Remove duplicates and prioritize
        unique_recommendations = []
        seen = set()
        for rec in all_recommendations:
            rec_lower = rec.lower()
            if rec_lower not in seen:
                unique_recommendations.append(rec)
                seen.add(rec_lower)
        
        # Return top 15 most important recommendations
        return unique_recommendations[:15]
    
    def _generate_next_steps(self, workflow_state: 'WorkflowState') -> List[str]:
        """Generate actionable next steps"""
        next_steps = []
        
        # Risk-based next steps
        if workflow_state.overall_risk_level == "high":
            next_steps.extend([
                "Immediate compliance audit required",
                "Prioritize high-risk feature remediation",
                "Engage legal team for compliance review",
                "Implement immediate privacy safeguards"
            ])
        elif workflow_state.overall_risk_level == "medium":
            next_steps.extend([
                "Conduct detailed compliance assessment",
                "Address medium-risk features",
                "Update privacy policies and procedures",
                "Implement monitoring and reporting systems"
            ])
        else:
            next_steps.extend([
                "Continue monitoring compliance status",
                "Implement preventive measures",
                "Regular compliance reviews",
                "Maintain current privacy practices"
            ])
        
        # Feature-specific next steps
        high_risk_features = [f for f in workflow_state.feature_compliance_results if f.risk_level == "high"]
        if high_risk_features:
            next_steps.append(f"Focus on {len(high_risk_features)} high-risk features for immediate attention")
        
        # State-specific next steps
        if hasattr(workflow_state, 'non_compliant_states_dict') and workflow_state.non_compliant_states_dict:
            critical_states = [state for state, data in workflow_state.non_compliant_states_dict.items() 
                             if data.get("risk_level") == "high"]
            if critical_states:
                next_steps.append(f"Prioritize compliance in {len(critical_states)} high-risk states")
        
        return next_steps
    
    def _generate_executive_summary(self, workflow_state: 'WorkflowState', 
                                  key_findings: List[str], 
                                  risk_assessment: Dict[str, Any],
                                  compliance_overview: Dict[str, Any]) -> str:
        """Generate the main executive summary"""
        
        # Use LLM if available for more sophisticated summary
        if self.llm:
            return self._generate_llm_summary(workflow_state, key_findings, risk_assessment, compliance_overview)
        else:
            return self._generate_rule_based_summary(workflow_state, key_findings, risk_assessment, compliance_overview)
    
    def _generate_llm_summary(self, workflow_state: 'WorkflowState', 
                            key_findings: List[str], 
                            risk_assessment: Dict[str, Any],
                            compliance_overview: Dict[str, Any]) -> str:
        """Generate executive summary using LLM"""
        
        prompt = f"""Generate a comprehensive executive summary for a PRD compliance analysis.

PRD Information:
- Name: {workflow_state.prd_name}
- Description: {workflow_state.prd_description}
- Overall Risk Level: {workflow_state.overall_risk_level.upper()}
- Overall Confidence Score: {workflow_state.overall_confidence_score:.2f}

Key Findings:
{chr(10).join(f"- {finding}" for finding in key_findings)}

Risk Assessment:
- Feature Risk Distribution: {risk_assessment.get('feature_risk_distribution', {})}
- Critical Issues: {len(risk_assessment.get('critical_issues', []))} identified
- States with Compliance Issues: {len(risk_assessment.get('state_risk_analysis', {}))}

Compliance Overview:
- Total Features: {compliance_overview.get('total_features', 0)}
- Overall Compliance Rate: {compliance_overview.get('overall_compliance_rate', 0.0):.1%}

Top Recommendations:
{chr(10).join(f"- {rec}" for rec in self._extract_recommendations(workflow_state)[:5])}

Generate a professional executive summary that includes:
1. Executive Overview (2-3 sentences)
2. Key Risk Assessment (2-3 sentences)
3. Compliance Status Summary (2-3 sentences)
4. Critical Issues and Concerns (2-3 sentences)
5. Strategic Recommendations (2-3 sentences)
6. Next Steps (1-2 sentences)

Make it business-friendly, actionable, and suitable for executive leadership."""
        
        try:
            response = self.llm.generate_content(prompt)
            if response and response.text:
                return response.text.strip()
            else:
                raise Exception("LLM returned empty response")
        except Exception as e:
            print(f"⚠️ LLM summary generation failed: {e}")
            return self._generate_rule_based_summary(workflow_state, key_findings, risk_assessment, compliance_overview)
    
    def _generate_rule_based_summary(self, workflow_state: 'WorkflowState', 
                                   key_findings: List[str], 
                                   risk_assessment: Dict[str, Any],
                                   compliance_overview: Dict[str, Any]) -> str:
        """Generate executive summary using rule-based approach"""
        
        # Executive Overview
        overview = f"Executive Summary for {workflow_state.prd_name}\n\n"
        
        # Risk Assessment
        risk_level = workflow_state.overall_risk_level.upper()
        confidence = workflow_state.overall_confidence_score
        
        overview += f"EXECUTIVE OVERVIEW\n"
        overview += f"Our comprehensive compliance analysis of '{workflow_state.prd_name}' reveals a {risk_level} RISK assessment "
        overview += f"with {confidence:.1%} confidence. The analysis examined {compliance_overview.get('total_features', 0)} features "
        overview += f"across all 50 US states to identify potential compliance issues and regulatory risks.\n\n"
        
        # Key Findings
        overview += f"KEY RISK ASSESSMENT\n"
        feature_dist = risk_assessment.get('feature_risk_distribution', {})
        high_risk_features = feature_dist.get('high', 0)
        low_risk_features = feature_dist.get('low', 0)
        
        overview += f"The analysis identified {high_risk_features} high-risk features and {low_risk_features} low-risk features. "
        overview += f"Overall compliance rate stands at {compliance_overview.get('overall_compliance_rate', 0.0):.1%}, "
        overview += f"indicating {'significant compliance challenges' if compliance_overview.get('overall_compliance_rate', 0.0) < 0.6 else 'generally good compliance posture'}.\n\n"
        
        # Compliance Status
        overview += f"COMPLIANCE STATUS SUMMARY\n"
        critical_issues = len(risk_assessment.get('critical_issues', []))
        non_compliant_states = len(risk_assessment.get('state_risk_analysis', {}))
        
        overview += f"Critical compliance issues were identified in {critical_issues} areas, with {non_compliant_states} states "
        overview += f"showing compliance concerns. The analysis covered key privacy regulations including GDPR, CCPA, "
        overview += f"and state-specific data protection laws.\n\n"
        
        # Critical Issues
        overview += f"CRITICAL ISSUES AND CONCERNS\n"
        if critical_issues > 0:
            overview += f"{critical_issues} critical compliance issues require immediate attention. "
            overview += f"High-risk features pose significant regulatory exposure and potential legal consequences. "
            overview += f"State-specific compliance gaps may result in enforcement actions and penalties.\n\n"
        else:
            overview += f"No critical compliance issues were identified. The system demonstrates good compliance posture "
            overview += f"with minor areas requiring attention.\n\n"
        
        # Strategic Recommendations
        overview += f"STRATEGIC RECOMMENDATIONS\n"
        recommendations = self._extract_recommendations(workflow_state)[:3]
        for i, rec in enumerate(recommendations, 1):
            overview += f"{i}. {rec}\n"
        overview += "\n"
        
        # Next Steps
        overview += f"NEXT STEPS\n"
        if workflow_state.overall_risk_level == "high":
            overview += f"Immediate action required: Conduct compliance audit, prioritize high-risk feature remediation, "
            overview += f"and engage legal team for comprehensive review."
        elif workflow_state.overall_risk_level == "medium":
            overview += f"Proceed with detailed compliance assessment and implement recommended safeguards "
            overview += f"within the next 30 days."
        else:
            overview += f"Continue monitoring compliance status and implement preventive measures "
            overview += f"to maintain current compliance posture."
        
        return overview
