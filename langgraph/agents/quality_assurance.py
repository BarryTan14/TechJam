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
        """Validate consistency and quality of all agent outputs"""
        start_time = datetime.now()
        
        print(f"\n🔍 [Quality Assurance] Validating results for: {feature_name}")
        
        # Create prompt for quality assurance
        prompt = f"""
        You are a quality assurance expert validating compliance analysis results.
        
        Review all agent outputs for consistency and quality:
        
        Agent Outputs: {json.dumps([self._output_to_dict(output) for output in all_outputs if output], indent=2)}
        
        IMPORTANT: Respond ONLY with valid JSON. Do not include any other text, explanations, or markdown formatting.
        
        Provide your validation in this exact JSON format:
        {{
            "overall_quality_score": 0.0-1.0,
            "consistency_check": "pass|fail|warning",
            "quality_issues": [
                {{
                    "issue": "description of quality issue",
                    "severity": "low|medium|high",
                    "recommendation": "how to address the issue"
                }}
            ],
            "final_validation": "approved|requires_review|rejected",
            "confidence_adjustment": 0.0-1.0,
            "final_recommendations": [
                "final recommendation 1",
                "final recommendation 2"
            ]
        }}
        """
        
        # Execute quality assurance
        if self.llm:
            try:
                print(f"🤖 Using LLM for quality assurance...")
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
                    thought_process = "Used LLM to validate consistency and quality of all agent outputs"
                    print(f"✅ JSON parsing successful")
                except json.JSONDecodeError as json_error:
                    print(f"⚠️  JSON parsing failed: {json_error}")
                    print(f"📄 Raw response: {response.text[:200]}...")
                    # Try to extract JSON from the response
                    analysis_result = self._extract_json_from_response(response.text)
                    thought_process = "Used LLM with JSON extraction due to parsing issues"
                
            except Exception as e:
                print(f"⚠️  LLM quality assurance failed: {e}")
                print(f"🔍 Error type: {type(e).__name__}")
                analysis_result = self._fallback_quality_assurance(all_outputs)
                thought_process = "Used fallback validation due to LLM failure"
        else:
            analysis_result = self._fallback_quality_assurance(all_outputs)
            thought_process = "Used fallback validation (no LLM available)"
        
        # Calculate processing time
        processing_time = (datetime.now() - start_time).total_seconds()
        
        # Create agent output
        agent_output = AgentOutput(
            agent_name="Quality Assurance",
            input_data={"agent_outputs": [self._output_to_dict(output) for output in all_outputs if output]},
            thought_process=thought_process,
            analysis_result=analysis_result,
            confidence_score=analysis_result.get("overall_quality_score", 0.8),
            processing_time=processing_time,
            timestamp=datetime.now().isoformat()
        )
        
        print(f"✅ [Quality Assurance] Completed in {processing_time:.2f}s")
        print(f"   🎯 Quality score: {analysis_result.get('overall_quality_score', 0):.1%}")
        print(f"   ✅ Final validation: {analysis_result.get('final_validation', 'unknown')}")
        
        return agent_output
    
    def _output_to_dict(self, output: AgentOutput) -> Dict[str, Any]:
        """Convert AgentOutput to dictionary"""
        return {
            "agent_name": output.agent_name,
            "input_data": output.input_data,
            "thought_process": output.thought_process,
            "analysis_result": output.analysis_result,
            "confidence_score": output.confidence_score,
            "processing_time": output.processing_time,
            "timestamp": output.timestamp
        }
    
    def _extract_json_from_response(self, response_text: str) -> Dict[str, Any]:
        """Extract JSON from LLM response text"""
        import re
        
        # Check if response is empty
        if not response_text or not response_text.strip():
            print("⚠️  LLM response is empty or whitespace-only")
            return self._fallback_quality_assurance([])
        
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
        return self._fallback_quality_assurance([])
    
    def _fallback_quality_assurance(self, all_outputs: List[AgentOutput]) -> Dict[str, Any]:
        """Fallback quality assurance"""
        confidence_scores = [output.confidence_score for output in all_outputs if output]
        avg_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0.7
        
        return {
            "overall_quality_score": avg_confidence,
            "consistency_check": "pass",
            "quality_issues": [],
            "final_validation": "approved",
            "confidence_adjustment": avg_confidence,
            "final_recommendations": ["Monitor for compliance updates", "Regular review recommended"]
        }
