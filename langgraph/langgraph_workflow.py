import os
import json
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
from dotenv import load_dotenv

# Load .env file if it exists
load_dotenv()

# Get API key from environment (now loaded from .env)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Import agents
from agents import (
    FeatureAnalyzerAgent,
    RegulationMatcherAgent,
    RiskAssessorAgent,
    ReasoningGeneratorAgent,
    QualityAssuranceAgent,
    PRDParserAgent,
    USStateComplianceAgent,
    AgentOutput,
    ExtractedFeature,
    FeatureComplianceResult,
    PRDAnalysisResult
)

@dataclass
class WorkflowState:
    """State object for the workflow"""
    prd_id: str
    prd_name: str
    prd_description: str
    prd_content: str
    metadata: Dict[str, Any]
    
    # PRD Parser output
    prd_parser_output: Optional[AgentOutput] = None
    extracted_features: List[ExtractedFeature] = None
    
    # Feature analysis results
    feature_compliance_results: List[FeatureComplianceResult] = None
    
    # Final results
    overall_risk_level: str = "unknown"
    overall_confidence_score: float = 0.0
    critical_compliance_issues: List[str] = None
    summary_recommendations: List[str] = None
    
    # Workflow metadata
    workflow_id: str = ""
    start_time: str = ""
    end_time: str = ""
    total_processing_time: float = 0.0
    
    def __post_init__(self):
        if self.extracted_features is None:
            self.extracted_features = []
        if self.feature_compliance_results is None:
            self.feature_compliance_results = []
        if self.critical_compliance_issues is None:
            self.critical_compliance_issues = []
        if self.summary_recommendations is None:
            self.summary_recommendations = []
        if not self.workflow_id:
            self.workflow_id = f"workflow_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        if not self.start_time:
            self.start_time = datetime.now().isoformat()

