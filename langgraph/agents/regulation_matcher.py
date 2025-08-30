"""
Regulation Matcher Agent - Matches features to relevant regulations
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


class RegulationMatcherAgent:
    """Regulation Matcher Agent - Matches features to relevant regulations"""
    
    def __init__(self, llm=None):
        self.llm = llm
    
    def match_regulations(self, feature_name: str, feature_analysis: Dict[str, Any]) -> AgentOutput:
        """Match feature analysis to applicable regulations"""
        start_time = get_singapore_time()
        
        # Optimized prompt - more concise and focused
        prompt = f"""Match this feature to regulations:

Feature: {feature_name}
Analysis: {json.dumps(feature_analysis, indent=2)}

Available Regulations:
- GDPR (EU): Personal data processing, consent, data rights
- CCPA (California): Consumer privacy, data sales, access rights
- PIPL (China): Personal information, data localization
- LGPD (Brazil): Data protection, legal basis, data subject rights

Return JSON:
{{
    "applicable_regulations": ["GDPR", "CCPA"],
    "regulation_reasons": {{
        "GDPR": "reason why GDPR applies",
        "CCPA": "reason why CCPA applies"
    }},
    "key_requirements": ["consent_management", "data_minimization"],
    "compliance_priority": "high|medium|low",
    "geographic_scope": ["EU", "California"]
}}"""
        
        # Execute regulation matching
        if self.llm:
            try:
                response = self.llm.generate_content(prompt)
                
                if not response or not response.text:
                    raise Exception("LLM returned empty response")
                
                # Try to parse JSON response
                try:
                    analysis_result = json.loads(response.text)
                    thought_process = "Used LLM to match feature requirements to applicable regulations"
                except json.JSONDecodeError:
                    analysis_result = self._extract_json_from_response(response.text)
                    thought_process = "Used LLM with JSON extraction"
                
            except Exception as e:
                raise Exception(f"Regulation matching failed: {e}")
        else:
            raise Exception("No LLM available for regulation matching")
        
        # Calculate processing time
        processing_time = (get_singapore_time() - start_time).total_seconds()
        
        # Create agent output
        agent_output = AgentOutput(
            agent_name="Regulation Matcher",
            input_data={"feature_analysis": feature_analysis},
            thought_process=thought_process,
            analysis_result=analysis_result,
            confidence_score=0.80 if self.llm else 0.60,
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
                "geographic_scope": ["EU", "California"]
            }
        except:
            pass
        
        # If no JSON found, raise an exception
        raise Exception("Failed to extract valid JSON from LLM response")
    

