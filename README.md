# Nytech Social Content Generator

Internal AI-powered content generation tool for creating brand-safe,
original marketing captions from inspiration content.

## Features
- Provider-agnostic LLM engine
- Brand-as-data architecture
- Inspiration analysis (structure, not wording)
- Similarity guardrails to prevent copying
- Presets for tone, platform, and conversion style
- Streamlit-based internal UI

## Tech Stack
- Python 3
- Streamlit
- Google Gemini API
- Virtualenv
- Environment variables for secrets

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
