"""
Optimized State Analyzer - Efficient batch analysis of features against states
"""

import json
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass

from .models import AgentOutput, ExtractedFeature
from .state_regulations_cache import state_regulations_cache, StateRegulation


@dataclass
class StateAnalysisResult:
    """Result of analyzing a feature against a state"""
    state_code: str
    state_name: str
    feature_id: str
    feature_name: str
    risk_score: float
    risk_level: str
    is_compliant: bool
    non_compliant_regulations: List[str]
    required_actions: List[str]
    reasoning: str
    confidence_score: float
    processing_time: float


@dataclass
class BatchAnalysisResult:
    """Result of batch analysis for multiple features against multiple states"""
    state_results: Dict[str, List[StateAnalysisResult]]
    feature_results: Dict[str, List[StateAnalysisResult]]
    overall_stats: Dict[str, Any]
    processing_time: float


class OptimizedStateAnalyzer:
    """Optimized analyzer for efficient state-feature compliance analysis"""
    
    def __init__(self, llm=None):
        self.llm = llm
        self.agent_name = "Optimized State Analyzer"
        self.state_cache = state_regulations_cache
    
    def analyze_features_against_states(self, features: List[ExtractedFeature], 
                                      target_states: Optional[List[str]] = None) -> BatchAnalysisResult:
        """
        Analyze all features against all states efficiently using batch processing
        
        Args:
            features: List of features to analyze
            target_states: Optional list of state codes to analyze (if None, analyzes all states)
            
        Returns:
            BatchAnalysisResult containing all analysis results
        """
        start_time = datetime.now()
        
        # Get states to analyze
        if target_states is None:
            states = list(self.state_cache.get_all_states().keys())
        else:
            states = [s.upper() for s in target_states if s.upper() in self.state_cache.get_all_states()]
        
        print(f"🔍 Analyzing {len(features)} features against {len(states)} states...")
        
        # Initialize result containers
        state_results = {state_code: [] for state_code in states}
        feature_results = {feature.feature_id: [] for feature in features}
        
        # Group states by risk level for efficient processing
        high_risk_states = self.state_cache.get_high_risk_states()
        medium_risk_states = self.state_cache.get_medium_risk_states()
        low_risk_states = self.state_cache.get_low_risk_states()
        
        # Process high-risk states first (most important)
        print(f"🚨 Processing {len(high_risk_states)} high-risk states...")
        for state_code in high_risk_states:
            if state_code in states:
                state_results[state_code] = self._analyze_features_for_state(features, state_code, "high")
        
        # Process medium-risk states
        print(f"⚠️ Processing {len(medium_risk_states)} medium-risk states...")
        for state_code in medium_risk_states:
            if state_code in states:
                state_results[state_code] = self._analyze_features_for_state(features, state_code, "medium")
        
        # Process low-risk states (can use simplified analysis)
        print(f"✅ Processing {len(low_risk_states)} low-risk states...")
        for state_code in low_risk_states:
            if state_code in states:
                state_results[state_code] = self._analyze_features_for_state(features, state_code, "low")
        
        # Organize results by feature
        for state_code, results in state_results.items():
            for result in results:
                feature_results[result.feature_id].append(result)
        
        # Calculate overall statistics
        overall_stats = self._calculate_overall_stats(state_results, feature_results)
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        return BatchAnalysisResult(
            state_results=state_results,
            feature_results=feature_results,
            overall_stats=overall_stats,
            processing_time=processing_time
        )
    
    def _analyze_features_for_state(self, features: List[ExtractedFeature], 
                                  state_code: str, risk_level: str) -> List[StateAnalysisResult]:
        """
        Analyze all features against a specific state
        
        Args:
            features: List of features to analyze
            state_code: State code to analyze against
            risk_level: Risk level of the state (high/medium/low)
            
        Returns:
            List of StateAnalysisResult objects
        """
        state_regulation = self.state_cache.get_state_regulation(state_code)
        if not state_regulation:
            return []
        
        results = []
        
        # Use different analysis strategies based on risk level
        if risk_level == "high":
            # High-risk states: Use LLM for detailed analysis
            results = self._analyze_high_risk_state(features, state_regulation)
        elif risk_level == "medium":
            # Medium-risk states: Use LLM for analysis
            results = self._analyze_medium_risk_state(features, state_regulation)
        else:
            # Low-risk states: Use LLM for analysis
            results = self._analyze_low_risk_state(features, state_regulation)
        
        return results
    
    def _analyze_high_risk_state(self, features: List[ExtractedFeature], 
                                state_regulation: StateRegulation) -> List[StateAnalysisResult]:
        """Analyze features against high-risk state using LLM"""
        if not self.llm:
            raise Exception(f"No LLM available for high-risk state analysis of {state_regulation.state_name}")
        
        try:
            # Use batch LLM analysis for efficiency
            results = self._batch_llm_analysis(features, state_regulation)
            return results
        except Exception as e:
            print(f"⚠️ LLM analysis failed for {state_regulation.state_name}: {e}")
            raise Exception(f"High-risk state analysis failed for {state_regulation.state_name}: {e}")
    
    def _analyze_medium_risk_state(self, features: List[ExtractedFeature], 
                                  state_regulation: StateRegulation) -> List[StateAnalysisResult]:
        """Analyze features against medium-risk state using LLM"""
        if not self.llm:
            raise Exception(f"No LLM available for medium-risk state analysis of {state_regulation.state_name}")
        
        try:
            # Use batch LLM analysis for efficiency
            results = self._batch_llm_analysis(features, state_regulation)
            return results
        except Exception as e:
            print(f"⚠️ LLM analysis failed for {state_regulation.state_name}: {e}")
            raise Exception(f"Medium-risk state analysis failed for {state_regulation.state_name}: {e}")
    
    def _analyze_low_risk_state(self, features: List[ExtractedFeature], 
                               state_regulation: StateRegulation) -> List[StateAnalysisResult]:
        """Analyze features against low-risk state using LLM"""
        if not self.llm:
            raise Exception(f"No LLM available for low-risk state analysis of {state_regulation.state_name}")
        
        try:
            # Use batch LLM analysis for efficiency
            results = self._batch_llm_analysis(features, state_regulation)
            return results
        except Exception as e:
            print(f"⚠️ LLM analysis failed for {state_regulation.state_name}: {e}")
            raise Exception(f"Low-risk state analysis failed for {state_regulation.state_name}: {e}")
    
    def _batch_llm_analysis(self, features: List[ExtractedFeature], 
                           state_regulation: StateRegulation) -> List[StateAnalysisResult]:
        """Use LLM to analyze all features against a state in a single call"""
        
        # Prepare feature summaries for efficient analysis
        feature_summaries = []
        for feature in features:
            feature_summaries.append({
                "feature_id": feature.feature_id,
                "feature_name": feature.feature_name,
                "feature_description": feature.feature_description[:300],
                "data_types": feature.data_types,
                "technical_requirements": feature.technical_requirements[:5] if feature.technical_requirements else []
            })
        
        # Create comprehensive prompt for detailed analysis
        prompt = f"""Perform a comprehensive compliance analysis for {len(features)} features against {state_regulation.state_name} ({state_regulation.state_code}) regulations.

STATE REGULATORY CONTEXT:
- State: {state_regulation.state_name} ({state_regulation.state_code})
- Applicable Regulations: {', '.join(state_regulation.regulations)}
- Risk Level: {state_regulation.risk_level.upper()}
- Enforcement Level: {state_regulation.enforcement_level.upper()}
- Key Requirements: {', '.join(state_regulation.key_requirements)}
- Potential Penalties: {', '.join(state_regulation.penalties)}
- Effective Date: {state_regulation.effective_date}

FEATURES TO ANALYZE:
{json.dumps(feature_summaries, indent=2)}

ANALYSIS REQUIREMENTS:
For each feature, provide a detailed analysis including:

1. **Data Type Assessment**: Evaluate the sensitivity of data types being collected
2. **Requirement Mapping**: Check each key requirement against the feature implementation
3. **Compliance Status**: Determine if the feature meets state requirements
4. **Risk Assessment**: Calculate risk based on data sensitivity and compliance gaps (ONLY use "low" or "high" - no "medium" or "critical")
5. **Detailed Reasoning**: Provide comprehensive explanation of findings
6. **Required Actions**: List specific actions needed for compliance

CRITICAL JSON FORMATTING REQUIREMENTS:
- Respond ONLY with valid JSON - no additional text, explanations, or markdown
- Use ONLY standard ASCII characters - no special characters, emojis, or Unicode
- Use ONLY double quotes for strings - no single quotes or smart quotes
- Escape all special characters in strings properly
- Use ONLY "true" or "false" for boolean values - no "True" or "False"
- Ensure all strings are properly quoted and escaped
- Remove any trailing commas in objects and arrays
- Use ONLY standard JSON syntax - no comments or extra formatting

Return JSON with detailed analysis for each feature:
{{
    "feature_results": [
        {{
            "feature_id": "feature_1",
            "risk_score": 0.3,
            "risk_level": "low",
            "is_compliant": true,
            "non_compliant_regulations": ["regulation_name"],
            "required_actions": ["Implement specific compliance measures", "Establish data protection controls", "Create audit procedures"],
            "reasoning": "COMPREHENSIVE ANALYSIS: Include detailed explanation of data types, requirement compliance, risk factors, and specific compliance gaps. Use clear language and provide actionable insights.",
            "confidence_score": 0.8
        }}
    ]
}}

IMPORTANT: Provide detailed, actionable reasoning that explains:
- Why the feature is compliant or non-compliant
- Which specific requirements are met or violated
- What data types create compliance risks
- How the state's enforcement level affects the analysis
- Specific steps needed to achieve compliance

For required_actions, provide specific, actionable recommendations such as:
- Technical implementation steps (e.g., "Implement PII encryption at rest and in transit")
- Policy and procedure updates (e.g., "Establish data retention policies for PII")
- Compliance measures (e.g., "Create PII inventory and mapping")
- Training and awareness (e.g., "Implement compliance training for development teams")
- Monitoring and auditing (e.g., "Establish compliance monitoring and reporting procedures")

Make the reasoning comprehensive and business-friendly.

REMEMBER: Respond with ONLY valid JSON - no other text or formatting."""
        
        try:
            response = self.llm.generate_content(prompt)
            
            # Validate response
            if not response:
                print(f"⚠️ LLM returned None response for {state_regulation.state_name}")
                raise Exception("LLM returned None response")
            
            if not response.text:
                print(f"⚠️ LLM returned empty text response for {state_regulation.state_name}")
                raise Exception("LLM returned empty text response")
            
            if not response.text.strip():
                print(f"⚠️ LLM returned whitespace-only response for {state_regulation.state_name}")
                raise Exception("LLM returned whitespace-only response")
            
            print(f"📝 LLM Response received for {state_regulation.state_name} ({len(response.text)} characters)")
            print(f"📄 Raw response preview: {response.text[:200]}...")
            
            # Pre-validate and sanitize the response
            try:
                sanitized_response = self._sanitize_llm_response(response.text)
                print(f"✅ Response sanitization completed successfully")
            except Exception as sanitize_error:
                print(f"⚠️ Response sanitization failed: {sanitize_error}")
                print(f"📄 Original response preview: {response.text[:200]}...")
                raise Exception(f"Response sanitization failed: {sanitize_error}")
            
            # Parse JSON response
            try:
                analysis_result = json.loads(sanitized_response)
                feature_results = analysis_result.get("feature_results", [])
                print(f"✅ JSON parsing successful for {state_regulation.state_name}")
            except json.JSONDecodeError as json_error:
                print(f"⚠️ JSON parsing failed for {state_regulation.state_name}: {json_error}")
                print(f"📄 Raw response: {response.text[:500]}...")
                # Try to extract JSON from response
                feature_results = self._extract_json_from_response(response.text)
            
            # Validate feature_results
            if not feature_results:
                print(f"⚠️ No feature results found for {state_regulation.state_name}")
                raise Exception("No feature results found in LLM response")
            
            # Convert to StateAnalysisResult objects
            results = []
            for i, result in enumerate(feature_results):
                if i < len(features):
                    feature = features[i]
                    
                    # Ensure risk_level is only "low" or "high"
                    risk_level = result.get("risk_level", "low")
                    if risk_level not in ["low", "high"]:
                        # Convert any other values to "low" or "high" based on risk_score
                        risk_score = result.get("risk_score", 0.5)
                        risk_level = "high" if risk_score >= 0.6 else "low"
                        print(f"⚠️ Converted risk_level from '{result.get('risk_level', 'unknown')}' to '{risk_level}' for {feature.feature_name}")
                    
                    state_result = StateAnalysisResult(
                        state_code=state_regulation.state_code,
                        state_name=state_regulation.state_name,
                        feature_id=feature.feature_id,
                        feature_name=feature.feature_name,
                        risk_score=result.get("risk_score", 0.5),
                        risk_level=risk_level,
                        is_compliant=result.get("is_compliant", True),
                        non_compliant_regulations=result.get("non_compliant_regulations", []),
                        required_actions=result.get("required_actions", []),
                        reasoning=result.get("reasoning", ""),
                        confidence_score=result.get("confidence_score", 0.8),
                        processing_time=0.0
                    )
                    results.append(state_result)
            
            print(f"✅ Successfully processed {len(results)} features for {state_regulation.state_name}")
            return results
            
        except Exception as e:
            print(f"❌ Batch LLM analysis failed for {state_regulation.state_name}: {e}")
            print(f"🔍 Error type: {type(e).__name__}")
            raise Exception(f"Batch LLM analysis failed for {state_regulation.state_name}: {e}")
    

    

    
    def _has_complex_features(self, features: List[ExtractedFeature]) -> bool:
        """Check if any features are complex enough to warrant LLM analysis"""
        complex_keywords = ["biometric", "health", "financial", "location", "behavioral", "tracking", "analytics"]
        
        for feature in features:
            feature_text = f"{feature.feature_name} {feature.feature_description}".lower()
            if any(keyword in feature_text for keyword in complex_keywords):
                return True
        
        return False
    

    
    def _extract_json_from_response(self, response_text: str) -> List[Dict[str, Any]]:
        """Extract JSON from LLM response text with robust error handling"""
        import re
        
        if not response_text or not response_text.strip():
            print("⚠️ Empty response text provided to JSON extraction")
            raise Exception("Empty response text provided to JSON extraction")
        
        # Clean the response text
        cleaned_text = response_text.strip()
        
        # Remove markdown code blocks
        cleaned_text = re.sub(r'^```json\s*\n?', '', cleaned_text)
        cleaned_text = re.sub(r'^```\s*\n?', '', cleaned_text)
        cleaned_text = re.sub(r'\n?```\s*$', '', cleaned_text)
        cleaned_text = cleaned_text.strip()
        
        print(f"🔍 Attempting JSON extraction from cleaned text ({len(cleaned_text)} characters)")
        print(f"📄 Cleaned text preview: {cleaned_text[:200]}...")
        
        # Enhanced cleaning for common LLM response issues
        cleaned_text = self._clean_json_text(cleaned_text)
        
        # Try to parse the cleaned JSON directly
        try:
            result = json.loads(cleaned_text)
            feature_results = result.get("feature_results", [])
            print(f"✅ Direct JSON parsing successful, found {len(feature_results)} feature results")
            return feature_results
        except json.JSONDecodeError as e:
            print(f"⚠️ Direct JSON parsing failed: {e}")
        
        # Try to find JSON object in the response with more robust pattern
        try:
            json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
            matches = re.findall(json_pattern, cleaned_text, re.DOTALL)
        except Exception as regex_error:
            print(f"⚠️ Regex pattern matching failed: {regex_error}")
            print(f"📄 Problematic text preview: {cleaned_text[:200]}...")
            matches = []
        
        print(f"🔍 Found {len(matches)} potential JSON matches")
        
        if matches:
            for i, match in enumerate(matches):
                try:
                    # Clean the individual match
                    cleaned_match = self._clean_json_text(match)
                    result = json.loads(cleaned_match)
                    feature_results = result.get("feature_results", [])
                    if feature_results:
                        print(f"✅ JSON extraction successful from match {i+1}, found {len(feature_results)} feature results")
                        return feature_results
                except json.JSONDecodeError as e:
                    print(f"⚠️ JSON parsing failed for match {i+1}: {e}")
                    continue
        
        # Try to extract JSON using more aggressive cleaning
        try:
            aggressive_cleaned = self._aggressive_json_cleaning(cleaned_text)
            result = json.loads(aggressive_cleaned)
            feature_results = result.get("feature_results", [])
            if feature_results:
                print(f"✅ Aggressive JSON cleaning successful, found {len(feature_results)} feature results")
                return feature_results
        except json.JSONDecodeError as e:
            print(f"⚠️ Aggressive JSON cleaning failed: {e}")
        
        print("❌ No valid JSON found in response after all cleaning attempts")
        raise Exception("Failed to extract valid JSON from LLM response after multiple cleaning attempts")
    
    def _clean_json_text(self, text: str) -> str:
        """Clean JSON text to handle common LLM response issues"""
        import re
        
        # Remove invalid control characters (except newlines and tabs) - use a safer approach
        import string
        printable_chars = string.printable
        text = ''.join(char for char in text if char in printable_chars)
        
        # Fix common quote issues - use string replacement instead of regex
        try:
            text = text.replace('"', '"').replace('"', '"')  # Replace smart quotes with regular quotes
            text = text.replace(''', "'").replace(''', "'")  # Replace smart apostrophes with regular apostrophes
        except Exception as e:
            print(f"⚠️ Quote replacement failed in _clean_json_text: {e}")
            # Continue with original text
        
        # Fix common escape sequence issues
        try:
            text = re.sub(r'\\(?!["\\/bfnrt])', r'\\\\', text)  # Fix invalid escape sequences
        except Exception as e:
            print(f"⚠️ Escape sequence fixing failed in _clean_json_text: {e}")
        
        # Remove trailing commas in objects and arrays
        try:
            text = re.sub(r',(\s*[}\]])', r'\1', text)
        except Exception as e:
            print(f"⚠️ Trailing comma removal failed in _clean_json_text: {e}")
        
        # Fix common formatting issues
        try:
            text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
            text = text.strip()
        except Exception as e:
            print(f"⚠️ Whitespace normalization failed in _clean_json_text: {e}")
        
        return text
    
    def _aggressive_json_cleaning(self, text: str) -> str:
        """More aggressive JSON cleaning for problematic responses"""
        import re
        
        # Try to extract just the JSON object
        # Look for the start of a JSON object
        start_match = re.search(r'\{', text)
        if not start_match:
            raise Exception("No JSON object start found")
        
        start_pos = start_match.start()
        
        # Find the matching closing brace
        brace_count = 0
        end_pos = -1
        
        for i, char in enumerate(text[start_pos:], start_pos):
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count == 0:
                    end_pos = i + 1
                    break
        
        if end_pos == -1:
            raise Exception("No matching closing brace found")
        
        # Extract the JSON object
        json_text = text[start_pos:end_pos]
        
        # Apply aggressive cleaning
        json_text = self._clean_json_text(json_text)
        
        # Remove any remaining problematic characters - use a safer approach
        # Remove all non-printable characters except newlines and tabs
        import string
        printable_chars = string.printable
        json_text = ''.join(char for char in json_text if char in printable_chars or char in '\n\t')
        
        return json_text
    
    def _sanitize_llm_response(self, response_text: str) -> str:
        """Sanitize LLM response to prevent JSON parsing issues"""
        import re
        
        if not response_text or not response_text.strip():
            raise Exception("Empty LLM response")
        
        print(f"🔍 Sanitizing response of length: {len(response_text)}")
        
        # Remove any markdown formatting
        text = response_text.strip()
        try:
            text = re.sub(r'^```json\s*\n?', '', text)
            text = re.sub(r'^```\s*\n?', '', text)
            text = re.sub(r'\n?```\s*$', '', text)
            text = text.strip()
            print(f"✅ Markdown removal completed")
        except Exception as e:
            print(f"⚠️ Markdown removal failed: {e}")
            # Continue with original text
        
        # Remove invalid control characters - use a safer approach
        try:
            import string
            printable_chars = string.printable
            text = ''.join(char for char in text if char in printable_chars)
            print(f"✅ Control character removal completed")
        except Exception as e:
            print(f"⚠️ Control character removal failed: {e}")
            # Continue with original text
        
        # Fix common quote issues - use string replacement instead of regex
        try:
            text = text.replace('"', '"').replace('"', '"')  # Replace smart quotes with regular quotes
            text = text.replace(''', "'").replace(''', "'")  # Replace smart apostrophes with regular apostrophes
            print(f"✅ Quote replacement completed")
        except Exception as e:
            print(f"⚠️ Quote replacement failed: {e}")
            # Continue with original text
        
        # Fix boolean values
        try:
            text = re.sub(r'\bTrue\b', 'true', text)
            text = re.sub(r'\bFalse\b', 'false', text)
            print(f"✅ Boolean value conversion completed")
        except Exception as e:
            print(f"⚠️ Boolean value conversion failed: {e}")
        
        # Fix common escape sequence issues
        try:
            text = re.sub(r'\\(?!["\\/bfnrt])', r'\\\\', text)
            print(f"✅ Escape sequence fixing completed")
        except Exception as e:
            print(f"⚠️ Escape sequence fixing failed: {e}")
        
        # Remove trailing commas in objects and arrays
        try:
            text = re.sub(r',(\s*[}\]])', r'\1', text)
            print(f"✅ Trailing comma removal completed")
        except Exception as e:
            print(f"⚠️ Trailing comma removal failed: {e}")
        
        # Normalize whitespace
        try:
            text = re.sub(r'\s+', ' ', text)
            text = text.strip()
            print(f"✅ Whitespace normalization completed")
        except Exception as e:
            print(f"⚠️ Whitespace normalization failed: {e}")
        
        return text
    
    def _calculate_overall_stats(self, state_results: Dict[str, List[StateAnalysisResult]], 
                                feature_results: Dict[str, List[StateAnalysisResult]]) -> Dict[str, Any]:
        """Calculate overall statistics from analysis results"""
        
        total_analyses = sum(len(results) for results in state_results.values())
        total_states = len(state_results)
        total_features = len(feature_results)
        
        # Calculate compliance rates
        compliant_analyses = sum(
            sum(1 for result in results if result.is_compliant)
            for results in state_results.values()
        )
        
        compliance_rate = compliant_analyses / total_analyses if total_analyses > 0 else 0.0
        
        # Calculate risk distribution
        risk_levels = {}
        for results in state_results.values():
            for result in results:
                risk_levels[result.risk_level] = risk_levels.get(result.risk_level, 0) + 1
        
        # Find high-risk states
        high_risk_states = []
        for state_code, results in state_results.items():
            high_risk_count = sum(1 for result in results if result.risk_level == "high")
            if high_risk_count > 0:
                high_risk_states.append({
                    "state_code": state_code,
                    "state_name": results[0].state_name if results else "",
                    "high_risk_features": high_risk_count,
                    "total_features": len(results)
                })
        
        return {
            "total_analyses": total_analyses,
            "total_states": total_states,
            "total_features": total_features,
            "compliance_rate": compliance_rate,
            "risk_distribution": risk_levels,
            "high_risk_states": high_risk_states,
            "average_risk_score": sum(
                sum(result.risk_score for result in results)
                for results in state_results.values()
            ) / total_analyses if total_analyses > 0 else 0.0
        }
