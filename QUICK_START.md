# 🚀 Quick Start Guide - ML Chatbot

## ⚡ Installation (30 seconds)

```bash
# Navigate to project directory
cd "e:\Ajinkya\IT\VS code\Chatbot"

# Install dependencies (already done!)
python -m pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org scikit-learn numpy

# Verify installation
python test_chatbot.py
```

---

## 🎮 Running the Chatbot

### Interactive Mode
```bash
python chatbot.py
```

**What happens:**
1. ✅ Loads/trains ML model (first time: ~2 seconds)
2. ✅ Starts interactive conversation
3. ✅ Tracks metrics in real-time
4. ✅ Generates report on exit

### Test Mode
```bash
python test_chatbot.py
```

**Tests performed:**
- Intent classification (8 test cases)
- Sentiment analysis (5 test cases)
- Escalation logic (3 scenarios)
- Performance benchmark (100 queries)

---

## 💬 Example Conversations

### Normal Customer
```
You: Hello
Bot: Hello! Welcome to Customer Support. I'm here to help you with any questions or concerns...

You: Where is my order ORD12345?
Bot: Let me check that for you. Your order ORD12345 is currently being processed...

You: Thank you!
Bot: You're very welcome! Is there anything else I can help you with today?

You: No, bye
Bot: Thank you for contacting us! If you need anything else, feel free to reach out...
[Satisfaction survey appears]
[Metrics report generated]
[JSON file saved]
```

### Frustrated Customer (Escalation)
```
You: Where is my order?
Bot: I'd be happy to check your order status. Please provide your order ID...

You: I already told you! This is terrible!
Bot: I'm sorry to hear that you're experiencing difficulties. Could you please provide more details...

You: This is awful and frustrating! I've been waiting forever!
Bot: I sincerely apologize for the inconvenience you're experiencing...

You: Where is my order? (repeated)
Bot: I understand this situation requires personalized attention. I'm connecting you 
     with a human agent now who can better assist you.
     (Escalation reason: Repeated question, High frustration detected)
     Estimated wait time: 2-3 minutes. Thank you for your patience.
```

---

## 📊 Understanding the Metrics Report

After typing "bye", you'll see:

```
============================================================
📊 CHATBOT PERFORMANCE METRICS (Research Evaluation)
============================================================

📈 Session Statistics:
  • Total Interactions: 12
  • Session Duration: 3.45 minutes
  • Human Escalations: 1
  • Escalation Rate: 8.3%
  • Avg Response Time: 0.85ms

🎯 Intent Distribution:
  • Order Status: 5 (41.7%)
  • Greeting: 2 (16.7%)
  • Refund: 1 (8.3%)
  • Help: 1 (8.3%)
  • Goodbye: 1 (8.3%)
  • Unknown: 2 (16.7%)

😊 Sentiment Analysis:
  • Neutral: 7 (58.3%)
  • Negative: 3 (25.0%)
  • Positive: 2 (16.7%)

⭐ Customer Satisfaction:
  • Average Score: 4.00/5.00
  • Total Ratings: 1
  • 4 stars: 1

🤖 AI Model Performance:
  • ML Model Active: Yes
  • Context Tracking: Enabled
  • Sentiment Analysis: Enhanced
```

---

## 📁 Generated Files

### After Training (First Run)
```
chatbot_model.pkl  (saved ML model)
```

### After Each Session
```
chatbot_metrics_20260114_143052.json  (full session data)
```

**JSON Contents:**
- Session timestamps
- All metrics (escalation rate, satisfaction, etc.)
- Complete conversation history with metadata
- Intent and sentiment distribution

---

## 🔍 Troubleshooting

### Model Training Takes Time
**Normal:** First run trains the model (~2 seconds)  
**Solution:** Model is saved and loads instantly on subsequent runs

### Import Errors
**Error:** `ModuleNotFoundError: No module named 'numpy'`  
**Solution:**
```bash
python -m pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org numpy scikit-learn
```

### Low Intent Accuracy
**Normal:** 75% accuracy with basic training data  
**Solution:** Add more training examples in `train_model()` method

---

## 🎯 Intents Supported

