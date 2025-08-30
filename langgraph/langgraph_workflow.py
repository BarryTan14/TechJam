import os
import json
import logging
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Helper function for Singapore timezone
def get_singapore_time():
    """Get current time in Singapore timezone (UTC+8)"""
    singapore_tz = timezone(timedelta(hours=8))
    return datetime.now(singapore_tz)

# Load environment variables from .env file
from dotenv import load_dotenv

# Load .env file if it exists
load_dotenv()

# Get API key from environment (now loaded from .env)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Import agents
from agents import (
    PRDParserAgent,
    FeatureAnalyzerAgent,
    RegulationMatcherAgent,
    RiskAssessorAgent,
    ReasoningGeneratorAgent,
    QualityAssuranceAgent,
    USStateComplianceAgent,
    ExecutiveReportGenerator,
    NonCompliantStatesAnalyzerAgent,
    OptimizedStateAnalyzer,
    state_regulations_cache,
    AgentOutput,
    ExtractedFeature,
    FeatureComplianceResult,
    PRDAnalysisResult,
    USStateCompliance,
    StateComplianceScore,
    BatchAnalysisResult
)
from agents.executive_report_manager import ExecutiveReportManager
from agents.cultural_sensitivity_analyzer import CulturalSensitivityAnalyzer

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
    
    # Feature analysis results (for backward compatibility)
    feature_compliance_results: List[FeatureComplianceResult] = None
    
    # State-centric analysis results (new)
    state_analysis_results: Dict[str, Dict[str, Any]] = None
    
    # Final results
    overall_risk_level: str = "unknown"
    overall_confidence_score: float = 0.0
    critical_compliance_issues: List[str] = None
    summary_recommendations: List[str] = None
    non_compliant_states_dict: Dict[str, Dict[str, Any]] = None
    
    # Executive report
    executive_report: Optional[Dict[str, Any]] = None
    
    # Cultural sensitivity analysis
    cultural_sensitivity_analysis: Optional[Dict[str, Any]] = None
    
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
            self.workflow_id = f"workflow_{get_singapore_time().strftime('%Y%m%d_%H%M%S')}"
        if not self.start_time:
            self.start_time = get_singapore_time().isoformat()

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
        self.non_compliant_states_analyzer = NonCompliantStatesAnalyzerAgent(self.llm)
        
        # Initialize optimized state analyzer
        self.optimized_state_analyzer = OptimizedStateAnalyzer(self.llm)
        self.state_cache = state_regulations_cache
        
        # Initialize executive report generator
        self.executive_report_generator = ExecutiveReportGenerator(self.llm)
        
        # Initialize executive report manager for MongoDB
        self.executive_report_manager = ExecutiveReportManager()
        
        # Initialize cultural sensitivity analyzer
        self.cultural_sensitivity_analyzer = CulturalSensitivityAnalyzer(self.llm)
    
    def setup_llm(self):
        """Setup LLM with fallback models"""
        if not GEMINI_API_KEY:
            print("⚠️  No GEMINI_API_KEY found. System will not be able to run.")
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
            
            print("❌ All Gemini models failed. System will not be able to run.")
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
        start_time = get_singapore_time()
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
            
            # Cultural Sensitivity Analysis
            print(f"🌍 Analyzing cultural sensitivity for feature: {feature.feature_name}")
            cultural_sensitivity_scores = self.cultural_sensitivity_analyzer.analyze_feature_for_all_regions(
                feature.feature_name,
                feature.feature_description,
                feature.feature_content
            )
            agent_outputs["cultural_sensitivity_analyzer"] = {
                "scores": cultural_sensitivity_scores,
                "timestamp": datetime.now().isoformat()
            }
            
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
            
            # Convert US state compliance data to USStateCompliance objects
            us_state_compliance_list = []
            state_compliance_scores_dict = {}
            state_compliance_data = us_state_analysis.get("state_compliance", [])
            for state_data in state_compliance_data:
                state_compliance = USStateCompliance(
                    state_name=state_data.get("state_name", ""),
                    state_code=state_data.get("state_code", ""),
                    is_compliant=state_data.get("is_compliant", True),
                    non_compliant_regulations=state_data.get("non_compliant_regulations", []),
                    risk_level=state_data.get("risk_level", "Low"),
                    required_actions=state_data.get("required_actions", []),
                    notes=state_data.get("notes", "")
                )
                us_state_compliance_list.append(state_compliance)
                
                # Create StateComplianceScore object for the new dictionary
                # Calculate compliance score based on risk score (0.0 to 1.0)
                risk_score = state_data.get("risk_score", 0.5)
                # Convert risk score to compliance score: 1.0 = fully compliant, 0.0 = non-compliant
                compliance_score = max(0.0, min(1.0, 1.0 - risk_score))
                
                # Determine risk level based on compliance score (only low or high)
                if compliance_score >= 0.6:
                    risk_level = "low"
                else:
                    risk_level = "high"
                
                # Get reasoning from state data
                reasoning = state_data.get("reasoning", "")
                if not reasoning:
                    if state_data.get("is_compliant", True):
                        reasoning = f"Feature complies with {state_data.get('state_name', '')}'s data protection requirements."
                    else:
                        regulations = state_data.get("non_compliant_regulations", [])
                        reasoning = f"Feature is non-compliant with {state_data.get('state_name', '')}'s regulations: {', '.join(regulations)}."
                
                state_compliance_score = StateComplianceScore(
                    state_code=state_data.get("state_code", ""),
                    state_name=state_data.get("state_name", ""),
                    compliance_score=compliance_score,
                    risk_level=risk_level,
                    reasoning=reasoning,
                    non_compliant_regulations=state_data.get("non_compliant_regulations", []),
                    required_actions=state_data.get("required_actions", []),
                    notes=state_data.get("notes", "")
                )
                state_compliance_scores_dict[state_data.get("state_code", "")] = state_compliance_score
            
        except Exception as e:
            print(f"⚠️  Error in feature analysis: {e}")
            raise Exception(f"Feature analysis failed: {e}")
        
        processing_time = (get_singapore_time() - start_time).total_seconds()
        
        return FeatureComplianceResult(
            feature=feature,
            agent_outputs=agent_outputs,
            compliance_flags=compliance_flags,
            risk_level=risk_level,
            confidence_score=confidence_score,
            requires_human_review=requires_human_review,
            reasoning=reasoning,
            recommendations=recommendations,
            us_state_compliance=us_state_compliance_list,
            non_compliant_states=non_compliant_states,
            state_compliance_scores=state_compliance_scores_dict,
            cultural_sensitivity_scores=cultural_sensitivity_scores,
            processing_time=processing_time,
            timestamp=get_singapore_time().isoformat()
        )
    
    def run_workflow(self, prd_data: Dict[str, Any]) -> WorkflowState:
        """Run the complete workflow with state-centric analysis"""
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
        
        # Check if any features were detected
        if not state.extracted_features or len(state.extracted_features) == 0:
            error_msg = f"No features detected in PRD content. The uploaded content does not contain any identifiable software features that require compliance analysis."
            print(f"❌ {error_msg}")
            raise ValueError(error_msg)
        
        # Step 2: Analyze each state against all features
        print(f"\n🇺🇸 Step 2: Analyzing each state against {len(state.extracted_features)} features...")
        state_analysis_results = self.analyze_states_against_features(state.extracted_features)
        
        # Step 3: Convert state-centric results to feature-centric format for backward compatibility
        print(f"\n🔄 Step 3: Converting results to feature-centric format...")
        state.feature_compliance_results = self.convert_state_results_to_feature_results(
            state.extracted_features, state_analysis_results
        )
        
        # Step 4: Generate overall results
        print(f"\n📈 Step 4: Generating overall results...")
        self._generate_overall_results(state, state_analysis_results)
        
        # Step 5: Generate cultural sensitivity analysis
        print(f"\n🌍 Step 5: Generating cultural sensitivity analysis...")
        cultural_analysis = self._generate_cultural_sensitivity_analysis(state)
        state.cultural_sensitivity_analysis = cultural_analysis
        print(f"✅ Cultural sensitivity analysis generated")
        
        # Step 6: Generate executive report
        print(f"\n📊 Step 6: Generating executive report...")
        executive_report = self.executive_report_generator.generate_executive_report(state)
        state.executive_report = {
            "report_id": executive_report.report_id,
            "prd_name": executive_report.prd_name,
            "generated_at": executive_report.generated_at,
            "executive_summary": executive_report.executive_summary,
            "key_findings": executive_report.key_findings,
            "risk_assessment": executive_report.risk_assessment,
            "compliance_overview": executive_report.compliance_overview,
            "recommendations": executive_report.recommendations,
            "next_steps": executive_report.next_steps
        }
        
        print(f"✅ Executive report generated: {executive_report.report_id}")
        
        # Store both executive report and cultural sensitivity analysis in MongoDB
        print(f"💾 Storing workflow results in MongoDB...")
        storage_success = self.executive_report_manager.store_workflow_results(
            state.executive_report,
            state.cultural_sensitivity_analysis,
            state.prd_id,
            state.workflow_id
        )
        
        if storage_success:
            print(f"✅ Workflow results stored in MongoDB successfully")
        else:
            print(f"⚠️ Failed to store workflow results in MongoDB")
        
        # Save results
        self.save_workflow_results(state, state_analysis_results)
        
        return state
    
    def _generate_overall_results(self, state: WorkflowState, state_analysis_results: Dict[str, Dict[str, Any]]):
        """Generate overall results from state-centric analysis"""
        
        # Store state analysis results
        state.state_analysis_results = state_analysis_results
        
        # Calculate overall risk level from state analysis
        if state_analysis_results:
            state_risk_levels = [state_data.get("overall_risk_level", "low") for state_data in state_analysis_results.values()]
            if "high" in state_risk_levels:
                overall_risk = "high"
            elif "medium" in state_risk_levels:
                overall_risk = "high"
            else:
                overall_risk = "low"
        else:
            # Fallback to feature-based calculation
            risk_levels = [result.risk_level for result in state.feature_compliance_results]
            if "critical" in risk_levels:
                overall_risk = "critical"
            elif "high" in risk_levels:
                overall_risk = "high"
            elif "medium" in risk_levels:
                overall_risk = "high"
            else:
                overall_risk = "low"
        
        state.overall_risk_level = overall_risk
        
        # Calculate overall confidence
        if state_analysis_results:
            # Calculate from state analysis
            state_risk_scores = [state_data.get("overall_risk_score", 0.5) for state_data in state_analysis_results.values()]
            avg_risk_score = sum(state_risk_scores) / len(state_risk_scores) if state_risk_scores else 0.5
            state.overall_confidence_score = 1.0 - avg_risk_score  # Convert risk to confidence
        else:
            # Fallback to feature-based calculation
            total_confidence = sum(result.confidence_score for result in state.feature_compliance_results)
            state.overall_confidence_score = total_confidence / len(state.feature_compliance_results) if state.feature_compliance_results else 0.0
        
        # Collect critical issues from state analysis
        critical_issues = []
        if state_analysis_results:
            for state_code, state_data in state_analysis_results.items():
                if state_data.get("overall_risk_level") == "high":
                    non_compliant_count = state_data.get("non_compliant_features", 0)
                    critical_issues.append(f"{state_data.get('state_name', state_code)}: {non_compliant_count} non-compliant features")
        else:
            # Collect critical issues from feature compliance results
            for result in state.feature_compliance_results:
                if result.risk_level in ["high", "critical"]:
                    critical_issues.append(f"{result.feature.feature_name}: {result.risk_level} risk")
        
        state.critical_compliance_issues = critical_issues
        
        # Collect summary recommendations from state analysis
        all_recommendations = []
        if state_analysis_results:
            for state_code, state_data in state_analysis_results.items():
                for feature_data in state_data.get("features", []):
                    all_recommendations.extend(feature_data.get("required_actions", []))
        else:
            # Collect recommendations from feature compliance results
            for result in state.feature_compliance_results:
                all_recommendations.extend(result.recommendations)
        
        # Remove duplicates and limit
        unique_recommendations = list(set(all_recommendations))
        state.summary_recommendations = unique_recommendations[:10]  # Top 10 recommendations
        
        # Generate non-compliant states dictionary from state analysis
        if state_analysis_results:
            state.non_compliant_states_dict = {}
            for state_code, state_data in state_analysis_results.items():
                if state_data.get("non_compliant_features", 0) > 0:
                    state.non_compliant_states_dict[state_code] = {
                        "state_name": state_data.get("state_name", ""),
                        "risk_score": state_data.get("overall_risk_score", 0.5),
                        "risk_level": state_data.get("overall_risk_level", "low"),
                        "non_compliant_features": state_data.get("non_compliant_features", 0),
                        "compliance_rate": state_data.get("compliance_rate", 0.0),
                        "features": state_data.get("features", [])
                    }
        else:
            # Use non-compliant states analyzer
            non_compliant_states_analysis = self.non_compliant_states_analyzer.analyze_non_compliant_states(state.feature_compliance_results)
            state.non_compliant_states_dict = non_compliant_states_analysis.analysis_result.get("non_compliant_states_dict", {})
        
        state.end_time = get_singapore_time().isoformat()
        state.total_processing_time = (get_singapore_time() - datetime.fromisoformat(state.start_time)).total_seconds()
    
    def _generate_cultural_sensitivity_analysis(self, state: WorkflowState) -> Dict[str, Any]:
        """Generate overall cultural sensitivity analysis from feature results"""
        
        if not state.feature_compliance_results:
            return {
                "overall_cultural_sensitivity": "No features analyzed",
                "regional_scores": {},
                "key_cultural_issues": [],
                "recommendations": [],
                "requires_human_review": True
            }
        
        # Aggregate cultural sensitivity scores across all features and regions
        regional_scores = {}
        all_cultural_issues = []
        all_recommendations = []
        
        # Initialize regional scores (now US-focused)
        regions = ["united_states"]
        for region in regions:
            regional_scores[region] = {
                "average_score": 0.0,
                "score_level": "medium",
                "total_features": 0,
                "high_sensitivity_features": 0,
                "medium_sensitivity_features": 0,
                "low_sensitivity_features": 0,
                "cultural_issues": [],
                "recommendations": []
            }
        
        # Aggregate scores from all features (US-focused)
        for result in state.feature_compliance_results:
            if hasattr(result, 'cultural_sensitivity_scores') and result.cultural_sensitivity_scores:
                for region, score in result.cultural_sensitivity_scores.items():
                    if region in regional_scores:
                        regional_scores[region]["total_features"] += 1
                        regional_scores[region]["average_score"] += score.overall_score
                        
                        # Count by sensitivity level
                        if score.score_level == "high":
                            regional_scores[region]["high_sensitivity_features"] += 1
                        elif score.score_level == "medium":
                            regional_scores[region]["medium_sensitivity_features"] += 1
                        else:
                            regional_scores[region]["low_sensitivity_features"] += 1
                        
                        # Collect issues and recommendations
                        regional_scores[region]["cultural_issues"].extend(score.potential_issues)
                        regional_scores[region]["recommendations"].extend(score.recommendations)
                        
                        all_cultural_issues.extend(score.potential_issues)
                        all_recommendations.extend(score.recommendations)
        
        # Calculate averages and determine overall levels
        overall_cultural_sensitivity = "medium"
        total_global_score = 0.0
        total_features = 0
        
        for region, data in regional_scores.items():
            if data["total_features"] > 0:
                data["average_score"] /= data["total_features"]
                
                # Determine regional level
                if data["average_score"] >= 0.7:
                    data["score_level"] = "high"
                elif data["average_score"] >= 0.4:
                    data["score_level"] = "medium"
                else:
                    data["score_level"] = "low"
                
                total_global_score += data["average_score"]
                total_features += 1
        
        # Calculate overall cultural sensitivity
        if total_features > 0:
            overall_average = total_global_score / total_features
            if overall_average >= 0.7:
                overall_cultural_sensitivity = "high"
            elif overall_average >= 0.4:
                overall_cultural_sensitivity = "medium"
            else:
                overall_cultural_sensitivity = "low"
        
        # Remove duplicates from issues and recommendations
        unique_issues = list(set(all_cultural_issues))
        unique_recommendations = list(set(all_recommendations))
        
        return {
            "overall_cultural_sensitivity": overall_cultural_sensitivity,
            "overall_average_score": total_global_score / total_features if total_features > 0 else 0.0,
            "regional_scores": regional_scores,
            "key_cultural_issues": unique_issues[:10],  # Top 10 issues
            "recommendations": unique_recommendations[:10],  # Top 10 recommendations
            "total_features_analyzed": len(state.feature_compliance_results),
            "regions_analyzed": len([r for r in regional_scores.values() if r["total_features"] > 0]),
            "requires_human_review": any(
                any(score.requires_human_review for score in result.cultural_sensitivity_scores.values())
                for result in state.feature_compliance_results
                if hasattr(result, 'cultural_sensitivity_scores') and result.cultural_sensitivity_scores
            )
        }
    
    def save_workflow_results(self, state: WorkflowState, state_analysis_results: Dict[str, Dict[str, Any]]):
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
                        "agent_outputs": {name: asdict(output) for name, output in result.agent_outputs.items()},
                        "compliance_flags": result.compliance_flags,
                        "risk_level": result.risk_level,
                        "confidence_score": result.confidence_score,
                        "requires_human_review": result.requires_human_review,
                        "reasoning": result.reasoning,
                        "recommendations": result.recommendations,
                        "non_compliant_states": result.non_compliant_states,
                        "us_state_compliance": [asdict(compliance) for compliance in result.us_state_compliance],
                        "state_compliance_scores": {
                            state_code: asdict(score_data) 
                            for state_code, score_data in result.state_compliance_scores.items()
                        },
                        "cultural_sensitivity_scores": {
                            region: asdict(score_data) 
                            for region, score_data in result.cultural_sensitivity_scores.items()
                        },
                        "processing_time": result.processing_time,
                        "timestamp": result.timestamp
                    }
                    for result in state.feature_compliance_results
                ],
                "state_analysis_results": state_analysis_results,
                "overall_results": {
                    "total_features": len(state.extracted_features),
                    "overall_risk_level": state.overall_risk_level,
                    "overall_confidence_score": state.overall_confidence_score,
                    "critical_compliance_issues": state.critical_compliance_issues,
                    "summary_recommendations": state.summary_recommendations,
                    "non_compliant_states_dict": state.non_compliant_states_dict
                },
                "cultural_sensitivity_analysis": state.cultural_sensitivity_analysis,
                "executive_report": state.executive_report
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
    
    def analyze_states_against_features(self, features: List[ExtractedFeature]) -> Dict[str, Dict[str, Any]]:
        """
        Analyze each state against all features - OPTIMIZED VERSION
        
        Args:
            features: List of extracted features
            
        Returns:
            Dictionary with state codes as keys and analysis results as values
        """
        print(f"\n🚀 Using Optimized State Analyzer for {len(features)} features across all states...")
        
        # Use the optimized state analyzer
        batch_result = self.optimized_state_analyzer.analyze_features_against_states(features)
        
        # Convert BatchAnalysisResult to the expected format
        state_analysis = {}
        
        for state_code, state_results in batch_result.state_results.items():
            if not state_results:
                continue
            
            # Calculate overall state risk
            state_risk_scores = [result.risk_score for result in state_results]
            avg_risk_score = sum(state_risk_scores) / len(state_risk_scores) if state_risk_scores else 0.5
            
            # Determine overall state risk level (only low or high)
            if avg_risk_score >= 0.6:
                overall_risk_level = "high"
            else:
                overall_risk_level = "low"
            
            # Count non-compliant features
            non_compliant_features = [result for result in state_results if not result.is_compliant]
            
            # Convert state results to expected format with detailed feature information
            state_features = []
            for result in state_results:
                # Find the original feature to get complete information
                original_feature = None
                for feature in features:
                    if feature.feature_id == result.feature_id:
                        original_feature = feature
                        break
                
                state_features.append({
                    "feature": {
                        "feature_id": result.feature_id,
                        "feature_name": result.feature_name,
                        "feature_description": original_feature.feature_description if original_feature else "",
                        "feature_content": original_feature.feature_content if original_feature else "",
                        "section": original_feature.section if original_feature else "",
                        "priority": original_feature.priority if original_feature else "",
                        "complexity": original_feature.complexity if original_feature else "",
                        "data_types": original_feature.data_types if original_feature else [],
                        "user_impact": original_feature.user_impact if original_feature else "",
                        "technical_requirements": original_feature.technical_requirements if original_feature else [],
                        "compliance_considerations": original_feature.compliance_considerations if original_feature else []
                    },
                    "risk_score": result.risk_score,
                    "risk_level": result.risk_level,
                    "reasoning": result.reasoning,
                    "is_compliant": result.is_compliant,
                    "non_compliant_regulations": result.non_compliant_regulations,
                    "required_actions": result.required_actions,
                    "confidence_score": result.confidence_score,
                    "processing_time": result.processing_time
                })
            
            state_analysis[state_code] = {
                "state_name": state_results[0].state_name if state_results else "",
                "state_code": state_code,
                "overall_risk_score": avg_risk_score,
                "overall_risk_level": overall_risk_level,
                "total_features": len(features),
                "non_compliant_features": len(non_compliant_features),
                "compliance_rate": (len(features) - len(non_compliant_features)) / len(features) if features else 0.0,
                "features": state_features
            }
        
        print(f"✅ Optimized analysis complete in {batch_result.processing_time:.2f}s")
        print(f"📊 Overall stats: {batch_result.overall_stats['total_analyses']} analyses, "
              f"{batch_result.overall_stats['compliance_rate']:.1%} compliance rate")
        
        return state_analysis
    
    # Removed: analyze_all_features_for_state - replaced by OptimizedStateAnalyzer
    
    # Removed: Old individual analysis methods - replaced by OptimizedStateAnalyzer
    
    def get_state_regulations(self, state_code: str) -> Dict[str, Any]:
        """
        Get regulations for a specific state using the centralized cache
        
        Args:
            state_code: State code (e.g., "CA")
            
        Returns:
            Dictionary containing state regulations
        """
        state_regulation = self.state_cache.get_state_regulation(state_code)
        if state_regulation:
            return {
                "name": state_regulation.state_name,
                "regulations": state_regulation.regulations,
                "risk_level": state_regulation.risk_level,
                "enforcement_level": state_regulation.enforcement_level,
                "key_requirements": state_regulation.key_requirements,
                "penalties": state_regulation.penalties,
                "effective_date": state_regulation.effective_date,
                "notes": state_regulation.notes
            }
        else:
            return {"name": "Unknown", "regulations": []}
    
    def convert_state_results_to_feature_results(self, features: List[ExtractedFeature], 
                                               state_analysis: Dict[str, Dict[str, Any]]) -> List[FeatureComplianceResult]:
        """
        Convert state-centric results back to feature-centric format for backward compatibility
        
        Args:
            features: List of extracted features
            state_analysis: State-centric analysis results
            
        Returns:
            List of FeatureComplianceResult objects
        """
        feature_results = []
        
        for feature in features:
            # Collect all state results for this feature
            feature_state_results = []
            non_compliant_states = []
            state_compliance_scores = {}
            
            for state_code, state_data in state_analysis.items():
                # Find this feature in the state's feature list
                feature_in_state = None
                for f in state_data.get("features", []):
                    if f.get("feature", {}).get("feature_id") == feature.feature_id:
                        feature_in_state = f
                        break
                
                if feature_in_state:
                    feature_state_results.append(feature_in_state)
                    
                    # Track non-compliant states
                    if not feature_in_state.get("is_compliant", True):
                        non_compliant_states.append(state_code)
                    
                    # Calculate compliance score based on risk score (0.0 to 1.0)
                    risk_score = feature_in_state.get("risk_score", 0.5)
                    # Convert risk score to compliance score: 1.0 = fully compliant, 0.0 = non-compliant
                    compliance_score = max(0.0, min(1.0, 1.0 - risk_score))
                    
                    # Determine risk level based on compliance score (only low or high)
                    if compliance_score >= 0.6:
                        risk_level = "low"
                    else:
                        risk_level = "high"
                    
                    # Create state compliance score
                    state_compliance_scores[state_code] = StateComplianceScore(
                        state_code=state_code,
                        state_name=state_data.get("state_name", ""),
                        compliance_score=compliance_score,
                        risk_level=risk_level,
                        reasoning=feature_in_state.get("reasoning", ""),
                        non_compliant_regulations=feature_in_state.get("non_compliant_regulations", []),
                        required_actions=feature_in_state.get("required_actions", []),
                        notes=""
                    )
            
            # Calculate overall feature risk
            if feature_state_results:
                risk_scores = [f.get("risk_score", 0.5) for f in feature_state_results]
                avg_risk_score = sum(risk_scores) / len(risk_scores)
                
                if avg_risk_score >= 0.6:
                    overall_risk_level = "high"
                else:
                    overall_risk_level = "low"
                
                # Collect recommendations from all state analyses
                all_recommendations = []
                for state_result in feature_state_results:
                    # Get required actions from state analysis
                    required_actions = state_result.get("required_actions", [])
                    all_recommendations.extend(required_actions)
                    
                    # Get non-compliant regulations that need attention
                    non_compliant_regulations = state_result.get("non_compliant_regulations", [])
                    if non_compliant_regulations:
                        for regulation in non_compliant_regulations:
                            all_recommendations.append(f"Ensure compliance with {regulation}")
                
                # Remove duplicates and prioritize recommendations
                unique_recommendations = []
                seen_recommendations = set()
                for rec in all_recommendations:
                    rec_lower = rec.lower()
                    if rec_lower not in seen_recommendations:
                        unique_recommendations.append(rec)
                        seen_recommendations.add(rec_lower)
                
                # Add feature-specific recommendations based on risk level
                if overall_risk_level == "high":
                    unique_recommendations.append("Conduct detailed compliance audit")
                    unique_recommendations.append("Implement additional privacy safeguards")
                    unique_recommendations.append("Review data processing practices")
                else:
                    unique_recommendations.append("Monitor compliance status regularly")
                    unique_recommendations.append("Update privacy policies if needed")
                
                # Add general recommendations
                if len(non_compliant_states) > 0:
                    unique_recommendations.append(f"Address compliance issues in {len(non_compliant_states)} states")
                
                # Limit to top 10 most important recommendations
                final_recommendations = unique_recommendations[:10]
                
                # Create FeatureComplianceResult
                feature_result = FeatureComplianceResult(
                     feature=feature,
                     agent_outputs={},  # Empty dict since this is converted from state analysis
                     compliance_flags=[],  # Will be populated from regulation matching
                     risk_level=overall_risk_level,
                     confidence_score=0.8,  # Default confidence
                     requires_human_review=overall_risk_level == "high",
                     reasoning=f"Feature analyzed across {len(feature_state_results)} states. {len(non_compliant_states)} non-compliant states.",
                     recommendations=final_recommendations,  # Populated with collected recommendations
                     us_state_compliance=[],  # Empty list since this is converted from state analysis
                     non_compliant_states=non_compliant_states,
                     state_compliance_scores=state_compliance_scores,
                     cultural_sensitivity_scores={},  # Empty dict since cultural sensitivity is analyzed separately
                     processing_time=0.0,  # Will be calculated
                     timestamp=get_singapore_time().isoformat()
                 )
                
                feature_results.append(feature_result)
        
        return feature_results

