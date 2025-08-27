# 📦 Installation Guide

This guide helps you install the LangGraph Multi-Agent Geo-Compliance Detection System without dependency conflicts.

## 🚨 Dependency Conflict Fix

The main issue was a conflict between:
- `google-generativeai 0.3.0` requiring `google-ai-generativelanguage==0.4.0`
- `langchain-google-genai 2.1.10` requiring `google-ai-generativelanguage>=0.6.18`

## ✅ Solution: Two-Tier Installation

### Tier 1: Basic Installation (Recommended)

This gives you a fully functional system with just the essential packages:

```bash
# Method 1: Use the setup script
python setup.py
# Choose option 1 for basic setup

# Method 2: Manual installation
pip install google-generativeai
```

**What you get:**
- ✅ Complete multi-agent workflow
- ✅ LLM integration with Gemini
- ✅ Fallback pattern matching
- ✅ JSON output generation
- ✅ All core functionality

**What you can run:**
- `python simple_workflow.py` ✅
- `python test_workflow.py` ✅
- `python main.py` ✅

### Tier 2: Full Installation (Advanced)

This adds LangGraph orchestration and advanced features:

```bash
# Method 1: Use the setup script
python setup.py
# Choose option 2 for full setup

# Method 2: Manual installation
pip install -r requirements_full.txt
```

**Additional features:**
- ✅ LangGraph workflow orchestration
- ✅ Advanced vector database
- ✅ Enhanced RAG capabilities
- ✅ `python langgraph_workflow.py` ✅

## 🔧 Installation Options

### Option 1: Guided Setup (Recommended)
```bash
python setup.py
```
The setup script will:
1. Check your Python version
2. Detect your API key
3. Install compatible packages
4. Avoid dependency conflicts

### Option 2: Manual Installation
```bash
# Basic (works immediately)
pip install google-generativeai

# Full (may have conflicts)
pip install -r requirements_full.txt
```

### Option 3: Virtual Environment
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

## 🛠️ Troubleshooting

### Issue: "Cannot install -r requirements.txt"
**Solution:** Use the basic installation instead:
```bash
pip install google-generativeai
```

### Issue: "google-ai-generativelanguage version conflict"
**Solution:** Use the setup script:
```bash
python setup.py
# Choose option 1
```

### Issue: "ImportError: No module named 'google.generativeai'"
**Solution:** Install the package:
```bash
pip install google-generativeai
```

### Issue: "LangGraph not available"
**Solution:** This is normal for basic installation. Use `simple_workflow.py` instead of `langgraph_workflow.py`.

## 📋 What Works Without Full Dependencies

The basic installation provides:
- ✅ All 5 agents (Feature Analyzer, Regulation Matcher, Risk Assessor, Reasoning Generator, Quality Assurance)
- ✅ LLM integration with Gemini AI
- ✅ Fallback pattern matching
- ✅ Detailed logging and output tracking
- ✅ JSON output files with complete audit trails
- ✅ Processing time tracking
- ✅ Confidence scoring
- ✅ Human-in-the-loop flagging

## 🎯 Recommended Approach

1. **Start with Basic Installation**
   ```bash
   python setup.py
   # Choose option 1
   ```

2. **Test the System**
   ```bash
   python simple_workflow.py
   ```

3. **If you need advanced features, upgrade later**
   ```bash
   python setup.py
   # Choose option 2
   ```

## ✅ Verification

After installation, verify everything works:

```bash
# Test basic functionality
python simple_workflow.py

# Check output
ls output_*.json

# Test with API key (if you have one)
python setup_env.py  # Set up your API key
python test_workflow.py
```

## 🚀 Ready to Go!

Once you see the multi-agent workflow running and generating JSON output files, your installation is complete and working perfectly!
