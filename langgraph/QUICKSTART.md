# 🚀 Quick Start Guide

Get your LangGraph Multi-Agent Geo-Compliance Detection System running in minutes!

## ⚡ Super Quick Start

### 1. Run Setup (Optional)
```bash
python setup.py
```

### 2. Run the System
```bash
python langgraph_workflow.py
```

That's it! The system will run in fallback mode and analyze a sample document.

## 🔑 With API Key (Recommended)

### 1. Set Up Your API Key
```bash
# Option A: Use setup script (Recommended)
python setup_env.py

# Option B: Create .env file manually
cp env_template.txt .env
# Edit .env file with your actual API key
```

### 2. Test with API Key
```bash
python test_workflow.py
```

### 3. Run Main Workflow
```bash
python langgraph_workflow.py
```

## 📊 What You'll See

```
🚀 Starting Multi-Agent Workflow for: Sample Product Requirements Document
================================================================================
🔄 Running agents sequentially...

🔍 [Feature Analyzer] Processing document: Sample Product Requirements Document
✅ [Feature Analyzer] Completed in 0.15s
   📊 Data types: ['personal_data', 'location_data']
   🎯 Processing purposes: ['analytics', 'personalization']

🏛️  [Regulation Matcher] Matching regulations for: Sample Product Requirements Document
✅ [Regulation Matcher] Completed in 0.12s
   📋 Applicable regulations: ['GDPR', 'CCPA', 'PIPL', 'LGPD']
   🎯 Compliance priority: high

⚠️  [Risk Assessor] Assessing risks for: Sample Product Requirements Document
✅ [Risk Assessor] Completed in 0.18s
   🚨 Risk level: high
   📊 Confidence: 85.0%

💭 [Reasoning Generator] Generating reasoning for: Sample Product Requirements Document
✅ [Reasoning Generator] Completed in 0.14s
   📝 Compliance status: requires_review
   💡 Recommendations: 5

🔍 [Quality Assurance] Validating results for: Sample Product Requirements Document
✅ [Quality Assurance] Completed in 0.10s
   🎯 Quality score: 82.5%
   ✅ Final validation: approved

🎉 Workflow Analysis Complete!
================================================================================
🔴 Risk Level: HIGH
📈 Confidence: 82.5%
👤 Human Review: Not Required
🏛️  Compliance Flags: GDPR, CCPA, PIPL, LGPD
💭 Reasoning: Document requires high level compliance attention...
💡 Recommendations:
   • Implement explicit consent mechanisms
   • Add data minimization controls
   • Establish user rights portal
   • Monitor for compliance updates
   • Regular review recommended

📊 Total Processing Time: 0.69s
📁 Results saved to: output/output_workflow_20250827_234144.json
```

## 📁 Output Files

The system generates detailed JSON files with complete audit trails:
- `output/output_workflow_*.json` - Complete analysis results
- Contains all agent outputs, thought processes, and recommendations

## 🎯 Next Steps

1. **Customize Documents**: Modify the sample documents in the scripts
2. **Add Your Data**: Replace the sample data with your own documents
3. **Review Results**: Check the generated JSON files for detailed analysis
4. **Scale Up**: Use the system for batch processing of multiple documents

## 🆘 Need Help?

- **No API Key**: System works in fallback mode with pattern matching
- **Import Errors**: Run `pip install google-generativeai`
- **Performance**: Use `simple_workflow.py` for fastest processing
- **More Info**: Check `README.md` for detailed documentation

## 🚀 Ready to Go!

Your LangGraph Multi-Agent Geo-Compliance Detection System is now ready to use! 🎉
