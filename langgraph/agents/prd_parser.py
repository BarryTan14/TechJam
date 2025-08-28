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
        
        # Create optimized prompt for PRD parsing that handles both detailed and concise PRDs
        prompt = f"""
Extract features from this PRD content:

Name: {prd_name}
Description: {prd_description}
Content: {prd_content}

Analyze the content and extract distinct features. A feature can be:
- A specific functionality or capability
- A data processing operation
- A system component
- A business process

For each feature, provide:
- feature_id: unique identifier (feature_1, feature_2, etc.)
- feature_name: clear, descriptive name
- feature_description: what the feature does
- feature_content: relevant text from the PRD
- section: where this feature is described
- priority: High/Medium/Low
- complexity: High/Medium/Low
- data_types: list of data types handled
- user_impact: how it affects users
- technical_requirements: technical needs
- compliance_considerations: compliance issues

Return JSON with this structure:
{{
    "extracted_features": [
        {{
            "feature_id": "feature_1",
            "feature_name": "Feature Name",
            "feature_description": "Brief description",
            "feature_content": "Relevant content from PRD",
            "section": "Section name",
            "priority": "High",
            "complexity": "Medium",
            "data_types": ["data_type1", "data_type2"],
            "user_impact": "Impact description",
            "technical_requirements": ["req1", "req2"],
            "compliance_considerations": ["GDPR", "CCPA"]
        }}
    ],
    "total_features": 1,
    "analysis_summary": "Summary of extracted features"
}}
"""
        
        # Execute PRD parsing using LLM
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
        
        # Calculate processing time
        processing_time = (datetime.now() - start_time).total_seconds()
        
        # Create agent output
        agent_output = AgentOutput(
            agent_name="PRD Parser",
            input_data={
                "prd_name": prd_name,
                "prd_description": prd_description,
                "prd_content": prd_content
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
        
        # If still no JSON found, try to extract just the extracted_features array
        try:
            # Look for extracted_features pattern
            features_pattern = r'"extracted_features":\s*\[([^\]]+)\]'
            features_match = re.search(features_pattern, cleaned_text)
            if features_match:
                features_str = features_match.group(1)
                # Try to extract individual feature objects
                feature_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
                feature_matches = re.findall(feature_pattern, features_str, re.DOTALL)
                
                extracted_features = []
                for i, feature_match in enumerate(feature_matches, 1):
                    try:
                        feature_data = json.loads(feature_match)
                        # Ensure required fields exist
                        if "feature_name" in feature_data:
                            extracted_features.append(feature_data)
                    except json.JSONDecodeError:
                        continue
                
                if extracted_features:
                    return {
                        "extracted_features": extracted_features,
                        "total_features": len(extracted_features),
                        "analysis_summary": f"Extracted {len(extracted_features)} features from PRD"
                    }
        except:
            pass
        
        # If no JSON found, create a basic feature from the content
        return {
            "extracted_features": [
                {
                    "feature_id": "feature_1",
                    "feature_name": "PRD Feature",
                    "feature_description": "Feature extracted from PRD content",
                    "feature_content": response_text[:500] + "..." if len(response_text) > 500 else response_text,
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
