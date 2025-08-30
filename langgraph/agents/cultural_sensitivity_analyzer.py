"""
Cultural Sensitivity Analyzer Agent
Analyzes features for cultural sensitivity specifically for the United States and provides detailed reasoning
"""

import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

from .models import AgentOutput


@dataclass
class CulturalSensitivityScore:
    """Cultural sensitivity score data structure for US analysis"""
    region: str
    overall_score: float  # 0.0 to 1.0
    score_level: str  # "low", "medium", "high"
    reasoning: str
    cultural_factors: List[str]
    potential_issues: List[str]
    recommendations: List[str]
    confidence_score: float
    requires_human_review: bool


class CulturalSensitivityAnalyzer:
    """Agent for analyzing cultural sensitivity of features specifically for the United States"""
    
    def __init__(self, llm=None):
        self.llm = llm
        self.agent_name = "US Cultural Sensitivity Analyzer"
        
        # US-specific cultural sensitivity factors
        self.us_cultural_factors = {
            "diversity_and_inclusion": {
                "racial_diversity": ["African American", "Hispanic/Latino", "Asian American", "Native American", "Multiracial"],
                "ethnic_diversity": ["Immigrant communities", "Cultural heritage", "Language diversity", "Religious diversity"],
                "gender_identity": ["LGBTQ+ rights", "Gender equality", "Non-binary inclusion", "Transgender rights"],
                "age_diversity": ["Baby Boomers", "Gen X", "Millennials", "Gen Z", "Age discrimination"],
                "disability_rights": ["ADA compliance", "Accessibility", "Inclusive design", "Assistive technologies"],
                "socioeconomic": ["Income inequality", "Educational access", "Digital divide", "Rural vs urban"]
            },
            "privacy_and_data": {
                "individual_privacy": ["Personal data rights", "Privacy expectations", "Data ownership", "Consent culture"],
                "state_regulations": ["CCPA (California)", "CPRA", "VCDPA (Virginia)", "CDPA (Colorado)", "State-specific laws"],
                "federal_regulations": ["HIPAA", "FERPA", "COPPA", "GLBA", "Federal privacy laws"],
                "surveillance_concerns": ["Government surveillance", "Corporate tracking", "Facial recognition", "Location privacy"]
            },
            "communication_style": {
                "direct_communication": ["Straightforward language", "Clear expectations", "Transparent messaging", "Honest feedback"],
                "cultural_sensitivity": ["Inclusive language", "Avoiding stereotypes", "Respectful terminology", "Cultural awareness"],
                "accessibility": ["Plain language", "Multiple languages", "Visual aids", "Audio alternatives"],
                "digital_communication": ["Email etiquette", "Social media", "Text messaging", "Video calls"]
            },
            "values_and_beliefs": {
                "individualism": ["Personal responsibility", "Self-reliance", "Individual achievement", "Personal choice"],
                "equality": ["Equal opportunity", "Civil rights", "Social justice", "Anti-discrimination"],
                "freedom": ["Freedom of speech", "Religious freedom", "Personal liberty", "Constitutional rights"],
                "innovation": ["Technology adoption", "Entrepreneurship", "Risk-taking", "Progress orientation"]
            },
            "regional_differences": {
                "geographic_regions": ["Northeast", "Southeast", "Midwest", "Southwest", "West Coast", "Alaska/Hawaii"],
                "urban_vs_rural": ["City culture", "Suburban lifestyle", "Rural communities", "Digital access"],
                "coastal_vs_inland": ["Coastal culture", "Inland perspectives", "Regional identity", "Economic differences"],
                "red_vs_blue_states": ["Political culture", "Policy preferences", "Social values", "Regulatory environment"]
            },
            "religious_and_spiritual": {
                "christianity": ["Protestant", "Catholic", "Orthodox", "Evangelical", "Mainline"],
                "other_religions": ["Judaism", "Islam", "Hinduism", "Buddhism", "Sikhism", "Atheism/Agnosticism"],
                "religious_freedom": ["Separation of church and state", "Religious accommodation", "Holiday recognition", "Prayer practices"],
                "spiritual_diversity": ["New Age", "Indigenous spirituality", "Secular humanism", "Personal beliefs"]
            },
            "social_issues": {
                "racial_justice": ["Systemic racism", "Police reform", "Criminal justice", "Educational equity"],
                "immigration": ["Immigrant rights", "DACA", "Border policies", "Cultural integration"],
                "healthcare": ["Healthcare access", "Mental health", "Disability rights", "Aging population"],
                "environmental": ["Climate change", "Environmental justice", "Sustainability", "Green initiatives"]
            },
            "technology_and_digital": {
                "digital_literacy": ["Technology adoption", "Digital skills", "Online safety", "Information literacy"],
                "social_media": ["Platform diversity", "Content moderation", "Online harassment", "Digital wellbeing"],
                "artificial_intelligence": ["AI bias", "Algorithmic fairness", "Automation concerns", "Ethical AI"],
                "cybersecurity": ["Data breaches", "Identity theft", "Online privacy", "Digital security"]
            }
        }
    
    def analyze_cultural_sensitivity(self, feature_name: str, feature_description: str, 
                                   feature_content: str, region: str = "united_states") -> CulturalSensitivityScore:
        """
        Analyze cultural sensitivity for a feature specifically for the United States
        
        Args:
            feature_name: Name of the feature
            feature_description: Description of the feature
            feature_content: Detailed content of the feature
            region: Target region (defaults to "united_states")
            
        Returns:
            CulturalSensitivityScore object with detailed US-specific analysis
        """
        print(f"🇺🇸 Analyzing US cultural sensitivity for '{feature_name}'")
        
        # Generate analysis using LLM
        if self.llm:
            return self._analyze_with_llm(feature_name, feature_description, feature_content)
        else:
            return self._analyze_with_rules(feature_name, feature_description, feature_content)
    
    def _analyze_with_llm(self, feature_name: str, feature_description: str, 
                         feature_content: str) -> CulturalSensitivityScore:
        """Analyze cultural sensitivity using LLM with US-specific focus"""
        
        prompt = f"""You are a US cultural sensitivity expert analyzing a feature for deployment in the United States.

FEATURE INFORMATION:
Name: {feature_name}
Description: {feature_description}
Content: {feature_content[:1500]}{'...' if len(feature_content) > 1500 else ''}

US CULTURAL SENSITIVITY FACTORS TO CONSIDER:

1. DIVERSITY & INCLUSION:
   - Racial diversity (African American, Hispanic/Latino, Asian American, Native American, Multiracial)
   - Ethnic diversity (Immigrant communities, cultural heritage, language diversity)
   - Gender identity (LGBTQ+ rights, gender equality, non-binary inclusion)
   - Age diversity (Baby Boomers, Gen X, Millennials, Gen Z)
   - Disability rights (ADA compliance, accessibility, inclusive design)
   - Socioeconomic factors (Income inequality, educational access, digital divide)

2. PRIVACY & DATA:
   - Individual privacy rights and expectations
   - State regulations (CCPA, CPRA, VCDPA, CDPA)
   - Federal regulations (HIPAA, FERPA, COPPA, GLBA)
   - Surveillance concerns and data ownership

3. COMMUNICATION STYLE:
   - Direct communication preferences
   - Inclusive and respectful language
   - Accessibility requirements
   - Digital communication norms

4. VALUES & BELIEFS:
   - Individualism vs collectivism
   - Equality and civil rights
   - Freedom and personal liberty
   - Innovation and technology adoption

5. REGIONAL DIFFERENCES:
   - Geographic regions (Northeast, Southeast, Midwest, Southwest, West Coast)
   - Urban vs rural perspectives
   - Political and cultural differences
   - Economic and social variations

6. RELIGIOUS & SPIRITUAL:
   - Religious diversity and freedom
   - Separation of church and state
   - Holiday recognition and accommodation
   - Spiritual and secular perspectives

7. SOCIAL ISSUES:
   - Racial justice and systemic racism
   - Immigration and cultural integration
   - Healthcare access and mental health
   - Environmental justice and sustainability

8. TECHNOLOGY & DIGITAL:
   - Digital literacy and technology adoption
   - Social media and online behavior
   - AI bias and algorithmic fairness
   - Cybersecurity and privacy concerns

ANALYSIS REQUIREMENTS:
1. Evaluate the feature's cultural sensitivity for US users on a scale of 0.0 to 1.0
   - 0.0-0.3: Highly insensitive (significant cultural issues)
   - 0.4-0.6: Moderately sensitive (some concerns, needs improvement)
   - 0.7-1.0: Highly sensitive (culturally appropriate)

2. Provide detailed reasoning explaining:
   - How the feature aligns with or conflicts with US cultural values
   - Specific cultural factors that influenced your assessment
   - Regional considerations if applicable
   - Diversity and inclusion implications

3. Identify specific potential cultural issues or concerns:
   - Privacy and data handling concerns
   - Accessibility and inclusion barriers
   - Language and communication issues
   - Regional or demographic-specific concerns

4. Provide actionable recommendations for improvement:
   - Specific changes to enhance cultural sensitivity
   - Accessibility improvements
   - Privacy and security enhancements
   - Communication and language improvements
   - Testing and validation suggestions

5. Assess your confidence in the analysis (0.0 to 1.0)

6. Determine if human review is needed (true/false)

Return JSON with this structure:
{{
    "overall_score": 0.75,
    "score_level": "high",
    "reasoning": "Detailed explanation of US cultural sensitivity assessment with specific examples...",
    "cultural_factors": ["factor1", "factor2"],
    "potential_issues": ["specific issue1", "specific issue2"],
    "recommendations": ["specific recommendation1", "specific recommendation2"],
    "confidence_score": 0.85,
    "requires_human_review": false
}}

Focus on US-specific cultural context, legal requirements, and social values. Provide thorough, nuanced analysis with specific examples and actionable recommendations."""

        try:
            response = self.llm.generate_content(prompt)
            
            if not response or not response.text:
                raise Exception("LLM returned empty response")
            
            # Parse JSON response
            try:
                analysis_result = json.loads(response.text)
            except json.JSONDecodeError:
                analysis_result = self._extract_json_from_response(response.text)
            
            return CulturalSensitivityScore(
                region="united_states",
                overall_score=analysis_result.get("overall_score", 0.5),
                score_level=analysis_result.get("score_level", "medium"),
                reasoning=analysis_result.get("reasoning", "Analysis not available"),
                cultural_factors=analysis_result.get("cultural_factors", []),
                potential_issues=analysis_result.get("potential_issues", []),
                recommendations=analysis_result.get("recommendations", []),
                confidence_score=analysis_result.get("confidence_score", 0.5),
                requires_human_review=analysis_result.get("requires_human_review", True)
            )
            
        except Exception as e:
            print(f"⚠️ LLM analysis failed: {e}")
            return self._analyze_with_rules(feature_name, feature_description, feature_content)
    
    def _analyze_with_rules(self, feature_name: str, feature_description: str, 
                           feature_content: str) -> CulturalSensitivityScore:
        """Analyze cultural sensitivity using rule-based approach for US context"""
        
        # Basic scoring logic for US cultural factors
        score = 0.5  # Default medium score
        cultural_factors = []
        potential_issues = []
        recommendations = []
        
        # Analyze feature content for US-specific cultural factors
        content_lower = feature_content.lower()
        
        # Check for privacy and data handling
        if any(term in content_lower for term in ["personal data", "user data", "tracking", "analytics"]):
            cultural_factors.append("Privacy and data handling")
            if "consent" not in content_lower or "opt-out" not in content_lower:
                potential_issues.append("May not provide adequate user consent mechanisms")
                recommendations.append("Implement clear consent mechanisms and opt-out options")
                score -= 0.1
        
        # Check for accessibility
        if any(term in content_lower for term in ["interface", "user interface", "design", "layout"]):
            cultural_factors.append("Accessibility and inclusion")
            if "accessibility" not in content_lower and "ada" not in content_lower:
                potential_issues.append("May not meet ADA accessibility requirements")
                recommendations.append("Ensure ADA compliance and inclusive design principles")
                score -= 0.1
        
        # Check for language and communication
        if any(term in content_lower for term in ["language", "communication", "text", "message"]):
            cultural_factors.append("Communication style")
            if "inclusive" not in content_lower and "diverse" not in content_lower:
                potential_issues.append("May not use inclusive language")
                recommendations.append("Use inclusive and culturally sensitive language")
                score -= 0.05
        
        # Check for diversity considerations
        if any(term in content_lower for term in ["user", "customer", "audience", "target"]):
            cultural_factors.append("Diversity and inclusion")
            if "diverse" not in content_lower and "inclusive" not in content_lower:
                potential_issues.append("May not consider diverse user populations")
                recommendations.append("Consider diverse user populations in design and testing")
                score -= 0.05
        
        # Determine score level
        if score >= 0.7:
            score_level = "high"
        elif score >= 0.4:
            score_level = "medium"
        else:
            score_level = "low"
        
        # Generate reasoning
        reasoning = f"Feature analyzed for US cultural sensitivity. "
        if cultural_factors:
            reasoning += f"Key factors considered: {', '.join(cultural_factors)}. "
        if potential_issues:
            reasoning += f"Potential issues identified: {len(potential_issues)}. "
        reasoning += f"Overall assessment: {score_level} cultural sensitivity."
        
        return CulturalSensitivityScore(
            region="united_states",
            overall_score=max(0.0, min(1.0, score)),
            score_level=score_level,
            reasoning=reasoning,
            cultural_factors=cultural_factors,
            potential_issues=potential_issues,
            recommendations=recommendations,
            confidence_score=0.6,
            requires_human_review=score < 0.7
        )
    
    def _extract_json_from_response(self, response_text: str) -> Dict[str, Any]:
        """Extract JSON from LLM response text"""
        try:
            # Try to find JSON in the response
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx != -1 and end_idx != 0:
                json_str = response_text[start_idx:end_idx]
                return json.loads(json_str)
            else:
                raise Exception("No JSON found in response")
        except Exception as e:
            print(f"⚠️ Failed to extract JSON: {e}")
            return {
                "overall_score": 0.5,
                "score_level": "medium",
                "reasoning": "Analysis failed - using default values",
                "cultural_factors": [],
                "potential_issues": [],
                "recommendations": [],
                "confidence_score": 0.3,
                "requires_human_review": True
            }
    
    def get_us_cultural_factors(self) -> Dict[str, Dict[str, List[str]]]:
        """Get US-specific cultural factors"""
        return self.us_cultural_factors
    
    def get_all_regions(self) -> List[str]:
        """Get list of regions (now focused on US)"""
        return ["united_states"]
    
    def analyze_feature_for_all_regions(self, feature_name: str, feature_description: str, 
                                      feature_content: str) -> Dict[str, CulturalSensitivityScore]:
        """
        Analyze feature for US cultural sensitivity (simplified to focus on US only)
        
        Args:
            feature_name: Name of the feature
            feature_description: Description of the feature
            feature_content: Detailed content of the feature
            
        Returns:
            Dictionary with US cultural sensitivity analysis
        """
        print(f"🇺🇸 Analyzing US cultural sensitivity for feature: {feature_name}")
        
        # Analyze for US only
        us_analysis = self.analyze_cultural_sensitivity(feature_name, feature_description, feature_content)
        
        return {
            "united_states": us_analysis
        }
