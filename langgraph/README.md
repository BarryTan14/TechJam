# LangGraph Multi-Agent PRD Geo-Compliance Detection System

A comprehensive automated geo-compliance detection system that analyzes Product Requirements Documents (PRDs) to extract features and detect geo-specific legal compliance needs using multi-agent workflows powered by Google Gemini AI.

## 🚀 Quick Start

### 1. Install Dependencies

**Basic Installation (Recommended):**
```bash
pip install google-generativeai
```

**Full Installation (Advanced):**
```bash
pip install -r requirements.txt
```

**Note:** If you encounter dependency conflicts, use the basic installation which provides all core functionality.

### 2. Set Up API Key (Required)
Create a `.env` file in the langgraph directory with your Gemini API key:
```
GEMINI_API_KEY=your_api_key_here
```

**Note**: This system requires a Gemini API key to function. Get your API key from: https://makersuite.google.com/app/apikey

### 3. Run the System
```bash
python langgraph_workflow.py
```

That's it! The system will prompt you for PRD details and analyze it for compliance.

## 🔧 Installation Options

### Option 1: Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Unix/Mac)
source venv/bin/activate

# Install basic packages
pip install google-generativeai
```

### Option 2: Basic Installation
```bash
pip install google-generativeai
```

### Option 3: Full Installation
```bash
pip install -r requirements.txt
```

## 📋 What It Does

The system uses 8 specialized AI agents to analyze your PRDs:

1. **📋 PRD Parser** - Extracts individual features from PRD documents using AI
2. **🔍 Feature Analyzer** - Extracts compliance-relevant information from each feature using AI
3. **🏛️ Regulation Matcher** - Matches features to applicable regulations (GDPR, CCPA, PIPL, LGPD) using AI
4. **⚠️ Risk Assessor** - Scores compliance risks and identifies gaps using AI
5. **💭 Reasoning Generator** - Produces clear justifications and recommendations using AI
6. **🔍 Quality Assurance** - Validates results and provides final assessment using AI
7. **🇺🇸 US State Compliance** - Analyzes compliance for each US state (50 states) using AI
8. **🔍 Non-Compliant States Analyzer** - Generates comprehensive non-compliant states dictionary with risk scores and reasoning using AI

## 📊 Output

- **Console Output**: Real-time analysis progress and final results
- **JSON File**: Complete audit trail saved to `output/output_workflow_*.json`
- **US State Analysis**: List of non-compliant states for each feature

## 🎯 Example Output

```
🚀 Starting Multi-Agent PRD Analysis Workflow for: Sample PRD
================================================================================
📋 Step 1: Parsing PRD and extracting features...
✅ Extracted 11 features from PRD

🔍 Step 2: Analyzing 11 features...

📊 Feature 1/11: User Preference Collection
🔍 [Feature Analyzer] Processing feature...
✅ [Feature Analyzer] Completed in 2.1s
🏛️  [Regulation Matcher] Matching regulations...
✅ [Regulation Matcher] Completed in 1.8s
⚠️  [Risk Assessor] Assessing risks...
✅ [Risk Assessor] Completed in 2.3s
💭 [Reasoning Generator] Generating reasoning...
✅ [Reasoning Generator] Completed in 1.9s
🔍 [Quality Assurance] Validating results...
✅ [Quality Assurance] Completed in 1.2s
🇺🇸 [US State Compliance] Analyzing US state compliance...
✅ [US State Compliance] Analyzed 50 states, found 0 non-compliant in 1.5s

🎉 PRD Analysis Complete!
================================================================================
📊 Total Features Analyzed: 11
🔴 Overall Risk Level: HIGH
📈 Overall Confidence: 87.3%
🚨 Critical Issues: 11

📋 Feature Summary:
  1. User Preference Collection
     Risk: HIGH
     Non-compliant states: 0

  2. Browsing History Tracking
     Risk: HIGH
     Non-compliant states: 10
     States: CA, CO, CT, FL, IL, NY, TX, UT, VA, WA

  3. Location Data Collection
     Risk: HIGH
     Non-compliant states: 0

💡 Top Recommendations:
   • Implement state-specific consent mechanisms
   • Add data minimization controls
   • Establish user rights portal
   • Monitor for regulation updates

