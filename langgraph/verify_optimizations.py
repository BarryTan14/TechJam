"""
Quick verification script for optimizations
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def verify_imports():
    """Verify all optimized components can be imported"""
    print("🔍 Verifying imports...")
    
    try:
        # Test state regulations cache
        from agents import state_regulations_cache, StateRegulation
        print("✅ State regulations cache imported successfully")
        
        # Test optimized state analyzer
        from agents import OptimizedStateAnalyzer, StateAnalysisResult, BatchAnalysisResult
        print("✅ Optimized state analyzer imported successfully")
        
        # Test workflow
        from langgraph_workflow import ComplianceWorkflow
        print("✅ Compliance workflow imported successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False


def verify_state_cache():
    """Verify state regulations cache functionality"""
    print("\n🔍 Verifying state regulations cache...")
    
    try:
        from agents import state_regulations_cache
        
        # Test basic functionality
        ca_regulation = state_regulations_cache.get_state_regulation("CA")
        assert ca_regulation is not None
        assert ca_regulation.state_name == "California"
        print("✅ California regulation retrieved")
        
        # Test filtering
        high_risk_states = state_regulations_cache.get_high_risk_states()
        assert len(high_risk_states) > 0
        assert "CA" in high_risk_states
        print(f"✅ High-risk states filtering: {len(high_risk_states)} states")
        
        # Test all states
        all_states = state_regulations_cache.get_all_states()
        assert len(all_states) == 50
        print(f"✅ All {len(all_states)} states loaded")
        
        return True
        
    except Exception as e:
        print(f"❌ State cache verification failed: {e}")
        return False


def verify_workflow_integration():
    """Verify workflow integration"""
    print("\n🔍 Verifying workflow integration...")
    
    try:
        from langgraph_workflow import ComplianceWorkflow
        
        # Create workflow
        workflow = ComplianceWorkflow()
        
        # Check that optimized components are available
        assert hasattr(workflow, 'optimized_state_analyzer')
        assert hasattr(workflow, 'state_cache')
        print("✅ Workflow has optimized components")
        
        # Test state regulations access
        ca_reg = workflow.get_state_regulations("CA")
        assert ca_reg["name"] == "California"
        print("✅ Workflow can access state regulations")
        
        return True
        
    except Exception as e:
        print(f"❌ Workflow integration verification failed: {e}")
        return False


def main():
    """Run all verifications"""
    print("🚀 Verifying Optimized Workflow Components")
    print("=" * 50)
    
    success = True
    
    # Test imports
    if not verify_imports():
        success = False
    
    # Test state cache
    if not verify_state_cache():
        success = False
    
    # Test workflow integration
    if not verify_workflow_integration():
        success = False
    
    if success:
        print("\n🎉 All verifications passed! Optimizations are working correctly.")
    else:
        print("\n❌ Some verifications failed. Please check the errors above.")
    
    return success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
