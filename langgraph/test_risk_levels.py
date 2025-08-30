"""
Test script to verify that all risk levels in state compliance scores are only "low" or "high"
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_risk_levels():
    """Test that all risk levels are only 'low' or 'high'"""
    print("🧪 Testing Risk Level Validation")
    print("=" * 50)
    
    try:
        from langgraph_workflow import ComplianceWorkflow
        from agents import ExtractedFeature
        
        # Create workflow
        workflow = ComplianceWorkflow()
        
        # Create test features with different data types
        test_features = [
            ExtractedFeature(
                feature_id="feature_1",
                feature_name="User Behavior Tracking",
                feature_description="Tracks user behavior across the platform for analytics and personalized recommendations",
                feature_content="Comprehensive user behavior tracking system that collects personal data",
                section="Analytics",
                priority="High",
                complexity="Medium",
                data_types=["personal_identifiable_information", "behavioral_data", "location_data"],
                user_impact="High",
                technical_requirements=["Consent mechanisms", "Data deletion"],
                compliance_considerations=["GDPR", "CCPA"]
            ),
            ExtractedFeature(
                feature_id="feature_2",
                feature_name="Biometric Authentication",
                feature_description="Uses fingerprint and facial recognition for secure login",
                feature_content="Biometric authentication system for user login",
                section="Security",
                priority="High",
                complexity="High",
                data_types=["biometric_data"],
                user_impact="High",
                technical_requirements=["Secure storage", "Consent mechanisms"],
                compliance_considerations=["BIPA", "GDPR"]
            )
        ]
        
        print(f"📋 Testing with {len(test_features)} features...")
        
        # Run workflow analysis
        result = workflow.analyze_prd(
            prd_name="Test PRD for Risk Levels",
            prd_description="Testing risk level validation",
            prd_content="Test content for risk level analysis"
        )
        
        print(f"✅ Workflow analysis completed")
        print(f"   - Total features analyzed: {len(result.feature_compliance_results)}")
        
        # Check risk levels for each feature
        invalid_risk_levels = []
        valid_risk_levels = []
        
        for i, feature_result in enumerate(result.feature_compliance_results):
            print(f"\n📋 Feature {i+1}: {feature_result.feature.feature_name}")
            print(f"   - Feature Risk Level: {feature_result.risk_level}")
            
            # Check feature risk level
            if feature_result.risk_level not in ["low", "high"]:
                invalid_risk_levels.append(f"Feature {i+1} risk level: {feature_result.risk_level}")
            else:
                valid_risk_levels.append(f"Feature {i+1} risk level: {feature_result.risk_level}")
            
            # Check state compliance scores
            for state_code, state_score in feature_result.state_compliance_scores.items():
                state_risk_level = state_score.risk_level
                print(f"   - State {state_code} Risk Level: {state_risk_level}")
                
                if state_risk_level not in ["low", "high"]:
                    invalid_risk_levels.append(f"Feature {i+1}, State {state_code} risk level: {state_risk_level}")
                else:
                    valid_risk_levels.append(f"Feature {i+1}, State {state_code} risk level: {state_risk_level}")
        
        # Check overall risk level
        print(f"\n📊 Overall Risk Level: {result.overall_risk_level}")
        if result.overall_risk_level not in ["low", "high"]:
            invalid_risk_levels.append(f"Overall risk level: {result.overall_risk_level}")
        else:
            valid_risk_levels.append(f"Overall risk level: {result.overall_risk_level}")
        
        # Report results
        print(f"\n📊 Risk Level Validation Results:")
        print(f"   - Valid risk levels: {len(valid_risk_levels)}")
        print(f"   - Invalid risk levels: {len(invalid_risk_levels)}")
        
        if invalid_risk_levels:
            print(f"\n❌ Invalid risk levels found:")
            for invalid in invalid_risk_levels:
                print(f"   - {invalid}")
            return False
        else:
            print(f"\n✅ All risk levels are valid (only 'low' or 'high')")
            print(f"   - Total valid risk levels: {len(valid_risk_levels)}")
            return True
        
    except Exception as e:
        print(f"❌ Risk level test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_optimized_state_analyzer_risk_levels():
    """Test that OptimizedStateAnalyzer only generates 'low' or 'high' risk levels"""
    print("\n🧪 Testing OptimizedStateAnalyzer Risk Levels")
    print("=" * 50)
    
    try:
        from agents import OptimizedStateAnalyzer, ExtractedFeature, state_regulations_cache
        
        # Create analyzer
        analyzer = OptimizedStateAnalyzer(llm=None)
        
        # Test feature with multiple data types
        test_feature = ExtractedFeature(
            feature_id="test_feature",
            feature_name="Comprehensive Data Collection",
            feature_description="Collects various types of sensitive data for analysis",
            feature_content="System that collects PII, biometric data, and location data",
            section="Data Collection",
            priority="High",
            complexity="High",
            data_types=["personal_identifiable_information", "biometric_data", "location_data"],
            user_impact="High",
            technical_requirements=["Encryption", "Consent"],
            compliance_considerations=["GDPR", "CCPA", "BIPA"]
        )
        
        # Test with multiple states
        test_states = ["CA", "VA", "TX", "NY"]
        invalid_risk_levels = []
        valid_risk_levels = []
        
        for state_code in test_states:
            state_regulation = state_regulations_cache.get_state_regulation(state_code)
            if state_regulation:
                print(f"📋 Testing with {state_regulation.state_name} ({state_code})")
                
                # Analyze feature
                results = analyzer._analyze_features_for_state([test_feature], state_code, "high")
                
                if results:
                    result = results[0]
                    risk_level = result.risk_level
                    print(f"   - Risk Level: {risk_level}")
                    
                    if risk_level not in ["low", "high"]:
                        invalid_risk_levels.append(f"{state_code}: {risk_level}")
                    else:
                        valid_risk_levels.append(f"{state_code}: {risk_level}")
        
        # Report results
        print(f"\n📊 OptimizedStateAnalyzer Risk Level Results:")
        print(f"   - Valid risk levels: {len(valid_risk_levels)}")
        print(f"   - Invalid risk levels: {len(invalid_risk_levels)}")
        
        if invalid_risk_levels:
            print(f"\n❌ Invalid risk levels found:")
            for invalid in invalid_risk_levels:
                print(f"   - {invalid}")
            return False
        else:
            print(f"\n✅ All OptimizedStateAnalyzer risk levels are valid (only 'low' or 'high')")
            return True
        
    except Exception as e:
        print(f"❌ OptimizedStateAnalyzer risk level test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all risk level tests"""
    print("🚀 Testing Risk Level Validation")
    print("=" * 60)
    
    success = True
    
    # Test workflow risk levels
    if not test_risk_levels():
        success = False
    
    # Test OptimizedStateAnalyzer risk levels
    if not test_optimized_state_analyzer_risk_levels():
        success = False
    
    if success:
        print("\n🎉 All risk level tests passed!")
        print("\n📝 Summary:")
        print("   ✅ All risk levels are only 'low' or 'high'")
        print("   ✅ No 'medium' or 'critical' risk levels found")
        print("   ✅ State compliance scores have correct risk levels")
        print("   ✅ Feature compliance results have correct risk levels")
        print("   ✅ Overall risk levels are correct")
    else:
        print("\n❌ Some risk level tests failed. Please check the errors above.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
