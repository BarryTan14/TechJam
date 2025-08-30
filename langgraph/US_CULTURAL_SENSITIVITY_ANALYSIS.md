# US Cultural Sensitivity Analysis

## Overview

The Cultural Sensitivity Analyzer has been redesigned to focus specifically on the United States, providing detailed analysis of features for US cultural sensitivity, compliance, and inclusivity. This analysis considers the diverse cultural landscape of the United States and provides actionable recommendations for improvement.

## Key Features

### 🇺🇸 US-Specific Cultural Factors

The analyzer evaluates features against 8 major categories of US cultural factors:

#### 1. **Diversity & Inclusion**
- **Racial Diversity**: African American, Hispanic/Latino, Asian American, Native American, Multiracial
- **Ethnic Diversity**: Immigrant communities, cultural heritage, language diversity, religious diversity
- **Gender Identity**: LGBTQ+ rights, gender equality, non-binary inclusion, transgender rights
- **Age Diversity**: Baby Boomers, Gen X, Millennials, Gen Z, age discrimination
- **Disability Rights**: ADA compliance, accessibility, inclusive design, assistive technologies
- **Socioeconomic**: Income inequality, educational access, digital divide, rural vs urban

#### 2. **Privacy & Data**
- **Individual Privacy**: Personal data rights, privacy expectations, data ownership, consent culture
- **State Regulations**: CCPA (California), CPRA, VCDPA (Virginia), CDPA (Colorado), state-specific laws
- **Federal Regulations**: HIPAA, FERPA, COPPA, GLBA, federal privacy laws
- **Surveillance Concerns**: Government surveillance, corporate tracking, facial recognition, location privacy

#### 3. **Communication Style**
- **Direct Communication**: Straightforward language, clear expectations, transparent messaging, honest feedback
- **Cultural Sensitivity**: Inclusive language, avoiding stereotypes, respectful terminology, cultural awareness
- **Accessibility**: Plain language, multiple languages, visual aids, audio alternatives
- **Digital Communication**: Email etiquette, social media, text messaging, video calls

#### 4. **Values & Beliefs**
- **Individualism**: Personal responsibility, self-reliance, individual achievement, personal choice
- **Equality**: Equal opportunity, civil rights, social justice, anti-discrimination
- **Freedom**: Freedom of speech, religious freedom, personal liberty, constitutional rights
- **Innovation**: Technology adoption, entrepreneurship, risk-taking, progress orientation

#### 5. **Regional Differences**
- **Geographic Regions**: Northeast, Southeast, Midwest, Southwest, West Coast, Alaska/Hawaii
- **Urban vs Rural**: City culture, suburban lifestyle, rural communities, digital access
- **Coastal vs Inland**: Coastal culture, inland perspectives, regional identity, economic differences
- **Political Culture**: Red vs blue states, policy preferences, social values, regulatory environment

#### 6. **Religious & Spiritual**
- **Christianity**: Protestant, Catholic, Orthodox, Evangelical, Mainline
- **Other Religions**: Judaism, Islam, Hinduism, Buddhism, Sikhism, Atheism/Agnosticism
- **Religious Freedom**: Separation of church and state, religious accommodation, holiday recognition, prayer practices
- **Spiritual Diversity**: New Age, indigenous spirituality, secular humanism, personal beliefs

#### 7. **Social Issues**
- **Racial Justice**: Systemic racism, police reform, criminal justice, educational equity
- **Immigration**: Immigrant rights, DACA, border policies, cultural integration
- **Healthcare**: Healthcare access, mental health, disability rights, aging population
- **Environmental**: Climate change, environmental justice, sustainability, green initiatives

#### 8. **Technology & Digital**
- **Digital Literacy**: Technology adoption, digital skills, online safety, information literacy
- **Social Media**: Platform diversity, content moderation, online harassment, digital wellbeing
- **Artificial Intelligence**: AI bias, algorithmic fairness, automation concerns, ethical AI
- **Cybersecurity**: Data breaches, identity theft, online privacy, digital security

## Scoring System

### Score Ranges
- **0.0-0.3**: **Highly Insensitive** - Significant cultural issues that need immediate attention
- **0.4-0.6**: **Moderately Sensitive** - Some concerns, needs improvement
- **0.7-1.0**: **Highly Sensitive** - Culturally appropriate and inclusive

