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
        
        print(f"\n🔍 [Feature Analyzer] Processing feature: {feature_name}")
        
        # Create prompt for feature analysis
        prompt = f"""
        You are a compliance expert analyzing software features for regulatory requirements.
        
        Analyze the following feature and extract compliance-relevant information:
        
        Feature Name: {feature_name}
        Description: {feature_description}
        Content: {feature_content}
        
        IMPORTANT: Respond ONLY with valid JSON. Do not include any other text, explanations, or markdown formatting.
        
        Provide your analysis in this exact JSON format:
        {{
            "data_types_collected": ["personal_data", "location_data", "biometric_data"],
            "processing_purposes": ["analytics", "personalization", "advertising"],
            "data_flows": ["user_input", "cloud_storage", "third_party", "cross_border"],
            "user_interactions": ["consent_required", "opt_out_available", "data_access"],
            "technical_implementation": ["encryption", "anonymization", "retention_policy"],
            "compliance_concerns": ["data_minimization", "purpose_limitation", "consent_management"]
        }}
        
        Analysis steps:
        1. Identify data types being collected
        2. Determine processing purposes
        3. Map data flows and storage
        4. List user interactions and controls
        5. Note technical safeguards
        6. Identify compliance concerns
        """
        
        # Execute analysis
        if self.llm:
            try:
                print(f"🤖 Using LLM for analysis...")
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
                    thought_process = "Used LLM to analyze feature structure and extract compliance-relevant information"
                    print(f"✅ JSON parsing successful")
                except json.JSONDecodeError as json_error:
                    print(f"⚠️  JSON parsing failed: {json_error}")
                    print(f"📄 Raw response: {response.text[:200]}...")
                    # Try to extract JSON from the response
                    analysis_result = self._extract_json_from_response(response.text)
                    thought_process = "Used LLM with JSON extraction due to parsing issues"
                
            except Exception as e:
                print(f"⚠️  LLM analysis failed: {e}")
                print(f"🔍 Error type: {type(e).__name__}")
                analysis_result = self._fallback_analysis(feature_content)
                thought_process = "Used fallback pattern matching due to LLM failure"
        else:
            analysis_result = self._fallback_analysis(feature_content)
            thought_process = "Used fallback pattern matching (no LLM available)"
        
        # Calculate processing time
        processing_time = (datetime.now() - start_time).total_seconds()
        
        # Create agent output
        agent_output = AgentOutput(
            agent_name="Feature Analyzer",
            input_data={
                "feature_name": feature_name,
                "feature_description": feature_description,
                "feature_content": feature_content
            },
            thought_process=thought_process,
            analysis_result=analysis_result,
            confidence_score=0.85 if self.llm else 0.65,
            processing_time=processing_time,
            timestamp=datetime.now().isoformat()
        )
        
        print(f"✅ [Feature Analyzer] Completed in {processing_time:.2f}s")
        print(f"   📊 Data types: {analysis_result.get('data_types_collected', [])}")
        print(f"   🎯 Processing purposes: {analysis_result.get('processing_purposes', [])}")
        
        return agent_output
    
    def _extract_json_from_response(self, response_text: str) -> Dict[str, Any]:
        """Extract JSON from LLM response text"""
        import re
        
        # Check if response is empty
        if not response_text or not response_text.strip():
            print("⚠️  LLM response is empty or whitespace-only")
            return self._fallback_analysis("")
        
        # Clean the response text
        cleaned_text = response_text.strip()
        
        # Remove markdown code blocks if present - handle multiline properly
        if cleaned_text.startswith('```json'):
            # Remove ```json and everything up to the first newline
            cleaned_text = re.sub(r'^```json\s*\n?', '', cleaned_text)
        elif cleaned_text.startswith('```'):
            # Remove ``` and everything up to the first newline
            cleaned_text = re.sub(r'^```\s*\n?', '', cleaned_text)
        
        # Remove trailing ```
        cleaned_text = re.sub(r'\n?```\s*$', '', cleaned_text)
        
        cleaned_text = cleaned_text.strip()
        
        # Try to parse the cleaned JSON directly
        try:
            return json.loads(cleaned_text)
        except json.JSONDecodeError:
            pass
        
        # Try to find JSON object in the response using a more robust pattern
        json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
        matches = re.findall(json_pattern, cleaned_text, re.DOTALL)
        
        if matches:
            for match in matches:
                try:
                    return json.loads(match)
                except json.JSONDecodeError:
                    continue
        
        # If no JSON found, return fallback
        print("⚠️  Could not extract JSON from LLM response")
        print(f"📄 Raw response: {response_text[:200]}...")
        return self._fallback_analysis("")
    
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
            "data_types_collected": data_types,
            "processing_purposes": ["analytics", "personalization"],
            "data_flows": ["user_input", "cloud_storage"],
            "user_interactions": ["consent_required"],
            "technical_implementation": ["encryption"],
            "compliance_concerns": ["data_minimization", "consent_management"]
        }
