"""
Feature Analyzer Agent - Extracts compliance-relevant information from documents
"""

import json
from datetime import datetime
from typing import Dict, Any
from .models import AgentOutput


class FeatureAnalyzerAgent:
    """Feature Analyzer Agent - Extracts compliance-relevant information"""
    
    def __init__(self, llm=None):
        self.llm = llm
    
    def analyze(self, feature_name: str, feature_description: str, feature_content: str) -> AgentOutput:
        """Analyze feature and extract compliance-relevant information"""
        start_time = datetime.now()
        
        # Optimized prompt - more concise and focused
        prompt = f"""Analyze this feature for compliance:

Name: {feature_name}
Description: {feature_description}
Content: {feature_content[:1500]}{'...' if len(feature_content) > 1500 else ''}

Return JSON:
{{
    "data_types_collected": ["personal_data", "location_data"],
    "processing_purposes": ["analytics", "personalization"],
    "data_flows": ["user_input", "cloud_storage"],
    "user_interactions": ["consent_required", "opt_out_available"],
    "technical_implementation": ["encryption", "anonymization"],
    "compliance_concerns": ["data_minimization", "consent_management"]
}}

Focus on data types, processing purposes, and compliance concerns."""
        
        # Execute analysis
        if self.llm:
            try:
                response = self.llm.generate_content(prompt)
                
                if not response or not response.text:
                    raise Exception("LLM returned empty response")
                
                # Try to parse JSON response
                try:
                    analysis_result = json.loads(response.text)
                    thought_process = "Used LLM to analyze feature structure"
                except json.JSONDecodeError:
                    analysis_result = self._extract_json_from_response(response.text)
                    thought_process = "Used LLM with JSON extraction"
                
            except Exception as e:
                analysis_result = self._fallback_analysis(feature_content)
                thought_process = f"Used fallback analysis due to LLM failure: {e}"
        else:
            analysis_result = self._fallback_analysis(feature_content)
            thought_process = "Used fallback analysis (no LLM available)"
        
        # Calculate processing time
        processing_time = (datetime.now() - start_time).total_seconds()
        
        # Create agent output
        agent_output = AgentOutput(
            agent_name="Feature Analyzer",
            input_data={
                "feature_name": feature_name,
                "feature_description": feature_description,
                "content_length": len(feature_content)
            },
            thought_process=thought_process,
            analysis_result=analysis_result,
            confidence_score=0.85 if self.llm else 0.65,
            processing_time=processing_time,
            timestamp=datetime.now().isoformat()
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
            # Look for data_types_collected
            data_types_pattern = r'"data_types_collected":\s*\[([^\]]+)\]'
            data_types_match = re.search(data_types_pattern, cleaned_text)
            data_types = []
            if data_types_match:
                data_types_str = data_types_match.group(1)
                data_types = re.findall(r'"([^"]+)"', data_types_str)
            
            # Look for processing_purposes
            purposes_pattern = r'"processing_purposes":\s*\[([^\]]+)\]'
            purposes_match = re.search(purposes_pattern, cleaned_text)
            processing_purposes = []
            if purposes_match:
                purposes_str = purposes_match.group(1)
                processing_purposes = re.findall(r'"([^"]+)"', purposes_str)
            
            # Look for compliance_concerns
            concerns_pattern = r'"compliance_concerns":\s*\[([^\]]+)\]'
            concerns_match = re.search(concerns_pattern, cleaned_text)
            compliance_concerns = []
            if concerns_match:
                concerns_str = concerns_match.group(1)
                compliance_concerns = re.findall(r'"([^"]+)"', concerns_str)
            
            return {
                "data_types_collected": data_types or ["personal_data"],
                "processing_purposes": processing_purposes or ["analytics"],
                "data_flows": ["user_input", "cloud_storage"],
                "user_interactions": ["consent_required", "opt_out_available"],
                "technical_implementation": ["encryption", "anonymization"],
                "compliance_concerns": compliance_concerns or ["data_minimization", "consent_management"]
            }
        except:
            pass
        
        # If no JSON found, return default structure
        return {
            "data_types_collected": ["personal_data"],
            "processing_purposes": ["analytics"],
            "data_flows": ["user_input", "cloud_storage"],
            "user_interactions": ["consent_required", "opt_out_available"],
            "technical_implementation": ["encryption", "anonymization"],
            "compliance_concerns": ["data_minimization", "consent_management"]
        }
    
    def _fallback_analysis(self, feature_content: str) -> Dict[str, Any]:
        """Fallback feature analysis using pattern matching"""
        content_lower = feature_content.lower()
        
        data_types = []
        if any(term in content_lower for term in ["personal", "user", "customer"]):
            data_types.append("personal_data")
        if any(term in content_lower for term in ["location", "gps", "geolocation"]):
            data_types.append("location_data")
        if any(term in content_lower for term in ["facial", "fingerprint", "biometric"]):
            data_types.append("biometric_data")
        
        return {
            "data_types_collected": data_types or ["personal_data"],
            "processing_purposes": ["analytics", "personalization"],
            "data_flows": ["user_input", "cloud_storage"],
            "user_interactions": ["consent_required"],
            "technical_implementation": ["encryption"],
            "compliance_concerns": ["data_minimization", "consent_management"]
        }
