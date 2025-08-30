"""
State Regulations Cache - Centralized state information management
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import json
import os


@dataclass
class StateRegulation:
    """Represents a state's regulation information"""
    state_code: str
    state_name: str
    regulations: List[str]
    risk_level: str  # low/medium/high based on regulation complexity
    enforcement_level: str  # strict/moderate/lenient
    key_requirements: List[str]
    penalties: List[str]
    effective_date: str
    notes: str


class StateRegulationsCache:
    """Centralized cache for state regulations and information"""
    
    def __init__(self):
        self._cache: Dict[str, StateRegulation] = {}
        self._initialized = False
        self._load_state_regulations()
    
    def _load_state_regulations(self):
        """Load comprehensive state regulations data"""
        if self._initialized:
            return
        
        # Comprehensive state regulations with detailed information
        state_data = {
            "AL": {
                "state_name": "Alabama",
                "regulations": ["Alabama Data Breach Notification Act"],
                "risk_level": "low",
                "enforcement_level": "moderate",
                "key_requirements": ["Data breach notification within 45 days"],
                "penalties": ["Up to $500,000 per breach"],
                "effective_date": "2018-06-01",
                "notes": "Basic breach notification requirements"
            },
            "AK": {
                "state_name": "Alaska",
                "regulations": ["Alaska Personal Information Protection Act"],
                "risk_level": "low",
                "enforcement_level": "moderate",
                "key_requirements": ["Data breach notification", "Reasonable security measures"],
                "penalties": ["Up to $500 per violation"],
                "effective_date": "2009-07-01",
                "notes": "Standard breach notification law"
            },
            "AZ": {
                "state_name": "Arizona",
                "regulations": ["Arizona Data Breach Notification Law"],
                "risk_level": "low",
                "enforcement_level": "moderate",
                "key_requirements": ["Data breach notification within 45 days"],
                "penalties": ["Up to $500,000 per breach"],
                "effective_date": "2006-12-31",
                "notes": "Basic breach notification requirements"
            },
            "AR": {
                "state_name": "Arkansas",
                "regulations": ["Arkansas Personal Information Protection Act"],
                "risk_level": "low",
                "enforcement_level": "moderate",
                "key_requirements": ["Data breach notification", "Security measures"],
                "penalties": ["Up to $10,000 per violation"],
                "effective_date": "2003-08-12",
                "notes": "Standard breach notification law"
            },
            "CA": {
                "state_name": "California",
                "regulations": ["CCPA", "CPRA", "California Privacy Rights Act", "California Consumer Privacy Act"],
                "risk_level": "high",
                "enforcement_level": "strict",
                "key_requirements": [
                    "Consumer rights (access, deletion, portability)",
                    "Opt-out of data sales",
                    "Consent for sensitive data",
                    "Data minimization",
                    "Purpose limitation",
                    "Right to correct inaccurate data"
                ],
                "penalties": ["Up to $7,500 per intentional violation", "Up to $2,500 per unintentional violation"],
                "effective_date": "2020-01-01",
                "notes": "Most comprehensive state privacy law in the US"
            },
            "CO": {
                "state_name": "Colorado",
                "regulations": ["Colorado Privacy Act (CPA)"],
                "risk_level": "high",
                "enforcement_level": "strict",
                "key_requirements": [
                    "Consumer rights (access, deletion, portability)",
                    "Opt-out of targeted advertising",
                    "Consent for sensitive data",
                    "Data minimization",
                    "Universal opt-out mechanism"
                ],
                "penalties": ["Up to $20,000 per violation"],
                "effective_date": "2023-07-01",
                "notes": "Comprehensive privacy law with universal opt-out"
            },
            "CT": {
                "state_name": "Connecticut",
                "regulations": ["Connecticut Data Privacy Act (CTDPA)"],
                "risk_level": "high",
                "enforcement_level": "strict",
                "key_requirements": [
                    "Consumer rights (access, deletion, portability)",
                    "Opt-out of targeted advertising",
                    "Consent for sensitive data",
                    "Data minimization"
                ],
                "penalties": ["Up to $5,000 per violation"],
                "effective_date": "2023-07-01",
                "notes": "Comprehensive privacy law"
            },
            "DE": {
                "state_name": "Delaware",
                "regulations": ["Delaware Personal Data Privacy Act"],
                "risk_level": "medium",
                "enforcement_level": "moderate",
                "key_requirements": [
                    "Consumer rights (access, deletion, portability)",
                    "Opt-out of targeted advertising",
                    "Consent for sensitive data"
                ],
                "penalties": ["Up to $10,000 per violation"],
                "effective_date": "2025-01-01",
                "notes": "Comprehensive privacy law"
            },
            "FL": {
                "state_name": "Florida",
                "regulations": ["Florida Digital Bill of Rights"],
                "risk_level": "medium",
                "enforcement_level": "moderate",
                "key_requirements": [
                    "Consumer rights (access, deletion, portability)",
                    "Opt-out of targeted advertising",
                    "Consent for sensitive data"
                ],
                "penalties": ["Up to $50,000 per violation"],
                "effective_date": "2024-07-01",
                "notes": "Comprehensive privacy law"
            },
            "GA": {
                "state_name": "Georgia",
                "regulations": ["Georgia Personal Data Privacy Act"],
                "risk_level": "medium",
                "enforcement_level": "moderate",
                "key_requirements": [
                    "Consumer rights (access, deletion, portability)",
                    "Opt-out of targeted advertising",
                    "Consent for sensitive data"
                ],
                "penalties": ["Up to $7,500 per violation"],
                "effective_date": "2024-07-01",
                "notes": "Comprehensive privacy law"
            },
            "HI": {
                "state_name": "Hawaii",
                "regulations": ["Hawaii Consumer Privacy Protection Act"],
                "risk_level": "medium",
                "enforcement_level": "moderate",
                "key_requirements": [
                    "Consumer rights (access, deletion, portability)",
                    "Opt-out of targeted advertising",
                    "Consent for sensitive data"
                ],
                "penalties": ["Up to $7,500 per violation"],
                "effective_date": "2024-07-01",
                "notes": "Comprehensive privacy law"
            },
            "ID": {
                "state_name": "Idaho",
                "regulations": ["Idaho Consumer Privacy Act"],
                "risk_level": "medium",
                "enforcement_level": "moderate",
                "key_requirements": [
                    "Consumer rights (access, deletion, portability)",
                    "Opt-out of targeted advertising",
                    "Consent for sensitive data"
                ],
                "penalties": ["Up to $7,500 per violation"],
                "effective_date": "2024-07-01",
                "notes": "Comprehensive privacy law"
            },
            "IL": {
                "state_name": "Illinois",
                "regulations": ["BIPA", "Illinois Biometric Information Privacy Act"],
                "risk_level": "high",
                "enforcement_level": "strict",
                "key_requirements": [
                    "Written consent for biometric data collection",
                    "Disclosure of purpose and retention period",
                    "Prohibition on selling biometric data",
                    "Right of action for violations"
                ],
                "penalties": ["$1,000-$5,000 per violation"],
                "effective_date": "2008-10-03",
                "notes": "Strict biometric data protection law"
            },
            "IN": {
                "state_name": "Indiana",
                "regulations": ["Indiana Consumer Data Protection Act"],
                "risk_level": "medium",
                "enforcement_level": "moderate",
                "key_requirements": [
                    "Consumer rights (access, deletion, portability)",
                    "Opt-out of targeted advertising",
                    "Consent for sensitive data"
                ],
                "penalties": ["Up to $7,500 per violation"],
                "effective_date": "2026-01-01",
                "notes": "Comprehensive privacy law"
            },
            "IA": {
                "state_name": "Iowa",
                "regulations": ["Iowa Consumer Data Protection Act"],
                "risk_level": "medium",
                "enforcement_level": "moderate",
                "key_requirements": [
                    "Consumer rights (access, deletion, portability)",
                    "Opt-out of targeted advertising",
                    "Consent for sensitive data"
                ],
                "penalties": ["Up to $7,500 per violation"],
                "effective_date": "2025-01-01",
                "notes": "Comprehensive privacy law"
            },
            "KS": {
                "state_name": "Kansas",
                "regulations": ["Kansas Consumer Privacy Act"],
                "risk_level": "medium",
                "enforcement_level": "moderate",
                "key_requirements": [
                    "Consumer rights (access, deletion, portability)",
                    "Opt-out of targeted advertising",
                    "Consent for sensitive data"
                ],
                "penalties": ["Up to $7,500 per violation"],
                "effective_date": "2025-07-01",
                "notes": "Comprehensive privacy law"
            },
            "KY": {
                "state_name": "Kentucky",
                "regulations": ["Kentucky Consumer Data Protection Act"],
                "risk_level": "medium",
                "enforcement_level": "moderate",
                "key_requirements": [
                    "Consumer rights (access, deletion, portability)",
                    "Opt-out of targeted advertising",
                    "Consent for sensitive data"
                ],
                "penalties": ["Up to $7,500 per violation"],
                "effective_date": "2026-01-01",
                "notes": "Comprehensive privacy law"
            },
            "LA": {
                "state_name": "Louisiana",
                "regulations": ["Louisiana Consumer Privacy Act"],
                "risk_level": "medium",
                "enforcement_level": "moderate",
                "key_requirements": [
                    "Consumer rights (access, deletion, portability)",
                    "Opt-out of targeted advertising",
                    "Consent for sensitive data"
                ],
                "penalties": ["Up to $7,500 per violation"],
                "effective_date": "2025-07-01",
                "notes": "Comprehensive privacy law"
            },
            "ME": {
                "state_name": "Maine",
                "regulations": ["Maine Consumer Privacy Act"],
                "risk_level": "medium",
                "enforcement_level": "moderate",
                "key_requirements": [
                    "Consumer rights (access, deletion, portability)",
                    "Opt-out of targeted advertising",
                    "Consent for sensitive data"
                ],
                "penalties": ["Up to $7,500 per violation"],
                "effective_date": "2025-07-01",
                "notes": "Comprehensive privacy law"
            },
            "MD": {
                "state_name": "Maryland",
                "regulations": ["Maryland Online Data Privacy Act"],
                "risk_level": "medium",
                "enforcement_level": "moderate",
                "key_requirements": [
                    "Consumer rights (access, deletion, portability)",
                    "Opt-out of targeted advertising",
                    "Consent for sensitive data"
                ],
                "penalties": ["Up to $7,500 per violation"],
                "effective_date": "2025-10-01",
                "notes": "Comprehensive privacy law"
            },
            "MA": {
                "state_name": "Massachusetts",
                "regulations": ["Massachusetts Data Privacy Law"],
                "risk_level": "medium",
                "enforcement_level": "moderate",
                "key_requirements": [
                    "Consumer rights (access, deletion, portability)",
                    "Opt-out of targeted advertising",
                    "Consent for sensitive data"
                ],
                "penalties": ["Up to $7,500 per violation"],
                "effective_date": "2025-07-01",
                "notes": "Comprehensive privacy law"
            },
            "MI": {
                "state_name": "Michigan",
                "regulations": ["Michigan Consumer Privacy Act"],
                "risk_level": "medium",
                "enforcement_level": "moderate",
                "key_requirements": [
                    "Consumer rights (access, deletion, portability)",
                    "Opt-out of targeted advertising",
                    "Consent for sensitive data"
                ],
                "penalties": ["Up to $7,500 per violation"],
                "effective_date": "2025-07-01",
                "notes": "Comprehensive privacy law"
            },
            "MN": {
                "state_name": "Minnesota",
                "regulations": ["Minnesota Consumer Data Privacy Act"],
                "risk_level": "medium",
                "enforcement_level": "moderate",
                "key_requirements": [
                    "Consumer rights (access, deletion, portability)",
                    "Opt-out of targeted advertising",
                    "Consent for sensitive data"
                ],
                "penalties": ["Up to $7,500 per violation"],
                "effective_date": "2025-07-01",
                "notes": "Comprehensive privacy law"
            },
            "MS": {
                "state_name": "Mississippi",
                "regulations": ["Mississippi Consumer Data Privacy Act"],
                "risk_level": "medium",
                "enforcement_level": "moderate",
                "key_requirements": [
                    "Consumer rights (access, deletion, portability)",
                    "Opt-out of targeted advertising",
                    "Consent for sensitive data"
                ],
                "penalties": ["Up to $7,500 per violation"],
                "effective_date": "2025-07-01",
                "notes": "Comprehensive privacy law"
            },
            "MO": {
                "state_name": "Missouri",
                "regulations": ["Missouri Data Protection Act"],
                "risk_level": "medium",
                "enforcement_level": "moderate",
                "key_requirements": [
                    "Consumer rights (access, deletion, portability)",
                    "Opt-out of targeted advertising",
                    "Consent for sensitive data"
                ],
                "penalties": ["Up to $7,500 per violation"],
                "effective_date": "2025-08-28",
                "notes": "Comprehensive privacy law"
            },
            "MT": {
                "state_name": "Montana",
                "regulations": ["Montana Consumer Data Privacy Act"],
                "risk_level": "medium",
                "enforcement_level": "moderate",
                "key_requirements": [
                    "Consumer rights (access, deletion, portability)",
                    "Opt-out of targeted advertising",
                    "Consent for sensitive data"
                ],
                "penalties": ["Up to $7,500 per violation"],
                "effective_date": "2024-10-01",
                "notes": "Comprehensive privacy law"
            },
            "NE": {
                "state_name": "Nebraska",
                "regulations": ["Nebraska Data Privacy Act"],
                "risk_level": "medium",
                "enforcement_level": "moderate",
                "key_requirements": [
                    "Consumer rights (access, deletion, portability)",
                    "Opt-out of targeted advertising",
                    "Consent for sensitive data"
                ],
                "penalties": ["Up to $7,500 per violation"],
                "effective_date": "2025-01-01",
                "notes": "Comprehensive privacy law"
            },
            "NV": {
                "state_name": "Nevada",
                "regulations": ["Nevada Privacy of Information Collected on the Internet from Consumers Act"],
                "risk_level": "medium",
                "enforcement_level": "moderate",
                "key_requirements": [
                    "Opt-out of data sales",
                    "Privacy policy requirements"
                ],
                "penalties": ["Up to $5,000 per violation"],
                "effective_date": "2019-10-01",
                "notes": "Limited to data sales opt-out"
            },
            "NH": {
                "state_name": "New Hampshire",
                "regulations": ["New Hampshire Privacy Act"],
                "risk_level": "medium",
                "enforcement_level": "moderate",
                "key_requirements": [
                    "Consumer rights (access, deletion, portability)",
                    "Opt-out of targeted advertising",
                    "Consent for sensitive data"
                ],
                "penalties": ["Up to $7,500 per violation"],
                "effective_date": "2025-01-01",
                "notes": "Comprehensive privacy law"
            },
            "NJ": {
                "state_name": "New Jersey",
                "regulations": ["New Jersey Data Privacy Act"],
                "risk_level": "medium",
                "enforcement_level": "moderate",
                "key_requirements": [
                    "Consumer rights (access, deletion, portability)",
                    "Opt-out of targeted advertising",
                    "Consent for sensitive data"
                ],
                "penalties": ["Up to $7,500 per violation"],
                "effective_date": "2025-01-15",
                "notes": "Comprehensive privacy law"
            },
            "NM": {
                "state_name": "New Mexico",
                "regulations": ["New Mexico Data Privacy Act"],
                "risk_level": "medium",
                "enforcement_level": "moderate",
                "key_requirements": [
                    "Consumer rights (access, deletion, portability)",
                    "Opt-out of targeted advertising",
                    "Consent for sensitive data"
                ],
                "penalties": ["Up to $7,500 per violation"],
                "effective_date": "2025-07-01",
                "notes": "Comprehensive privacy law"
            },
            "NY": {
                "state_name": "New York",
                "regulations": ["NY SHIELD Act", "New York Privacy Act"],
                "risk_level": "high",
                "enforcement_level": "strict",
                "key_requirements": [
                    "Data breach notification",
                    "Reasonable security measures",
                    "Consumer rights (proposed)",
                    "Opt-out of targeted advertising (proposed)"
                ],
                "penalties": ["Up to $5,000 per violation"],
                "effective_date": "2020-03-21",
                "notes": "Comprehensive data security law with proposed privacy enhancements"
            },
            "NC": {
                "state_name": "North Carolina",
                "regulations": ["North Carolina Consumer Privacy Act"],
                "risk_level": "medium",
                "enforcement_level": "moderate",
                "key_requirements": [
                    "Consumer rights (access, deletion, portability)",
                    "Opt-out of targeted advertising",
                    "Consent for sensitive data"
                ],
                "penalties": ["Up to $7,500 per violation"],
                "effective_date": "2025-10-01",
                "notes": "Comprehensive privacy law"
            },
            "ND": {
                "state_name": "North Dakota",
                "regulations": ["North Dakota Consumer Data Privacy Act"],
                "risk_level": "medium",
                "enforcement_level": "moderate",
                "key_requirements": [
                    "Consumer rights (access, deletion, portability)",
                    "Opt-out of targeted advertising",
                    "Consent for sensitive data"
                ],
                "penalties": ["Up to $7,500 per violation"],
                "effective_date": "2025-07-01",
                "notes": "Comprehensive privacy law"
            },
            "OH": {
                "state_name": "Ohio",
                "regulations": ["Ohio Personal Privacy Act"],
                "risk_level": "medium",
                "enforcement_level": "moderate",
                "key_requirements": [
                    "Consumer rights (access, deletion, portability)",
                    "Opt-out of targeted advertising",
                    "Consent for sensitive data"
                ],
                "penalties": ["Up to $7,500 per violation"],
                "effective_date": "2025-07-01",
                "notes": "Comprehensive privacy law"
            },
            "OK": {
                "state_name": "Oklahoma",
                "regulations": ["Oklahoma Computer Data Privacy Act"],
                "risk_level": "medium",
                "enforcement_level": "moderate",
                "key_requirements": [
                    "Consumer rights (access, deletion, portability)",
                    "Opt-out of targeted advertising",
                    "Consent for sensitive data"
                ],
                "penalties": ["Up to $7,500 per violation"],
                "effective_date": "2025-07-01",
                "notes": "Comprehensive privacy law"
            },
            "OR": {
                "state_name": "Oregon",
                "regulations": ["Oregon Consumer Privacy Act"],
                "risk_level": "medium",
                "enforcement_level": "moderate",
                "key_requirements": [
                    "Consumer rights (access, deletion, portability)",
                    "Opt-out of targeted advertising",
                    "Consent for sensitive data"
                ],
                "penalties": ["Up to $7,500 per violation"],
                "effective_date": "2024-07-01",
                "notes": "Comprehensive privacy law"
            },
            "PA": {
                "state_name": "Pennsylvania",
                "regulations": ["Pennsylvania Consumer Privacy Act"],
                "risk_level": "medium",
                "enforcement_level": "moderate",
                "key_requirements": [
                    "Consumer rights (access, deletion, portability)",
                    "Opt-out of targeted advertising",
                    "Consent for sensitive data"
                ],
                "penalties": ["Up to $7,500 per violation"],
                "effective_date": "2025-07-01",
                "notes": "Comprehensive privacy law"
            },
            "RI": {
                "state_name": "Rhode Island",
                "regulations": ["Rhode Island Data Transparency and Privacy Protection Act"],
                "risk_level": "medium",
                "enforcement_level": "moderate",
                "key_requirements": [
                    "Consumer rights (access, deletion, portability)",
                    "Opt-out of targeted advertising",
                    "Consent for sensitive data"
                ],
                "penalties": ["Up to $7,500 per violation"],
                "effective_date": "2025-07-01",
                "notes": "Comprehensive privacy law"
            },
            "SC": {
                "state_name": "South Carolina",
                "regulations": ["South Carolina Consumer Privacy Act"],
                "risk_level": "medium",
                "enforcement_level": "moderate",
                "key_requirements": [
                    "Consumer rights (access, deletion, portability)",
                    "Opt-out of targeted advertising",
                    "Consent for sensitive data"
                ],
                "penalties": ["Up to $7,500 per violation"],
                "effective_date": "2025-07-01",
                "notes": "Comprehensive privacy law"
            },
            "SD": {
                "state_name": "South Dakota",
                "regulations": ["South Dakota Consumer Data Privacy Act"],
                "risk_level": "medium",
                "enforcement_level": "moderate",
                "key_requirements": [
                    "Consumer rights (access, deletion, portability)",
                    "Opt-out of targeted advertising",
                    "Consent for sensitive data"
                ],
                "penalties": ["Up to $7,500 per violation"],
                "effective_date": "2025-07-01",
                "notes": "Comprehensive privacy law"
            },
            "TN": {
                "state_name": "Tennessee",
                "regulations": ["Tennessee Information Protection Act"],
                "risk_level": "medium",
                "enforcement_level": "moderate",
                "key_requirements": [
                    "Consumer rights (access, deletion, portability)",
                    "Opt-out of targeted advertising",
                    "Consent for sensitive data"
                ],
                "penalties": ["Up to $7,500 per violation"],
                "effective_date": "2025-07-01",
                "notes": "Comprehensive privacy law"
            },
            "TX": {
                "state_name": "Texas",
                "regulations": ["Texas Data Privacy and Security Act"],
                "risk_level": "medium",
                "enforcement_level": "moderate",
                "key_requirements": [
                    "Consumer rights (access, deletion, portability)",
                    "Opt-out of targeted advertising",
                    "Consent for sensitive data"
                ],
                "penalties": ["Up to $7,500 per violation"],
                "effective_date": "2024-07-01",
                "notes": "Comprehensive privacy law"
            },
            "UT": {
                "state_name": "Utah",
                "regulations": ["Utah Consumer Privacy Act"],
                "risk_level": "medium",
                "enforcement_level": "moderate",
                "key_requirements": [
                    "Consumer rights (access, deletion, portability)",
                    "Opt-out of targeted advertising",
                    "Consent for sensitive data"
                ],
                "penalties": ["Up to $7,500 per violation"],
                "effective_date": "2023-12-31",
                "notes": "Comprehensive privacy law"
            },
            "VT": {
                "state_name": "Vermont",
                "regulations": ["Vermont Data Broker Regulation"],
                "risk_level": "low",
                "enforcement_level": "moderate",
                "key_requirements": [
                    "Data broker registration",
                    "Security requirements",
                    "Opt-out mechanisms"
                ],
                "penalties": ["Up to $5,000 per violation"],
                "effective_date": "2019-01-01",
                "notes": "Limited to data broker regulation"
            },
            "VA": {
                "state_name": "Virginia",
                "regulations": ["Virginia Consumer Data Protection Act"],
                "risk_level": "high",
                "enforcement_level": "strict",
                "key_requirements": [
                    "Consumer rights (access, deletion, portability)",
                    "Opt-out of targeted advertising",
                    "Consent for sensitive data",
                    "Data minimization",
                    "Purpose limitation"
                ],
                "penalties": ["Up to $7,500 per violation"],
                "effective_date": "2023-01-01",
                "notes": "Comprehensive privacy law with strict enforcement"
            },
            "WA": {
                "state_name": "Washington",
                "regulations": ["Washington My Health My Data Act"],
                "risk_level": "high",
                "enforcement_level": "strict",
                "key_requirements": [
                    "Consent for health data collection",
                    "Prohibition on geofencing",
                    "Right to delete health data",
                    "Restrictions on data sales"
                ],
                "penalties": ["Up to $7,500 per violation"],
                "effective_date": "2024-03-31",
                "notes": "Strict health data protection law"
            },
            "WV": {
                "state_name": "West Virginia",
                "regulations": ["West Virginia Consumer Privacy Act"],
                "risk_level": "medium",
                "enforcement_level": "moderate",
                "key_requirements": [
                    "Consumer rights (access, deletion, portability)",
                    "Opt-out of targeted advertising",
                    "Consent for sensitive data"
                ],
                "penalties": ["Up to $7,500 per violation"],
                "effective_date": "2025-07-01",
                "notes": "Comprehensive privacy law"
            },
            "WI": {
                "state_name": "Wisconsin",
                "regulations": ["Wisconsin Data Privacy Act"],
                "risk_level": "medium",
                "enforcement_level": "moderate",
                "key_requirements": [
                    "Consumer rights (access, deletion, portability)",
                    "Opt-out of targeted advertising",
                    "Consent for sensitive data"
                ],
                "penalties": ["Up to $7,500 per violation"],
                "effective_date": "2025-07-01",
                "notes": "Comprehensive privacy law"
            },
            "WY": {
                "state_name": "Wyoming",
                "regulations": ["Wyoming Consumer Data Privacy Act"],
                "risk_level": "medium",
                "enforcement_level": "moderate",
                "key_requirements": [
                    "Consumer rights (access, deletion, portability)",
                    "Opt-out of targeted advertising",
                    "Consent for sensitive data"
                ],
                "penalties": ["Up to $7,500 per violation"],
                "effective_date": "2025-07-01",
                "notes": "Comprehensive privacy law"
            }
        }
        
        # Convert to StateRegulation objects
        for state_code, data in state_data.items():
            self._cache[state_code] = StateRegulation(
                state_code=state_code,
                state_name=data["state_name"],
                regulations=data["regulations"],
                risk_level=data["risk_level"],
                enforcement_level=data["enforcement_level"],
                key_requirements=data["key_requirements"],
                penalties=data["penalties"],
                effective_date=data["effective_date"],
                notes=data["notes"]
            )
        
        self._initialized = True
    
    def get_state_regulation(self, state_code: str) -> Optional[StateRegulation]:
        """Get regulation information for a specific state"""
        return self._cache.get(state_code.upper())
    
    def get_all_states(self) -> Dict[str, StateRegulation]:
        """Get all state regulations"""
        return self._cache.copy()
    
    def get_high_risk_states(self) -> List[str]:
        """Get list of high-risk states"""
        return [code for code, reg in self._cache.items() if reg.risk_level == "high"]
    
    def get_medium_risk_states(self) -> List[str]:
        """Get list of medium-risk states"""
        return [code for code, reg in self._cache.items() if reg.risk_level == "medium"]
    
    def get_low_risk_states(self) -> List[str]:
        """Get list of low-risk states"""
        return [code for code, reg in self._cache.items() if reg.risk_level == "low"]
    
    def get_states_by_enforcement_level(self, level: str) -> List[str]:
        """Get states by enforcement level"""
        return [code for code, reg in self._cache.items() if reg.enforcement_level == level]
    
    def get_states_with_regulation(self, regulation_name: str) -> List[str]:
        """Get states that have a specific regulation"""
        return [code for code, reg in self._cache.items() if regulation_name in reg.regulations]
    
    def export_to_json(self, filepath: str):
        """Export state regulations to JSON file"""
        data = {}
        for state_code, regulation in self._cache.items():
            data[state_code] = {
                "state_name": regulation.state_name,
                "regulations": regulation.regulations,
                "risk_level": regulation.risk_level,
                "enforcement_level": regulation.enforcement_level,
                "key_requirements": regulation.key_requirements,
                "penalties": regulation.penalties,
                "effective_date": regulation.effective_date,
                "notes": regulation.notes
            }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)


# Global instance for easy access
state_regulations_cache = StateRegulationsCache()
