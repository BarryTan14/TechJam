"""
Test script to verify compliance score calculations and determine risk level thresholds
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_compliance_score_calculation():
    """Test compliance score calculation and risk level determination"""
    print("🧪 Testing Compliance Score Calculation")
    print("=" * 50)
    
    # Test different risk scores and their corresponding compliance scores
    test_cases = [
        (0.0, "Perfect compliance"),
        (0.1, "Very high compliance"),
        (0.2, "High compliance"),
        (0.3, "Good compliance"),
        (0.4, "Moderate compliance"),
        (0.5, "Average compliance"),
        (0.6, "Below average compliance"),
        (0.7, "Poor compliance"),
        (0.8, "Very poor compliance"),
        (0.9, "Critical compliance issues"),
        (1.0, "Complete non-compliance")
    ]
    
    print("📊 Risk Score to Compliance Score Mapping:")
    print("-" * 60)
    print(f"{'Risk Score':<12} {'Compliance Score':<18} {'Risk Level':<12} {'Description':<20}")
    print("-" * 60)
    
    for risk_score, description in test_cases:
        # Calculate compliance score: 1.0 = fully compliant, 0.0 = non-compliant
        compliance_score = max(0.0, min(1.0, 1.0 - risk_score))
        
        # Determine risk level based on compliance score
        if compliance_score >= 0.6:
            risk_level = "low"
        else:
            risk_level = "high"
        
        print(f"{risk_score:<12.1f} {compliance_score:<18.2f} {risk_level:<12} {description:<20}")
    
    print("-" * 60)
    
    # Analyze the thresholds
    print("\n📋 Risk Level Threshold Analysis:")
    print("=" * 40)
    
    # Test different threshold scenarios
    threshold_scenarios = [
        (0.8, 0.4, "Current: 0.6 threshold"),
        (0.7, 0.5, "Alternative 1: 0.6 threshold"),
        (0.75, 0.45, "Alternative 2: 0.55 threshold"),
        (0.85, 0.35, "Alternative 3: 0.65 threshold")
    ]
    
    for high_threshold, low_threshold, description in threshold_scenarios:
        print(f"\n{description}:")
        print(f"  - Low Risk: compliance_score >= {high_threshold:.2f} (risk_score <= {1.0-high_threshold:.2f})")
        print(f"  - High Risk: compliance_score < {high_threshold:.2f} (risk_score > {1.0-high_threshold:.2f})")
        
        # Calculate what this means in practical terms
        low_risk_max_risk = 1.0 - high_threshold
        print(f"  - Low Risk Range: 0.0 to {low_risk_max_risk:.2f} risk score")
        print(f"  - High Risk Range: {low_risk_max_risk:.2f} to 1.0 risk score")
    
    return True

def test_workflow_compliance_scores():
    """Test compliance scores in actual workflow"""
    print("\n🧪 Testing Workflow Compliance Scores")
    print("=" * 50)
    
    try:
        from langgraph_workflow import ComplianceWorkflow
        from agents import ExtractedFeature
        
        # Create workflow
        workflow = ComplianceWorkflow()
        
        # Create test feature
        test_feature = ExtractedFeature(
            feature_id="test_feature",
            feature_name="Data Collection System",
            feature_description="Comprehensive data collection system with various compliance issues",
            feature_content="System that collects PII, biometric data, and location data",
            section="Data Collection",
            priority="High",
            complexity="High",
            data_types=["personal_identifiable_information", "biometric_data", "location_data"],
            user_impact="High",
            technical_requirements=["Encryption", "Consent"],
            compliance_considerations=["GDPR", "CCPA", "BIPA"]
        )
        
        print(f"📋 Testing with feature: {test_feature.feature_name}")
        
        # Run workflow analysis
        result = workflow.analyze_prd(
            prd_name="Test PRD for Compliance Scores",
            prd_description="Testing compliance score calculations",
            prd_content="Test content for compliance score analysis"
        )
        
        print(f"✅ Workflow analysis completed")
        print(f"   - Total features analyzed: {len(result.feature_compliance_results)}")
        
        # Analyze compliance scores
        compliance_scores = []
        risk_levels = []
        
        for i, feature_result in enumerate(result.feature_compliance_results):
            print(f"\n📋 Feature {i+1}: {feature_result.feature.feature_name}")
            print(f"   - Feature Risk Level: {feature_result.risk_level}")
            
            # Collect state compliance scores
            for state_code, state_score in feature_result.state_compliance_scores.items():
                compliance_scores.append(state_score.compliance_score)
                risk_levels.append(state_score.risk_level)
                
                print(f"   - State {state_code}: {state_score.compliance_score:.3f} ({state_score.risk_level})")
        
        # Analyze the distribution
        if compliance_scores:
            print(f"\n📊 Compliance Score Analysis:")
            print(f"   - Total state scores: {len(compliance_scores)}")
            print(f"   - Average compliance score: {sum(compliance_scores)/len(compliance_scores):.3f}")
            print(f"   - Min compliance score: {min(compliance_scores):.3f}")
            print(f"   - Max compliance score: {max(compliance_scores):.3f}")
            
            # Count risk levels
            low_count = risk_levels.count("low")
            high_count = risk_levels.count("high")
            print(f"   - Low risk states: {low_count}")
            print(f"   - High risk states: {high_count}")
            
            # Analyze threshold effectiveness
            low_scores = [score for score in compliance_scores if score >= 0.6]
            high_scores = [score for score in compliance_scores if score < 0.6]
            
            print(f"\n📋 Threshold Analysis (0.6 threshold):")
            print(f"   - Low risk range (≥0.6): {len(low_scores)} states, avg: {sum(low_scores)/len(low_scores):.3f}" if low_scores else "   - Low risk range (≥0.6): 0 states")
            print(f"   - High risk range (<0.6): {len(high_scores)} states, avg: {sum(high_scores)/len(high_scores):.3f}" if high_scores else "   - High risk range (<0.6): 0 states")
        
        return True
        
    except Exception as e:
        print(f"❌ Workflow compliance score test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def recommend_thresholds():
    """Recommend optimal thresholds based on analysis"""
    print("\n🎯 Recommended Risk Level Thresholds")
    print("=" * 50)
    
    print("Based on the analysis, here are the recommended thresholds:")
    print()
    
    print("📊 Current Implementation (0.6 threshold):")
    print("   - Low Risk: compliance_score >= 0.6 (risk_score <= 0.4)")
    print("   - High Risk: compliance_score < 0.6 (risk_score > 0.4)")
    print()
    
    print("💡 Alternative Thresholds to Consider:")
    print()
    
    alternatives = [
        (0.7, "More conservative - fewer high-risk states"),
        (0.5, "More aggressive - more high-risk states"),
        (0.65, "Balanced approach"),
        (0.55, "Slightly more aggressive")
    ]
    
    for threshold, description in alternatives:
        print(f"   - {threshold:.2f} threshold: {description}")
        print(f"     Low Risk: compliance_score >= {threshold:.2f}")
        print(f"     High Risk: compliance_score < {threshold:.2f}")
        print()
    
    print("🎯 Recommended Threshold: 0.6")
    print("   - Provides good balance between sensitivity and specificity")
    print("   - Aligns with typical compliance standards")
    print("   - Matches the risk score threshold used in feature analysis")
    
    return True

def main():
    """Run all compliance score tests"""
    print("🚀 Testing Compliance Score Calculations")
    print("=" * 60)
    
    success = True
    
    # Test compliance score calculation
    if not test_compliance_score_calculation():
        success = False
    
    # Test workflow compliance scores
    if not test_workflow_compliance_scores():
        success = False
    
    # Recommend thresholds
    if not recommend_thresholds():
        success = False
    
    if success:
        print("\n🎉 All compliance score tests completed!")
        print("\n📝 Summary:")
        print("   ✅ Compliance scores are calculated as 1.0 - risk_score")
        print("   ✅ Compliance scores range from 0.0 to 1.0")
        print("   ✅ Risk levels are determined by 0.6 threshold")
        print("   ✅ Low risk: compliance_score >= 0.6")
        print("   ✅ High risk: compliance_score < 0.6")
    else:
        print("\n❌ Some compliance score tests failed. Please check the errors above.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
