"""
Reasoning Generator Agent - Produces clear justifications for compliance decisions
"""

import json
from datetime import datetime
from typing import Dict, Any
from .models import AgentOutput


class ReasoningGeneratorAgent:
    """Reasoning Generator Agent - Produces clear justifications"""
    
    def __init__(self, llm=None):
        self.llm = llm
    
    def generate_reasoning(self, feature_name: str, feature_analysis: Dict[str, Any], 
                          regulation_matching: Dict[str, Any], risk_assessment: Dict[str, Any]) -> AgentOutput:
        """Generate clear reasoning based on all previous analyses"""
        start_time = datetime.now()
        
        print(f"\n💭 [Reasoning Generator] Generating reasoning for: {feature_name}")
        
        # Create prompt for reasoning generation
        prompt = f"""
        You are a compliance reasoning expert creating clear justifications.
        
        Based on the complete analysis, generate clear reasoning:
        
        Feature Analysis: {json.dumps(feature_analysis, indent=2)}
        Regulation Matching: {json.dumps(regulation_matching, indent=2)}
        Risk Assessment: {json.dumps(risk_assessment, indent=2)}
        
        IMPORTANT: Respond ONLY with valid JSON. Do not include any other text, explanations, or markdown formatting.
        
        Provide your reasoning in this exact JSON format:
        {{
            "executive_summary": "Clear summary of compliance status",
            "detailed_reasoning": "Step-by-step explanation of compliance analysis",
            "key_findings": [
                "finding 1 with explanation",
                "finding 2 with explanation"
            ],
            "compliance_status": "compliant|non_compliant|requires_review",
            "audit_evidence": [
                "evidence point 1",
                "evidence point 2"
            ],
            "recommendations": [
                "specific recommendation 1",
                "specific recommendation 2"
            ]
        }}
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
                analysis_result = self._fallback_reasoning_generation(feature_analysis, regulation_matching, risk_assessment)
                thought_process = "Used fallback pattern matching due to LLM failure"
        else:
            analysis_result = self._fallback_reasoning_generation(feature_analysis, regulation_matching, risk_assessment)
            thought_process = "Used fallback pattern matching (no LLM available)"
        
        # Calculate processing time
        processing_time = (datetime.now() - start_time).total_seconds()
        
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
            timestamp=datetime.now().isoformat()
        )
        
        print(f"✅ [Reasoning Generator] Completed in {processing_time:.2f}s")
        print(f"   📝 Compliance status: {analysis_result.get('compliance_status', 'unknown')}")
        print(f"   💡 Recommendations: {len(analysis_result.get('recommendations', []))}")
        
        return agent_output
    
    def _extract_json_from_response(self, response_text: str) -> Dict[str, Any]:
        """Extract JSON from LLM response text"""
        import re
        
        # Check if response is empty
        if not response_text or not response_text.strip():
            print("⚠️  LLM response is empty or whitespace-only")
            return self._fallback_reasoning_generation({}, {}, {})
        
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
        return self._fallback_reasoning_generation({}, {}, {})
    
    def _fallback_reasoning_generation(self, feature_analysis: Dict[str, Any], 
                                     regulation_matching: Dict[str, Any], 
                                     risk_assessment: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback reasoning generation"""
        risk_level = risk_assessment.get("overall_risk_level", "medium")
        regulations = regulation_matching.get("applicable_regulations", [])
        
        return {
            "executive_summary": f"Feature requires {risk_level} level compliance attention for {', '.join(regulations)}",
            "detailed_reasoning": "Analysis completed using pattern matching due to LLM unavailability",
            "key_findings": [
                f"Feature processes {len(feature_analysis.get('data_types_collected', []))} data types",
                f"Applies to {len(regulations)} regulations"
            ],
            "compliance_status": "requires_review" if risk_level == "high" else "compliant",
            "audit_evidence": ["Pattern matching analysis completed", "Risk level assessed"],
            "recommendations": ["Review consent mechanisms", "Implement data minimization"]
        }
