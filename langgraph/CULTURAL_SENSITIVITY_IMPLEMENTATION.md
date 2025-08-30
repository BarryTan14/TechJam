# Cultural Sensitivity Analyzer Implementation

## Overview

The Cultural Sensitivity Analyzer is a new agent that determines cultural sensitivity scores for features across different regions. It provides detailed reasoning for each score and specific recommendations for improving cultural sensitivity.

## Problem Solved

Previously, the workflow only analyzed compliance and risk from a regulatory perspective. The Cultural Sensitivity Analyzer adds a crucial cultural dimension to ensure features are appropriate and respectful across different global regions and cultures.

## Solution Implemented

### 1. Cultural Sensitivity Analyzer Agent

**File**: `langgraph/agents/cultural_sensitivity_analyzer.py`

**Features**:
- Analyzes features for cultural sensitivity across 7 global regions
- Provides detailed reasoning for each cultural sensitivity score
- Identifies specific cultural factors and potential issues
- Generates actionable recommendations for improvement
- Supports both LLM-based and rule-based analysis
- Comprehensive cultural factors database by region

**Key Methods**:
```python
class CulturalSensitivityAnalyzer:
    def analyze_cultural_sensitivity(self, feature_name, feature_description, feature_content, region) -> CulturalSensitivityScore
    def analyze_feature_for_all_regions(self, feature_name, feature_description, feature_content) -> Dict[str, CulturalSensitivityScore]
    def get_regional_cultural_factors(self, region) -> Dict[str, List[str]]
    def get_all_regions(self) -> List[str]
```

### 2. Cultural Sensitivity Score Data Structure

**File**: `langgraph/agents/models.py`

**New Data Structure**:
```python
@dataclass
class CulturalSensitivityScore:
    region: str
    overall_score: float  # 0.0 to 1.0
    score_level: str  # "low", "medium", "high"
    reasoning: str
    cultural_factors: List[str]
    potential_issues: List[str]
    recommendations: List[str]
    confidence_score: float
    requires_human_review: bool
```

### 3. Regional Cultural Factors Database

The analyzer includes comprehensive cultural factors for 7 regions:

**Global Factors**:
- Language and communication patterns
- Religious and spiritual considerations
- Social norms and customs
- Values and beliefs
- Communication styles

**North America**:
- Multicultural populations
- Individual privacy rights
- Disability rights and accessibility
- Gender equality and LGBTQ+ rights
- Age discrimination considerations

**Europe**:
- GDPR and privacy compliance
- Multilingual requirements
- Social welfare considerations
- Environmental awareness
- Cultural heritage preservation

**Asia Pacific**:
- Collectivism and group harmony
- Hierarchy and respect for authority
- Face culture and indirect communication
- Technology adoption patterns
- Religious diversity

**Middle East**:
- Islamic principles and religious law
- Family honor and extended families
- Hospitality culture
- Modesty and dress codes
- Authority and traditional governance

**Africa**:
- Ubuntu philosophy and community
- Oral tradition and elder wisdom
- Ethnic and linguistic diversity
- Traditional spirituality
- Extended family structures

**Latin America**:
- Family bonds and extended families
- Personal relationships and social networks
- Catholic influence and religious diversity
- Flexible time orientation
- Warm communication styles

### 4. Workflow Integration

**File**: `langgraph/langgraph_workflow.py`

**Changes**:
- Added `CulturalSensitivityAnalyzer` import and initialization
- Integrated cultural sensitivity analysis in `analyze_single_feature` method
- Added cultural sensitivity scores to `FeatureComplianceResult`
- Added overall cultural sensitivity analysis generation
- Updated `WorkflowState` to include cultural sensitivity analysis

**Integration Points**:
```python
# Cultural Sensitivity Analysis
print(f"🌍 Analyzing cultural sensitivity for feature: {feature.feature_name}")
cultural_sensitivity_scores = self.cultural_sensitivity_analyzer.analyze_feature_for_all_regions(
    feature.feature_name,
    feature.feature_description,
    feature.feature_content
)
```

### 5. Overall Cultural Sensitivity Analysis

The workflow generates an overall cultural sensitivity analysis that includes:

- **Overall cultural sensitivity level** (low/medium/high)
- **Average score across all regions**
- **Regional breakdown** with individual scores and levels
- **Key cultural issues** identified across all features
- **Recommendations** for improving cultural sensitivity
- **Human review requirements**

### 6. API Integration

**File**: `langgraph/main.py`

**Changes**:
- Added `cultural_sensitivity_analysis` field to `WorkflowResponse` model
- Updated API response to include cultural sensitivity analysis

## Analysis Process

### 1. Feature-Level Analysis

For each feature, the analyzer:

1. **Extracts cultural factors** relevant to the feature content
2. **Analyzes regional considerations** based on the cultural factors database
3. **Generates detailed reasoning** for the cultural sensitivity score
4. **Identifies potential issues** specific to each region
5. **Provides recommendations** for cultural sensitivity improvements
6. **Assesses confidence** in the analysis
7. **Determines if human review** is required

