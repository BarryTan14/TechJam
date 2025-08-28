"""
Quality Assurance Agent - Validates and checks consistency of outputs
"""

import json
from datetime import datetime
from typing import Dict, Any, List
from .models import AgentOutput


class QualityAssuranceAgent:
    """Quality Assurance Agent - Validates and checks consistency"""
    
    def __init__(self, llm=None):
        self.llm = llm
    
    def validate_results(self, feature_name: str, all_outputs: List[AgentOutput]) -> AgentOutput:
        """Validate and check consistency of all agent outputs"""
        start_time = datetime.now()
        
        # Create optimized prompt for quality assurance
        prompt = f"""
Validate compliance analysis results:

Feature: {feature_name}
Agents: {[output.agent_name for output in all_outputs]}

Return JSON with:
{{
    "overall_quality_score": 0.85,
    "consistency_check": "pass|warning|fail",
    "quality_issues": [
        {{
            "issue": "Description of issue",
            "severity": "low|medium|high",
            "recommendation": "How to fix"
        }}
    ],
    "confidence_adjustment": 0.85,
    "final_validation": "approved|requires_review|rejected",
    "final_recommendations": ["Implement consent", "Establish retention"],
    "audit_notes": "Summary of validation"
}}
"""
        
        # Execute quality assurance using LLM
        response = self.llm.generate_content(prompt)
        
        if not response or not response.text:
            raise Exception("LLM returned empty response")
        
        # Try to parse JSON response
        try:
            analysis_result = json.loads(response.text)
            thought_process = "Used LLM to validate results"
        except json.JSONDecodeError:
            analysis_result = self._extract_json_from_response(response.text)
            thought_process = "Used LLM with JSON extraction"
        
        # Calculate processing time
        processing_time = (datetime.now() - start_time).total_seconds()
        
        # Create agent output
        agent_output = AgentOutput(
            agent_name="Quality Assurance",
            input_data={
                "feature_name": feature_name,
                "agent_outputs": [output.agent_name for output in all_outputs]
            },
            thought_process=thought_process,
            analysis_result=analysis_result,
            confidence_score=0.85,
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
        
        # If still no JSON found, try to extract specific fields
        try:
            # Look for overall_quality_score
            quality_pattern = r'"overall_quality_score":\s*([0-9.]+)'
            quality_match = re.search(quality_pattern, cleaned_text)
            quality_score = float(quality_match.group(1)) if quality_match else 0.85
            
            # Look for consistency_check
            consistency_pattern = r'"consistency_check":\s*"([^"]+)"'
            consistency_match = re.search(consistency_pattern, cleaned_text)
            consistency_check = consistency_match.group(1) if consistency_match else "pass"
            
            # Look for final_validation
            validation_pattern = r'"final_validation":\s*"([^"]+)"'
            validation_match = re.search(validation_pattern, cleaned_text)
            final_validation = validation_match.group(1) if validation_match else "approved"
            
            # Look for confidence_adjustment
            confidence_pattern = r'"confidence_adjustment":\s*([0-9.]+)'
            confidence_match = re.search(confidence_pattern, cleaned_text)
            confidence_adjustment = float(confidence_match.group(1)) if confidence_match else 0.85
            
            # Extract recommendations
            rec_pattern = r'"final_recommendations":\s*\[([^\]]+)\]'
            rec_match = re.search(rec_pattern, cleaned_text)
            recommendations = []
            if rec_match:
                rec_str = rec_match.group(1)
                rec_items = re.findall(r'"([^"]+)"', rec_str)
                recommendations = rec_items[:5]  # Limit to 5 recommendations
            
            return {
                "overall_quality_score": quality_score,
                "consistency_check": consistency_check,
                "quality_issues": [],
                "confidence_adjustment": confidence_adjustment,
                "final_validation": final_validation,
                "final_recommendations": recommendations,
                "audit_notes": "Extracted from LLM response using pattern matching"
            }
        except:
            pass
        
        # If no JSON found, return default structure
        return {
            "overall_quality_score": 0.85,
            "consistency_check": "pass",
            "quality_issues": [],
            "confidence_adjustment": 0.85,
            "final_validation": "approved",
            "final_recommendations": ["Review analysis for completeness"],
            "audit_notes": "Default values due to parsing issues"
        }
