"""
Gemini Geo-Compliance Detection System
Main application file with Gemini AI integration
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path

# Try to import required modules, with fallbacks
try:
    from fastapi import FastAPI, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    from pydantic import BaseModel, Field
    from dotenv import load_dotenv
    import uvicorn
    FASTAPI_AVAILABLE = True
except ImportError:
    print("⚠️  FastAPI not available. Running in console mode only.")
    FASTAPI_AVAILABLE = False

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    print("⚠️  Google Generative AI not available. Running in pattern matching mode only.")
    GEMINI_AVAILABLE = False

# Load environment variables from .env file
if 'load_dotenv' in globals():
    load_dotenv()
    print("✅ Loaded environment variables from .env file")
else:
    print("⚠️  python-dotenv not available. Using system environment variables only.")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY and GEMINI_AVAILABLE:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-pro')
        print("✅ Gemini AI configured successfully")
    except Exception as e:
        print(f"⚠️  Gemini configuration failed: {e}")
        model = None
else:
    model = None
    if not GEMINI_API_KEY:
        print("⚠️  No GEMINI_API_KEY found. Running in pattern matching mode.")
    if not GEMINI_AVAILABLE:
        print("⚠️  Google Generative AI not installed. Running in pattern matching mode.")

# Pydantic models (if available)
if FASTAPI_AVAILABLE:
    class FeatureArtifact(BaseModel):
        feature_id: str
        feature_name: str
        feature_description: str
        feature_content: str
        metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)

    class ComplianceAnalysisRequest(BaseModel):
        feature: FeatureArtifact

    class ComplianceAnalysisResponse(BaseModel):
        feature_id: str
        feature_name: str
        overall_risk_level: str
        confidence_score: float
        requires_human_review: bool
        compliance_flags: List[str]
        reasoning: str
        recommendations: List[str]
        timestamp: str

    class HealthResponse(BaseModel):
        status: str
        timestamp: str
        version: str
        components: Dict[str, bool]

# Global state
analysis_history = []

def analyze_feature_with_gemini(feature_data: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze feature compliance using Gemini AI"""
    
    if not model:
        # Fallback to pattern matching if no API key
        return analyze_feature_pattern_matching(feature_data)
    
    try:
        # Create prompt for Gemini
        prompt = f"""
        You are a compliance expert analyzing software features for geo-specific legal requirements.
        
        Analyze the following feature for compliance with global regulations (GDPR, CCPA, PIPL, LGPD, etc.):
        
        Feature Name: {feature_data['feature_name']}
        Description: {feature_data['feature_description']}
        Content: {feature_data['feature_content']}
        
        Provide your analysis in the following JSON format:
        {{
            "risk_level": "low|medium|high|critical",
            "confidence_score": 0.0-1.0,
            "requires_human_review": true/false,
            "compliance_flags": ["GDPR", "CCPA", "PIPL", etc.],
            "reasoning": "detailed explanation of compliance analysis",
            "recommendations": ["list of specific recommendations"]
        }}
        
        Focus on:
        1. Data handling practices
        2. User privacy implications
        3. Cross-border data transfers
        4. Automated decision making
        5. Biometric data processing
        6. Specific regulatory requirements
        """
        
        # Get response from Gemini
        response = model.generate_content(prompt)
        
        # Parse JSON response
        try:
            analysis = json.loads(response.text)
        except json.JSONDecodeError:
            # If JSON parsing fails, extract information from text
            analysis = parse_gemini_text_response(response.text)
        
        return {
            "feature_id": feature_data['feature_id'],
            "feature_name": feature_data['feature_name'],
            "overall_risk_level": analysis.get("risk_level", "medium"),
            "confidence_score": analysis.get("confidence_score", 0.7),
            "requires_human_review": analysis.get("requires_human_review", False),
            "compliance_flags": analysis.get("compliance_flags", []),
            "reasoning": analysis.get("reasoning", "Analysis completed"),
            "recommendations": analysis.get("recommendations", []),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Gemini analysis failed: {e}")
        # Fallback to pattern matching
        return analyze_feature_pattern_matching(feature_data)

def parse_gemini_text_response(text: str) -> Dict[str, Any]:
    """Parse Gemini text response when JSON parsing fails"""
    
    # Extract compliance flags
    compliance_flags = []
    if "GDPR" in text.upper():
        compliance_flags.append("GDPR")
    if "CCPA" in text.upper():
        compliance_flags.append("CCPA")
    if "PIPL" in text.upper():
        compliance_flags.append("PIPL")
    if "LGPD" in text.upper():
        compliance_flags.append("LGPD")
    
    # Determine risk level from text
    text_lower = text.lower()
    if "critical" in text_lower or "high risk" in text_lower:
        risk_level = "critical"
    elif "high" in text_lower:
        risk_level = "high"
    elif "medium" in text_lower:
        risk_level = "medium"
    else:
        risk_level = "low"
    
    return {
        "risk_level": risk_level,
        "confidence_score": 0.7,
        "requires_human_review": len(compliance_flags) > 0,
        "compliance_flags": compliance_flags,
        "reasoning": text[:500] + "..." if len(text) > 500 else text,
        "recommendations": ["Review the analysis for specific recommendations"]
    }

def analyze_feature_pattern_matching(feature_data: Dict[str, Any]) -> Dict[str, Any]:
    """Fallback pattern matching analysis"""
    
    content_lower = feature_data['feature_content'].lower()
    description_lower = feature_data['feature_description'].lower()
    
    compliance_flags = []
    risk_factors = []
    
    # Check for data collection patterns
    if any(term in content_lower for term in ["personal data", "user data", "collect", "tracking"]):
        compliance_flags.extend(["GDPR", "CCPA", "PIPL"])
        risk_factors.append("Personal data collection")
    
    # Check for location data
    if any(term in content_lower for term in ["location", "gps", "geolocation", "coordinates"]):
        compliance_flags.extend(["GDPR", "CCPA", "PIPL"])
        risk_factors.append("Location data processing")
    
    # Check for biometric data
    if any(term in content_lower for term in ["facial", "fingerprint", "biometric", "recognition"]):
        compliance_flags.extend(["GDPR", "CCPA", "PIPL"])
        risk_factors.append("Biometric data processing")
    
    # Check for cross-border transfer
    if any(term in content_lower for term in ["cross-border", "international", "global", "transfer"]):
        compliance_flags.extend(["GDPR", "PIPL", "LGPD"])
        risk_factors.append("Cross-border data transfer")
    
    # Check for automated decision making
    if any(term in content_lower for term in ["ai", "machine learning", "automated", "algorithm"]):
        compliance_flags.extend(["GDPR", "CCPA"])
        risk_factors.append("Automated decision making")
    
    # Remove duplicates
    compliance_flags = list(set(compliance_flags))
    
    # Determine risk level
    if len(risk_factors) >= 3:
        risk_level = "critical"
        confidence = 0.9
        requires_review = True
    elif len(risk_factors) >= 2:
        risk_level = "high"
        confidence = 0.8
        requires_review = True
    elif len(risk_factors) >= 1:
        risk_level = "medium"
        confidence = 0.7
        requires_review = False
    else:
        risk_level = "low"
        confidence = 0.6
        requires_review = False
    
    # Generate reasoning
    if risk_factors:
        reasoning = f"Feature involves {', '.join(risk_factors)} which triggers compliance requirements for {', '.join(compliance_flags)}."
    else:
        reasoning = "No significant compliance risks identified in the feature."
    
    # Generate recommendations
    recommendations = []
    if "Personal data collection" in risk_factors:
        recommendations.append("Implement explicit user consent mechanisms")
        recommendations.append("Add data minimization practices")
    
    if "Cross-border data transfer" in risk_factors:
        recommendations.append("Implement data localization controls")
        recommendations.append("Add cross-border transfer safeguards")
    
    if "Biometric data processing" in risk_factors:
        recommendations.append("Implement additional consent requirements")
        recommendations.append("Add biometric data protection measures")
    
    if not recommendations:
        recommendations.append("Monitor for any changes that might affect compliance")
    
    return {
        "feature_id": feature_data['feature_id'],
        "feature_name": feature_data['feature_name'],
        "overall_risk_level": risk_level,
        "confidence_score": confidence,
        "requires_human_review": requires_review,
        "compliance_flags": compliance_flags,
        "reasoning": reasoning,
        "recommendations": recommendations,
        "timestamp": datetime.now().isoformat()
    }

def demo_analysis():
    """Run a demo analysis"""
    print("\n" + "="*60)
    print("🧪 DEMO COMPLIANCE ANALYSIS")
    print("="*60)
    
    # Sample feature for demo
    demo_feature = {
        "feature_id": "demo_001",
        "feature_name": "User Tracking System",
        "feature_description": "Tracks user behavior and location data",
        "feature_content": "This feature collects personal data including location information, browsing history, and user behavior patterns for analytics and personalized recommendations. Data is stored in cloud databases and may be transferred internationally."
    }
    
    print(f"📋 Analyzing: {demo_feature['feature_name']}")
    print(f"📝 Description: {demo_feature['feature_description']}")
    
    # Perform analysis
    result = analyze_feature_with_gemini(demo_feature)
    
    # Display results
    print("\n📊 ANALYSIS RESULTS:")
    print(f"🔴 Risk Level: {result['overall_risk_level'].upper()}")
    print(f"📈 Confidence: {result['confidence_score']:.1%}")
    print(f"👤 Human Review: {'Required' if result['requires_human_review'] else 'Not Required'}")
    print(f"🏛️  Compliance Flags: {', '.join(result['compliance_flags']) if result['compliance_flags'] else 'None'}")
    print(f"💭 Reasoning: {result['reasoning']}")
    print(f"💡 Recommendations:")
    for rec in result['recommendations']:
        print(f"   • {rec}")
    
    return result

def interactive_mode():
    """Run interactive mode for manual feature analysis"""
    print("\n" + "="*60)
    print("🎯 INTERACTIVE COMPLIANCE ANALYSIS")
    print("="*60)
    
    while True:
        print("\nEnter feature details (or 'quit' to exit):")
        
        feature_id = input("Feature ID: ").strip()
        if feature_id.lower() == 'quit':
            break
            
        feature_name = input("Feature Name: ").strip()
        if feature_name.lower() == 'quit':
            break
            
        feature_description = input("Feature Description: ").strip()
        if feature_description.lower() == 'quit':
            break
            
        print("Feature Content (press Enter twice to finish):")
        content_lines = []
        while True:
            line = input()
            if line == "":
                break
            content_lines.append(line)
        feature_content = "\n".join(content_lines)
        
        if not all([feature_id, feature_name, feature_description, feature_content]):
            print("❌ All fields are required. Please try again.")
            continue
        
        # Create feature data
        feature_data = {
            "feature_id": feature_id,
            "feature_name": feature_name,
            "feature_description": feature_description,
            "feature_content": feature_content
        }
        
        # Perform analysis
        print(f"\n🔍 Analyzing {feature_name}...")
        result = analyze_feature_with_gemini(feature_data)
        
        # Display results
        print(f"\n📊 RESULTS:")
        print(f"🔴 Risk Level: {result['overall_risk_level'].upper()}")
        print(f"📈 Confidence: {result['confidence_score']:.1%}")
        print(f"👤 Human Review: {'Required' if result['requires_human_review'] else 'Not Required'}")
        print(f"🏛️  Compliance Flags: {', '.join(result['compliance_flags']) if result['compliance_flags'] else 'None'}")
        print(f"💭 Reasoning: {result['reasoning']}")
        print(f"💡 Recommendations:")
        for rec in result['recommendations']:
            print(f"   • {rec}")
        
        # Store in history
        analysis_history.append(result)
        
        print(f"\n✅ Analysis completed. Total analyses: {len(analysis_history)}")

# FastAPI app (if available)
if FASTAPI_AVAILABLE:
    app = FastAPI(
        title="Gemini Geo-Compliance Detection System",
        description="AI-powered compliance analysis using Google Gemini",
        version="1.0.0"
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/", response_model=Dict[str, str])
    async def root():
        """Root endpoint"""
        return {
            "message": "Gemini Geo-Compliance Detection System",
            "version": "1.0.0",
            "status": "running",
            "ai_provider": "Google Gemini"
        }

    @app.get("/health", response_model=HealthResponse)
    async def health_check():
        """Health check endpoint"""
        return HealthResponse(
            status="healthy",
            timestamp=datetime.now().isoformat(),
            version="1.0.0",
            components={
                "api": True,
                "gemini_ai": model is not None,
                "analysis_engine": True,
                "storage": True
            }
        )

    @app.post("/analyze-feature", response_model=ComplianceAnalysisResponse)
    async def analyze_feature(request: ComplianceAnalysisRequest):
        """Analyze a single feature for compliance using Gemini"""
        try:
            logger.info(f"Analyzing feature: {request.feature.feature_name}")
            
            # Convert to dict for analysis
            feature_data = {
                "feature_id": request.feature.feature_id,
                "feature_name": request.feature.feature_name,
                "feature_description": request.feature.feature_description,
                "feature_content": request.feature.feature_content
            }
            
            # Perform analysis
            result = analyze_feature_with_gemini(feature_data)
            
            # Store in history
            analysis_history.append(result)
            
            logger.info(f"Analysis completed for {request.feature.feature_id}")
            return ComplianceAnalysisResponse(**result)
            
        except Exception as e:
            logger.error(f"Error analyzing feature: {e}")
            raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

    @app.get("/analysis-history")
    async def get_analysis_history():
        """Get analysis history"""
        return {
            "total_analyses": len(analysis_history),
            "analyses": analysis_history[-10:]  # Last 10 analyses
        }

def main():
    """Main function"""
    print("🚀 Gemini Geo-Compliance Detection System")
    print("=" * 60)
    
    if not GEMINI_API_KEY:
        print("⚠️  No GEMINI_API_KEY found. Running in pattern matching mode.")
        print("💡 Get your API key from: https://makersuite.google.com/app/apikey")
        print("💡 Set it as: GEMINI_API_KEY=your_key_here")
    
    if not GEMINI_AVAILABLE:
        print("⚠️  Google Generative AI not installed. Running in pattern matching mode.")
        print("💡 Install with: pip install google-generativeai")
    
    if not FASTAPI_AVAILABLE:
        print("⚠️  FastAPI not installed. Running in console mode only.")
        print("💡 Install with: pip install fastapi uvicorn")
    
    print("\nChoose mode:")
    print("1. Demo analysis")
    print("2. Interactive mode")
    if FASTAPI_AVAILABLE:
        print("3. Start API server")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == "1":
        demo_analysis()
    elif choice == "2":
        interactive_mode()
    elif choice == "3" and FASTAPI_AVAILABLE:
        # Create necessary directories
        Path("logs").mkdir(exist_ok=True)
        Path("exports").mkdir(exist_ok=True)
        
        print("\n🚀 Starting API server...")
        print("📊 API Documentation: http://localhost:8000/docs")
        print("🔍 Health Check: http://localhost:8000/health")
        print("⏹️  Press Ctrl+C to stop")
        
        uvicorn.run(app, host="0.0.0.0", port=8000)
    else:
        print("❌ Invalid choice or mode not available")

if __name__ == "__main__":
    main() 
