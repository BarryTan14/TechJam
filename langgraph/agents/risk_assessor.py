"""
Risk Assessor Agent - Scores compliance risk and flags issues
"""

import json
from datetime import datetime
from typing import Dict, Any
from .models import AgentOutput


class RiskAssessorAgent:
    """Risk Assessor Agent - Scores compliance risk and flags issues"""
    
    def __init__(self, llm=None):
        self.llm = llm
    
    def assess_risk(self, feature_name: str, feature_analysis: Dict[str, Any], regulation_matching: Dict[str, Any]) -> AgentOutput:
        """Assess compliance risks based on feature analysis and regulation matching"""
        start_time = datetime.now()
        
        print(f"\n⚠️  [Risk Assessor] Assessing risks for: {feature_name}")
        
        # Create prompt for risk assessment
        prompt = f"""
        You are a risk assessment expert evaluating compliance risks.
        
        Based on the feature analysis and regulation matching, assess compliance risks:
        
        Feature Analysis: {json.dumps(feature_analysis, indent=2)}
        Regulation Matching: {json.dumps(regulation_matching, indent=2)}
        
        IMPORTANT: Respond ONLY with valid JSON. Do not include any other text, explanations, or markdown formatting.
        
        Provide your risk assessment in this exact JSON format:
        {{
            "overall_risk_level": "low|medium|high|critical",
            "risk_factors": [
                {{
                    "factor": "data_collection_scope",
                    "risk_level": "low|medium|high",
                    "description": "explanation of the risk factor"
                }}
            ],
            "compliance_gaps": [
                {{
                    "gap": "missing_consent_mechanism",
                    "severity": "low|medium|high|critical",
                    "description": "description of the compliance gap"
                }}
            ],
            "mitigation_recommendations": [
                "implement_explicit_consent",
                "add_data_minimization",
                "establish_user_rights_portal"
            ],
            "confidence_score": 0.0-1.0,
            "requires_human_review": true/false
        }}
        """
        
        # Execute risk assessment
        if self.llm:
            try:
                print(f"🤖 Using LLM for risk assessment...")
                response = self.llm.generate_content(prompt)
                
                if not response or not response.text:
                    raise Exception("LLM returned empty response")
                
                print(f"📝 LLM Response received ({len(response.text)} characters)")
                print(f"📄 Raw response preview: {response.text[:100]}...")
                
                # Check if response is empty or just whitespace
                if not response.text.strip():
                    raise Exception("LLM returned empty or whitespace-only response")
                
                # Try to parse JSON response
                try:
                    analysis_result = json.loads(response.text)
                    thought_process = "Used LLM to assess compliance risks and identify gaps"
                    print(f"✅ JSON parsing successful")
                except json.JSONDecodeError as json_error:
                    print(f"⚠️  JSON parsing failed: {json_error}")
                    print(f"📄 Raw response: {response.text[:200]}...")
                    # Try to extract JSON from the response
                    analysis_result = self._extract_json_from_response(response.text)
                    thought_process = "Used LLM with JSON extraction due to parsing issues"
                
            except Exception as e:
                print(f"⚠️  LLM risk assessment failed: {e}")
                print(f"🔍 Error type: {type(e).__name__}")
                analysis_result = self._fallback_risk_assessment(feature_analysis, regulation_matching)
                thought_process = "Used fallback pattern matching due to LLM failure"
        else:
            analysis_result = self._fallback_risk_assessment(feature_analysis, regulation_matching)
            thought_process = "Used fallback pattern matching (no LLM available)"
        
        # Calculate processing time
        processing_time = (datetime.now() - start_time).total_seconds()
        
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
            timestamp=datetime.now().isoformat()
        )
        
        print(f"✅ [Risk Assessor] Completed in {processing_time:.2f}s")
        print(f"   🚨 Risk level: {analysis_result.get('overall_risk_level', 'unknown')}")
        print(f"   📊 Confidence: {analysis_result.get('confidence_score', 0):.1%}")
        
        return agent_output
    
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
        
        # If still no JSON found, try to extract specific fields
        try:
            # Look for overall_risk_level
            risk_pattern = r'"overall_risk_level":\s*"([^"]+)"'
            risk_match = re.search(risk_pattern, cleaned_text)
            overall_risk_level = risk_match.group(1) if risk_match else "medium"
            
            # Look for risk_score
            score_pattern = r'"risk_score":\s*([0-9.]+)'
            score_match = re.search(score_pattern, cleaned_text)
            risk_score = float(score_match.group(1)) if score_match else 0.5
            
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
                "risk_score": risk_score,
                "confidence_level": "medium",
                "recommendations": recommendations or ["Implement consent management", "Establish data retention"]
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
            "risk_score": 0.5,
            "confidence_level": "medium",
            "recommendations": ["Implement consent management", "Establish data retention"]
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
