# AI-Enhanced Customer Support Chatbot 🤖

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3+-orange.svg)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## Research Problem

Customers often experience dissatisfaction with AI chatbots due to **irrelevant, repetitive, or context-insensitive responses**, leading to reduced trust in automated customer support.

## Solution

This project implements a **Machine Learning-enhanced chatbot** that addresses these issues through:

- ✅ **Advanced NLP** with TF-IDF vectorization and Naive Bayes classification
- ✅ **Enhanced Sentiment Analysis** with weighted lexicon scoring
- ✅ **Intelligent Human Escalation** based on frustration detection
- ✅ **Context-Aware Responses** using conversation history
- ✅ **Comprehensive Metrics Tracking** for research evaluation
- ✅ **Personalized Interactions** with adaptive response generation

---

## Features

### 🎯 Core Capabilities
- **12 Intent Categories**: Greeting, Order Status, Refunds, Cancellations, Shipping, Payment, Product Info, Complaints, Help, Human Escalation, Thanks, Goodbye
- **3-Level Sentiment Detection**: Positive, Negative, Neutral
- **Real-time Metrics**: Response time, satisfaction scores, escalation rates
- **Session Persistence**: Full conversation history with metadata

### 🧠 Machine Learning
- **Model**: Multinomial Naive Bayes
- **Features**: 500 TF-IDF features with bi-gram support
- **Confidence Threshold**: 0.4 (automatic fallback to rules)
- **Training**: Auto-trains on first run with 60+ examples

### 🚨 Smart Escalation
Automatically escalates to human agents when:
- Customer frustration level ≥ 3
- Repeated questions detected (2+ times)
- Complex complaints (>15 words)
- Explicit human agent request
- Multiple unclear intents

---

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/AjinkyaxSuryawanshi/AI-CHATBOT.git
cd AI-CHATBOT

# Install dependencies
pip install -r requirements.txt

# Run the chatbot
python chatbot.py
```

### First Run
The chatbot will automatically:
1. Train the ML model
2. Save model as `chatbot_model.pkl`
3. Start the interactive session

### Example Usage

```
You: Hello
Bot: Hello! Welcome to Customer Support...

You: Where is my order ORD12345?
Bot: Let me check that for you. Your order ORD12345 is currently being processed...

You: This is taking too long, I'm very frustrated!
Bot: I sincerely apologize for the inconvenience you're experiencing...

