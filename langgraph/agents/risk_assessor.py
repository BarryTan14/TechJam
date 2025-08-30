"""
Risk Assessor Agent - Assesses compliance risks for features
"""

import json
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List
from .models import AgentOutput

# Helper function for Singapore timezone
def get_singapore_time():
    """Get current time in Singapore timezone (UTC+8)"""
    singapore_tz = timezone(timedelta(hours=8))
    return datetime.now(singapore_tz)


class RiskAssessorAgent:
    """Risk Assessor Agent - Scores compliance risk and flags issues"""
    
    def __init__(self, llm=None):
        self.llm = llm
    
    def assess_risk(self, feature_name: str, feature_analysis: Dict[str, Any], regulation_matching: Dict[str, Any]) -> AgentOutput:
        """Assess compliance risks based on feature analysis and regulation matching"""
        start_time = get_singapore_time()
        
        # Optimized prompt - more concise and focused
        prompt = f"""Assess compliance risks:

Feature: {feature_name}
Analysis: {json.dumps(feature_analysis, indent=2)}
Regulations: {json.dumps(regulation_matching, indent=2)}

Return JSON:
{{
    "overall_risk_level": "low|medium|high|critical",
    "risk_factors": [
        {{
            "factor": "data_collection_scope",
            "risk_level": "low|medium|high",
            "description": "explanation"
        }}
    ],
    "compliance_gaps": [
        {{
            "gap": "missing_consent_mechanism",
            "severity": "low|medium|high|critical",
            "description": "description"
        }}
    ],
    "mitigation_recommendations": ["implement_explicit_consent"],
    "confidence_score": 0.0-1.0,
    "requires_human_review": true/false
}}"""
        
        # Execute risk assessment
        if self.llm:
            try:
                response = self.llm.generate_content(prompt)
                
                if not response or not response.text:
                    raise Exception("LLM returned empty response")
                
                # Try to parse JSON response
                try:
                    analysis_result = json.loads(response.text)
                    thought_process = "Used LLM to assess compliance risks and identify gaps"
                except json.JSONDecodeError:
                    analysis_result = self._extract_json_from_response(response.text)
                    thought_process = "Used LLM with JSON extraction"
                
            except Exception as e:
                analysis_result = self._fallback_risk_assessment(feature_analysis, regulation_matching)
                thought_process = f"Used fallback assessment due to LLM failure: {e}"
        else:
            analysis_result = self._fallback_risk_assessment(feature_analysis, regulation_matching)
            thought_process = "Used fallback assessment (no LLM available)"
        
        # Calculate processing time
        processing_time = (get_singapore_time() - start_time).total_seconds()
        
        # Create agent output
        agent_output = AgentOutput(
            agent_name="Risk Assessor",
            input_data={
                "feature_analysis": feature_analysis,
                "regulation_matching": regulation_matching
            },
            thought_process=thought_process,
            analysis_result=analysis_result,
            confidence_score=analysis_result.get("confidence_score", 0.7),
            processing_time=processing_time,
            timestamp=get_singapore_time().isoformat()
        )
        
        return agent_output
    
    def _extract_json_from_response(self, response_text: str) -> Dict[str, Any]:
        """Extract JSON from LLM response text"""
        import re
        
        if not response_text or not response_text.strip():
            raise Exception("LLM response is empty")
        
        # Clean the response text
        cleaned_text = response_text.strip()
        
        # Remove markdown code blocks
        cleaned_text = re.sub(r'^```json\s*\n?', '', cleaned_text)
        cleaned_text = re.sub(r'^```\s*\n?', '', cleaned_text)
        cleaned_text = re.sub(r'\n?```\s*$', '', cleaned_text)
        cleaned_text = cleaned_text.strip()
        
        # Try to parse the cleaned JSON directly
        try:
            return json.loads(cleaned_text)
        except json.JSONDecodeError:
            pass
        
        # Try to find JSON object in the response
        json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
        matches = re.findall(json_pattern, cleaned_text, re.DOTALL)
        
        if matches:
            for match in matches:
                try:
                    return json.loads(match)
                except json.JSONDecodeError:
                    continue
        
        # If still no JSON found, try to extract specific fields
        try:
            # Look for overall_risk_level
            risk_pattern = r'"overall_risk_level":\s*"([^"]+)"'
            risk_match = re.search(risk_pattern, cleaned_text)
            overall_risk_level = risk_match.group(1) if risk_match else "medium"
            
            # Look for confidence_score
            score_pattern = r'"confidence_score":\s*([0-9.]+)'
            score_match = re.search(score_pattern, cleaned_text)
            confidence_score = float(score_match.group(1)) if score_match else 0.7
            
            # Look for compliance_gaps
            gaps_pattern = r'"compliance_gaps":\s*\[([^\]]+)\]'
            gaps_match = re.search(gaps_pattern, cleaned_text)
            compliance_gaps = []
            if gaps_match:
                gaps_str = gaps_match.group(1)
                compliance_gaps = re.findall(r'"([^"]+)"', gaps_str)
            
            # Look for recommendations
            rec_pattern = r'"recommendations":\s*\[([^\]]+)\]'
            rec_match = re.search(rec_pattern, cleaned_text)
            recommendations = []
            if rec_match:
                rec_str = rec_match.group(1)
                recommendations = re.findall(r'"([^"]+)"', rec_str)
            
            return {
                "overall_risk_level": overall_risk_level,
                "risk_factors": [
                    {
                        "factor": "data_collection_scope",
                        "risk_level": overall_risk_level,
                        "description": "Data collection and processing risks"
                    }
                ],
                "compliance_gaps": compliance_gaps or ["Missing consent management"],
                "confidence_score": confidence_score,
                "mitigation_recommendations": recommendations or ["Implement consent management"]
            }
        except:
            pass
        
        # If no JSON found, return default structure
        return {
            "overall_risk_level": "medium",
            "risk_factors": [
                {
                    "factor": "data_collection_scope",
                    "risk_level": "medium",
                    "description": "Data collection and processing risks"
                }
            ],
            "compliance_gaps": ["Missing consent management"],
            "confidence_score": 0.7,
            "mitigation_recommendations": ["Implement consent management"]
        }
    
    def _fallback_risk_assessment(self, feature_analysis: Dict[str, Any], regulation_matching: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback risk assessment"""
        data_types = feature_analysis.get("data_types_collected", [])
        regulations = regulation_matching.get("applicable_regulations", [])
        
        risk_level = "medium"
        if len(data_types) > 2 or len(regulations) > 2:
            risk_level = "high"
        
        return {
            "overall_risk_level": risk_level,
            "risk_factors": [
                {
                    "factor": "data_collection_scope",
                    "risk_level": "medium",
                    "description": "Multiple data types being collected"
                }
            ],
            "compliance_gaps": [
                {
                    "gap": "consent_mechanism",
                    "severity": "medium",
                    "description": "Consent mechanism may need review"
                }
            ],
            "mitigation_recommendations": ["implement_explicit_consent", "add_data_minimization"],
            "confidence_score": 0.7,
            "requires_human_review": risk_level == "high"
        }
