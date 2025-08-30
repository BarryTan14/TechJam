"""
Cultural Sensitivity Analyzer Agent
Analyzes features for cultural sensitivity across different regions and provides detailed reasoning
"""

import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

from .models import AgentOutput


@dataclass
class CulturalSensitivityScore:
    """Cultural sensitivity score data structure"""
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
    """Agent for analyzing cultural sensitivity of features across regions"""
    
    def __init__(self, llm=None):
        self.llm = llm
        self.agent_name = "Cultural Sensitivity Analyzer"
        
        # Cultural sensitivity factors by region
        self.cultural_factors = {
            "global": {
                "language": ["Translation quality", "Local dialects", "Cultural idioms"],
                "religion": ["Religious holidays", "Dietary restrictions", "Prayer times"],
                "social_norms": ["Gender roles", "Age hierarchy", "Social customs"],
                "values": ["Individualism vs collectivism", "Time orientation", "Power distance"],
                "communication": ["Direct vs indirect", "Formality levels", "Non-verbal cues"]
            },
            "north_america": {
                "diversity": ["Multicultural populations", "Indigenous rights", "Immigration history"],
                "privacy": ["Individual privacy rights", "Data protection", "Personal space"],
                "accessibility": ["Disability rights", "Universal design", "Inclusive language"],
                "gender": ["Gender equality", "LGBTQ+ rights", "Non-binary inclusion"],
                "age": ["Age discrimination", "Intergenerational respect", "Youth culture"]
            },
            "europe": {
                "privacy": ["GDPR compliance", "Data sovereignty", "Right to be forgotten"],
                "multilingual": ["Official languages", "Regional dialects", "Translation requirements"],
                "social_welfare": ["Universal healthcare", "Social safety nets", "Worker rights"],
                "environmental": ["Sustainability", "Green initiatives", "Climate awareness"],
                "cultural_heritage": ["Historical preservation", "Traditional customs", "Regional identity"]
            },
            "asia_pacific": {
                "collectivism": ["Group harmony", "Family values", "Community focus"],
                "hierarchy": ["Respect for authority", "Age-based respect", "Social status"],
                "face_culture": ["Saving face", "Indirect communication", "Conflict avoidance"],
                "technology": ["Digital adoption", "Mobile-first", "Innovation culture"],
                "religion": ["Buddhism", "Hinduism", "Islam", "Christianity", "Local beliefs"]
            },
            "middle_east": {
                "religion": ["Islamic principles", "Religious law", "Prayer requirements"],
                "family": ["Family honor", "Extended families", "Gender roles"],
                "hospitality": ["Guest culture", "Generosity", "Social obligations"],
                "modesty": ["Dress codes", "Behavior standards", "Privacy concerns"],
                "authority": ["Respect for leaders", "Traditional governance", "Social hierarchy"]
            },
            "africa": {
                "community": ["Ubuntu philosophy", "Collective responsibility", "Village culture"],
                "oral_tradition": ["Storytelling", "Elder wisdom", "Cultural knowledge"],
                "diversity": ["Ethnic groups", "Languages", "Cultural practices"],
                "spirituality": ["Traditional beliefs", "Ancestral worship", "Religious diversity"],
                "family": ["Extended families", "Respect for elders", "Community support"]
            },
            "latin_america": {
                "family": ["Family bonds", "Extended families", "Intergenerational support"],
                "social": ["Personal relationships", "Social networks", "Community ties"],
                "religion": ["Catholic influence", "Indigenous beliefs", "Religious diversity"],
                "time": ["Flexible time", "Social time", "Event-oriented"],
                "communication": ["Warm communication", "Personal touch", "Emotional expression"]
            }
        }
    
    def analyze_cultural_sensitivity(self, feature_name: str, feature_description: str, 
                                   feature_content: str, region: str) -> CulturalSensitivityScore:
        """
        Analyze cultural sensitivity for a feature in a specific region
        
        Args:
            feature_name: Name of the feature
            feature_description: Description of the feature
            feature_content: Detailed content of the feature
            region: Target region for analysis
            
        Returns:
            CulturalSensitivityScore object with detailed analysis
        """
        print(f"🌍 Analyzing cultural sensitivity for '{feature_name}' in {region}")
        
        # Generate analysis using LLM
        if self.llm:
            return self._analyze_with_llm(feature_name, feature_description, feature_content, region)
        else:
            return self._analyze_with_rules(feature_name, feature_description, feature_content, region)
    
    def _analyze_with_llm(self, feature_name: str, feature_description: str, 
                         feature_content: str, region: str) -> CulturalSensitivityScore:
        """Analyze cultural sensitivity using LLM"""
        
        # Get cultural factors for the region
        region_factors = self.cultural_factors.get(region, self.cultural_factors["global"])
        
        prompt = f"""You are a cultural sensitivity expert analyzing a feature for deployment in {region.upper()}.

FEATURE INFORMATION:
Name: {feature_name}
Description: {feature_description}
Content: {feature_content[:1000]}{'...' if len(feature_content) > 1000 else ''}

REGIONAL CULTURAL FACTORS TO CONSIDER:
{json.dumps(region_factors, indent=2)}

ANALYSIS REQUIREMENTS:
1. Evaluate the feature's cultural sensitivity on a scale of 0.0 to 1.0 (0.0 = highly insensitive, 1.0 = highly sensitive)
2. Provide detailed reasoning for your score
3. Identify specific cultural factors that influenced your assessment
4. List potential cultural issues or concerns
5. Provide specific recommendations for improvement
6. Assess your confidence in the analysis (0.0 to 1.0)
7. Determine if human review is needed

Return JSON with this structure:
{{
    "overall_score": 0.75,
    "score_level": "high",
    "reasoning": "Detailed explanation of cultural sensitivity assessment...",
    "cultural_factors": ["factor1", "factor2"],
    "potential_issues": ["issue1", "issue2"],
    "recommendations": ["recommendation1", "recommendation2"],
    "confidence_score": 0.85,
    "requires_human_review": false
}}

Focus on:
- Language and communication patterns
- Religious and spiritual considerations
- Social norms and customs
- Values and beliefs
- Historical and political context
- Gender and age considerations
- Accessibility and inclusion
- Privacy and data handling
- Local regulations and laws

Provide thorough, nuanced analysis with specific examples and actionable recommendations."""

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
                region=region,
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
            return self._analyze_with_rules(feature_name, feature_description, feature_content, region)
    
    def _analyze_with_rules(self, feature_name: str, feature_description: str, 
                           feature_content: str, region: str) -> CulturalSensitivityScore:
        """Analyze cultural sensitivity using rule-based approach"""
        
        # Get cultural factors for the region
        region_factors = self.cultural_factors.get(region, self.cultural_factors["global"])
        
        # Basic scoring logic
        score = 0.5  # Default medium score
        cultural_factors = []
        potential_issues = []
        recommendations = []
        
        # Analyze content for cultural sensitivity indicators
        content_lower = feature_content.lower()
        
        # Check for language considerations
        if any(word in content_lower for word in ["language", "translation", "localization"]):
            cultural_factors.append("Language and localization")
            score += 0.1
        else:
            potential_issues.append("No language localization mentioned")
            recommendations.append("Consider adding multi-language support")
        
        # Check for privacy considerations
        if any(word in content_lower for word in ["privacy", "data protection", "gdpr"]):
            cultural_factors.append("Privacy and data protection")
            score += 0.1
        else:
            potential_issues.append("Privacy considerations not addressed")
            recommendations.append("Review privacy implications for the region")
        
        # Check for accessibility
        if any(word in content_lower for word in ["accessibility", "disability", "inclusive"]):
            cultural_factors.append("Accessibility and inclusion")
            score += 0.1
        else:
            potential_issues.append("Accessibility not considered")
            recommendations.append("Implement accessibility features")
        
        # Check for religious considerations
        if any(word in content_lower for word in ["religion", "religious", "prayer", "halal", "kosher"]):
            cultural_factors.append("Religious considerations")
            score += 0.1
        else:
            potential_issues.append("Religious factors not addressed")
            recommendations.append("Consider religious requirements for the region")
        
        # Check for gender considerations
        if any(word in content_lower for word in ["gender", "women", "men", "equality"]):
            cultural_factors.append("Gender considerations")
            score += 0.1
        else:
            potential_issues.append("Gender considerations not addressed")
            recommendations.append("Review gender-related implications")
        
        # Determine score level
        if score >= 0.7:
            score_level = "high"
        elif score >= 0.4:
            score_level = "medium"
        else:
            score_level = "low"
        
        # Generate reasoning
        reasoning = f"""
        Cultural sensitivity analysis for '{feature_name}' in {region}:
        
        Overall Assessment: {score_level.upper()} sensitivity level (score: {score:.2f})
        
        Cultural Factors Identified: {', '.join(cultural_factors) if cultural_factors else 'Limited cultural factors considered'}
        
        Key Considerations:
        - Language and localization: {'Addressed' if 'Language and localization' in cultural_factors else 'Not addressed'}
        - Privacy and data protection: {'Addressed' if 'Privacy and data protection' in cultural_factors else 'Not addressed'}
        - Accessibility and inclusion: {'Addressed' if 'Accessibility and inclusion' in cultural_factors else 'Not addressed'}
        - Religious considerations: {'Addressed' if 'Religious considerations' in cultural_factors else 'Not addressed'}
        - Gender considerations: {'Addressed' if 'Gender considerations' in cultural_factors else 'Not addressed'}
        
        This analysis is based on rule-based assessment and should be reviewed by cultural experts for the specific region.
        """
        
        return CulturalSensitivityScore(
            region=region,
            overall_score=min(score, 1.0),
            score_level=score_level,
            reasoning=reasoning,
            cultural_factors=cultural_factors,
            potential_issues=potential_issues,
            recommendations=recommendations,
            confidence_score=0.6,  # Lower confidence for rule-based analysis
            requires_human_review=True
        )
    
    def _extract_json_from_response(self, response_text: str) -> Dict[str, Any]:
        """Extract JSON from LLM response text"""
        import re
        
        if not response_text or not response_text.strip():
            return {}
        
        # Clean the response text
        cleaned_text = response_text.strip()
        
        # Remove markdown code blocks
        cleaned_text = re.sub(r'^```json\s*\n?', '', cleaned_text)
        cleaned_text = re.sub(r'^```\s*\n?', '', cleaned_text)
        cleaned_text = re.sub(r'\n?```\s*$', '', cleaned_text)
        cleaned_text = cleaned_text.strip()
        
        # Try to parse the cleaned JSON directly
        try:
            return json.loads(cleaned_text)
        except json.JSONDecodeError:
            pass
        
        # Try to find JSON object in the response
        json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
        matches = re.findall(json_pattern, cleaned_text, re.DOTALL)
        
        if matches:
            for match in matches:
                try:
                    return json.loads(match)
                except json.JSONDecodeError:
                    continue
        
        # Return default structure if no JSON found
        return {
            "overall_score": 0.5,
            "score_level": "medium",
            "reasoning": "Unable to parse LLM response",
            "cultural_factors": [],
            "potential_issues": ["Analysis parsing failed"],
            "recommendations": ["Manual review required"],
            "confidence_score": 0.3,
            "requires_human_review": True
        }
    
    def get_regional_cultural_factors(self, region: str) -> Dict[str, List[str]]:
        """Get cultural factors for a specific region"""
        return self.cultural_factors.get(region, self.cultural_factors["global"])
    
    def get_all_regions(self) -> List[str]:
        """Get list of all available regions"""
        return list(self.cultural_factors.keys())
    
    def analyze_feature_for_all_regions(self, feature_name: str, feature_description: str, 
                                      feature_content: str) -> Dict[str, CulturalSensitivityScore]:
        """Analyze cultural sensitivity for a feature across all regions"""
        results = {}
        
        for region in self.cultural_factors.keys():
            try:
                score = self.analyze_cultural_sensitivity(feature_name, feature_description, feature_content, region)
                results[region] = score
            except Exception as e:
                print(f"⚠️ Failed to analyze {region}: {e}")
                # Create default score for failed analysis
                results[region] = CulturalSensitivityScore(
                    region=region,
                    overall_score=0.5,
                    score_level="medium",
                    reasoning=f"Analysis failed: {str(e)}",
                    cultural_factors=[],
                    potential_issues=["Analysis error"],
                    recommendations=["Manual review required"],
                    confidence_score=0.0,
                    requires_human_review=True
                )
        
        return results