class ComplianceWorkflow:
    """Main workflow orchestrator"""
    
    def __init__(self):
        self.llm = None
        self.setup_llm()
        
        # Initialize agents
        self.prd_parser = PRDParserAgent(self.llm)
        self.feature_analyzer = FeatureAnalyzerAgent(self.llm)
        self.regulation_matcher = RegulationMatcherAgent(self.llm)
        self.risk_assessor = RiskAssessorAgent(self.llm)
        self.reasoning_generator = ReasoningGeneratorAgent(self.llm)
        self.quality_assurance = QualityAssuranceAgent(self.llm)
        self.us_state_compliance = USStateComplianceAgent(self.llm)
    
    def setup_llm(self):
        """Setup LLM with fallback models"""
        if not GEMINI_API_KEY:
            print("⚠️  No GEMINI_API_KEY found. System will run in fallback mode.")
            return
        
        try:
            import google.generativeai as genai
            genai.configure(api_key=GEMINI_API_KEY)
            
            # Try different models in order of preference
            models_to_try = [
                'gemini-1.5-pro',
                'gemini-1.5-flash', 
                'gemini-pro',
                'gemini-1.0-pro'
            ]
            
            for model_name in models_to_try:
                try:
                    print(f"🔄 Trying model: {model_name}")
                    self.llm = genai.GenerativeModel(model_name)
                    
                    # Test the model with a simple prompt
                    test_response = self.llm.generate_content("Hello")
                    if test_response and test_response.text:
                        print(f"✅ Gemini LLM configured successfully with model: {model_name}")
                        return
                    else:
                        print(f"⚠️  Model {model_name} returned empty response")
                        
                except Exception as model_error:
                    print(f"⚠️  Model {model_name} failed: {model_error}")
                    continue
            
            print("❌ All Gemini models failed. System will run in fallback mode.")
            self.llm = None
            
        except Exception as e:
            print(f"❌ Gemini setup failed: {e}")
            print("💡 Check your API key and internet connection")
            self.llm = None
    
    def prd_parser_agent(self, state: WorkflowState) -> WorkflowState:
        """PRD Parser Agent - Extracts features from PRD document"""
        agent_output = self.prd_parser.parse_prd(
            state.prd_name,
            state.prd_description,
            state.prd_content
        )
        state.prd_parser_output = agent_output
        
        # Convert extracted features to ExtractedFeature objects
        extracted_features_data = agent_output.analysis_result.get("extracted_features", [])
        state.extracted_features = []
        
        for feature_data in extracted_features_data:
            feature = ExtractedFeature(
                feature_id=feature_data.get("feature_id", ""),
                feature_name=feature_data.get("feature_name", ""),
                feature_description=feature_data.get("feature_description", ""),
                feature_content=feature_data.get("feature_content", ""),
                section=feature_data.get("section", ""),
                priority=feature_data.get("priority", "Medium"),
                complexity=feature_data.get("complexity", "Medium"),
                data_types=feature_data.get("data_types", []),
                user_impact=feature_data.get("user_impact", ""),
                technical_requirements=feature_data.get("technical_requirements", []),
                compliance_considerations=feature_data.get("compliance_considerations", [])
            )
            state.extracted_features.append(feature)
        
        return state
    
    def analyze_single_feature(self, feature: ExtractedFeature) -> FeatureComplianceResult:
        """Analyze a single feature through all agents - optimized"""
        start_time = datetime.now()
        agent_outputs = {}
        
        try:
            # Feature Analyzer
            feature_analyzer_output = self.feature_analyzer.analyze(
                feature.feature_name,
                feature.feature_description,
                feature.feature_content
            )
            agent_outputs["feature_analyzer"] = feature_analyzer_output
            
            # Regulation Matcher
            feature_analysis = feature_analyzer_output.analysis_result
            regulation_matcher_output = self.regulation_matcher.match_regulations(
                feature.feature_name,
                feature_analysis
            )
            agent_outputs["regulation_matcher"] = regulation_matcher_output
            
            # Risk Assessor
            regulation_matching = regulation_matcher_output.analysis_result
            risk_assessor_output = self.risk_assessor.assess_risk(
                feature.feature_name,
                feature_analysis,
                regulation_matching
            )
            agent_outputs["risk_assessor"] = risk_assessor_output
            
            # Reasoning Generator
            risk_assessment = risk_assessor_output.analysis_result
            reasoning_generator_output = self.reasoning_generator.generate_reasoning(
                feature.feature_name,
                feature_analysis,
                regulation_matching,
                risk_assessment
            )
            agent_outputs["reasoning_generator"] = reasoning_generator_output
            
            # Quality Assurance
            all_outputs = [
                feature_analyzer_output,
                regulation_matcher_output,
                risk_assessor_output,
                reasoning_generator_output
            ]
            quality_assurance_output = self.quality_assurance.validate_results(
                feature.feature_name,
                all_outputs
            )
            agent_outputs["quality_assurance"] = quality_assurance_output
            
            # US State Compliance
            us_state_compliance_output = self.us_state_compliance.analyze_us_state_compliance(
                feature.feature_name,
                feature_analysis,
                regulation_matching,
                risk_assessment
            )
            agent_outputs["us_state_compliance"] = us_state_compliance_output
            
            # Extract final results
            compliance_flags = regulation_matcher_output.analysis_result.get("applicable_regulations", [])
            risk_level = risk_assessor_output.analysis_result.get("overall_risk_level", "unknown")
            confidence_score = quality_assurance_output.analysis_result.get("confidence_adjustment", 0.8)
            requires_human_review = quality_assurance_output.analysis_result.get("final_validation") == "requires_review"
            reasoning = reasoning_generator_output.analysis_result.get("executive_summary", "")
            recommendations = quality_assurance_output.analysis_result.get("final_recommendations", [])
            
            # US State compliance results
            us_state_analysis = us_state_compliance_output.analysis_result
            non_compliant_states = us_state_analysis.get("non_compliant_states", [])
            
        except Exception as e:
            print(f"⚠️  Error in feature analysis: {e}")
            # Create fallback results
            compliance_flags = ["GDPR", "CCPA"]
            risk_level = "medium"
            confidence_score = 0.7
            requires_human_review = True
            reasoning = f"Analysis incomplete due to error: {str(e)}"
            recommendations = ["Review feature manually", "Check system configuration"]
            non_compliant_states = ["California", "Virginia"]
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        return FeatureComplianceResult(
            feature=feature,
            agent_outputs=agent_outputs,
            compliance_flags=compliance_flags,
            risk_level=risk_level,
            confidence_score=confidence_score,
            requires_human_review=requires_human_review,
            reasoning=reasoning,
            recommendations=recommendations,
            us_state_compliance=[],
            non_compliant_states=non_compliant_states,
            processing_time=processing_time,
            timestamp=datetime.now().isoformat()
        )
    
    def run_workflow(self, prd_data: Dict[str, Any]) -> WorkflowState:
        """Run the complete workflow"""
        print(f"\n🚀 Starting Multi-Agent PRD Analysis Workflow for: {prd_data['prd_name']}")
        print("=" * 80)
        
        # Create initial state
        initial_state = WorkflowState(
            prd_id=prd_data['prd_id'],
            prd_name=prd_data['prd_name'],
            prd_description=prd_data['prd_description'],
            prd_content=prd_data['prd_content'],
            metadata=prd_data.get('metadata', {})
        )
        
        # Step 1: Parse PRD and extract features
        print("📋 Step 1: Parsing PRD and extracting features...")
        state = self.prd_parser_agent(initial_state)
        
        print(f"✅ Extracted {len(state.extracted_features)} features from PRD")
        
        # Step 2: Analyze each feature
        print(f"\n🔍 Step 2: Analyzing {len(state.extracted_features)} features...")
        for i, feature in enumerate(state.extracted_features, 1):
            print(f"\n📊 Feature {i}/{len(state.extracted_features)}: {feature.feature_name}")
            feature_result = self.analyze_single_feature(feature)
            state.feature_compliance_results.append(feature_result)
        
        # Step 3: Generate overall results
        print(f"\n📈 Step 3: Generating overall results...")
        self._generate_overall_results(state)
        
        # Save results
        self.save_workflow_results(state)
        
        return state
    
    def _generate_overall_results(self, state: WorkflowState):
        """Generate overall results from all feature analyses"""
        
        # Calculate overall risk level
        risk_levels = [result.risk_level for result in state.feature_compliance_results]
        if "critical" in risk_levels:
            overall_risk = "critical"
        elif "high" in risk_levels:
            overall_risk = "high"
        elif "medium" in risk_levels:
            overall_risk = "medium"
        else:
            overall_risk = "low"
        
        state.overall_risk_level = overall_risk
        
        # Calculate overall confidence
        total_confidence = sum(result.confidence_score for result in state.feature_compliance_results)
        state.overall_confidence_score = total_confidence / len(state.feature_compliance_results) if state.feature_compliance_results else 0.0
        
        # Collect critical issues
        critical_issues = []
        for result in state.feature_compliance_results:
            if result.risk_level in ["high", "critical"]:
                critical_issues.append(f"{result.feature.feature_name}: {result.risk_level} risk")
        
        state.critical_compliance_issues = critical_issues
        
        # Collect summary recommendations
        all_recommendations = []
        for result in state.feature_compliance_results:
            all_recommendations.extend(result.recommendations)
        
        # Remove duplicates and limit
        unique_recommendations = list(set(all_recommendations))
        state.summary_recommendations = unique_recommendations[:10]  # Top 10 recommendations
        
        state.end_time = datetime.now().isoformat()
        state.total_processing_time = (datetime.now() - datetime.fromisoformat(state.start_time)).total_seconds()
    
    def save_workflow_results(self, state: WorkflowState):
        """Save workflow results to output.json"""
        try:
            # Convert state to dictionary
            output_data = {
                "workflow_metadata": {
                    "workflow_id": state.workflow_id,
                    "start_time": state.start_time,
                    "end_time": state.end_time,
                    "total_processing_time": state.total_processing_time
                },
                "prd_info": {
                    "prd_id": state.prd_id,
                    "prd_name": state.prd_name,
                    "prd_description": state.prd_description,
                    "prd_content": state.prd_content,
                    "metadata": state.metadata
                },
                "prd_parser_output": asdict(state.prd_parser_output) if state.prd_parser_output else None,
                "extracted_features": [asdict(feature) for feature in state.extracted_features],
                "feature_compliance_results": [
                    {
                        "feature": asdict(result.feature),
                        "compliance_flags": result.compliance_flags,
                        "risk_level": result.risk_level,
                        "confidence_score": result.confidence_score,
                        "requires_human_review": result.requires_human_review,
                        "reasoning": result.reasoning,
                        "recommendations": result.recommendations,
                        "non_compliant_states": result.non_compliant_states,
                        "processing_time": result.processing_time,
                        "timestamp": result.timestamp
                    }
                    for result in state.feature_compliance_results
                ],
                "overall_results": {
                    "total_features": len(state.extracted_features),
                    "overall_risk_level": state.overall_risk_level,
                    "overall_confidence_score": state.overall_confidence_score,
                    "critical_compliance_issues": state.critical_compliance_issues,
                    "summary_recommendations": state.summary_recommendations
                }
            }
            
            # Create output directory if it doesn't exist
            os.makedirs("output", exist_ok=True)
            
            # Save to file in output folder
            output_file = f"output/output_{state.workflow_id}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Workflow results saved to: {output_file}")
            
        except Exception as e:
            print(f"❌ Failed to save results: {e}")

