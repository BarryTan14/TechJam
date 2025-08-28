"""
Non-Compliant States Analyzer Agent - Generates comprehensive non-compliant states dictionary
"""

import json
from datetime import datetime
from typing import Dict, Any, List, Optional
import google.generativeai as genai

from .models import AgentOutput, FeatureComplianceResult


class NonCompliantStatesAnalyzerAgent:
    """Agent responsible for generating comprehensive non-compliant states dictionary"""
    
    def __init__(self, llm=None):
        self.llm = llm
        self.agent_name = "Non-Compliant States Analyzer"
    
    def analyze_non_compliant_states(self, feature_compliance_results: List[FeatureComplianceResult]) -> AgentOutput:
        """
        Analyze all feature compliance results and generate comprehensive non-compliant states dictionary
        
        Args:
            feature_compliance_results: List of feature compliance results from all agents
            
        Returns:
            AgentOutput containing non-compliant states dictionary analysis
        """
        start_time = datetime.now()
        
        print(f"🔍 [{self.agent_name}] Analyzing non-compliant states from {len(feature_compliance_results)} features")
        
        # Prepare input data
        input_data = {
            "total_features": len(feature_compliance_results),
            "feature_names": [result.feature.feature_name for result in feature_compliance_results],
            "feature_compliance_results": feature_compliance_results
        }
        
        # Analyze non-compliant states
        if self.llm:
            try:
                analysis_result = self._analyze_with_llm(feature_compliance_results)
                confidence_score = 0.9
                thought_process = "Used LLM to analyze non-compliant states and generate comprehensive dictionary with risk scores and reasoning."
            except Exception as e:
                print(f"⚠️  LLM non-compliant states analysis failed: {e}")
                analysis_result = self._analyze_fallback(feature_compliance_results)
                confidence_score = 0.7
                thought_process = f"LLM analysis failed, used fallback pattern matching: {e}"
        else:
            analysis_result = self._analyze_fallback(feature_compliance_results)
            confidence_score = 0.7
            thought_process = "No LLM available, used fallback pattern matching to analyze non-compliant states."
        
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
        
        non_compliant_count = len(analysis_result.get("non_compliant_states_dict", {}))
        print(f"✅ [{self.agent_name}] Generated non-compliant states dict with {non_compliant_count} states in {processing_time:.2f}s")
        
        return agent_output
    
    def _analyze_with_llm(self, feature_compliance_results: List[FeatureComplianceResult]) -> Dict[str, Any]:
        """Analyze non-compliant states using LLM"""
        
        # Prepare feature data for LLM
        feature_data = []
        for result in feature_compliance_results:
            feature_info = {
                "feature_name": result.feature.feature_name,
                "risk_level": result.risk_level,
                "reasoning": result.reasoning,
                "non_compliant_states": result.non_compliant_states,
                "us_state_compliance": [
                    {
                        "state_code": state.state_code,
                        "state_name": state.state_name,
                        "is_compliant": state.is_compliant,
                        "non_compliant_regulations": state.non_compliant_regulations,
                        "risk_level": state.risk_level,
                        "required_actions": state.required_actions,
                        "notes": state.notes
                    }
                    for state in result.us_state_compliance
                    if not state.is_compliant
                ]
            }
            feature_data.append(feature_info)
        
        prompt = f"""
You are a compliance analysis expert. Your task is to generate a comprehensive non-compliant states dictionary from feature compliance results.

Feature Compliance Data:
{json.dumps(feature_data, indent=2)}

Your task is to:
1. Analyze all non-compliant states across all features
2. Generate a dictionary where keys are state codes (e.g., "CA", "NY")
3. For each state, provide comprehensive analysis including:
   - Risk score (0.0-1.0, where 1.0 is highest risk)
   - Risk level (low/medium/high/critical)
   - Detailed reasoning for non-compliance
   - List of non-compliant features
   - Non-compliant regulations
   - Required actions to achieve compliance
   - Additional notes

Consider these factors when generating risk scores:
- Critical: 1.0 (immediate compliance issues)
- High: 0.8 (significant compliance gaps)
- Medium: 0.5 (moderate compliance concerns)
- Low: 0.2 (minor compliance issues)

Return your response as a JSON object with this EXACT structure:
{{
    "non_compliant_states_dict": {{
        "CA": {{
            "state_name": "California",
            "risk_score": 0.85,
            "risk_level": "high",
            "reasoning": "Feature collects personal data without proper consent mechanisms required by CCPA/CPRA. California has the strictest privacy laws in the US.",
            "non_compliant_features": ["User Preference Collection", "Browsing History Tracking"],
            "non_compliant_regulations": ["CCPA", "CPRA"],
            "required_actions": ["Implement consent management", "Add data deletion rights", "Establish user rights portal"],
            "notes": "California requires explicit consent and comprehensive user rights for personal data processing"
        }},
        "NY": {{
            "state_name": "New York",
            "risk_score": 0.75,
            "risk_level": "high",
            "reasoning": "Feature processes data for analytics without meeting NY SHIELD Act requirements for data security and breach notification.",
            "non_compliant_features": ["Browsing History Tracking"],
            "non_compliant_regulations": ["NY SHIELD Act"],
            "required_actions": ["Implement data security measures", "Add breach notification procedures"],
            "notes": "New York has strict data security and breach notification requirements"
        }}
    }},
    "analysis_summary": {{
        "total_non_compliant_states": 15,
        "highest_risk_states": ["CA", "NY", "IL"],
        "most_common_violations": ["Consent requirements", "Data security", "User rights"],
        "overall_compliance_risk": "high"
    }},
    "recommendations": [
        "Implement state-specific consent mechanisms",
        "Add comprehensive data security measures",
        "Establish user rights portal for data access and deletion",
        "Monitor for regulation updates in all states"
    ]
}}

Ensure your response is valid JSON and provides comprehensive analysis for all non-compliant states.
"""
        
        print(f"🤖 Using LLM for non-compliant states analysis...")
        
        response = self.llm.generate_content(prompt)
        
        print(f"📝 LLM Response received for non-compliant states analysis")
        
        if response and response.text:
            print(f"📄 Raw response preview: {response.text[:200]}...")
            
            # Extract JSON from response
            json_data = self._extract_json_from_response(response.text)
            
            if json_data:
                return json_data
            else:
                print("⚠️  Failed to extract JSON from LLM response")
                return self._analyze_fallback(feature_compliance_results)
        else:
            print("⚠️  Empty LLM response")
            return self._analyze_fallback(feature_compliance_results)
    
    def _analyze_fallback(self, feature_compliance_results: List[FeatureComplianceResult]) -> Dict[str, Any]:
        """Analyze non-compliant states using pattern matching fallback"""
        
        non_compliant_states_dict = {}
        all_non_compliant_states = set()
        highest_risk_states = []
        
        # Risk level to score mapping
        risk_scores = {
            "critical": 1.0,
            "high": 0.8,
            "medium": 0.5,
            "low": 0.2
        }
        
        for result in feature_compliance_results:
            feature_name = result.feature.feature_name
            risk_level = result.risk_level
            reasoning = result.reasoning
            
            # Process US state compliance data
            for state_compliance in result.us_state_compliance:
                if not state_compliance.is_compliant:
                    state_code = state_compliance.state_code
                    state_name = state_compliance.state_name
                    all_non_compliant_states.add(state_code)
                    
                    # Convert risk level to numeric score
                    risk_score = risk_scores.get(risk_level.lower(), 0.5)
                    
                    # Create or update state entry
                    if state_code not in non_compliant_states_dict:
                        non_compliant_states_dict[state_code] = {
                            "state_name": state_name,
                            "risk_score": risk_score,
                            "risk_level": risk_level,
                            "reasoning": reasoning,
                            "non_compliant_features": [feature_name],
                            "non_compliant_regulations": state_compliance.non_compliant_regulations,
                            "required_actions": state_compliance.required_actions,
                            "notes": state_compliance.notes
                        }
                    else:
                        # Update existing state entry
                        existing_entry = non_compliant_states_dict[state_code]
                        existing_entry["non_compliant_features"].append(feature_name)
                        
                        # Update risk score (take the highest)
                        if risk_score > existing_entry["risk_score"]:
                            existing_entry["risk_score"] = risk_score
                            existing_entry["risk_level"] = risk_level
                            existing_entry["reasoning"] = reasoning
                        
                        # Merge non-compliant regulations
                        existing_entry["non_compliant_regulations"].extend(state_compliance.non_compliant_regulations)
                        existing_entry["non_compliant_regulations"] = list(set(existing_entry["non_compliant_regulations"]))
                        
                        # Merge required actions
                        existing_entry["required_actions"].extend(state_compliance.required_actions)
                        existing_entry["required_actions"] = list(set(existing_entry["required_actions"]))
        
        # Identify highest risk states
        for state_code, state_data in non_compliant_states_dict.items():
            if state_data["risk_score"] >= 0.8:
                highest_risk_states.append(state_code)
        
        # Determine overall compliance risk
        if any(state_data["risk_score"] >= 0.8 for state_data in non_compliant_states_dict.values()):
            overall_risk = "high"
        elif any(state_data["risk_score"] >= 0.5 for state_data in non_compliant_states_dict.values()):
            overall_risk = "medium"
        else:
            overall_risk = "low"
        
        return {
            "non_compliant_states_dict": non_compliant_states_dict,
            "analysis_summary": {
                "total_non_compliant_states": len(non_compliant_states_dict),
                "highest_risk_states": highest_risk_states,
                "most_common_violations": ["Consent requirements", "Data security", "User rights"],
                "overall_compliance_risk": overall_risk
            },
            "recommendations": [
                "Implement state-specific consent mechanisms",
                "Add comprehensive data security measures",
                "Establish user rights portal for data access and deletion",
                "Monitor for regulation updates in all states"
            ]
        }
    
    def _extract_json_from_response(self, response_text: str) -> Dict[str, Any]:
        """Extract JSON from LLM response text"""
        import re
        
        # Check if response is empty
        if not response_text or not response_text.strip():
            raise Exception("LLM response is empty")
        
        # Clean the response text
        cleaned_text = response_text.strip()
        
        # Remove markdown code blocks if present
        if cleaned_text.startswith('```json'):
            cleaned_text = re.sub(r'^```json\s*\n?', '', cleaned_text)
        elif cleaned_text.startswith('```'):
            cleaned_text = re.sub(r'^```\s*\n?', '', cleaned_text)
        
        # Remove trailing ```
        cleaned_text = re.sub(r'\n?```\s*$', '', cleaned_text)
        cleaned_text = cleaned_text.strip()
        
        # Try to parse the cleaned JSON directly
        try:
            return json.loads(cleaned_text)
        except json.JSONDecodeError:
            pass
        
        # Try to find JSON object in the response - more robust pattern
        json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
        matches = re.findall(json_pattern, cleaned_text, re.DOTALL)
        
        if matches:
            for match in matches:
                try:
                    return json.loads(match)
                except json.JSONDecodeError:
                    continue
        
        # If no JSON found, return default structure
        return {
            "non_compliant_states_dict": {},
            "analysis_summary": {
                "total_non_compliant_states": 0,
                "highest_risk_states": [],
                "most_common_violations": [],
                "overall_compliance_risk": "low"
            },
            "recommendations": []
        }
