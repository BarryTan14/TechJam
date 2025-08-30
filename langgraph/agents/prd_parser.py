"""
PRD Parser Agent - Extracts features from PRD documents
"""

import json
from datetime import datetime
from typing import Dict, Any, List
from .models import AgentOutput, ExtractedFeature


class PRDParserAgent:
    """PRD Parser Agent - Extracts features from PRD documents"""
    
    def __init__(self, llm=None):
        self.llm = llm
    
    def parse_prd(self, prd_name: str, prd_description: str, prd_content: str) -> AgentOutput:
        """Parse PRD and extract features"""
        start_time = datetime.now()
        
        # Optimized prompt - more concise and focused
        prompt = f"""Extract features from this PRD:

Name: {prd_name}
Description: {prd_description}
Content: {prd_content[:2000]}{'...' if len(prd_content) > 2000 else ''}

Return JSON with this structure:
{{
    "extracted_features": [
        {{
            "feature_id": "feature_1",
            "feature_name": "Feature Name",
            "feature_description": "Brief description",
            "feature_content": "Relevant content",
            "section": "Section name",
            "priority": "High/Medium/Low",
            "complexity": "High/Medium/Low",
            "data_types": ["data_type1"],
            "user_impact": "Impact description",
            "technical_requirements": ["req1"],
            "compliance_considerations": ["GDPR", "CCPA"]
        }}
    ],
    "total_features": 1,
    "analysis_summary": "Summary"
}}

Focus on distinct functionalities, data operations, and system components. Limit to 10 features maximum."""
        
        # Execute PRD parsing using LLM
        if self.llm:
            try:
                response = self.llm.generate_content(prompt)
                
                if not response or not response.text:
                    raise Exception("LLM returned empty response")
                
                # Try to parse JSON response
                try:
                    analysis_result = json.loads(response.text)
                    thought_process = "Used LLM to parse PRD and extract features"
                except json.JSONDecodeError:
                    analysis_result = self._extract_json_from_response(response.text)
                    thought_process = "Used LLM with JSON extraction"
            except Exception as e:
                print(f"⚠️ LLM parsing failed: {e}")
                analysis_result = self._fallback_parsing(prd_content)
                thought_process = "Used fallback parsing due to LLM failure"
        else:
            analysis_result = self._fallback_parsing(prd_content)
            thought_process = "Used fallback parsing (no LLM available)"
        
        # Calculate processing time
        processing_time = (datetime.now() - start_time).total_seconds()
        
        # Create agent output
        agent_output = AgentOutput(
            agent_name="PRD Parser",
            input_data={
                "prd_name": prd_name,
                "prd_description": prd_description,
                "prd_content_length": len(prd_content)
            },
            thought_process=thought_process,
            analysis_result=analysis_result,
            confidence_score=0.9,
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
        
        # If no JSON found, create a basic feature
        return self._fallback_parsing(cleaned_text)
    
    def _fallback_parsing(self, content: str) -> Dict[str, Any]:
        """Fallback parsing when LLM fails"""
        return {
            "extracted_features": [
                {
                    "feature_id": "feature_1",
                    "feature_name": "PRD Feature",
                    "feature_description": "Feature extracted from PRD content",
                    "feature_content": content[:500] + "..." if len(content) > 500 else content,
                    "section": "General",
                    "priority": "Medium",
                    "complexity": "Medium",
                    "data_types": ["unknown"],
                    "user_impact": "Unknown",
                    "technical_requirements": ["analysis_required"],
                    "compliance_considerations": ["GDPR", "CCPA"]
                }
            ],
            "total_features": 1,
            "analysis_summary": "Created basic feature from PRD content due to parsing issues"
        }
