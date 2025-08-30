"""
Simple test to verify the FeatureComplianceResult fix
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_feature_compliance_result_creation():
    """Test that FeatureComplianceResult can be created with all required parameters"""
    print("🧪 Testing FeatureComplianceResult creation...")
    
    try:
        from agents import FeatureComplianceResult, ExtractedFeature, USStateCompliance, StateComplianceScore
        from datetime import datetime
        
        # Create a test feature
        test_feature = ExtractedFeature(
            feature_id="test_feature_1",
            feature_name="Test Feature",
            feature_description="A test feature for compliance analysis",
            feature_content="Test content",
            section="Test",
            priority="Medium",
            complexity="Medium",
            data_types=["personal_identifiable_information"],
            user_impact="Medium",
            technical_requirements=["Consent mechanisms"],
            compliance_considerations=["GDPR"]
        )
        
        # Create test US state compliance
        test_us_state_compliance = [
            USStateCompliance(
                state_name="California",
                state_code="CA",
                is_compliant=False,
                non_compliant_regulations=["CCPA"],
                risk_level="High",
                required_actions=["Implement consent mechanisms"],
                notes="Test compliance data"
            )
        ]
        
        # Create test state compliance scores
        test_state_compliance_scores = {
            "CA": StateComplianceScore(
                state_code="CA",
                state_name="California",
                compliance_score=0.3,
                risk_level="high",
                reasoning="Test reasoning",
                non_compliant_regulations=["CCPA"],
                required_actions=["Implement consent mechanisms"],
                notes="Test score data"
            )
        }
        
        # Test creating FeatureComplianceResult with all required parameters
        result = FeatureComplianceResult(
            feature=test_feature,
            agent_outputs={},  # Empty dict for this test
            compliance_flags=["GDPR", "CCPA"],
            risk_level="high",
            confidence_score=0.8,
            requires_human_review=True,
            reasoning="Test reasoning",
            recommendations=["Implement consent mechanisms"],
            us_state_compliance=test_us_state_compliance,
            non_compliant_states=["CA"],
            state_compliance_scores=test_state_compliance_scores,
            processing_time=1.5,
            timestamp=datetime.now().isoformat()
        )
        
        print("✅ FeatureComplianceResult created successfully!")
        print(f"   - Feature: {result.feature.feature_name}")
        print(f"   - Risk Level: {result.risk_level}")
        print(f"   - Non-compliant states: {result.non_compliant_states}")
        print(f"   - State compliance scores: {len(result.state_compliance_scores)} states")
        
        return True
        
    except Exception as e:
        print(f"❌ FeatureComplianceResult creation failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_workflow_import():
    """Test that the workflow can be imported without errors"""
    print("\n🧪 Testing workflow import...")
    
    try:
        from langgraph_workflow import ComplianceWorkflow
        print("✅ ComplianceWorkflow imported successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Workflow import failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("🚀 Testing FeatureComplianceResult Fix")
    print("=" * 40)
    
    success = True
    
    # Test FeatureComplianceResult creation
    if not test_feature_compliance_result_creation():
        success = False
    
    # Test workflow import
    if not test_workflow_import():
        success = False
    
    if success:
        print("\n🎉 All tests passed! The fix is working correctly.")
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
    
    return success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
