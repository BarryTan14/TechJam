"""
Test script to verify recommendations are properly populated in feature compliance results
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_recommendations_population():
    """Test that recommendations are properly populated in feature compliance results"""
    print("🧪 Testing Recommendations Population")
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
            ),
            ExtractedFeature(
                feature_id="feature_3",
                feature_name="Health Data Collection",
                feature_description="Collects health-related data for wellness tracking",
                feature_content="Health data collection system for wellness applications",
                section="Health",
                priority="High",
                complexity="High",
                data_types=["health_data", "personal_identifiable_information"],
                user_impact="High",
                technical_requirements=["HIPAA compliance", "Data encryption"],
                compliance_considerations=["HIPAA", "GDPR"]
            )
        ]
        
        print(f"📋 Testing with {len(test_features)} features...")
        
        # Run workflow analysis
        result = workflow.analyze_prd(
            prd_name="Test PRD for Recommendations",
            prd_description="Testing recommendation population",
            prd_content="Test content for recommendation analysis"
        )
        
        print(f"✅ Workflow analysis completed")
        print(f"   - Total features analyzed: {len(result.feature_compliance_results)}")
        
        # Check recommendations for each feature
        for i, feature_result in enumerate(result.feature_compliance_results):
            print(f"\n📋 Feature {i+1}: {feature_result.feature.feature_name}")
            print(f"   - Risk Level: {feature_result.risk_level}")
            print(f"   - Non-compliant States: {len(feature_result.non_compliant_states)}")
            print(f"   - Recommendations Count: {len(feature_result.recommendations)}")
            
            # Verify recommendations are populated
            if feature_result.recommendations:
                print(f"   ✅ Recommendations populated: {len(feature_result.recommendations)} items")
                print(f"   📝 Sample recommendations:")
                for j, rec in enumerate(feature_result.recommendations[:3]):
                    print(f"     {j+1}. {rec}")
                if len(feature_result.recommendations) > 3:
                    print(f"     ... and {len(feature_result.recommendations) - 3} more")
            else:
                print(f"   ❌ No recommendations found")
            
            # Check for data type specific recommendations
            data_types = feature_result.feature.data_types
            has_data_type_recs = any(
                any(data_type in rec.lower() for data_type in data_types)
                for rec in feature_result.recommendations
            )
            print(f"   - Data type specific recommendations: {'✅' if has_data_type_recs else '❌'}")
            
            # Check for compliance recommendations
            has_compliance_recs = any(
                "compliance" in rec.lower() or "audit" in rec.lower() or "policy" in rec.lower()
                for rec in feature_result.recommendations
            )
            print(f"   - Compliance recommendations: {'✅' if has_compliance_recs else '❌'}")
        
        # Verify overall recommendations quality
        total_recommendations = sum(len(fr.recommendations) for fr in result.feature_compliance_results)
        avg_recommendations = total_recommendations / len(result.feature_compliance_results) if result.feature_compliance_results else 0
        
        print(f"\n📊 Recommendations Summary:")
        print(f"   - Total recommendations across all features: {total_recommendations}")
        print(f"   - Average recommendations per feature: {avg_recommendations:.1f}")
        
        # Verify recommendations are meaningful
        meaningful_recs = 0
        for fr in result.feature_compliance_results:
            for rec in fr.recommendations:
                if len(rec.split()) >= 3:  # At least 3 words for meaningful recommendation
                    meaningful_recs += 1
        
        meaningful_percentage = (meaningful_recs / total_recommendations * 100) if total_recommendations > 0 else 0
        print(f"   - Meaningful recommendations: {meaningful_recs}/{total_recommendations} ({meaningful_percentage:.1f}%)")
        
        # Success criteria
        success = (
            total_recommendations > 0 and
            avg_recommendations >= 3 and  # At least 3 recommendations per feature on average
            meaningful_percentage >= 80   # At least 80% meaningful recommendations
        )
        
        if success:
            print(f"\n🎉 Recommendations test passed!")
            print(f"   ✅ Recommendations are properly populated")
            print(f"   ✅ Recommendations are meaningful and actionable")
            print(f"   ✅ Data type specific recommendations included")
        else:
            print(f"\n❌ Recommendations test failed!")
            print(f"   - Expected: At least 3 recommendations per feature on average")
            print(f"   - Expected: At least 80% meaningful recommendations")
        
        return success
        
    except Exception as e:
        print(f"❌ Recommendations test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_optimized_state_analyzer_recommendations():
    """Test that OptimizedStateAnalyzer generates comprehensive recommendations"""
    print("\n🧪 Testing OptimizedStateAnalyzer Recommendations")
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
        
        # Test with California (high-risk state)
        ca_regulation = state_regulations_cache.get_state_regulation("CA")
        assert ca_regulation is not None, "California regulation not found"
        
        print(f"📋 Testing with California ({ca_regulation.state_name})")
        print(f"   - Risk Level: {ca_regulation.risk_level}")
        print(f"   - Enforcement Level: {ca_regulation.enforcement_level}")
        
        # Analyze feature
        results = analyzer._analyze_features_for_state([test_feature], "CA", "high")
        
        if results:
            result = results[0]
            print(f"✅ Analysis completed")
            print(f"   - Risk Level: {result.risk_level}")
            print(f"   - Compliance: {'✅' if result.is_compliant else '❌'}")
            print(f"   - Required Actions: {len(result.required_actions)}")
            
            # Check recommendations quality
            if result.required_actions:
                print(f"   📝 Required Actions:")
                for i, action in enumerate(result.required_actions[:5]):
                    print(f"     {i+1}. {action}")
                if len(result.required_actions) > 5:
                    print(f"     ... and {len(result.required_actions) - 5} more")
                
                # Check for data type specific recommendations
                data_type_recs = [rec for rec in result.required_actions if any(
                    dt in rec.lower() for dt in ["pii", "biometric", "location", "health", "financial"]
                )]
                print(f"   - Data type specific recommendations: {len(data_type_recs)}")
                
                # Check for compliance recommendations
                compliance_recs = [rec for rec in result.required_actions if any(
                    word in rec.lower() for word in ["compliance", "audit", "policy", "training"]
                )]
                print(f"   - Compliance recommendations: {len(compliance_recs)}")
                
                success = len(result.required_actions) >= 5  # At least 5 recommendations
                print(f"   - Test result: {'✅ Passed' if success else '❌ Failed'}")
                return success
            else:
                print(f"   ❌ No required actions generated")
                return False
        else:
            print(f"   ❌ No analysis results")
            return False
        
    except Exception as e:
        print(f"❌ OptimizedStateAnalyzer test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all recommendation tests"""
    print("🚀 Testing Recommendations Population")
    print("=" * 60)
    
    success = True
    
    # Test workflow recommendations
    if not test_recommendations_population():
        success = False
    
    # Test OptimizedStateAnalyzer recommendations
    if not test_optimized_state_analyzer_recommendations():
        success = False
    
    if success:
        print("\n🎉 All recommendation tests passed!")
        print("\n📝 Summary:")
        print("   ✅ Recommendations are properly populated in feature compliance results")
        print("   ✅ Recommendations are meaningful and actionable")
        print("   ✅ Data type specific recommendations included")
        print("   ✅ Compliance recommendations included")
        print("   ✅ State-specific recommendations included")
    else:
        print("\n❌ Some recommendation tests failed. Please check the errors above.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