def main():
    """Main function to run the workflow"""
    print("🚀 Multi-Agent PRD Geo-Compliance Detection System")
    print("=" * 80)
    
    # Check dependencies
    if not GEMINI_API_KEY:
        print("⚠️  No GEMINI_API_KEY found. System will not be able to run.")
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
        "prd_id": f"prd_{get_singapore_time().strftime('%Y%m%d_%H%M%S')}",
        "prd_name": prd_name,
        "prd_description": prd_description,
        "prd_content": prd_content,
        "metadata": {
            "document_type": "product_requirements",
            "analysis_date": get_singapore_time().isoformat(),
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
        
        # Display state compliance scores for this feature
        if result.state_compliance_scores:
            print(f"     State Compliance Scores:")
            for state_code, score_data in result.state_compliance_scores.items():
                print(f"       {state_code}: {score_data.compliance_score:.2f} ({score_data.risk_level})")
                if score_data.compliance_score < 0.8:  # Show reasoning for non-compliant states
                    print(f"         Reasoning: {score_data.reasoning[:80]}...")
        print()
    
    # Display non-compliant states dictionary
    if final_state.non_compliant_states_dict:
        print(f"\n🇺🇸 Non-Compliant States Analysis:")
        print("=" * 50)
        for state_code, state_data in final_state.non_compliant_states_dict.items():
            print(f"\n📍 {state_code} - {state_data['state_name']}")
            print(f"   Risk Score: {state_data['risk_score']:.2f} ({state_data['risk_level'].upper()})")
            print(f"   Non-compliant Features: {', '.join(state_data['non_compliant_features'])}")
            print(f"   Reasoning: {state_data['reasoning'][:100]}...")
            if state_data['required_actions']:
                print(f"   Required Actions: {', '.join(state_data['required_actions'][:3])}")
    
    print(f"\n💡 Top Recommendations:")
    for rec in final_state.summary_recommendations[:5]:
        print(f"   • {rec}")
    
    print(f"\n📊 Total Processing Time: {final_state.total_processing_time:.2f}s")
    print(f"📁 Results saved to: output/output_{final_state.workflow_id}.json")

if __name__ == "__main__":
    main()
