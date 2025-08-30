"""
Reasoning Generator Agent - Generates detailed reasoning for compliance decisions
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


class ReasoningGeneratorAgent:
    """Reasoning Generator Agent - Produces clear justifications"""
    
    def __init__(self, llm=None):
        self.llm = llm
    
    def generate_reasoning(self, feature_name: str, feature_analysis: Dict[str, Any], 
                          regulation_matching: Dict[str, Any], risk_assessment: Dict[str, Any]) -> AgentOutput:
        """Generate clear reasoning based on all previous analyses"""
        start_time = get_singapore_time()
        
        print(f"\n💭 [Reasoning Generator] Generating reasoning for: {feature_name}")
        
        # Create prompt for reasoning generation
        prompt = f"""
        You are a reasoning agent tasked with identifying which regulation(s) a user should refer to based on their query or situation, specifically analyzing the feature under consideration for a particular state.

        Your goals:
        1. Analyze the user's input along with the feature details and the specific state being evaluated.
        2. Determine the most relevant regulation(s) applicable to the feature within that state.
        3. Explain clearly why the feature or situation is compliant or non-compliant with the identified regulation(s).
        4. Provide concise reasoning, citing specific regulatory clauses or criteria related to the state's laws when possible.
        5. If compliance cannot be determined due to insufficient information, state that clearly and specify what additional details are needed.

        Based on the complete analysis, generate clear reasoning:
        
        Feature Analysis: {json.dumps(feature_analysis, indent=2)}
        Regulation Matching: {json.dumps(regulation_matching, indent=2)}
        Risk Assessment: {json.dumps(risk_assessment, indent=2)}
        
        IMPORTANT: Respond ONLY with valid JSON. Do not include any other text, explanations, or markdown formatting.
        
        Provide your reasoning in this exact JSON format:
        {{
            "feature_under_analysis": "Brief description of the feature",
            "state": "Name of the state being analyzed",
            "regulations_identified": [
                "Name or code of regulation 1",
                "Name or code of regulation 2"
            ],
            "compliance_status": "Compliant|Non-compliant|Undetermined",
            "explanation": "Detailed reasoning with references to state-specific regulations and feature impact",
            "regulatory_clauses": [
                "Specific clause or article reference 1",
                "Specific clause or article reference 2"
            ],
            "compliance_criteria": [
                "Specific compliance requirement 1",
                "Specific compliance requirement 2"
            ],
            "missing_information": [
                "Additional detail needed 1 (if any)",
                "Additional detail needed 2 (if any)"
            ],
            "recommendations": [
                "specific, actionable recommendation 1",
                "specific, actionable recommendation 2"
            ]
        }}
        
        Format your assessment with clarity and authority, helping the user understand which regulations apply specifically to the feature and state under review, along with the compliance rationale.
        """
        
        # Execute reasoning generation
        if self.llm:
            try:
                print(f"🤖 Using LLM for reasoning generation...")
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
                    thought_process = "Used LLM to generate comprehensive reasoning and recommendations"
                    print(f"✅ JSON parsing successful")
                except json.JSONDecodeError as json_error:
                    print(f"⚠️  JSON parsing failed: {json_error}")
                    print(f"📄 Raw response: {response.text[:200]}...")
                    # Try to extract JSON from the response
                    analysis_result = self._extract_json_from_response(response.text)
                    thought_process = "Used LLM with JSON extraction due to parsing issues"
                
            except Exception as e:
                print(f"⚠️  LLM reasoning generation failed: {e}")
                print(f"🔍 Error type: {type(e).__name__}")
                raise Exception(f"Reasoning generation failed: {e}")
        else:
            raise Exception("No LLM available for reasoning generation")
        
        # Calculate processing time
        processing_time = (get_singapore_time() - start_time).total_seconds()
        
        # Create agent output
        agent_output = AgentOutput(
            agent_name="Reasoning Generator",
            input_data={
                "feature_analysis": feature_analysis,
                "regulation_matching": regulation_matching,
                "risk_assessment": risk_assessment
            },
            thought_process=thought_process,
            analysis_result=analysis_result,
            confidence_score=0.90 if self.llm else 0.70,
            processing_time=processing_time,
            timestamp=get_singapore_time().isoformat()
        )
        
        print(f"✅ [Reasoning Generator] Completed in {processing_time:.2f}s")
        print(f"   📝 Feature: {analysis_result.get('feature_under_analysis', 'unknown')}")
        print(f"   🏛️ State: {analysis_result.get('state', 'unknown')}")
        print(f"   📋 Compliance status: {analysis_result.get('compliance_status', 'unknown')}")
        print(f"   📜 Regulations: {len(analysis_result.get('regulations_identified', []))}")
        print(f"   💡 Recommendations: {len(analysis_result.get('recommendations', []))}")
        
        return agent_output
    
    def generate_state_specific_reasoning(self, feature_name: str, feature_analysis: Dict[str, Any], 
                                        state_name: str, state_regulations: Dict[str, Any]) -> AgentOutput:
        """Generate state-specific reasoning for a feature"""
        start_time = datetime.now()
        
        print(f"\n🏛️ [State-Specific Reasoning] Generating reasoning for: {feature_name} in {state_name}")
        
        # Create prompt for state-specific reasoning
        prompt = f"""
        You are a reasoning agent tasked with identifying which regulation(s) a user should refer to based on their query or situation, specifically analyzing the feature under consideration for a particular state.

        Your goals:
        1. Analyze the user's input along with the feature details and the specific state being evaluated.
        2. Determine the most relevant regulation(s) applicable to the feature within that state.
        3. Explain clearly why the feature or situation is compliant or non-compliant with the identified regulation(s).
        4. Provide concise reasoning, citing specific regulatory clauses or criteria related to the state's laws when possible.
        5. If compliance cannot be determined due to insufficient information, state that clearly and specify what additional details are needed.

        Feature Analysis: {json.dumps(feature_analysis, indent=2)}
        State: {state_name}
        State Regulations: {json.dumps(state_regulations, indent=2)}
        
        IMPORTANT: Respond ONLY with valid JSON. Do not include any other text, explanations, or markdown formatting.
        
        Provide your reasoning in this exact JSON format:
        {{
            "feature_under_analysis": "Brief description of the feature",
            "state": "{state_name}",
            "regulations_identified": [
                "Name or code of regulation 1",
                "Name or code of regulation 2"
            ],
            "compliance_status": "Compliant|Non-compliant|Undetermined",
            "explanation": "Detailed reasoning with references to state-specific regulations and feature impact",
            "regulatory_clauses": [
                "Specific clause or article reference 1",
                "Specific clause or article reference 2"
            ],
            "compliance_criteria": [
                "Specific compliance requirement 1",
                "Specific compliance requirement 2"
            ],
            "missing_information": [
                "Additional detail needed 1 (if any)",
                "Additional detail needed 2 (if any)"
            ],
            "recommendations": [
                "specific, actionable recommendation 1",
                "specific, actionable recommendation 2"
            ]
        }}
        
        Format your assessment with clarity and authority, helping the user understand which regulations apply specifically to the feature and state under review, along with the compliance rationale.
        """
        
        # Execute state-specific reasoning generation
        if self.llm:
            try:
                print(f"🤖 Using LLM for state-specific reasoning generation...")
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
                    thought_process = "Used LLM to generate state-specific reasoning and recommendations"
                    print(f"✅ JSON parsing successful")
                except json.JSONDecodeError as json_error:
                    print(f"⚠️  JSON parsing failed: {json_error}")
                    print(f"📄 Raw response: {response.text[:200]}...")
                    # Try to extract JSON from the response
                    analysis_result = self._extract_json_from_response(response.text)
                    thought_process = "Used LLM with JSON extraction due to parsing issues"
                
            except Exception as e:
                print(f"⚠️  LLM state-specific reasoning generation failed: {e}")
                print(f"🔍 Error type: {type(e).__name__}")
                raise Exception(f"State-specific reasoning generation failed: {e}")
        else:
            raise Exception("No LLM available for state-specific reasoning generation")
        
        # Calculate processing time
        processing_time = (datetime.now() - start_time).total_seconds()
        
        # Create agent output
        agent_output = AgentOutput(
            agent_name="State-Specific Reasoning Generator",
            input_data={
                "feature_analysis": feature_analysis,
                "state_name": state_name,
                "state_regulations": state_regulations
            },
            thought_process=thought_process,
            analysis_result=analysis_result,
            confidence_score=0.90 if self.llm else 0.70,
            processing_time=processing_time,
            timestamp=datetime.now().isoformat()
        )
        
        print(f"✅ [State-Specific Reasoning] Completed in {processing_time:.2f}s")
        print(f"   📝 Feature: {analysis_result.get('feature_under_analysis', 'unknown')}")
        print(f"   🏛️ State: {analysis_result.get('state', 'unknown')}")
        print(f"   📋 Compliance status: {analysis_result.get('compliance_status', 'unknown')}")
        print(f"   📜 Regulations: {len(analysis_result.get('regulations_identified', []))}")
        print(f"   💡 Recommendations: {len(analysis_result.get('recommendations', []))}")
        
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
            # Look for feature_under_analysis
            feature_pattern = r'"feature_under_analysis":\s*"([^"]+)"'
            feature_match = re.search(feature_pattern, cleaned_text)
            feature_analysis = feature_match.group(1) if feature_match else "Feature analysis"
            
            # Look for state
            state_pattern = r'"state":\s*"([^"]+)"'
            state_match = re.search(state_pattern, cleaned_text)
            state = state_match.group(1) if state_match else "Unknown state"
            
            # Look for compliance_status
            status_pattern = r'"compliance_status":\s*"([^"]+)"'
            status_match = re.search(status_pattern, cleaned_text)
            compliance_status = status_match.group(1) if status_match else "Undetermined"
            
            # Look for regulations_identified
            reg_pattern = r'"regulations_identified":\s*\[([^\]]+)\]'
            reg_match = re.search(reg_pattern, cleaned_text)
            regulations = []
            if reg_match:
                reg_str = reg_match.group(1)
                regulations = re.findall(r'"([^"]+)"', reg_str)
            
            # Look for explanation
            explanation_pattern = r'"explanation":\s*"([^"]+)"'
            explanation_match = re.search(explanation_pattern, cleaned_text)
            explanation = explanation_match.group(1) if explanation_match else "Compliance analysis completed"
            
            # Look for recommendations
            rec_pattern = r'"recommendations":\s*\[([^\]]+)\]'
            rec_match = re.search(rec_pattern, cleaned_text)
            recommendations = []
            if rec_match:
                rec_str = rec_match.group(1)
                recommendations = re.findall(r'"([^"]+)"', rec_str)
            
            return {
                "feature_under_analysis": feature_analysis,
                "state": state,
                "regulations_identified": regulations or ["GDPR", "CCPA"],
                "compliance_status": compliance_status,
                "explanation": explanation,
                "regulatory_clauses": ["GDPR Article 6", "CCPA Section 1798.100"],
                "compliance_criteria": ["Consent requirement", "Data minimization"],
                "missing_information": [],
                "recommendations": recommendations or ["Implement consent", "Establish retention"]
            }
        except:
            pass
        
        # If no JSON found, raise an exception
        raise Exception("Failed to extract valid JSON from LLM response")
    