def main():
    """Main function to run the workflow"""
    print("🚀 Multi-Agent PRD Geo-Compliance Detection System")
    print("=" * 80)
    
    # Check dependencies
    if not GEMINI_API_KEY:
        print("⚠️  No GEMINI_API_KEY found. System will run in fallback mode.")
        print("💡 Set your API key: GEMINI_API_KEY=your_key_here")
    
    # Create workflow
    workflow = ComplianceWorkflow()
    
    print("\n📋 PRD Analysis Mode")
    print("=" * 50)
    print("Enter your PRD details (or press Enter for sample):")
    
    # Get PRD details
    prd_name = input("PRD Name: ").strip()
    if not prd_name:
        prd_name = "Sample Product Requirements Document"
    
    prd_description = input("PRD Description (optional): ").strip()
    if not prd_description:
        prd_description = "Product requirements document for compliance analysis"
    
    print("\n📝 Enter your PRD content:")
    print("(Press Enter twice to finish, or type 'sample' for demo content)")
    
    content_lines = []
    while True:
        line = input()
        if line.lower() == "sample":
            # Use sample content
            content_lines = [
                "Product Requirements Document: User Behavior Tracking System",
                "",
                "1. Overview",
                "This feature implements comprehensive user behavior tracking across our platform.",
                "It collects personal data including user preferences, browsing history, location information,",
                "and interaction patterns for analytics and personalized recommendations.",
                "",
                "2. Data Collection",
                "- User preferences and settings",
                "- Browsing history and page interactions",
                "- Location data from GPS and IP addresses",
                "- Device information and usage patterns",
                "- Social media interactions and sharing behavior",
                "",
                "3. Data Processing",
                "- Machine learning algorithms for pattern recognition",
                "- Real-time analytics and insights generation",
                "- Personalized content recommendations",
                "- Targeted advertising optimization",
                "",
                "4. Data Storage and Sharing",
                "- Cloud databases for data storage",
                "- Third-party analytics providers (Google Analytics, Facebook Pixel)",
                "- Cross-border data transfers for global operations",
                "- Data retention period: 2 years",
                "",
                "5. User Controls",
                "- Opt-out mechanism through account settings",
                "- Data access and deletion requests",
                "- Consent management for data collection",
                "- Privacy policy updates and notifications"
            ]
            break
        elif line == "":
            if content_lines:  # If we have content and user pressed Enter
                break
            else:  # If no content yet, continue
                continue
        else:
            content_lines.append(line)
    
    prd_content = "\n".join(content_lines)
    
    # Create PRD data
    prd_data = {
        "prd_id": f"prd_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "prd_name": prd_name,
        "prd_description": prd_description,
        "prd_content": prd_content,
        "metadata": {
            "document_type": "product_requirements",
            "analysis_date": datetime.now().isoformat(),
            "word_count": len(prd_content.split())
        }
    }
    
    # Run workflow
    print(f"\n📋 Analyzing PRD: {prd_data['prd_name']}")
    print(f"📝 Description: {prd_data['prd_description']}")
    print(f"📄 Content length: {len(prd_content)} characters")
    
    final_state = workflow.run_workflow(prd_data)
    
    # Display final results
    print(f"\n🎉 PRD Analysis Complete!")
    print("=" * 80)
    print(f"📊 Total Features Analyzed: {len(final_state.extracted_features)}")
    print(f"🔴 Overall Risk Level: {final_state.overall_risk_level.upper()}")
    print(f"📈 Overall Confidence: {final_state.overall_confidence_score:.1%}")
    print(f"🚨 Critical Issues: {len(final_state.critical_compliance_issues)}")
    
    print(f"\n📋 Feature Summary:")
    for i, result in enumerate(final_state.feature_compliance_results, 1):
        print(f"  {i}. {result.feature.feature_name}")
        print(f"     Risk: {result.risk_level.upper()}")
        print(f"     Non-compliant states: {len(result.non_compliant_states)}")
        if result.non_compliant_states:
            print(f"     States: {', '.join(result.non_compliant_states)}")
        print()
    
    print(f"💡 Top Recommendations:")
    for rec in final_state.summary_recommendations[:5]:
        print(f"   • {rec}")
    
    print(f"\n📊 Total Processing Time: {final_state.total_processing_time:.2f}s")
    print(f"📁 Results saved to: output/output_{final_state.workflow_id}.json")

if __name__ == "__main__":
    main()
