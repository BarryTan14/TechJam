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
    AgentOutput
)

@dataclass
class WorkflowState:
    """State object for the workflow"""
    feature_id: str
    feature_name: str
    feature_description: str
    feature_content: str
    metadata: Dict[str, Any]
    
    # Agent outputs
    feature_analyzer_output: Optional[AgentOutput] = None
    regulation_matcher_output: Optional[AgentOutput] = None
    risk_assessor_output: Optional[AgentOutput] = None
    reasoning_generator_output: Optional[AgentOutput] = None
    quality_assurance_output: Optional[AgentOutput] = None
    
    # Final results
    compliance_flags: List[str] = None
    risk_level: str = "unknown"
    confidence_score: float = 0.0
    requires_human_review: bool = False
    reasoning: str = ""
    recommendations: List[str] = None
    
    # Workflow metadata
    workflow_id: str = ""
    start_time: str = ""
    end_time: str = ""
    total_processing_time: float = 0.0
    
    def __post_init__(self):
        if self.compliance_flags is None:
            self.compliance_flags = []
        if self.recommendations is None:
            self.recommendations = []
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
        self.feature_analyzer = FeatureAnalyzerAgent(self.llm)
        self.regulation_matcher = RegulationMatcherAgent(self.llm)
        self.risk_assessor = RiskAssessorAgent(self.llm)
        self.reasoning_generator = ReasoningGeneratorAgent(self.llm)
        self.quality_assurance = QualityAssuranceAgent(self.llm)
    
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
    
    def feature_analyzer_agent(self, state: WorkflowState) -> WorkflowState:
        """Feature Analyzer Agent - Extracts compliance-relevant information"""
        agent_output = self.feature_analyzer.analyze(
            state.feature_name,
            state.feature_description,
            state.feature_content
        )
        state.feature_analyzer_output = agent_output
        return state
    
    def regulation_matcher_agent(self, state: WorkflowState) -> WorkflowState:
        """Regulation Matcher Agent - Matches features to relevant regulations"""
        feature_analysis = state.feature_analyzer_output.analysis_result
        agent_output = self.regulation_matcher.match_regulations(
            state.feature_name,
            feature_analysis
        )
        state.regulation_matcher_output = agent_output
        return state
    
    def risk_assessor_agent(self, state: WorkflowState) -> WorkflowState:
        """Risk Assessor Agent - Scores compliance risk and flags issues"""
        feature_analysis = state.feature_analyzer_output.analysis_result
        regulation_matching = state.regulation_matcher_output.analysis_result
        agent_output = self.risk_assessor.assess_risk(
            state.feature_name,
            feature_analysis,
            regulation_matching
        )
        state.risk_assessor_output = agent_output
        return state
    
    def reasoning_generator_agent(self, state: WorkflowState) -> WorkflowState:
        """Reasoning Generator Agent - Produces clear justifications"""
        feature_analysis = state.feature_analyzer_output.analysis_result
        regulation_matching = state.regulation_matcher_output.analysis_result
        risk_assessment = state.risk_assessor_output.analysis_result
        agent_output = self.reasoning_generator.generate_reasoning(
            state.feature_name,
            feature_analysis,
            regulation_matching,
            risk_assessment
        )
        state.reasoning_generator_output = agent_output
        return state
    
    def quality_assurance_agent(self, state: WorkflowState) -> WorkflowState:
        """Quality Assurance Agent - Validates and checks consistency"""
        all_outputs = [
            state.feature_analyzer_output,
            state.regulation_matcher_output,
            state.risk_assessor_output,
            state.reasoning_generator_output
        ]
        
        agent_output = self.quality_assurance.validate_results(
            state.feature_name,
            all_outputs
        )
        state.quality_assurance_output = agent_output
        
        # Set final state values
        state.compliance_flags = state.regulation_matcher_output.analysis_result.get("applicable_regulations", [])
        state.risk_level = state.risk_assessor_output.analysis_result.get("overall_risk_level", "unknown")
        state.confidence_score = agent_output.analysis_result.get("confidence_adjustment", 0.8)
        state.requires_human_review = agent_output.analysis_result.get("final_validation") == "requires_review"
        state.reasoning = state.reasoning_generator_output.analysis_result.get("executive_summary", "")
        state.recommendations = agent_output.analysis_result.get("final_recommendations", [])
        state.end_time = datetime.now().isoformat()
        state.total_processing_time = (datetime.now() - datetime.fromisoformat(state.start_time)).total_seconds()
        
        return state
    

    
    def run_workflow(self, feature_data: Dict[str, Any]) -> WorkflowState:
        """Run the complete workflow"""
        print(f"\n🚀 Starting Multi-Agent Workflow for: {feature_data['feature_name']}")
        print("=" * 80)
        
        # Create initial state
        initial_state = WorkflowState(
            feature_id=feature_data['feature_id'],
            feature_name=feature_data['feature_name'],
            feature_description=feature_data['feature_description'],
            feature_content=feature_data['feature_content'],
            metadata=feature_data.get('metadata', {})
        )
        
        # Run agents sequentially
        print("🔄 Running agents sequentially...")
        
        state = self.feature_analyzer_agent(initial_state)
        state = self.regulation_matcher_agent(state)
        state = self.risk_assessor_agent(state)
        state = self.reasoning_generator_agent(state)
        state = self.quality_assurance_agent(state)
        
        # Save results
        self.save_workflow_results(state)
        
        return state
    
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
                "document_info": {
                    "document_id": state.feature_id,
                    "document_name": state.feature_name,
                    "document_description": state.feature_description,
                    "document_content": state.feature_content,
                    "metadata": state.metadata
                },
                "agent_outputs": {
                    "feature_analyzer": asdict(state.feature_analyzer_output) if state.feature_analyzer_output else None,
                    "regulation_matcher": asdict(state.regulation_matcher_output) if state.regulation_matcher_output else None,
                    "risk_assessor": asdict(state.risk_assessor_output) if state.risk_assessor_output else None,
                    "reasoning_generator": asdict(state.reasoning_generator_output) if state.reasoning_generator_output else None,
                    "quality_assurance": asdict(state.quality_assurance_output) if state.quality_assurance_output else None
                },
                "final_results": {
                    "compliance_flags": state.compliance_flags,
                    "risk_level": state.risk_level,
                    "confidence_score": state.confidence_score,
                    "requires_human_review": state.requires_human_review,
                    "reasoning": state.reasoning,
                    "recommendations": state.recommendations
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
    print("🚀 Multi-Agent Geo-Compliance Detection System")
    print("=" * 80)
    
    # Check dependencies
    if not GEMINI_API_KEY:
        print("⚠️  No GEMINI_API_KEY found. System will run in fallback mode.")
        print("💡 Set your API key: GEMINI_API_KEY=your_key_here")
    
    # Create workflow
    workflow = ComplianceWorkflow()
    
    print("\n📋 Document Analysis Mode")
    print("=" * 50)
    print("Enter your document details (or press Enter for sample):")
    
    # Get document details
    doc_name = input("Document Name: ").strip()
    if not doc_name:
        doc_name = "Sample Product Requirements Document"
    
    doc_description = input("Document Description (optional): ").strip()
    if not doc_description:
        doc_description = "Product requirements document for compliance analysis"
    
    print("\n📝 Enter your document content:")
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
    
    document_content = "\n".join(content_lines)
    
    # Create document data
    document_data = {
        "feature_id": f"doc_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "feature_name": doc_name,
        "feature_description": doc_description,
        "feature_content": document_content,
        "metadata": {
            "document_type": "product_requirements",
            "analysis_date": datetime.now().isoformat(),
            "word_count": len(document_content.split())
        }
    }
    
    # Run workflow
    print(f"\n📋 Analyzing document: {document_data['feature_name']}")
    print(f"📝 Description: {document_data['feature_description']}")
    print(f"📄 Content length: {len(document_content)} characters")
    
    final_state = workflow.run_workflow(document_data)
    
    # Display final results
    print(f"\n🎉 Workflow Analysis Complete!")
    print("=" * 80)
    print(f"🔴 Risk Level: {final_state.risk_level.upper()}")
    print(f"📈 Confidence: {final_state.confidence_score:.1%}")
    print(f"👤 Human Review: {'Required' if final_state.requires_human_review else 'Not Required'}")
    print(f"🏛️  Compliance Flags: {', '.join(final_state.compliance_flags) if final_state.compliance_flags else 'None'}")
    print(f"💭 Reasoning: {final_state.reasoning}")
    print(f"💡 Recommendations:")
    for rec in final_state.recommendations:
        print(f"   • {rec}")
    
    print(f"\n📊 Total Processing Time: {final_state.total_processing_time:.2f}s")
    print(f"📁 Results saved to: output/output_{final_state.workflow_id}.json")

if __name__ == "__main__":
    main()
