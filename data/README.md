# Data Directory

This directory contains training and testing datasets for the ML-Enhanced Customer Support Chatbot.

## Files

### Training Data
- **training_data.csv** - Training dataset for intent classification
  - Format: `text,intent`
  - Contains 100+ examples across 12 intent categories
  - Used by `train_model.py` and `chatbot.py`

### Testing Data
- **test_cases.csv** - Test cases for intent classification
  - Format: `user_input,expected_intent,description`
  - Contains 8 test cases covering main intents
  - Used by `test_chatbot.py`

- **sentiment_test_cases.csv** - Test cases for sentiment analysis
  - Format: `sentence,expected_sentiment`
  - Contains 5 test cases (positive, negative, neutral)
  - Used by `test_chatbot.py`

## Intent Categories

The chatbot recognizes 12 intent types:
1. **greeting** - Hello, hi, good morning, etc.
2. **goodbye** - Bye, exit, quit, etc.
3. **thanks** - Thank you, appreciate, etc.
4. **refund** - Refund requests, money back, etc.
5. **order_status** - Order tracking, delivery status, etc.
6. **cancel** - Order cancellation requests
7. **shipping** - Shipping information, delivery time, etc.
8. **payment** - Payment methods, billing info, etc.
9. **product_info** - Product details, specifications, etc.
10. **complaint** - Issues, problems, broken items, etc.
11. **help** - General assistance requests
12. **human** - Requests to speak with human agent

## Adding More Training Data

To improve model accuracy, add more examples to `training_data.csv`:

```csv
text,intent
new example text,intent_category
another example,intent_category
```

After adding data, retrain the model:
```bash
python train_model.py
```

## File Formats

All CSV files use:
- Encoding: UTF-8
- Separator: Comma (,)
- Header row: Yes
- Quotes: Optional (used for text with commas)
