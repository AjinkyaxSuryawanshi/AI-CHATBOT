"""
Test Script for ML-Enhanced Chatbot
Validates chatbot functionality and generates sample metrics
"""

from chatbot import CustomerSupportBot
import time
import csv
import os


def load_test_cases(csv_file='data/test_cases.csv'):
    """Load test cases from CSV file"""
    test_cases = []
    
    if not os.path.exists(csv_file):
        print(f"⚠ Test cases file not found: {csv_file}")
        print("Using default test cases...")
        return [
            ("Hello", "greeting", "Greeting detection"),
            ("Where is my order ORD12345?", "order_status", "Order status with ID"),
            ("I want a refund", "refund", "Refund request"),
            ("This product is broken", "complaint", "Complaint detection"),
            ("I need help", "help", "Help request"),
            ("Connect me to a human", "human", "Human escalation"),
            ("Thank you", "thanks", "Thanks detection"),
            ("Bye", "goodbye", "Goodbye detection"),
        ]
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                test_cases.append((row['user_input'], row['expected_intent'], row['description']))
    except Exception as e:
        print(f"⚠ Error loading test cases: {e}")
        print("Using default test cases...")
        test_cases = [
            ("Hello", "greeting", "Greeting detection"),
            ("Where is my order ORD12345?", "order_status", "Order status with ID"),
            ("I want a refund", "refund", "Refund request"),
            ("This product is broken", "complaint", "Complaint detection"),
            ("I need help", "help", "Help request"),
            ("Connect me to a human", "human", "Human escalation"),
            ("Thank you", "thanks", "Thanks detection"),
            ("Bye", "goodbye", "Goodbye detection"),
        ]
    
    return test_cases


def load_sentiment_test_cases(csv_file='data/sentiment_test_cases.csv'):
    """Load sentiment test cases from CSV file"""
    test_sentences = []
    
    if not os.path.exists(csv_file):
        print(f"⚠ Sentiment test cases file not found: {csv_file}")
        print("Using default sentiment test cases...")
        return [
            ("This is great! I love it!", "positive"),
            ("This is terrible and frustrating", "negative"),
            ("Can you help me with this?", "neutral"),
            ("I'm very angry and disappointed", "negative"),
            ("Excellent service, thank you!", "positive"),
        ]
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                test_sentences.append((row['sentence'], row['expected_sentiment']))
    except Exception as e:
        print(f"⚠ Error loading sentiment test cases: {e}")
        print("Using default sentiment test cases...")
        test_sentences = [
            ("This is great! I love it!", "positive"),
            ("This is terrible and frustrating", "negative"),
            ("Can you help me with this?", "neutral"),
            ("I'm very angry and disappointed", "negative"),
            ("Excellent service, thank you!", "positive"),
        ]
    
    return test_sentences


def run_automated_tests():
    """Run automated test cases"""
    print("="*60)
    print("🧪 AUTOMATED CHATBOT TESTING")
    print("="*60 + "\n")
    
    bot = CustomerSupportBot(use_ml=True)
    
    # Load test cases from CSV
    test_cases = load_test_cases()
    
    results = []
    
    for user_input, expected_intent, description in test_cases:
        detected_intent = bot.detect_intent(user_input)
        sentiment = bot.detect_sentiment(user_input)
        response = bot.get_response(user_input)
        
        passed = detected_intent == expected_intent
        results.append({
            'test': description,
            'input': user_input,
            'expected': expected_intent,
            'detected': detected_intent,
            'sentiment': sentiment,
            'passed': passed
        })
        
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status} | {description}")
        print(f"  Input: {user_input}")
        print(f"  Intent: {detected_intent} (expected: {expected_intent})")
        print(f"  Sentiment: {sentiment}")
        print(f"  Response: {response[:80]}...")
        print()
    
    # Summary
    total = len(results)
    passed = sum(1 for r in results if r['passed'])
    accuracy = (passed / total) * 100
    
    print("="*60)
    print(f"📊 TEST RESULTS: {passed}/{total} passed ({accuracy:.1f}%)")
    print("="*60)
    
    return results, accuracy


def test_sentiment_analysis():
    """Test sentiment detection"""
    print("\n" + "="*60)
    print("😊 SENTIMENT ANALYSIS TEST")
    print("="*60 + "\n")
    
    bot = CustomerSupportBot(use_ml=True)
    
    # Load sentiment test cases from CSV
    test_sentences = load_sentiment_test_cases()
    
    correct = 0
    for sentence, expected in test_sentences:
        detected = bot.detect_sentiment(sentence)
        match = "✓" if detected == expected else "✗"
        print(f"{match} '{sentence}'")
        print(f"   Expected: {expected}, Detected: {detected}\n")
        if detected == expected:
            correct += 1
    
    accuracy = (correct / len(test_sentences)) * 100
    print(f"Sentiment Accuracy: {accuracy:.1f}%\n")


def test_escalation_logic():
    """Test human escalation triggers"""
    print("\n" + "="*60)
    print("🚨 ESCALATION LOGIC TEST")
    print("="*60 + "\n")
    
    bot = CustomerSupportBot(use_ml=True)
    
    # Simulate frustrated customer
    print("Scenario: Customer asks same question 3 times")
    for i in range(3):
        response = bot.get_response("Where is my order?")
        print(f"  Attempt {i+1}: {'ESCALATED' if 'human agent' in response.lower() else 'Normal response'}")
    
    print("\nScenario: High frustration keywords")
    frustrating_input = "This is terrible, awful, and I'm very angry and frustrated!"
    bot.detect_sentiment(frustrating_input)  # Build frustration
    bot.detect_sentiment(frustrating_input)
    bot.detect_sentiment(frustrating_input)
    response = bot.get_response(frustrating_input)
    print(f"  Frustration level: {bot.user_frustration_level}")
    print(f"  Response: {'ESCALATED' if 'human agent' in response.lower() else 'Normal'}")
    
    print("\nScenario: Direct human request")
    response = bot.get_response("I want to speak to a real person")
    print(f"  Response: {'ESCALATED' if 'human agent' in response.lower() else 'Normal'}")


def performance_benchmark():
    """Benchmark response time"""
    print("\n" + "="*60)
    print("⚡ PERFORMANCE BENCHMARK")
    print("="*60 + "\n")
    
    bot = CustomerSupportBot(use_ml=True)
    
    test_inputs = [
        "Hello",
        "Where is my order?",
        "I need a refund for ORD12345",
        "This is broken and not working",
        "Thank you for your help"
    ] * 20  # 100 total queries
    
    start_time = time.time()
    for inp in test_inputs:
        bot.get_response(inp)
    end_time = time.time()
    
    total_time = end_time - start_time
    avg_time = (total_time / len(test_inputs)) * 1000
    
    print(f"Total queries: {len(test_inputs)}")
    print(f"Total time: {total_time:.2f}s")
    print(f"Average response time: {avg_time:.2f}ms")
    print(f"Queries per second: {len(test_inputs)/total_time:.1f}")


if __name__ == "__main__":
    # Run all tests
    results, accuracy = run_automated_tests()
    test_sentiment_analysis()
    test_escalation_logic()
    performance_benchmark()
    
    print("\n" + "="*60)
    print("✅ ALL TESTS COMPLETED")
    print("="*60)