📊 Total Processing Time: 566.78s
📁 Results saved to: output/output_workflow_20250828_172651.json
```

## 🔧 Configuration

### Environment Variables
- `GEMINI_API_KEY`: Your Google Gemini API key (required)

### Dependencies
- `google-generativeai`: For Gemini AI integration
- `python-dotenv`: For environment variable management
- `fastapi`, `uvicorn`, `pydantic`: For API functionality

## 📁 Project Structure

```
langgraph/
├── langgraph_workflow.py    # Main workflow (run this!)
├── agents/                  # Agent modules
│   ├── prd_parser.py        # PRD parsing and feature extraction
│   ├── feature_analyzer.py  # Feature analysis
│   ├── regulation_matcher.py # Regulation matching
│   ├── risk_assessor.py     # Risk assessment
│   ├── reasoning_generator.py # Reasoning generation
│   ├── quality_assurance.py # Quality validation
│   ├── us_state_compliance.py # US state compliance analysis
│   ├── non_compliant_states_analyzer.py # Non-compliant states dictionary generation
│   └── models.py            # Data models
├── main.py                  # Alternative API interface
├── requirements.txt         # Dependencies
├── README.md               # This file
├── QUICKSTART.md           # Quick start guide
└── output/                 # Generated analysis results
    └── output_*.json       # JSON output files
```

## 🛠️ Troubleshooting

### Common Issues

1. **Dependency Conflicts**: Use basic installation: `pip install google-generativeai`
2. **No API Key**: System will exit with clear error message
3. **Invalid API Key**: Check your API key at https://makersuite.google.com/app/apikey
4. **Network Issues**: Ensure stable internet connection for LLM calls
5. **Import Errors**: Run `pip install google-generativeai`

### What Works Without Full Dependencies

The basic installation provides:
- ✅ All 8 agents (PRD Parser, Feature Analyzer, Regulation Matcher, Risk Assessor, Reasoning Generator, Quality Assurance, US State Compliance, Non-Compliant States Analyzer)
- ✅ LLM integration with Gemini AI
- ✅ Fallback pattern matching
- ✅ Detailed logging and output tracking
- ✅ JSON output files with complete audit trails
- ✅ Processing time tracking
- ✅ Confidence scoring

## 🎯 Use Cases

- **PRD Compliance Analysis**: Analyze product requirements for regulatory compliance
- **Feature Extraction**: Automatically extract features from PRD documents using AI
- **US State Compliance**: Get detailed compliance analysis for all 50 US states
- **Audit Trail Generation**: Generate comprehensive audit trails
- **Risk Assessment**: Identify compliance risks and gaps
- **Training**: Use detailed reasoning to train teams on compliance

## 🔮 Supported Regulations

### Global Regulations
- **GDPR** (EU): General Data Protection Regulation
- **CCPA** (California): California Consumer Privacy Act  
- **PIPL** (China): Personal Information Protection Law
- **LGPD** (Brazil): Lei Geral de Proteção de Dados

### US State Regulations
The system analyzes compliance for all 50 US states, including:
- **California (CCPA/CPRA)**: California Consumer Privacy Act
- **Virginia (VCDPA)**: Virginia Consumer Data Protection Act
- **Colorado (CPA)**: Colorado Privacy Act
- **Connecticut (CTDPA)**: Connecticut Data Privacy Act
- **Utah (UCPA)**: Utah Consumer Privacy Act
- **Florida (FDBR)**: Florida Digital Bill of Rights
- **Texas (TDPSA)**: Texas Data Privacy and Security Act
- **And 42 more states** with their respective privacy laws

## 📈 Key Features

- **AI-Powered PRD Parsing**: Automatically extracts features from PRD documents using Gemini AI
- **Multi-Feature Analysis**: Analyzes each feature individually through all AI agents
- **US State Compliance**: Comprehensive analysis for all 50 US states using AI
- **Detailed Output**: Complete audit trail with reasoning and recommendations
- **Risk Assessment**: Identifies high-risk features and compliance gaps
- **Processing Time Tracking**: Performance metrics for each agent and feature
- **LLM-Only Operation**: All analysis performed by AI agents for maximum accuracy

## 🤖 AI Technology

This system is powered by Google Gemini AI and requires:
- **Gemini API Key**: Required for all operations
- **Internet Connection**: For LLM API calls
- **Stable Network**: For reliable AI analysis

All agents use advanced AI prompts and JSON parsing to provide accurate, detailed compliance analysis.

---

**Note**: This system is designed for educational and demonstration purposes. For production use, ensure proper validation and compliance with your organization's policies.