| Intent | Example Phrases | Response Type |
|--------|----------------|---------------|
| **greeting** | "hello", "hi", "good morning" | Welcome message |
| **order_status** | "where is my order", "track ORD123" | Status with ID extraction |
| **refund** | "I want a refund", "money back" | Refund process |
| **cancel** | "cancel my order" | Cancellation |
| **shipping** | "how long shipping", "delivery time" | Shipping options |
| **payment** | "payment methods", "how to pay" | Payment info |
| **product_info** | "product details", "features" | Product request |
| **complaint** | "broken", "not working" | Empathy + resolution |
| **help** | "help me", "what can you do" | Menu of options |
| **human** | "speak to agent", "real person" | Escalation |
| **thanks** | "thank you", "thanks" | Acknowledgment |
| **goodbye** | "bye", "quit", "exit" | Farewell + metrics |

---

## 🔧 Customization Guide

### Add New Intents

**1. Add training data** (in `train_model()`)
```python
training_data = [
    # ... existing data ...
    
    # New intent: "technical_support"
    ("my wifi is not working", "technical_support"),
    ("internet connection problem", "technical_support"),
    ("reset my password", "technical_support"),
]
```

**2. Add response** (in `_generate_intent_response()`)
```python
elif intent == 'technical_support':
    return "I'll help you with technical issues. Please describe the problem..."
```

**3. Add pattern** (fallback, in `__init__`)
```python
self.patterns = {
    # ... existing patterns ...
    'technical_support': ['wifi', 'internet', 'password', 'login', 'technical'],
}
```

### Adjust Escalation Threshold
```python
# In should_escalate_to_human()
if self.user_frustration_level >= 3:  # Change from 3 to 2 for earlier escalation
```

### Change Confidence Threshold
```python
# In detect_intent()
if confidence < 0.4:  # Change from 0.4 to 0.5 for stricter ML
```

---

## 📚 File Overview

```
AI-CHATBOT/
├── chatbot.py                    # 🤖 Main chatbot (440 lines, ML-powered)
├── test_chatbot.py               # 🧪 Automated tests (160 lines)
├── requirements.txt              # 📦 Dependencies
├── README.md                     # 📖 Project overview
├── RESEARCH_DOCUMENTATION.md     # 🔬 Full research guide (500+ lines)
├── IMPLEMENTATION_SUMMARY.md     # ✅ Implementation results
├── QUICK_START.md               # 🚀 This file
└── LICENSE                      # ⚖️ MIT License

Generated after use:
├── chatbot_model.pkl            # 🧠 Trained ML model
└── chatbot_metrics_*.json       # 📊 Session data
```

---

## 🎓 Research Use

### Collect Data for Analysis
1. Run multiple sessions with different scenarios
2. Collect all `chatbot_metrics_*.json` files
3. Aggregate results:

```python
import json
import glob

metrics_files = glob.glob('chatbot_metrics_*.json')
all_data = []

for file in metrics_files:
    with open(file, 'r') as f:
        all_data.append(json.load(f))

# Calculate aggregate metrics
total_interactions = sum(d['metrics']['total_interactions'] for d in all_data)
avg_satisfaction = sum(d['metrics']['average_satisfaction'] for d in all_data) / len(all_data)
avg_escalation_rate = sum(d['metrics']['escalation_rate'] for d in all_data) / len(all_data)

print(f"Across {len(all_data)} sessions:")
print(f"  Total Interactions: {total_interactions}")
print(f"  Avg Satisfaction: {avg_satisfaction:.2f}/5.0")
print(f"  Avg Escalation Rate: {avg_escalation_rate*100:.1f}%")
```

---

## 💡 Tips for Best Results

1. **Train with real data**: Add actual customer conversations to training data
2. **Monitor escalation rate**: Aim for 10-20% (too low = users frustrated, too high = over-escalating)
3. **Track satisfaction**: Target ≥ 4.0/5.0 average
4. **Analyze failures**: Review conversations with low satisfaction scores
5. **Iterate**: Add new intents based on "unknown" classifications

---

## 🎉 You're Ready!

Your ML-enhanced chatbot is production-ready for research. Start with:

```bash
# Run a test session
python chatbot.py

# Review the automated tests
python test_chatbot.py

# Check the documentation
# - README.md for overview
# - RESEARCH_DOCUMENTATION.md for methodology
# - IMPLEMENTATION_SUMMARY.md for results
```

**Happy researching! 🚀🤖**
