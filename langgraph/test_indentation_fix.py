#!/usr/bin/env python3
"""
Test script to verify that the indentation error is fixed
"""

import sys
import os

# Add the parent directory to the path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_import():
    """Test that the workflow can be imported without indentation errors"""
    try:
        from langgraph.langgraph_workflow import ComplianceWorkflow
        print("✅ Successfully imported ComplianceWorkflow - no indentation errors")
        return True
    except IndentationError as e:
        print(f"❌ Indentation error: {e}")
        return False
    except Exception as e:
        print(f"❌ Other error: {e}")
        return False

def test_syntax():
    """Test that the file has valid Python syntax"""
    try:
        import ast
        with open('langgraph_workflow.py', 'r', encoding='utf-8') as f:
            content = f.read()
        ast.parse(content)
        print("✅ File has valid Python syntax")
        return True
    except SyntaxError as e:
        print(f"❌ Syntax error: {e}")
        return False
    except Exception as e:
        print(f"❌ Other error: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Testing indentation fix...")
    print("=" * 50)
    
    # Test 1: Syntax check
    syntax_success = test_syntax()
    
    # Test 2: Import test
    import_success = test_import()
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    print(f"   Syntax Check: {'✅ PASS' if syntax_success else '❌ FAIL'}")
    print(f"   Import Test: {'✅ PASS' if import_success else '❌ FAIL'}")
    
    overall_success = syntax_success and import_success
    
    if overall_success:
        print("\n🎉 All tests passed! The indentation error is fixed.")
    else:
        print("\n⚠️ Some tests failed. The indentation error may still exist.")
    
    return overall_success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
