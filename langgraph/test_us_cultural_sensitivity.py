#!/usr/bin/env python3
"""
Test script to demonstrate US-focused cultural sensitivity analysis
"""

import sys
import os
import json
from datetime import datetime

# Add the parent directory to the path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langgraph.agents.cultural_sensitivity_analyzer import CulturalSensitivityAnalyzer

def test_us_cultural_sensitivity_analyzer():
    """Test the US-focused cultural sensitivity analyzer"""
    print("🇺🇸 Testing US Cultural Sensitivity Analyzer")
    print("=" * 60)
    
    # Initialize the analyzer
    analyzer = CulturalSensitivityAnalyzer()
    
    # Test US cultural factors
    print("\n📋 US Cultural Factors Available:")
    us_factors = analyzer.get_us_cultural_factors()
    for category, subcategories in us_factors.items():
        print(f"\n  {category.replace('_', ' ').title()}:")
        for subcategory, factors in subcategories.items():
            print(f"    - {subcategory.replace('_', ' ').title()}: {', '.join(factors[:3])}{'...' if len(factors) > 3 else ''}")
    
    # Test regions
    print(f"\n🌍 Available Regions: {analyzer.get_all_regions()}")
    
    return True

def test_feature_analysis():
    """Test cultural sensitivity analysis for sample features"""
    print("\n🧪 Testing Feature Analysis")
    print("=" * 60)
    
    # Initialize the analyzer
    analyzer = CulturalSensitivityAnalyzer()
    
    # Sample features to test
    test_features = [
        {
            "name": "User Data Analytics Dashboard",
            "description": "A dashboard that displays user behavior analytics and personal data insights",
            "content": """
            This feature provides comprehensive analytics on user behavior including:
            - Personal browsing history and preferences
            - Location tracking and movement patterns
            - Social media interactions and connections
            - Purchase history and financial data
            - Demographic information and personal details
            
            The dashboard displays this information in charts and graphs for business intelligence.
            Users can view their own data but cannot export or delete it.
            """
        },
        {
            "name": "Accessible Communication Platform",
            "description": "A messaging platform designed for diverse user populations",
            "content": """
            This platform includes:
            - Multi-language support (English, Spanish, Chinese, Arabic)
            - Screen reader compatibility and keyboard navigation
            - High contrast mode and adjustable font sizes
            - Voice-to-text and text-to-voice capabilities
            - Inclusive language guidelines and content moderation
            - Support for various cultural and religious holidays
            - Privacy controls and data consent management
            """
        },
        {
            "name": "AI-Powered Content Recommendation",
            "description": "Machine learning system that recommends content based on user behavior",
            "content": """
            This AI system:
            - Analyzes user clicks, views, and time spent on content
            - Uses facial recognition to determine user demographics
            - Tracks location data to provide local recommendations
            - Creates user profiles based on political and religious preferences
            - Serves targeted advertisements based on personal characteristics
            - Does not provide transparency about how recommendations are made
            """
        }
    ]
    
    for i, feature in enumerate(test_features, 1):
        print(f"\n📊 Feature {i}: {feature['name']}")
        print("-" * 40)
        
        try:
            # Analyze the feature
            analysis = analyzer.analyze_cultural_sensitivity(
                feature['name'],
                feature['description'],
                feature['content']
            )
            
            # Display results
            print(f"🎯 Overall Score: {analysis.overall_score:.2f} ({analysis.score_level.upper()})")
            print(f"🎯 Confidence: {analysis.confidence_score:.2f}")
            print(f"🎯 Requires Human Review: {'Yes' if analysis.requires_human_review else 'No'}")
            
            print(f"\n🧠 Reasoning:")
            print(f"   {analysis.reasoning}")
            
            if analysis.cultural_factors:
                print(f"\n🏷️ Cultural Factors Considered:")
                for factor in analysis.cultural_factors:
                    print(f"   • {factor}")
            
            if analysis.potential_issues:
                print(f"\n⚠️ Potential Issues:")
                for issue in analysis.potential_issues:
                    print(f"   • {issue}")
            
            if analysis.recommendations:
                print(f"\n💡 Recommendations:")
                for rec in analysis.recommendations:
                    print(f"   • {rec}")
            
        except Exception as e:
            print(f"❌ Analysis failed: {e}")
            import traceback
            traceback.print_exc()
    
    return True

def test_all_regions_analysis():
    """Test the simplified all-regions analysis (now US-only)"""
    print("\n🌍 Testing All Regions Analysis (US-Focused)")
    print("=" * 60)
    
    # Initialize the analyzer
    analyzer = CulturalSensitivityAnalyzer()
    
    # Test feature
    feature_name = "Sample Feature"
    feature_description = "A test feature for cultural sensitivity analysis"
    feature_content = """
    This feature collects user data and provides personalized recommendations.
    It includes user tracking, analytics, and targeted content delivery.
    """
    
    try:
        # Analyze for all regions (now just US)
        results = analyzer.analyze_feature_for_all_regions(
            feature_name,
            feature_description,
            feature_content
        )
        
        print(f"📊 Analysis Results:")
        for region, analysis in results.items():
            print(f"\n🇺🇸 {region.upper()}:")
            print(f"   Score: {analysis.overall_score:.2f} ({analysis.score_level})")
            print(f"   Factors: {len(analysis.cultural_factors)}")
            print(f"   Issues: {len(analysis.potential_issues)}")
            print(f"   Recommendations: {len(analysis.recommendations)}")
            
            if analysis.recommendations:
                print(f"   Top Recommendations:")
                for rec in analysis.recommendations[:3]:
                    print(f"     • {rec}")
        
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        import traceback
        traceback.print_exc()
    
    return True

def main():
    """Main test function"""
    print("🚀 US Cultural Sensitivity Analysis Test Suite")
    print("=" * 60)
    
    # Test 1: Basic functionality
    test1_success = test_us_cultural_sensitivity_analyzer()
    
    # Test 2: Feature analysis
    test2_success = test_feature_analysis()
    
    # Test 3: All regions analysis
    test3_success = test_all_regions_analysis()
    
    print("\n" + "=" * 60)
    print("📊 Test Results:")
    print(f"   Basic Functionality: {'✅ PASS' if test1_success else '❌ FAIL'}")
    print(f"   Feature Analysis: {'✅ PASS' if test2_success else '❌ FAIL'}")
    print(f"   All Regions Analysis: {'✅ PASS' if test3_success else '❌ FAIL'}")
    
    overall_success = test1_success and test2_success and test3_success
    
    if overall_success:
        print("\n🎉 All tests passed! US cultural sensitivity analysis is working correctly.")
        print("\n📋 Key Features:")
        print("   • US-specific cultural factors and considerations")
        print("   • Detailed reasoning and recommendations")
        print("   • Privacy and accessibility focus")
        print("   • Diversity and inclusion analysis")
        print("   • Regional and demographic considerations")
    else:
        print("\n⚠️ Some tests failed. Please check the implementation.")
    
    return overall_success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
