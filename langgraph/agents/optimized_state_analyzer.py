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

Return JSON with detailed analysis for each feature:
{{
    "feature_results": [
        {{
            "feature_id": "feature_1",
            "risk_score": 0.3,
            "risk_level": "low|high",
            "is_compliant": true/false,
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

Make the reasoning comprehensive and business-friendly."""
        
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
            
            # Parse JSON response
            try:
                analysis_result = json.loads(response.text)
                feature_results = analysis_result.get("feature_results", [])
                print(f"✅ JSON parsing successful for {state_regulation.state_name}")
            except json.JSONDecodeError as json_error:
                print(f"⚠️ JSON parsing failed for {state_regulation.state_name}: {json_error}")
                print(f"📄 Raw response: {response.text[:500]}...")
                # Try to extract JSON from response
                feature_results = self._extract_json_from_response(response.text)
                if not feature_results:
                    print(f"⚠️ JSON extraction also failed for {state_regulation.state_name}")
                    raise Exception(f"Failed to parse or extract JSON from LLM response: {json_error}")
            
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
            # Fall back to pattern matching analysis
            print(f"🔄 Falling back to pattern matching analysis for {state_regulation.state_name}")
            return self._pattern_matching_analysis(features, state_regulation, "medium")
    
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
        """Analyze a feature using pattern matching rules with detailed reasoning"""
        
        # Initialize analysis
        risk_score = 0.3  # Base risk score
        is_compliant = True
        non_compliant_regulations = []
        required_actions = []
        reasoning_parts = []
        
        # Start with comprehensive reasoning
        reasoning_parts.append(f"Analyzing feature '{feature.feature_name}' against {state_regulation.state_name} ({state_regulation.state_code}) regulations")
        
        # Check data types and their sensitivity
        sensitive_data_types = {
            "personal_identifiable_information": "PII requires strict protection under most privacy laws",
            "biometric_data": "Biometric data has special protections under laws like BIPA",
            "health_data": "Health data is protected under HIPAA and state health privacy laws",
            "financial_data": "Financial data requires additional security measures",
            "location_data": "Location data can reveal sensitive personal patterns",
            "behavioral_data": "Behavioral data can be used for profiling and targeting"
        }
        
        feature_data_types = [dt.lower() for dt in feature.data_types]
        sensitive_data_found = []
        
        for data_type in feature_data_types:
            for sensitive_type, explanation in sensitive_data_types.items():
                if sensitive_type in data_type:
                    risk_score += 0.2
                    sensitive_data_found.append(f"{data_type} ({explanation})")
        
        if sensitive_data_found:
            reasoning_parts.append(f"Feature collects sensitive data types: {', '.join(sensitive_data_found)}")
        
        # Analyze state-specific requirements in detail
        reasoning_parts.append(f"State risk level: {state_regulation.risk_level.upper()}")
        reasoning_parts.append(f"State enforcement level: {state_regulation.enforcement_level.upper()}")
        
        # Check key requirements against feature description
        feature_text = f"{feature.feature_name} {feature.feature_description}".lower()
        
        for requirement in state_regulation.key_requirements:
            req_lower = requirement.lower()
            
            if "consent" in req_lower:
                if "consent" not in feature_text and "opt-in" not in feature_text and "permission" not in feature_text:
                    is_compliant = False
                    non_compliant_regulations.extend(state_regulation.regulations)
                    required_actions.append("Implement explicit consent mechanisms")
                    reasoning_parts.append(f"❌ Consent requirement not met: {requirement}")
                else:
                    reasoning_parts.append(f"✅ Consent requirement appears satisfied: {requirement}")
            
            elif "deletion" in req_lower or "delete" in req_lower:
                if "delete" not in feature_text and "remove" not in feature_text and "erase" not in feature_text:
                    required_actions.append("Implement data deletion rights")
                    reasoning_parts.append(f"⚠️ Data deletion rights required: {requirement}")
                else:
                    reasoning_parts.append(f"✅ Data deletion rights appear implemented: {requirement}")
            
            elif "access" in req_lower:
                if "access" not in feature_text and "view" not in feature_text and "retrieve" not in feature_text:
                    required_actions.append("Implement data access rights")
                    reasoning_parts.append(f"⚠️ Data access rights required: {requirement}")
                else:
                    reasoning_parts.append(f"✅ Data access rights appear implemented: {requirement}")
            
            elif "portability" in req_lower:
                if "export" not in feature_text and "download" not in feature_text and "portability" not in feature_text:
                    required_actions.append("Implement data portability mechanisms")
                    reasoning_parts.append(f"⚠️ Data portability required: {requirement}")
                else:
                    reasoning_parts.append(f"✅ Data portability appears implemented: {requirement}")
            
            elif "minimization" in req_lower:
                if "minimal" not in feature_text and "necessary" not in feature_text and "limited" not in feature_text:
                    required_actions.append("Implement data minimization practices")
                    reasoning_parts.append(f"⚠️ Data minimization required: {requirement}")
                else:
                    reasoning_parts.append(f"✅ Data minimization appears implemented: {requirement}")
            
            elif "purpose" in req_lower and "limitation" in req_lower:
                if "purpose" not in feature_text and "use" not in feature_text:
                    required_actions.append("Implement purpose limitation controls")
                    reasoning_parts.append(f"⚠️ Purpose limitation required: {requirement}")
                else:
                    reasoning_parts.append(f"✅ Purpose limitation appears implemented: {requirement}")
        
        # Check enforcement level impact
        if state_regulation.enforcement_level == "strict":
            risk_score += 0.1
            reasoning_parts.append("⚠️ State has strict enforcement - higher penalties for violations")
        elif state_regulation.enforcement_level == "moderate":
            reasoning_parts.append("ℹ️ State has moderate enforcement - standard penalties apply")
        else:
            reasoning_parts.append("ℹ️ State has lenient enforcement - lower penalties for violations")
        
        # Analyze penalties
        if state_regulation.penalties:
            reasoning_parts.append(f"Potential penalties: {', '.join(state_regulation.penalties)}")
        
        # Determine final risk level with detailed explanation (only low or high)
        if risk_score >= 0.6:
            final_risk_level = "high"
            risk_explanation = "HIGH RISK: Multiple compliance issues detected with strict state enforcement"
        else:
            final_risk_level = "low"
            risk_explanation = "LOW RISK: Feature appears largely compliant with state requirements"
        
        reasoning_parts.append(f"Risk Assessment: {risk_explanation}")
        
        # Add compliance summary
        if is_compliant:
            compliance_summary = f"✅ Feature is COMPLIANT with {state_regulation.state_name} requirements"
        else:
            compliance_summary = f"❌ Feature is NON-COMPLIANT with {state_regulation.state_name} requirements"
        
        reasoning_parts.append(compliance_summary)
        
        # Add required actions summary
        if required_actions:
            reasoning_parts.append(f"Required Actions: {', '.join(required_actions)}")
        
        # Add data type specific recommendations
        data_type_recommendations = []
        for data_type in feature_data_types:
            if "personal_identifiable_information" in data_type:
                data_type_recommendations.extend([
                    "Implement PII encryption at rest and in transit",
                    "Establish data retention policies for PII",
                    "Create PII inventory and mapping"
                ])
            elif "biometric_data" in data_type:
                data_type_recommendations.extend([
                    "Implement biometric data protection measures",
                    "Obtain explicit consent for biometric processing",
                    "Establish biometric data deletion procedures"
                ])
            elif "health_data" in data_type:
                data_type_recommendations.extend([
                    "Ensure HIPAA compliance for health data",
                    "Implement health data access controls",
                    "Establish health data breach notification procedures"
                ])
            elif "financial_data" in data_type:
                data_type_recommendations.extend([
                    "Implement PCI DSS compliance measures",
                    "Establish financial data encryption standards",
                    "Create financial data access audit trails"
                ])
            elif "location_data" in data_type:
                data_type_recommendations.extend([
                    "Implement location data anonymization",
                    "Establish location data retention limits",
                    "Create location data access controls"
                ])
            elif "behavioral_data" in data_type:
                data_type_recommendations.extend([
                    "Implement behavioral data profiling controls",
                    "Establish behavioral data opt-out mechanisms",
                    "Create behavioral data impact assessments"
                ])
        
        # Add unique data type recommendations
        for rec in data_type_recommendations:
            if rec not in required_actions:
                required_actions.append(rec)
        
        # Add state-specific recommendations based on enforcement level
        if state_regulation.enforcement_level == "strict":
            required_actions.append(f"Implement enhanced compliance monitoring for {state_regulation.state_name}")
            required_actions.append(f"Establish regular compliance audits for {state_regulation.state_name}")
        elif state_regulation.enforcement_level == "moderate":
            required_actions.append(f"Monitor compliance requirements for {state_regulation.state_name}")
        
        # Add general compliance recommendations
        if not is_compliant:
            required_actions.extend([
                "Conduct compliance gap analysis",
                "Update privacy policies and terms of service",
                "Implement compliance training for development teams",
                "Establish compliance monitoring and reporting procedures"
            ])
        
        # Adjust confidence based on analysis depth
        if risk_level == "high":
            confidence_score = 0.8  # Higher confidence for detailed analysis
        else:
            confidence_score = 0.7  # Lower confidence for basic analysis
        
        # Combine all reasoning parts
        detailed_reasoning = "\n".join(reasoning_parts)
        
        return {
            "risk_score": min(risk_score, 1.0),
            "risk_level": final_risk_level,
            "is_compliant": is_compliant,
            "non_compliant_regulations": non_compliant_regulations,
            "required_actions": required_actions,
            "reasoning": detailed_reasoning,
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
            print("⚠️ Empty response text provided to JSON extraction")
            return []
        
        # Clean the response text
        cleaned_text = response_text.strip()
        
        # Remove markdown code blocks
        cleaned_text = re.sub(r'^```json\s*\n?', '', cleaned_text)
        cleaned_text = re.sub(r'^```\s*\n?', '', cleaned_text)
        cleaned_text = re.sub(r'\n?```\s*$', '', cleaned_text)
        cleaned_text = cleaned_text.strip()
        
        print(f"🔍 Attempting JSON extraction from cleaned text ({len(cleaned_text)} characters)")
        print(f"📄 Cleaned text preview: {cleaned_text[:200]}...")
        
        # Try to parse the cleaned JSON directly
        try:
            result = json.loads(cleaned_text)
            feature_results = result.get("feature_results", [])
            print(f"✅ Direct JSON parsing successful, found {len(feature_results)} feature results")
            return feature_results
        except json.JSONDecodeError as e:
            print(f"⚠️ Direct JSON parsing failed: {e}")
        
        # Try to find JSON object in the response
        json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
        matches = re.findall(json_pattern, cleaned_text, re.DOTALL)
        
        print(f"🔍 Found {len(matches)} potential JSON matches")
        
        if matches:
            for i, match in enumerate(matches):
                try:
                    result = json.loads(match)
                    feature_results = result.get("feature_results", [])
                    if feature_results:
                        print(f"✅ JSON extraction successful from match {i+1}, found {len(feature_results)} feature results")
                        return feature_results
                except json.JSONDecodeError as e:
                    print(f"⚠️ JSON parsing failed for match {i+1}: {e}")
                    continue
        
        print("❌ No valid JSON found in response")
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