### 2. LLM-Based Analysis

When LLM is available, the analyzer uses sophisticated prompts to:

- Evaluate cultural sensitivity on a 0.0-1.0 scale
- Provide nuanced reasoning considering multiple cultural dimensions
- Identify specific cultural factors that influenced the assessment
- Generate region-specific recommendations
- Assess confidence in the analysis

### 3. Rule-Based Analysis

When LLM is not available, the analyzer uses rule-based logic to:

- Check for language and localization considerations
- Assess privacy and data protection awareness
- Evaluate accessibility and inclusion features
- Consider religious and spiritual factors
- Review gender and equality considerations

## Data Structure

### Cultural Sensitivity Score Example

```json
{
  "region": "middle_east",
  "overall_score": 0.75,
  "score_level": "high",
  "reasoning": "Detailed explanation of cultural sensitivity assessment for Middle East region, considering Islamic principles, family values, and privacy concerns...",
  "cultural_factors": [
    "Religious considerations",
    "Privacy and modesty",
    "Family values"
  ],
  "potential_issues": [
    "Biometric authentication may conflict with modesty requirements",
    "Social media integration needs cultural adaptation"
  ],
  "recommendations": [
    "Provide alternative authentication methods",
    "Implement privacy-first design",
    "Consult with local cultural experts"
  ],
  "confidence_score": 0.85,
  "requires_human_review": false
}
```

### Overall Cultural Sensitivity Analysis Example

```json
{
  "overall_cultural_sensitivity": "high",
  "overall_average_score": 0.78,
  "regional_scores": {
    "north_america": {
      "average_score": 0.82,
      "score_level": "high",
      "total_features": 5,
      "high_sensitivity_features": 4,
      "medium_sensitivity_features": 1,
      "low_sensitivity_features": 0,
      "cultural_issues": ["Issue 1", "Issue 2"],
      "recommendations": ["Rec 1", "Rec 2"]
    }
  },
  "key_cultural_issues": [
    "Language localization needed",
    "Privacy considerations required",
    "Accessibility features missing"
  ],
  "recommendations": [
    "Implement multi-language support",
    "Add privacy controls",
    "Include accessibility features"
  ],
  "total_features_analyzed": 5,
  "regions_analyzed": 7,
  "requires_human_review": false
}
```

## Usage Examples

### Analyze Single Region

```python
from agents.cultural_sensitivity_analyzer import CulturalSensitivityAnalyzer

analyzer = CulturalSensitivityAnalyzer(llm=llm_instance)

score = analyzer.analyze_cultural_sensitivity(
    "User Authentication",
    "Multi-factor authentication system",
    "Detailed feature content...",
    "middle_east"
)

print(f"Score: {score.overall_score:.2f} ({score.score_level})")
print(f"Reasoning: {score.reasoning}")
print(f"Recommendations: {score.recommendations}")
```

### Analyze All Regions

```python
all_scores = analyzer.analyze_feature_for_all_regions(
    "User Authentication",
    "Multi-factor authentication system", 
    "Detailed feature content..."
)

for region, score in all_scores.items():
    print(f"{region}: {score.overall_score:.2f} ({score.score_level})")
```

### Get Regional Cultural Factors

```python
factors = analyzer.get_regional_cultural_factors("asia_pacific")
print(f"Cultural factors for Asia Pacific: {factors}")
```

## Testing

### Test Script

**File**: `langgraph/test_cultural_sensitivity.py`

**Tests**:
- Cultural Sensitivity Analyzer initialization
- Single region analysis with detailed reasoning
- All regions analysis
- Cultural factors retrieval
- Workflow integration
- Feature-level cultural sensitivity scoring
- Overall cultural sensitivity aggregation

### Running Tests

```bash
cd langgraph
python test_cultural_sensitivity.py
```

## Benefits

1. **Cultural Awareness**: Ensures features are culturally appropriate across regions
2. **Detailed Reasoning**: Provides comprehensive explanations for cultural sensitivity scores
3. **Actionable Recommendations**: Offers specific guidance for improvement
4. **Regional Specificity**: Considers unique cultural factors for each region
5. **Comprehensive Coverage**: Analyzes 7 major global regions
6. **Integration**: Seamlessly integrated into existing workflow
7. **Flexibility**: Supports both LLM and rule-based analysis

## Future Enhancements

1. **Expanded Regions**: Add more specific regions and sub-regions
2. **Cultural Expert Review**: Integrate with cultural experts for validation
3. **Historical Context**: Include historical and political considerations
4. **Real-time Updates**: Dynamic cultural factor updates
5. **Cultural Training**: Provide cultural sensitivity training recommendations
6. **Localization Tools**: Integration with localization platforms
7. **Cultural Metrics**: Track cultural sensitivity improvements over time

## Conclusion

The Cultural Sensitivity Analyzer provides a crucial cultural dimension to the PRD analysis workflow. It ensures that features are not only compliant and low-risk but also culturally appropriate and respectful across different global regions. The detailed reasoning and specific recommendations help teams make informed decisions about cultural adaptations and improvements.
