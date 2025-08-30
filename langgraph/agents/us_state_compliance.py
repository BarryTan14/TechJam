"""
US State Compliance Agent - Analyzes compliance for each US state
"""

import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from .models import AgentOutput, USStateCompliance


class USStateComplianceAgent:
    """Agent responsible for analyzing compliance for each US state"""
    
    def __init__(self, llm=None):
        self.llm = llm
        self.agent_name = "US State Compliance"
        
        # Use centralized state regulations cache
        from .state_regulations_cache import state_regulations_cache
        self.state_cache = state_regulations_cache
    
    def analyze_us_state_compliance(self, feature_name: str, feature_analysis: Dict[str, Any], 
                                   regulation_matching: Dict[str, Any], risk_assessment: Dict[str, Any]) -> AgentOutput:
        """
        Analyze compliance for each US state - optimized for efficiency
        
        Args:
            feature_name: Name of the feature being analyzed
            feature_analysis: Output from feature analyzer
            regulation_matching: Output from regulation matcher
            risk_assessment: Output from risk assessor
            
        Returns:
            AgentOutput containing US state compliance analysis
        """
        start_time = datetime.now()
        
        # Prepare input data
        input_data = {
            "feature_name": feature_name,
            "feature_analysis": feature_analysis,
            "regulation_matching": regulation_matching,
            "risk_assessment": risk_assessment,
            "total_states": len(self.state_cache.get_all_states())
        }
        
        # Analyze compliance for each state - optimized approach
        if self.llm:
            try:
                # Use a single LLM call for all states instead of individual calls
                analysis_result = self._analyze_states_batch(feature_name, feature_analysis, regulation_matching, risk_assessment)
                confidence_score = 0.85
                thought_process = "Used LLM to analyze compliance for all US states in a single batch call"
            except Exception as e:
                analysis_result = self._analyze_states_fallback(feature_analysis, regulation_matching, risk_assessment)
                confidence_score = 0.6
                thought_process = f"LLM batch analysis failed, used fallback pattern matching: {e}"
        else:
            analysis_result = self._analyze_states_fallback(feature_analysis, regulation_matching, risk_assessment)
            confidence_score = 0.6
            thought_process = "No LLM available, used fallback pattern matching to analyze US state compliance"
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        # Create agent output
        agent_output = AgentOutput(
            agent_name=self.agent_name,
            input_data=input_data,
            thought_process=thought_process,
            analysis_result=analysis_result,
            confidence_score=confidence_score,
            processing_time=processing_time,
            timestamp=datetime.now().isoformat()
        )
        
        non_compliant_count = len(analysis_result.get("non_compliant_states", []))
        
        return agent_output
    
    def _analyze_states_batch(self, feature_name: str, feature_analysis: Dict[str, Any], 
                             regulation_matching: Dict[str, Any], risk_assessment: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze all states in a single LLM call for efficiency"""
        
        # Prepare feature information
        data_types = feature_analysis.get("data_types_collected", [])
        processing_purposes = feature_analysis.get("processing_purposes", [])
        applicable_regulations = regulation_matching.get("applicable_regulations", [])
        risk_level = risk_assessment.get("overall_risk_level", "medium")
        
        # Create a comprehensive prompt for all states
        prompt = f"""Analyze compliance for feature "{feature_name}" across all US states:

Feature Details:
- Data Types: {data_types}
- Processing Purposes: {processing_purposes}
- Applicable Regulations: {applicable_regulations}
- Risk Level: {risk_level}

Return JSON with compliance analysis for all 50 states:
{{
    "non_compliant_states": ["CA", "VA", "NY"],
    "state_compliance": [
        {{
            "state_code": "CA",
            "state_name": "California",
            "is_compliant": false,
            "non_compliant_regulations": ["CCPA", "CPRA"],
            "risk_level": "high",
            "required_actions": ["Implement consent mechanisms"],
            "notes": "CCPA compliance required"
        }}
    ]
}}

Focus on states with comprehensive privacy laws (CA, VA, CO, CT, UT, NY, IL). For other states, assume basic compliance unless specific issues are identified."""
        
        try:
            response = self.llm.generate_content(prompt)
            
            if not response or not response.text:
                raise Exception("LLM returned empty response")
            
            # Try to parse JSON response
            try:
                analysis_result = json.loads(response.text)
            except json.JSONDecodeError:
                analysis_result = self._extract_json_from_response(response.text)
            
            # Ensure we have the required structure
            if "state_compliance" not in analysis_result:
                analysis_result["state_compliance"] = []
            if "non_compliant_states" not in analysis_result:
                analysis_result["non_compliant_states"] = []
            
            return analysis_result
            
        except Exception as e:
            raise Exception(f"Batch analysis failed: {e}")
    
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
        
        # If no JSON found, return fallback
        return self._analyze_states_fallback({}, {}, {})
    
    def _analyze_states_fallback(self, feature_analysis: Dict[str, Any], 
                                regulation_matching: Dict[str, Any], 
                                risk_assessment: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback analysis using pattern matching"""
        
        # Identify high-risk states based on feature characteristics
        data_types = feature_analysis.get("data_types_collected", [])
        processing_purposes = feature_analysis.get("processing_purposes", [])
        risk_level = risk_assessment.get("overall_risk_level", "medium")
        
        # States with comprehensive privacy laws that are likely to have compliance issues
        high_risk_states = self.state_cache.get_high_risk_states()
        medium_risk_states = self.state_cache.get_medium_risk_states()
        
        non_compliant_states = []
        state_compliance = []
        
        # Analyze each state
        for state_code, state_regulation in self.state_cache.get_all_states().items():
            state_name = state_regulation.state_name
            regulations = state_regulation.regulations
            
            # Determine compliance based on risk level and state
            is_compliant = True
            risk_level_state = "low"
            required_actions = []
            
            if state_code in high_risk_states and risk_level in ["high", "critical"]:
                is_compliant = False
                risk_level_state = "high"
                required_actions = ["Implement consent mechanisms", "Add data deletion rights"]
                non_compliant_states.append(state_code)
            elif state_code in medium_risk_states and risk_level in ["high", "critical", "medium"]:
                is_compliant = False
                risk_level_state = "medium"
                required_actions = ["Review consent mechanisms"]
                non_compliant_states.append(state_code)
            
            state_compliance.append({
                "state_code": state_code,
                "state_name": state_name,
                "is_compliant": is_compliant,
                "non_compliant_regulations": regulations if not is_compliant else [],
                "risk_level": risk_level_state,
                "required_actions": required_actions,
                "notes": f"Analysis based on {state_name} regulations"
            })
        
        return {
            "non_compliant_states": non_compliant_states,
            "state_compliance": state_compliance
        }
