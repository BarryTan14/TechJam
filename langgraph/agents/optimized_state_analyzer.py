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
            # Medium-risk states: Use pattern matching with LLM fallback
            results = self._analyze_medium_risk_state(features, state_regulation)
        else:
            # Low-risk states: Use pattern matching only
            results = self._analyze_low_risk_state(features, state_regulation)
        
        return results
    
    def _analyze_high_risk_state(self, features: List[ExtractedFeature], 
                                state_regulation: StateRegulation) -> List[StateAnalysisResult]:
        """Analyze features against high-risk state using LLM"""
        results = []
        
        if self.llm:
            try:
                # Use batch LLM analysis for efficiency
                batch_results = self._batch_llm_analysis(features, state_regulation)
                results = batch_results
            except Exception as e:
                print(f"⚠️ LLM analysis failed for {state_regulation.state_name}: {e}")
                # Fallback to pattern matching
                results = self._pattern_matching_analysis(features, state_regulation, "high")
        else:
            # No LLM available, use pattern matching
            results = self._pattern_matching_analysis(features, state_regulation, "high")
        
        return results
    
    def _analyze_medium_risk_state(self, features: List[ExtractedFeature], 
                                  state_regulation: StateRegulation) -> List[StateAnalysisResult]:
        """Analyze features against medium-risk state using pattern matching with LLM fallback"""
        results = []
        
        # Try pattern matching first
        results = self._pattern_matching_analysis(features, state_regulation, "medium")
        
        # If LLM is available and we have complex features, use LLM for validation
        if self.llm and self._has_complex_features(features):
            try:
                # Use LLM to validate and improve results
                validated_results = self._validate_with_llm(features, state_regulation, results)
                results = validated_results
            except Exception as e:
                print(f"⚠️ LLM validation failed for {state_regulation.state_name}: {e}")
                # Keep pattern matching results
        
        return results
    
    def _analyze_low_risk_state(self, features: List[ExtractedFeature], 
                               state_regulation: StateRegulation) -> List[StateAnalysisResult]:
        """Analyze features against low-risk state using pattern matching only"""
        return self._pattern_matching_analysis(features, state_regulation, "low")
    
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
        
        # Create comprehensive prompt
        prompt = f"""Analyze compliance for {len(features)} features against {state_regulation.state_name} ({state_regulation.state_code}):

State Information:
- State: {state_regulation.state_name}
- Regulations: {', '.join(state_regulation.regulations)}
- Risk Level: {state_regulation.risk_level}
- Enforcement Level: {state_regulation.enforcement_level}
- Key Requirements: {', '.join(state_regulation.key_requirements)}
- Penalties: {', '.join(state_regulation.penalties)}

Features to analyze:
{json.dumps(feature_summaries, indent=2)}

Return JSON with analysis for each feature:
{{
    "feature_results": [
        {{
            "feature_id": "feature_1",
            "risk_score": 0.3,
            "risk_level": "low|medium|high|critical",
            "is_compliant": true/false,
            "non_compliant_regulations": ["regulation_name"],
            "required_actions": ["action1", "action2"],
            "reasoning": "Brief explanation",
            "confidence_score": 0.8
        }}
    ]
}}

Focus on key compliance issues. Keep responses concise and accurate."""
        
        try:
            response = self.llm.generate_content(prompt)
            
            if not response or not response.text:
                raise Exception("LLM returned empty response")
            
            # Parse JSON response
            try:
                analysis_result = json.loads(response.text)
                feature_results = analysis_result.get("feature_results", [])
            except json.JSONDecodeError:
                # Try to extract JSON from response
                feature_results = self._extract_json_from_response(response.text)
            
            # Convert to StateAnalysisResult objects
            results = []
            for i, result in enumerate(feature_results):
                if i < len(features):
                    feature = features[i]
                    state_result = StateAnalysisResult(
                        state_code=state_regulation.state_code,
                        state_name=state_regulation.state_name,
                        feature_id=feature.feature_id,
                        feature_name=feature.feature_name,
                        risk_score=result.get("risk_score", 0.5),
                        risk_level=result.get("risk_level", "medium"),
                        is_compliant=result.get("is_compliant", True),
                        non_compliant_regulations=result.get("non_compliant_regulations", []),
                        required_actions=result.get("required_actions", []),
                        reasoning=result.get("reasoning", ""),
                        confidence_score=result.get("confidence_score", 0.8),
                        processing_time=0.0
                    )
                    results.append(state_result)
            
            return results
            
        except Exception as e:
            raise Exception(f"Batch LLM analysis failed: {e}")
    
    def _pattern_matching_analysis(self, features: List[ExtractedFeature], 
                                  state_regulation: StateRegulation, 
                                  risk_level: str) -> List[StateAnalysisResult]:
        """Analyze features using pattern matching rules"""
        results = []
        
        for feature in features:
            # Analyze feature based on data types and state regulations
            analysis = self._analyze_feature_patterns(feature, state_regulation, risk_level)
            
            state_result = StateAnalysisResult(
                state_code=state_regulation.state_code,
                state_name=state_regulation.state_name,
                feature_id=feature.feature_id,
                feature_name=feature.feature_name,
                risk_score=analysis["risk_score"],
                risk_level=analysis["risk_level"],
                is_compliant=analysis["is_compliant"],
                non_compliant_regulations=analysis["non_compliant_regulations"],
                required_actions=analysis["required_actions"],
                reasoning=analysis["reasoning"],
                confidence_score=analysis["confidence_score"],
                processing_time=0.0
            )
            results.append(state_result)
        
        return results
    
    def _analyze_feature_patterns(self, feature: ExtractedFeature, 
                                 state_regulation: StateRegulation, 
                                 risk_level: str) -> Dict[str, Any]:
        """Analyze a feature using pattern matching rules"""
        
        # Initialize analysis
        risk_score = 0.3  # Base risk score
        is_compliant = True
        non_compliant_regulations = []
        required_actions = []
        reasoning = []
        
        # Check data types
        sensitive_data_types = ["personal_identifiable_information", "biometric_data", "health_data", 
                               "financial_data", "location_data", "behavioral_data"]
        
        feature_data_types = [dt.lower() for dt in feature.data_types]
        
        # Adjust risk based on data types
        for data_type in feature_data_types:
            if any(sensitive in data_type for sensitive in sensitive_data_types):
                risk_score += 0.2
                reasoning.append(f"Feature collects sensitive data: {data_type}")
        
        # Check state-specific requirements
        if state_regulation.risk_level == "high":
            # High-risk states have stricter requirements
            if any("consent" in req.lower() for req in state_regulation.key_requirements):
                if "consent" not in feature.feature_description.lower():
                    is_compliant = False
                    non_compliant_regulations.extend(state_regulation.regulations)
                    required_actions.append("Implement consent mechanisms")
                    reasoning.append("Consent required but not implemented")
            
            if any("deletion" in req.lower() for req in state_regulation.key_requirements):
                if "delete" not in feature.feature_description.lower() and "remove" not in feature.feature_description.lower():
                    required_actions.append("Implement data deletion rights")
                    reasoning.append("Data deletion rights required")
        
        # Check enforcement level
        if state_regulation.enforcement_level == "strict":
            risk_score += 0.1
            reasoning.append("State has strict enforcement")
        
        # Determine final risk level
        if risk_score >= 0.8:
            final_risk_level = "high"
        elif risk_score >= 0.6:
            final_risk_level = "medium"
        else:
            final_risk_level = "low"
        
        # Adjust confidence based on analysis depth
        confidence_score = 0.7 if risk_level == "low" else 0.8
        
        return {
            "risk_score": min(risk_score, 1.0),
            "risk_level": final_risk_level,
            "is_compliant": is_compliant,
            "non_compliant_regulations": non_compliant_regulations,
            "required_actions": required_actions,
            "reasoning": "; ".join(reasoning) if reasoning else "Feature appears compliant with state requirements",
            "confidence_score": confidence_score
        }
    
    def _has_complex_features(self, features: List[ExtractedFeature]) -> bool:
        """Check if any features are complex enough to warrant LLM analysis"""
        complex_keywords = ["biometric", "health", "financial", "location", "behavioral", "tracking", "analytics"]
        
        for feature in features:
            feature_text = f"{feature.feature_name} {feature.feature_description}".lower()
            if any(keyword in feature_text for keyword in complex_keywords):
                return True
        
        return False
    
    def _validate_with_llm(self, features: List[ExtractedFeature], 
                          state_regulation: StateRegulation, 
                          pattern_results: List[StateAnalysisResult]) -> List[StateAnalysisResult]:
        """Use LLM to validate and improve pattern matching results"""
        
        # Create validation prompt
        validation_prompt = f"""Validate and improve compliance analysis for {state_regulation.state_name}:

State: {state_regulation.state_name}
Regulations: {', '.join(state_regulation.regulations)}
Key Requirements: {', '.join(state_regulation.key_requirements)}

Current Analysis Results:
{json.dumps([{
    'feature_name': r.feature_name,
    'risk_score': r.risk_score,
    'is_compliant': r.is_compliant,
    'reasoning': r.reasoning
} for r in pattern_results], indent=2)}

Provide improvements to the analysis. Return JSON with updated results."""
        
        try:
            response = self.llm.generate_content(validation_prompt)
            
            if response and response.text:
                # Parse improvements and apply them
                improvements = json.loads(response.text)
                # Apply improvements to results
                # (Implementation depends on the specific improvement format)
                pass
        
        except Exception as e:
            print(f"⚠️ LLM validation failed: {e}")
        
        return pattern_results
    
    def _extract_json_from_response(self, response_text: str) -> List[Dict[str, Any]]:
        """Extract JSON from LLM response text"""
        import re
        
        if not response_text or not response_text.strip():
            return []
        
        # Clean the response text
        cleaned_text = response_text.strip()
        
        # Remove markdown code blocks
        cleaned_text = re.sub(r'^```json\s*\n?', '', cleaned_text)
        cleaned_text = re.sub(r'^```\s*\n?', '', cleaned_text)
        cleaned_text = re.sub(r'\n?```\s*$', '', cleaned_text)
        cleaned_text = cleaned_text.strip()
        
        # Try to parse the cleaned JSON directly
        try:
            result = json.loads(cleaned_text)
            return result.get("feature_results", [])
        except json.JSONDecodeError:
            pass
        
        # Try to find JSON object in the response
        json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
        matches = re.findall(json_pattern, cleaned_text, re.DOTALL)
        
        if matches:
            for match in matches:
                try:
                    result = json.loads(match)
                    return result.get("feature_results", [])
                except json.JSONDecodeError:
                    continue
        
        return []
    
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
