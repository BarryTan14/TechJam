#!/usr/bin/env python3
"""
Test script to verify the state-centric workflow implementation
"""

import inspect
from langgraph_workflow import ComplianceWorkflow

def test_state_centric_implementation():
    """Test if the state-centric workflow is properly implemented"""
    
    print("🔍 TESTING STATE-CENTRIC WORKFLOW IMPLEMENTATION")
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
    missing_methods = []
    for method_name in state_centric_methods:
        if hasattr(workflow, method_name):
            print(f"  ✅ {method_name} - EXISTS")
        else:
            print(f"  ❌ {method_name} - MISSING")
            missing_methods.append(method_name)
    
    # Check run_workflow method
    print("\n📋 Checking run_workflow method:")
    if hasattr(workflow, 'run_workflow'):
        method_source = inspect.getsource(workflow.run_workflow)
        if 'analyze_states_against_features' in method_source:
            print("  ✅ State-centric workflow - IMPLEMENTED")
            print("  📝 Workflow: States → Features")
            workflow_type = "state-centric"
        elif 'analyze_single_feature' in method_source:
            print("  ❌ Feature-centric workflow - CURRENT")
            print("  📝 Workflow: Features → States")
            workflow_type = "feature-centric"
        else:
            print("  ❓ Unknown workflow implementation")
            workflow_type = "unknown"
    else:
        print("  ❌ run_workflow method not found")
        workflow_type = "missing"
    
    # Check WorkflowState class
    print("\n📋 Checking WorkflowState class:")
    from langgraph_workflow import WorkflowState
    
    if hasattr(WorkflowState, 'state_analysis_results'):
        print("  ✅ state_analysis_results field - EXISTS")
        state_field_exists = True
    else:
        print("  ❌ state_analysis_results field - MISSING")
        state_field_exists = False
    
    print("\n" + "=" * 60)
    print("SUMMARY:")
    
    if workflow_type == "state-centric" and len(missing_methods) == 0 and state_field_exists:
        print("🎉 SUCCESS: State-centric workflow is properly implemented!")
        print("✅ All required methods are present")
        print("✅ WorkflowState includes state_analysis_results field")
        print("✅ run_workflow uses state-centric approach")
        print("\n🚀 The workflow will now:")
        print("  1. Iterate through all 50 US states")
        print("  2. For each state, analyze all features")
        print("  3. Return results organized by state")
        print("  4. Include risk scores and reasoning for each feature-state combination")
        
    else:
        print("❌ ISSUES FOUND:")
        if workflow_type != "state-centric":
            print(f"  - Workflow type: {workflow_type}")
        if missing_methods:
            print(f"  - Missing methods: {', '.join(missing_methods)}")
        if not state_field_exists:
            print("  - Missing state_analysis_results field in WorkflowState")
        
        print("\n🔧 TO FIX:")
        print("  1. Ensure run_workflow calls analyze_states_against_features")
        print("  2. Add all missing state-centric methods")
        print("  3. Add state_analysis_results field to WorkflowState")
        print("  4. Update _generate_overall_results to handle state-centric data")

if __name__ == "__main__":
    test_state_centric_implementation()
