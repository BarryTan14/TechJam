#!/usr/bin/env python3
"""
Verification script to check the current workflow implementation
"""

import inspect
from langgraph_workflow import ComplianceWorkflow

def verify_workflow_implementation():
    """Verify what workflow implementation is currently in place"""
    
    print("🔍 VERIFYING LANGGRAPH WORKFLOW IMPLEMENTATION")
    print("=" * 60)
    
    # Create workflow instance
    workflow = ComplianceWorkflow()
    
    # Check if state-centric methods exist
    state_centric_methods = [
        'analyze_states_against_features',
        'analyze_feature_for_state', 
        'analyze_state_specific_compliance',
        'get_state_regulations',
        'convert_state_results_to_feature_results'
    ]
    
    print("\n📋 Checking for state-centric methods:")
    for method_name in state_centric_methods:
        if hasattr(workflow, method_name):
            print(f"  ✅ {method_name} - EXISTS")
        else:
            print(f"  ❌ {method_name} - MISSING")
    
    # Check run_workflow method
    print("\n📋 Checking run_workflow method:")
    if hasattr(workflow, 'run_workflow'):
        method_source = inspect.getsource(workflow.run_workflow)
        if 'analyze_states_against_features' in method_source:
            print("  ✅ State-centric workflow - IMPLEMENTED")
            print("  📝 Workflow: States → Features")
        elif 'analyze_single_feature' in method_source:
            print("  ❌ Feature-centric workflow - CURRENT")
            print("  📝 Workflow: Features → States")
        else:
            print("  ❓ Unknown workflow implementation")
    else:
        print("  ❌ run_workflow method not found")
    
    # Check WorkflowState class
    print("\n📋 Checking WorkflowState class:")
    from langgraph_workflow import WorkflowState
    
    if hasattr(WorkflowState, 'state_analysis_results'):
        print("  ✅ state_analysis_results field - EXISTS")
    else:
        print("  ❌ state_analysis_results field - MISSING")
    
    print("\n" + "=" * 60)
    print("SUMMARY:")
    print("The current implementation appears to be using the OLD feature-centric approach.")
    print("To implement the state-centric approach as requested, we need to:")
    print("1. Replace the run_workflow method with state-centric logic")
    print("2. Add the missing state-centric analysis methods")
    print("3. Update the WorkflowState class to include state_analysis_results")
    print("4. Update the _generate_overall_results method to handle state-centric data")

if __name__ == "__main__":
    verify_workflow_implementation()