### Assessment Criteria
1. **Privacy & Data Handling**: Consent mechanisms, data rights, regulatory compliance
2. **Accessibility & Inclusion**: ADA compliance, diverse user populations, inclusive design
3. **Language & Communication**: Inclusive language, cultural awareness, clear messaging
4. **Diversity Considerations**: Representation, cultural sensitivity, demographic awareness
5. **Legal Compliance**: State and federal regulations, industry standards
6. **Regional Awareness**: Geographic and cultural differences across the US

## Analysis Output

### Detailed Reasoning
The analyzer provides comprehensive reasoning explaining:
- How the feature aligns with or conflicts with US cultural values
- Specific cultural factors that influenced the assessment
- Regional considerations if applicable
- Diversity and inclusion implications

### Potential Issues
Identifies specific concerns such as:
- Privacy and data handling concerns
- Accessibility and inclusion barriers
- Language and communication issues
- Regional or demographic-specific concerns

### Actionable Recommendations
Provides specific recommendations for improvement:
- **Accessibility Improvements**: ADA compliance, inclusive design, assistive technologies
- **Privacy Enhancements**: Consent mechanisms, data rights, regulatory compliance
- **Communication Improvements**: Inclusive language, cultural sensitivity, clear messaging
- **Testing & Validation**: User testing with diverse populations, cultural review processes

## Example Analysis

### Feature: User Data Analytics Dashboard

**Score**: 0.35 (Moderately Sensitive)

**Reasoning**: 
"This feature raises significant privacy concerns for US users. The collection of personal browsing history, location data, and demographic information without clear consent mechanisms violates US privacy expectations and may conflict with state regulations like CCPA. The lack of data export and deletion capabilities further compounds privacy concerns."

**Cultural Factors Considered**:
- Privacy and data handling
- Individual privacy rights
- State regulations (CCPA, CPRA)
- Federal regulations

**Potential Issues**:
- May not provide adequate user consent mechanisms
- Violates US privacy expectations
- May conflict with state privacy regulations
- No data export/deletion capabilities

**Recommendations**:
- Implement clear consent mechanisms and opt-out options
- Add data export and deletion capabilities
- Ensure compliance with state privacy regulations
- Provide transparency about data collection and usage
- Conduct privacy impact assessment

## Integration with Workflow

The US cultural sensitivity analysis is integrated into the main workflow:

1. **Feature Analysis**: Each feature is analyzed for US cultural sensitivity
2. **Aggregation**: Results are aggregated across all features
3. **Overall Assessment**: Provides overall cultural sensitivity score and recommendations
4. **Storage**: Results are stored in MongoDB for future reference
5. **Reporting**: Included in executive reports and API responses

## Usage

### Basic Analysis
```python
from langgraph.agents.cultural_sensitivity_analyzer import CulturalSensitivityAnalyzer

analyzer = CulturalSensitivityAnalyzer()
analysis = analyzer.analyze_cultural_sensitivity(
    feature_name="My Feature",
    feature_description="Feature description",
    feature_content="Detailed feature content"
)

print(f"Score: {analysis.overall_score:.2f} ({analysis.score_level})")
print(f"Reasoning: {analysis.reasoning}")
print(f"Recommendations: {analysis.recommendations}")
```

### All Features Analysis
```python
results = analyzer.analyze_feature_for_all_regions(
    feature_name="My Feature",
    feature_description="Feature description", 
    feature_content="Detailed feature content"
)

# Results now contain only US analysis
us_analysis = results["united_states"]
```

## Benefits

### For Developers
- **Early Detection**: Identify cultural sensitivity issues during development
- **Compliance**: Ensure compliance with US regulations and standards
- **Inclusivity**: Create more inclusive and accessible features
- **Risk Mitigation**: Reduce legal and reputational risks

### For Users
- **Better Experience**: More culturally appropriate and accessible features
- **Privacy Protection**: Enhanced privacy controls and data rights
- **Inclusivity**: Features that work for diverse populations
- **Transparency**: Clear communication about data usage and features

### For Organizations
- **Compliance**: Meet regulatory requirements across US states
- **Reputation**: Demonstrate commitment to diversity and inclusion
- **Market Access**: Ensure features work for diverse US markets
- **Risk Management**: Avoid cultural missteps and legal issues

## Testing

Run the test suite to verify functionality:

```bash
cd langgraph
python test_us_cultural_sensitivity.py
```

This will test:
- Basic analyzer functionality
- Feature analysis with sample features
- All-regions analysis (US-focused)
- Cultural factors and recommendations

## Conclusion

The US-focused cultural sensitivity analysis provides comprehensive evaluation of features for the diverse US market. By considering privacy, accessibility, diversity, and regional differences, it helps create more inclusive and culturally appropriate features that work for all Americans.
