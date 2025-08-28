"""
US State Compliance Agent - Analyzes compliance for each US state
"""

import json
from datetime import datetime
from typing import Dict, Any, List, Optional
import google.generativeai as genai

from .models import AgentOutput, USStateCompliance


class USStateComplianceAgent:
    """Agent responsible for analyzing compliance for each US state"""
    
    def __init__(self, llm=None):
        self.llm = llm
        self.agent_name = "US State Compliance"
        
        # Define US states and their regulations
        self.us_states = {
            "AL": {"name": "Alabama", "regulations": ["Alabama Data Breach Notification Act"]},
            "AK": {"name": "Alaska", "regulations": ["Alaska Personal Information Protection Act"]},
            "AZ": {"name": "Arizona", "regulations": ["Arizona Data Breach Notification Law"]},
            "AR": {"name": "Arkansas", "regulations": ["Arkansas Personal Information Protection Act"]},
            "CA": {"name": "California", "regulations": ["CCPA", "CPRA", "California Privacy Rights Act"]},
            "CO": {"name": "Colorado", "regulations": ["Colorado Privacy Act (CPA)"]},
            "CT": {"name": "Connecticut", "regulations": ["Connecticut Data Privacy Act (CTDPA)"]},
            "DE": {"name": "Delaware", "regulations": ["Delaware Personal Data Privacy Act"]},
            "FL": {"name": "Florida", "regulations": ["Florida Digital Bill of Rights"]},
            "GA": {"name": "Georgia", "regulations": ["Georgia Personal Data Privacy Act"]},
            "HI": {"name": "Hawaii", "regulations": ["Hawaii Consumer Privacy Protection Act"]},
            "ID": {"name": "Idaho", "regulations": ["Idaho Consumer Privacy Act"]},
            "IL": {"name": "Illinois", "regulations": ["BIPA", "Illinois Biometric Information Privacy Act"]},
            "IN": {"name": "Indiana", "regulations": ["Indiana Consumer Data Protection Act"]},
            "IA": {"name": "Iowa", "regulations": ["Iowa Consumer Data Protection Act"]},
            "KS": {"name": "Kansas", "regulations": ["Kansas Consumer Privacy Act"]},
            "KY": {"name": "Kentucky", "regulations": ["Kentucky Consumer Data Protection Act"]},
            "LA": {"name": "Louisiana", "regulations": ["Louisiana Consumer Privacy Act"]},
            "ME": {"name": "Maine", "regulations": ["Maine Consumer Privacy Act"]},
            "MD": {"name": "Maryland", "regulations": ["Maryland Online Data Privacy Act"]},
            "MA": {"name": "Massachusetts", "regulations": ["Massachusetts Data Privacy Law"]},
            "MI": {"name": "Michigan", "regulations": ["Michigan Consumer Privacy Act"]},
            "MN": {"name": "Minnesota", "regulations": ["Minnesota Consumer Data Privacy Act"]},
            "MS": {"name": "Mississippi", "regulations": ["Mississippi Consumer Data Privacy Act"]},
            "MO": {"name": "Missouri", "regulations": ["Missouri Data Protection Act"]},
            "MT": {"name": "Montana", "regulations": ["Montana Consumer Data Privacy Act"]},
            "NE": {"name": "Nebraska", "regulations": ["Nebraska Data Privacy Act"]},
            "NV": {"name": "Nevada", "regulations": ["Nevada Privacy of Information Collected on the Internet from Consumers Act"]},
            "NH": {"name": "New Hampshire", "regulations": ["New Hampshire Privacy Act"]},
            "NJ": {"name": "New Jersey", "regulations": ["New Jersey Data Privacy Act"]},
            "NM": {"name": "New Mexico", "regulations": ["New Mexico Data Privacy Act"]},
            "NY": {"name": "New York", "regulations": ["NY SHIELD Act", "New York Privacy Act"]},
            "NC": {"name": "North Carolina", "regulations": ["North Carolina Consumer Privacy Act"]},
            "ND": {"name": "North Dakota", "regulations": ["North Dakota Consumer Privacy Act"]},
            "OH": {"name": "Ohio", "regulations": ["Ohio Personal Privacy Act"]},
            "OK": {"name": "Oklahoma", "regulations": ["Oklahoma Computer Data Privacy Act"]},
            "OR": {"name": "Oregon", "regulations": ["Oregon Consumer Privacy Act"]},
            "PA": {"name": "Pennsylvania", "regulations": ["Pennsylvania Consumer Privacy Act"]},
            "RI": {"name": "Rhode Island", "regulations": ["Rhode Island Data Transparency and Privacy Protection Act"]},
            "SC": {"name": "South Carolina", "regulations": ["South Carolina Consumer Privacy Act"]},
            "SD": {"name": "South Dakota", "regulations": ["South Dakota Consumer Data Privacy Act"]},
            "TN": {"name": "Tennessee", "regulations": ["Tennessee Information Protection Act"]},
            "TX": {"name": "Texas", "regulations": ["Texas Data Privacy and Security Act"]},
            "UT": {"name": "Utah", "regulations": ["Utah Consumer Privacy Act"]},
            "VT": {"name": "Vermont", "regulations": ["Vermont Data Broker Regulation"]},
            "VA": {"name": "Virginia", "regulations": ["Virginia Consumer Data Protection Act"]},
            "WA": {"name": "Washington", "regulations": ["Washington My Health My Data Act"]},
            "WV": {"name": "West Virginia", "regulations": ["West Virginia Consumer Privacy Act"]},
            "WI": {"name": "Wisconsin", "regulations": ["Wisconsin Data Privacy Act"]},
            "WY": {"name": "Wyoming", "regulations": ["Wyoming Consumer Data Privacy Act"]}
        }
    
    def analyze_us_state_compliance(self, feature_name: str, feature_analysis: Dict[str, Any], 
                                   regulation_matching: Dict[str, Any], risk_assessment: Dict[str, Any]) -> AgentOutput:
        """
        Analyze compliance for each US state
        
        Args:
            feature_name: Name of the feature being analyzed
            feature_analysis: Output from feature analyzer
            regulation_matching: Output from regulation matcher
            risk_assessment: Output from risk assessor
            
        Returns:
            AgentOutput containing US state compliance analysis
        """
        start_time = datetime.now()
        
        print(f"🇺🇸 [{self.agent_name}] Analyzing US state compliance for: {feature_name}")
        
        # Prepare input data
        input_data = {
            "feature_name": feature_name,
            "feature_analysis": feature_analysis,
            "regulation_matching": regulation_matching,
            "risk_assessment": risk_assessment,
            "total_states": len(self.us_states)
        }
        
        # Analyze compliance for each state
        if self.llm:
            try:
                analysis_result = self._analyze_states_with_llm(feature_name, feature_analysis, regulation_matching, risk_assessment)
                confidence_score = 0.85
                thought_process = "Used LLM to analyze compliance for each US state based on feature characteristics and applicable regulations."
            except Exception as e:
                print(f"⚠️  LLM state analysis failed: {e}")
                analysis_result = self._analyze_states_fallback(feature_analysis, regulation_matching, risk_assessment)
                confidence_score = 0.6
                thought_process = f"LLM state analysis failed, used fallback pattern matching: {e}"
        else:
            analysis_result = self._analyze_states_fallback(feature_analysis, regulation_matching, risk_assessment)
            confidence_score = 0.6
            thought_process = "No LLM available, used fallback pattern matching to analyze US state compliance."
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        # Create agent output
        agent_output = AgentOutput(
            agent_name=self.agent_name,
            input_data=input_data,
            thought_process=thought_process,
            analysis_result=analysis_result,
            confidence_score=confidence_score,
            processing_time=processing_time,
            timestamp=datetime.now().isoformat()
        )
        
        non_compliant_count = len(analysis_result.get("non_compliant_states", []))
        print(f"✅ [{self.agent_name}] Analyzed {len(self.us_states)} states, found {non_compliant_count} non-compliant in {processing_time:.2f}s")
        
        return agent_output
    
    def _analyze_states_with_llm(self, feature_name: str, feature_analysis: Dict[str, Any], 
                                regulation_matching: Dict[str, Any], risk_assessment: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze states using LLM"""
        
        # Prepare feature information
        data_types = feature_analysis.get("data_types", [])
        processing_purposes = feature_analysis.get("processing_purposes", [])
        applicable_regulations = regulation_matching.get("applicable_regulations", [])
        risk_level = risk_assessment.get("overall_risk_level", "medium")
        
        prompt = f"""
You are a US state compliance analyst. Your task is to analyze whether a feature is compliant with each US state's privacy and data protection regulations.

Feature: {feature_name}
Data Types: {data_types}
Processing Purposes: {processing_purposes}
Applicable Regulations: {applicable_regulations}
Risk Level: {risk_level}

For each US state, determine:
1. Is the feature compliant with that state's regulations?
2. Which specific regulations are violated (if any)?
3. What actions are required to achieve compliance?
4. Risk level for that state (Low/Medium/High/Critical)

Consider these key factors:
- Data types being processed (personal, biometric, financial, health, etc.)
- Processing purposes (analytics, marketing, authentication, etc.)
- Cross-border data transfers
- User consent requirements
- Data retention policies
- User rights (access, deletion, portability)

IMPORTANT: You must analyze ALL 50 US states and return a complete JSON response.

Return your response as a JSON object with this EXACT structure:
{{
    "state_compliance": [
        {{
            "state_code": "CA",
            "state_name": "California",
            "is_compliant": false,
            "non_compliant_regulations": ["CCPA", "CPRA"],
            "risk_level": "High",
            "required_actions": ["Implement consent management", "Add data deletion rights"],
            "notes": "California has strict privacy laws requiring explicit consent and user rights"
        }},
        {{
            "state_code": "VA",
            "state_name": "Virginia",
            "is_compliant": true,
            "non_compliant_regulations": [],
            "risk_level": "Low",
            "required_actions": [],
            "notes": "Feature complies with Virginia's data protection requirements"
        }}
    ],
    "non_compliant_states": ["CA", "NY", "IL"],
    "high_risk_states": ["CA", "NY"],
    "compliance_summary": "Feature is non-compliant in 15 states due to data processing practices",
    "recommendations": ["Implement state-specific consent mechanisms", "Add data minimization controls"]
}}

Key states to focus on with comprehensive privacy laws:
- California (CCPA/CPRA)
- Virginia (VCDPA)
- Colorado (CPA)
- Connecticut (CTDPA)
- Utah (UCPA)
- Florida (FDBR)
- Texas (TDPSA)
- New York (NY SHIELD Act)
- Illinois (BIPA)
- Washington (My Health My Data Act)

Ensure your response is valid JSON and includes all 50 states in the state_compliance array.
"""

        print(f"🤖 Using LLM for US state compliance analysis...")
        
        response = self.llm.generate_content(prompt)
        
        print(f"📝 LLM Response received for US state compliance")
        
        if response and response.text:
            print(f"📄 Raw response preview: {response.text[:200]}...")
            
            # Extract JSON from response
            json_data = self._extract_json_from_response(response.text)
            
            if json_data:
                return json_data
            else:
                print("⚠️  Failed to extract JSON from LLM response")
                return self._analyze_states_fallback(feature_analysis, regulation_matching, risk_assessment)
        else:
            print("⚠️  Empty LLM response")
            return self._analyze_states_fallback(feature_analysis, regulation_matching, risk_assessment)
    
    def _analyze_states_fallback(self, feature_analysis: Dict[str, Any], 
                                regulation_matching: Dict[str, Any], 
                                risk_assessment: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze states using pattern matching fallback"""
        
        state_compliance = []
        non_compliant_states = []
        high_risk_states = []
        
        # Get feature characteristics
        data_types = feature_analysis.get("data_types", [])
        processing_purposes = feature_analysis.get("processing_purposes", [])
        risk_level = risk_assessment.get("overall_risk_level", "medium")
        
        # High-risk states that typically have strict regulations
        strict_states = ["CA", "NY", "IL", "VA", "CO", "CT", "UT", "FL", "TX", "WA"]
        
        for state_code, state_info in self.us_states.items():
            state_name = state_info["name"]
            regulations = state_info["regulations"]
            
            # Determine compliance based on feature characteristics
            is_compliant = True
            non_compliant_regulations = []
            risk_level_state = "Low"
            required_actions = []
            notes = ""
            
            # Check for high-risk data types
            if any(dt in data_types for dt in ["biometric_data", "health_data", "financial_data"]):
                if state_code in strict_states:
                    is_compliant = False
                    non_compliant_regulations.extend(regulations)
                    risk_level_state = "High"
                    required_actions.append("Implement enhanced consent mechanisms")
                    required_actions.append("Add data minimization controls")
                    notes = f"{state_name} has strict regulations for sensitive data types"
            
            # Check for personal data processing
            if "personal_data" in data_types:
                if state_code in strict_states:
                    is_compliant = False
                    non_compliant_regulations.extend(regulations)
                    risk_level_state = "Medium" if risk_level_state == "Low" else risk_level_state
                    required_actions.append("Implement user rights portal")
                    required_actions.append("Add data deletion capabilities")
                    notes = f"{state_name} requires specific user rights for personal data"
            
            # Check for analytics/marketing purposes
            if any(purpose in processing_purposes for purpose in ["analytics", "marketing", "advertising"]):
                if state_code in strict_states:
                    is_compliant = False
                    non_compliant_regulations.extend(regulations)
                    risk_level_state = "Medium" if risk_level_state == "Low" else risk_level_state
                    required_actions.append("Implement opt-out mechanisms")
                    required_actions.append("Add consent management")
                    notes = f"{state_name} requires explicit consent for analytics/marketing"
            
            # Add to lists
            if not is_compliant:
                non_compliant_states.append(state_code)
                if risk_level_state in ["High", "Critical"]:
                    high_risk_states.append(state_code)
            
            # Create state compliance object
            state_compliance.append({
                "state_code": state_code,
                "state_name": state_name,
                "is_compliant": is_compliant,
                "non_compliant_regulations": non_compliant_regulations,
                "risk_level": risk_level_state,
                "required_actions": required_actions,
                "notes": notes
            })
        
        return {
            "state_compliance": state_compliance,
            "non_compliant_states": non_compliant_states,
            "high_risk_states": high_risk_states,
            "compliance_summary": f"Feature is non-compliant in {len(non_compliant_states)} states",
            "recommendations": [
                "Implement state-specific consent mechanisms",
                "Add data minimization controls",
                "Establish user rights portal",
                "Monitor for regulation updates"
            ]
        }
    
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
        
        # If still no JSON found, try to extract just the non_compliant_states array
        try:
            # Look for non_compliant_states pattern
            states_pattern = r'"non_compliant_states":\s*\[([^\]]+)\]'
            states_match = re.search(states_pattern, cleaned_text)
            if states_match:
                states_str = states_match.group(1)
                # Extract state names
                state_names = re.findall(r'"([^"]+)"', states_str)
                return {
                    "non_compliant_states": state_names,
                    "compliance_analysis": {},
                    "compliance_score": 0.5,
                    "key_violations": [],
                    "recommendations": []
                }
        except:
            pass
        
        # If no JSON found, return default structure
        return {
            "non_compliant_states": ["California", "Virginia"],
            "compliance_analysis": {},
            "compliance_score": 0.5,
            "key_violations": [],
            "recommendations": []
        }
