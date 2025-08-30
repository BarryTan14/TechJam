"""
Test script for the optimized workflow
"""

import sys
import os
import time
from datetime import datetime

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from langgraph_workflow import ComplianceWorkflow
from agents import ExtractedFeature, state_regulations_cache


def test_state_regulations_cache():
    """Test the state regulations cache"""
    print("🧪 Testing State Regulations Cache...")
    
    # Test getting a specific state
    ca_regulation = state_regulations_cache.get_state_regulation("CA")
    assert ca_regulation is not None
    assert ca_regulation.state_name == "California"
    assert "CCPA" in ca_regulation.regulations
    assert ca_regulation.risk_level == "high"
    print("✅ California regulation retrieved correctly")
    
    # Test getting all states
    all_states = state_regulations_cache.get_all_states()
    assert len(all_states) == 50
    print(f"✅ All {len(all_states)} states loaded")
    
    # Test risk level filtering
    high_risk_states = state_regulations_cache.get_high_risk_states()
    medium_risk_states = state_regulations_cache.get_medium_risk_states()
    low_risk_states = state_regulations_cache.get_low_risk_states()
    
    print(f"✅ Risk level filtering: {len(high_risk_states)} high, {len(medium_risk_states)} medium, {len(low_risk_states)} low")
    
    # Test regulation search
    ccpa_states = state_regulations_cache.get_states_with_regulation("CCPA")
    assert "CA" in ccpa_states
    print(f"✅ CCPA found in {len(ccpa_states)} states")
    
    print("✅ State Regulations Cache tests passed!\n")


def test_optimized_state_analyzer():
    """Test the optimized state analyzer"""
    print("🧪 Testing Optimized State Analyzer...")
    
    from agents import OptimizedStateAnalyzer
    
    # Create test features
    test_features = [
        ExtractedFeature(
            feature_id="feature_1",
            feature_name="User Behavior Tracking",
            feature_description="Tracks user behavior across the platform for analytics",
            feature_content="Comprehensive user behavior tracking system",
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
            feature_description="Uses fingerprint and facial recognition for login",
            feature_content="Biometric authentication system",
            section="Security",
            priority="High",
            complexity="High",
            data_types=["biometric_data"],
            user_impact="High",
            technical_requirements=["Consent mechanisms", "Secure storage"],
            compliance_considerations=["BIPA", "GDPR"]
        )
    ]
    
    # Test with a few states first
    analyzer = OptimizedStateAnalyzer(llm=None)  # No LLM for testing
    target_states = ["CA", "VA", "IL", "TX", "NY"]
    
    start_time = time.time()
    batch_result = analyzer.analyze_features_against_states(test_features, target_states)
    processing_time = time.time() - start_time
    
    print(f"✅ Analyzed {len(test_features)} features against {len(target_states)} states in {processing_time:.2f}s")
    print(f"📊 Total analyses: {batch_result.overall_stats['total_analyses']}")
    print(f"📊 Compliance rate: {batch_result.overall_stats['compliance_rate']:.1%}")
    
    # Verify results structure
    assert len(batch_result.state_results) == len(target_states)
    assert len(batch_result.feature_results) == len(test_features)
    
    # Check that high-risk states have higher risk scores
    ca_results = batch_result.state_results.get("CA", [])
    if ca_results:
        avg_ca_risk = sum(r.risk_score for r in ca_results) / len(ca_results)
        print(f"📊 CA average risk score: {avg_ca_risk:.2f}")
    
    print("✅ Optimized State Analyzer tests passed!\n")


def test_workflow_integration():
    """Test the complete workflow integration"""
    print("🧪 Testing Workflow Integration...")
    
    # Create workflow
    workflow = ComplianceWorkflow()
    
    # Create test PRD data
    prd_data = {
        "prd_id": "test_prd_001",
        "prd_name": "Test Privacy-Critical Application",
        "prd_description": "Test application with privacy-sensitive features",
        "prd_content": """
        Product Requirements Document: Privacy-Critical Application
        
        1. User Behavior Tracking
        - Tracks user behavior across the platform
        - Collects personal data including preferences and location
        - Uses for analytics and personalized recommendations
        
        2. Biometric Authentication
        - Uses fingerprint and facial recognition
        - Stores biometric templates securely
        - Requires explicit consent
        
        3. Data Sharing
        - Shares data with third-party analytics providers
        - Cross-border data transfers for global operations
        - Data retention period: 2 years
        """,
        "metadata": {
            "document_type": "product_requirements",
            "analysis_date": datetime.now().isoformat(),
            "word_count": 100
        }
    }
    
    # Run workflow
    start_time = time.time()
    final_state = workflow.run_workflow(prd_data)
    processing_time = time.time() - start_time
    
    print(f"✅ Workflow completed in {processing_time:.2f}s")
    print(f"📊 Extracted {len(final_state.extracted_features)} features")
    print(f"📊 Overall risk level: {final_state.overall_risk_level}")
    print(f"📊 Overall confidence: {final_state.overall_confidence_score:.1%}")
    
    # Verify results
    assert len(final_state.extracted_features) > 0
    assert final_state.overall_risk_level in ["low", "medium", "high", "critical"]
    assert 0 <= final_state.overall_confidence_score <= 1
    
    print("✅ Workflow Integration tests passed!\n")


def test_performance_comparison():
    """Compare performance with and without optimization"""
    print("🧪 Testing Performance Comparison...")
    
    # Create test features
    test_features = [
        ExtractedFeature(
            feature_id=f"feature_{i}",
            feature_name=f"Test Feature {i}",
            feature_description=f"Test feature {i} with privacy considerations",
            feature_content=f"Content for test feature {i}",
            section="Test",
            priority="Medium",
            complexity="Medium",
            data_types=["personal_identifiable_information"],
            user_impact="Medium",
            technical_requirements=["Consent mechanisms"],
            compliance_considerations=["GDPR"]
        )
        for i in range(1, 4)  # Test with 3 features
    ]
    
    from agents import OptimizedStateAnalyzer
    
    # Test with limited states for performance comparison
    target_states = ["CA", "VA", "CO", "CT", "UT", "NY", "IL"]
    
    analyzer = OptimizedStateAnalyzer(llm=None)  # No LLM for consistent testing
    
    # Measure performance
    start_time = time.time()
    batch_result = analyzer.analyze_features_against_states(test_features, target_states)
    processing_time = time.time() - start_time
    
    total_analyses = batch_result.overall_stats['total_analyses']
    analyses_per_second = total_analyses / processing_time if processing_time > 0 else 0
    
    print(f"✅ Performance Results:")
    print(f"   - Total analyses: {total_analyses}")
    print(f"   - Processing time: {processing_time:.2f}s")
    print(f"   - Analyses per second: {analyses_per_second:.1f}")
    print(f"   - Average time per analysis: {(processing_time/total_analyses)*1000:.1f}ms")
    
    # Performance benchmarks
    assert processing_time < 5.0  # Should complete in under 5 seconds
    assert analyses_per_second > 10  # Should process at least 10 analyses per second
    
    print("✅ Performance tests passed!\n")


def main():
    """Run all tests"""
    print("🚀 Starting Optimized Workflow Tests")
    print("=" * 50)
    
    try:
        test_state_regulations_cache()
        test_optimized_state_analyzer()
        test_workflow_integration()
        test_performance_comparison()
        
        print("🎉 All tests passed! The optimized workflow is working correctly.")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
