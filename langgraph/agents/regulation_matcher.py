"""
Regulation Matcher Agent - Matches features to relevant regulations
"""

import json
from datetime import datetime
from typing import Dict, Any
from .models import AgentOutput


class RegulationMatcherAgent:
    """Regulation Matcher Agent - Matches features to relevant regulations"""
    
    def __init__(self, llm=None):
        self.llm = llm
    
    def match_regulations(self, feature_name: str, feature_analysis: Dict[str, Any]) -> AgentOutput:
        """Match feature analysis to applicable regulations"""
        start_time = datetime.now()
        
        print(f"\n🏛️  [Regulation Matcher] Matching regulations for: {feature_name}")
        
        # Create prompt for regulation matching
        prompt = f"""
        You are a legal expert matching software features to relevant regulations.
        
        Based on the feature analysis, identify which regulations apply:
        
        Feature Analysis: {json.dumps(feature_analysis, indent=2)}
        
        Available Regulations:
        - GDPR (EU): Personal data processing, consent, data rights
        - CCPA (California): Consumer privacy, data sales, access rights
        - PIPL (China): Personal information, data localization, cross-border transfer
        - LGPD (Brazil): Data protection, legal basis, data subject rights
        
        IMPORTANT: Respond ONLY with valid JSON. Do not include any other text, explanations, or markdown formatting.
        
        Provide your analysis in this exact JSON format:
        {{
            "applicable_regulations": ["GDPR", "CCPA", "PIPL", "LGPD"],
            "regulation_reasons": {{
                "GDPR": "reason why GDPR applies",
                "CCPA": "reason why CCPA applies",
                "PIPL": "reason why PIPL applies",
                "LGPD": "reason why LGPD applies"
            }},
            "key_requirements": ["consent_management", "data_minimization", "user_rights"],
            "compliance_priority": "high|medium|low",
            "geographic_scope": ["EU", "California", "China", "Brazil"]
        }}
        """
        
        # Execute regulation matching
        if self.llm:
            try:
                print(f"🤖 Using LLM for regulation matching...")
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
                    thought_process = "Used LLM to match feature requirements to applicable regulations"
                    print(f"✅ JSON parsing successful")
                except json.JSONDecodeError as json_error:
                    print(f"⚠️  JSON parsing failed: {json_error}")
                    print(f"📄 Raw response: {response.text[:200]}...")
                    # Try to extract JSON from the response
                    analysis_result = self._extract_json_from_response(response.text)
                    thought_process = "Used LLM with JSON extraction due to parsing issues"
                
            except Exception as e:
                print(f"⚠️  LLM regulation matching failed: {e}")
                print(f"🔍 Error type: {type(e).__name__}")
                analysis_result = self._fallback_regulation_matching(feature_analysis)
                thought_process = "Used fallback pattern matching due to LLM failure"
        else:
            analysis_result = self._fallback_regulation_matching(feature_analysis)
            thought_process = "Used fallback pattern matching (no LLM available)"
        
        # Calculate processing time
        processing_time = (datetime.now() - start_time).total_seconds()
        
        # Create agent output
        agent_output = AgentOutput(
            agent_name="Regulation Matcher",
            input_data={"feature_analysis": feature_analysis},
            thought_process=thought_process,
            analysis_result=analysis_result,
            confidence_score=0.80 if self.llm else 0.60,
            processing_time=processing_time,
            timestamp=datetime.now().isoformat()
        )
        
        print(f"✅ [Regulation Matcher] Completed in {processing_time:.2f}s")
        print(f"   📋 Applicable regulations: {analysis_result.get('applicable_regulations', [])}")
        print(f"   🎯 Compliance priority: {analysis_result.get('compliance_priority', 'unknown')}")
        
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
            # Look for applicable_regulations
            regulations_pattern = r'"applicable_regulations":\s*\[([^\]]+)\]'
            regulations_match = re.search(regulations_pattern, cleaned_text)
            applicable_regulations = []
            if regulations_match:
                regulations_str = regulations_match.group(1)
                applicable_regulations = re.findall(r'"([^"]+)"', regulations_str)
            
            # Look for compliance_priority
            priority_pattern = r'"compliance_priority":\s*"([^"]+)"'
            priority_match = re.search(priority_pattern, cleaned_text)
            compliance_priority = priority_match.group(1) if priority_match else "medium"
            
            # Look for key_requirements
            requirements_pattern = r'"key_requirements":\s*\[([^\]]+)\]'
            requirements_match = re.search(requirements_pattern, cleaned_text)
            key_requirements = []
            if requirements_match:
                requirements_str = requirements_match.group(1)
                key_requirements = re.findall(r'"([^"]+)"', requirements_str)
            
            return {
                "applicable_regulations": applicable_regulations or ["GDPR", "CCPA"],
                "regulation_reasons": {
                    "GDPR": "Processing personal data of EU residents",
                    "CCPA": "California residents' data processing"
                },
                "compliance_priority": compliance_priority,
                "key_requirements": key_requirements or ["consent_management", "data_minimization"],
                "risk_areas": ["consent_management", "data_retention"]
            }
        except:
            pass
        
        # If no JSON found, return default structure
        return {
            "applicable_regulations": ["GDPR", "CCPA"],
            "regulation_reasons": {
                "GDPR": "Processing personal data of EU residents",
                "CCPA": "California residents' data processing"
            },
            "compliance_priority": "medium",
            "key_requirements": ["consent_management", "data_minimization"],
            "risk_areas": ["consent_management", "data_retention"]
        }
    
    def _fallback_regulation_matching(self, feature_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback regulation matching"""
        data_types = feature_analysis.get("data_types_collected", [])
        
        applicable_regulations = []
        if "personal_data" in data_types:
            applicable_regulations.extend(["GDPR", "CCPA", "PIPL", "LGPD"])
        
        return {
            "applicable_regulations": list(set(applicable_regulations)),
            "regulation_reasons": {
                "GDPR": "Personal data processing detected",
                "CCPA": "Personal data processing detected",
                "PIPL": "Personal data processing detected",
                "LGPD": "Personal data processing detected"
            },
            "key_requirements": ["consent_management", "data_minimization"],
            "compliance_priority": "medium",
            "geographic_scope": ["EU", "California", "China", "Brazil"]
        }