You: I want to speak to a human
Bot: I'll connect you with a human agent right away...
```

---

## Testing

Run automated tests to verify functionality:

```bash
python test_chatbot.py
```

**Test Coverage:**
- ✅ Intent classification accuracy
- ✅ Sentiment analysis validation
- ✅ Escalation logic triggers
- ✅ Response time benchmarks

---

## Research Evaluation

### Metrics Tracked

| Metric | Description | Target |
|--------|-------------|--------|
| **Customer Satisfaction** | 1-5 star rating | ≥ 4.0/5.0 |
| **Intent Accuracy** | ML classification accuracy | ≥ 85% |
| **Escalation Rate** | % requiring human help | 10-20% |
| **Response Time** | Average processing time | < 100ms |
| **Sentiment Detection** | Sentiment classification | ≥ 80% |

### Exported Data

After each session, the chatbot generates:
- **Console Report**: Summary statistics
- **JSON File**: Complete metrics (`chatbot_metrics_YYYYMMDD_HHMMSS.json`)

**Example JSON Structure:**
```json
{
  "session_info": {...},
  "metrics": {
    "total_interactions": 25,
    "escalations_to_human": 3,
    "average_satisfaction": 4.2,
    "intents_detected": {...},
    "sentiment_distribution": {...}
  },
  "conversation_history": [...]
}
```

---

## Project Structure

```
AI-CHATBOT/
├── chatbot.py                    # Main chatbot implementation
├── test_chatbot.py               # Automated testing suite
├── requirements.txt              # Python dependencies
├── RESEARCH_DOCUMENTATION.md     # Detailed research docs
├── README.md                     # This file
├── LICENSE                       # License information
└── chatbot_model.pkl            # Trained ML model (auto-generated)
```

---

## Research Approach

### 1. Define Objectives
Improve chatbot contextual understanding and personalization in customer service

### 2. Literature Review
Review studies on chatbot NLP, customer satisfaction, and hybrid human-AI systems

### 3. Data Collection
- Real customer-chatbot interaction logs ✅
- Customer satisfaction surveys ✅
- Dissatisfaction cause analysis ✅

### 4. Proposed Methodology
- Advanced NLP with TF-IDF + Naive Bayes ✅
- Enhanced sentiment analysis ✅
- Intelligent human escalation ✅
- Performance metrics tracking ✅

### 5. Evaluation
- Customer satisfaction scores ✅
- Response accuracy measurement ✅
- Escalation rate analysis ✅
- Complaint reduction tracking ✅

---

## Future Enhancements

### Phase 1: Immediate Improvements
- [ ] Expand training data to 500+ examples
- [ ] Add cross-validation for model evaluation
- [ ] Implement multi-language support
- [ ] Create web interface (Flask/FastAPI)

### Phase 2: Advanced Features
- [ ] Integrate transformer models (BERT/RoBERTa)
- [ ] Add FAQ retrieval system
- [ ] Implement user authentication
- [ ] Create admin dashboard with visualizations

### Phase 3: Research Extensions
- [ ] Fine-tune GPT models for domain-specific responses
- [ ] Implement reinforcement learning (RLHF)
- [ ] Add voice interface
- [ ] Develop predictive frustration detection

---

## Technical Details

**Framework**: Python 3.8+  
**ML Library**: scikit-learn  
**NLP**: TF-IDF Vectorization  
**Model**: Multinomial Naive Bayes  
**Data Format**: JSON for metrics export

---

## Contributing

This is a research project. Contributions are welcome!

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/improvement`)
3. Commit your changes (`git commit -m 'Add improvement'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Research Citation

If you use this implementation in your research, please cite:

```bibtex
@misc{ai_chatbot_2026,
  title={ML-Enhanced AI Chatbot for Customer Support},
  author={Ajinkya Suryawanshi},
  year={2026},
  publisher={GitHub},
  url={https://github.com/AjinkyaxSuryawanshi/AI-CHATBOT}
}
```

---

## Contact

**Author**: Ajinkya Suryawanshi  
**Repository**: [AI-CHATBOT](https://github.com/AjinkyaxSuryawanshi/AI-CHATBOT)

For detailed research documentation, see [RESEARCH_DOCUMENTATION.md](RESEARCH_DOCUMENTATION.md)

---

**Last Updated**: January 14, 2026  
**Version**: 2.0 - ML-Enhanced Implementation
A customer support chatbot project focusing on context awareness, sentiment analysis, and machine learning–based intent detection.
# AI Chatbot for Customer Support

## Overview
This project focuses on building and incrementally improving a customer support chatbot.
The chatbot addresses common limitations of traditional chatbots such as irrelevant responses,
lack of conversational context, and poor handling of user emotions.

## Problem Statement
Customers often experience dissatisfaction with customer support chatbots due to
context-insensitive replies, repetitive responses, and failure to recognize user frustration.
This project aims to study these limitations and improve chatbot behavior using
context-aware logic and machine learning techniques.

## Current Features
- Rule-based customer support chatbot
- Intent detection using keyword matching
- Basic sentiment detection (positive / neutral / negative)
- Empathetic responses for dissatisfied users
- Continuous conversation loop (terminal-based)

## Current Limitations
- Limited conversational context memory
- Keyword-based intent detection is fragile
- Follow-up queries may be misunderstood

## Planned Enhancements
- Context-aware multi-turn conversation handling
- Machine learning–based intent classification
- Machine learning–based sentiment analysis
- Improved response relevance and escalation logic

## Tech Stack
- Python
- Rule-based NLP
- (Planned) Scikit-learn for ML models

## Status
Project is under active development as part of an academic research project.
Project when completed will be deployed [SOON]
