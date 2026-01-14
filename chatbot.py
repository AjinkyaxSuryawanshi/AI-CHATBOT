"""
ML-Enhanced AI Chatbot for Customer Support - Research Implementation
Research Problem: Address customer dissatisfaction with AI chatbots through improved 
contextual understanding, personalization, and intelligent human escalation.

Features:
- Machine Learning-based intent classification
- Advanced sentiment analysis
- Context-aware response generation
- Conversation history and personalization
- Intelligent human escalation
- Customer satisfaction tracking
- Performance metrics and evaluation
- Hybrid human-AI support system
"""

import re
import json
import pickle
import numpy as np
from datetime import datetime
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')


class CustomerSupportBot:
    def __init__(self, use_ml=True):
        # Conversation tracking
        self.conversation_history = []
        self.user_name = None
        self.order_id = None
        self.current_context = None
        
        # ML components
        self.use_ml = use_ml
        self.vectorizer = TfidfVectorizer(max_features=500, ngram_range=(1, 2))
        self.intent_classifier = MultinomialNB()
        self.model_trained = False
        
        # Performance metrics
        self.metrics = {
            'total_interactions': 0,
            'escalations_to_human': 0,
            'satisfaction_scores': [],
            'response_times': [],
            'intents_detected': defaultdict(int),
            'sentiment_distribution': defaultdict(int)
        }
        
        # Context and personalization
        self.user_frustration_level = 0
        self.repeated_questions = defaultdict(int)
        self.session_start_time = datetime.now()
        
        # Enhanced patterns (fallback for non-ML mode)
        self.patterns = {
            'greeting': ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening', 'greetings'],
            'goodbye': ['bye', 'goodbye', 'see you', 'exit', 'quit', 'close'],
            'thanks': ['thank', 'thanks', 'appreciate', 'grateful'],
            'refund': ['refund', 'money back', 'return money', 'reimburs'],
            'order_status': ['order', 'status', 'tracking', 'where is my', 'delivery'],
            'cancel': ['cancel', 'cancellation'],
            'shipping': ['shipping', 'delivery time', 'when will', 'arrive'],
            'payment': ['payment', 'pay', 'credit card', 'payment method', 'charge'],
            'product_info': ['product', 'item', 'specification', 'details', 'feature'],
            'complaint': ['complaint', 'issue', 'problem', 'not working', 'broken', 'damaged'],
            'help': ['help', 'support', 'assist', 'what can you'],
            'human': ['speak to human', 'real person', 'agent', 'representative']
        }
        
        # Load or train model
        if self.use_ml:
            self.load_or_train_model()
    
    def load_or_train_model(self):
        """Load pre-trained model or train a new one"""
        try:
            with open('chatbot_model.pkl', 'rb') as f:
                model_data = pickle.load(f)
                self.vectorizer = model_data['vectorizer']
                self.intent_classifier = model_data['classifier']
                self.model_trained = True
                print("✓ ML model loaded successfully")
        except FileNotFoundError:
            print("⚠ No pre-trained model found. Training new model...")
            self.train_model()
    
    def train_model(self):
        """Train ML model with comprehensive training data"""
        # Enhanced training dataset
        training_data = [
            # Greetings
            ("hello", "greeting"), ("hi there", "greeting"), ("good morning", "greeting"),
            ("hey", "greeting"), ("greetings", "greeting"), ("good afternoon", "greeting"),
            
            # Goodbyes
            ("bye", "goodbye"), ("goodbye", "goodbye"), ("see you later", "goodbye"),
            ("exit", "goodbye"), ("quit", "goodbye"), ("close", "goodbye"),
            
            # Thanks
            ("thank you", "thanks"), ("thanks a lot", "thanks"), ("appreciate it", "thanks"),
            ("grateful", "thanks"), ("thanks for help", "thanks"),
            
            # Refunds
            ("i want a refund", "refund"), ("refund my money", "refund"),
            ("how do i get refund", "refund"), ("return money", "refund"),
            ("i need money back", "refund"), ("reimbursement", "refund"),
            
            # Order Status
            ("where is my order", "order_status"), ("track my order", "order_status"),
            ("order status", "order_status"), ("check delivery", "order_status"),
            ("when will it arrive", "order_status"), ("order tracking", "order_status"),
            
            # Cancellation
            ("cancel my order", "cancel"), ("i want to cancel", "cancel"),
            ("cancellation request", "cancel"), ("stop my order", "cancel"),
            
            # Shipping
            ("how long shipping takes", "shipping"), ("delivery time", "shipping"),
            ("when will it be delivered", "shipping"), ("shipping information", "shipping"),    
            ("shipping details", "shipping"),
            ("delivery options", "shipping"),
            ("shipping methods", "shipping"),
            ("estimated delivery", "shipping"),
            ("shipping cost", "shipping"),
            ("track shipment", "shipping"),
            ("where is my package", "shipping"),
            
            # Payment
            ("payment methods", "payment"), ("how can i pay", "payment"),
            ("credit card payment", "payment"), ("payment options", "payment"),
            ("payment information", "payment"),
            ("pay with paypal", "payment"),
            ("secure payment", "payment"),
            ("payment issues", "payment"),
            ("billing information", "payment"),
            ("transaction failed", "payment"),
            ("refund payment", "payment"),
            
            # Product Info
            ("product details", "product_info"), ("tell me about this item", "product_info"),
            ("product specifications", "product_info"), ("item features", "product_info"),
            
            # Complaints
            ("i have a complaint", "complaint"), ("this is not working", "complaint"),
            ("product is broken", "complaint"), ("damaged item", "complaint"),
            ("this is terrible", "complaint"), ("very disappointed", "complaint"),
            ('i am frustrated', "complaint"), ("this is unacceptable", "complaint"),
            ("i hate this", "complaint"), ("worst experience", "complaint"),
            ("this is awful", "complaint"),
            ("i am angry", "complaint"),
            ("i am upset", "complaint"),
            ("this is disgusting", "complaint"),
            ("i will never buy again", "complaint"),
            ("this product is useless", "complaint"),
            ("this is pathetic", "complaint"),
            ("order is damaged", "complaint"),
            ("item not working", "complaint"),
            ("damaged product", "complaint"),
            ("damaged goods", "complaint"),
            ("defective item", "complaint"),
            ("damaged upon arrival", "complaint"),
            ("damaged item received", "complaint"),
            ("broken upon delivery", "complaint"),
            ("received a broken item", "complaint"),

            
            # Help
            ("i need help", "help"), ("can you assist me", "help"),
            ("what can you do", "help"), ("help me please", "help"),
            ("i require assistance", "help"),
            ("i need support", "help"),
            ("can you support me", "help"),
            ("i am looking for help", "help"),
            
            # Human escalation
            ("speak to human", "human"), ("real person", "human"),
            ("talk to agent", "human"), ("customer representative", "human"),
        ]
        
        texts = [text for text, _ in training_data]
        labels = [label for _, label in training_data]
        
        # Train the model
        X = self.vectorizer.fit_transform(texts)
        self.intent_classifier.fit(X, labels)
        self.model_trained = True
        
        # Save the model
        model_data = {
            'vectorizer': self.vectorizer,
            'classifier': self.intent_classifier
        }
        with open('chatbot_model.pkl', 'wb') as f:
            pickle.dump(model_data, f)
        
        print("✓ ML model trained and saved successfully")
    
    def detect_intent(self, user_input):
        """ML-based intent detection with fallback to rule-based"""
        if self.use_ml and self.model_trained:
            try:
                X = self.vectorizer.transform([user_input.lower()])
                intent = self.intent_classifier.predict(X)[0]
                confidence = max(self.intent_classifier.predict_proba(X)[0])
                
                # If confidence is low, fall back to rule-based
                if confidence < 0.4:
                    return self._rule_based_intent(user_input)
                
                return intent
            except:
                return self._rule_based_intent(user_input)
        else:
            return self._rule_based_intent(user_input)
    
    def _rule_based_intent(self, user_input):
        """Fallback rule-based intent detection"""
        user_input = user_input.lower()
        for intent, keywords in self.patterns.items():
            for keyword in keywords:
                if keyword in user_input:
                    return intent
        return 'unknown'

    def detect_sentiment(self, user_input):
        """Enhanced sentiment analysis with weighted scoring"""
        # Extended sentiment lexicons
        positive_words = {
            'good': 1, 'great': 2, 'excellent': 3, 'happy': 2, 'satisfied': 2,
            'love': 3, 'awesome': 3, 'perfect': 3, 'wonderful': 2, 'fantastic': 3,
            'appreciate': 2, 'helpful': 2, 'amazing': 3, 'best': 3
        }
        
        negative_words = {
            'bad': 1, 'terrible': 3, 'awful': 3, 'hate': 3, 'angry': 2,
            'frustrated': 2, 'upset': 2, 'disappointed': 2, 'horrible': 3,
            'worst': 3, 'useless': 2, 'pathetic': 3, 'disgusting': 3,
            'never': 1, 'not': 1, 'no': 1, 'problem': 1, 'issue': 1
        }
        
        user_input = user_input.lower()
        words = user_input.split()
        
        positive_score = sum(positive_words.get(word, 0) for word in words)
        negative_score = sum(negative_words.get(word, 0) for word in words)
        
        # Track frustration level
        if negative_score > positive_score + 2:
            self.user_frustration_level += 1
        elif positive_score > negative_score:
            self.user_frustration_level = max(0, self.user_frustration_level - 1)
        
        # Determine sentiment
        if negative_score > positive_score:
            sentiment = 'negative'
        elif positive_score > negative_score:
            sentiment = 'positive'
        else:
            sentiment = 'neutral'
        
        # Update metrics
        self.metrics['sentiment_distribution'][sentiment] += 1
        
        return sentiment

    def extract_order_id(self, user_input):
        """Extract order ID from user input"""
        patterns = [
            r'[Oo][Rr][Dd]\d+',
            r'#\d+',
            r'order\s+(\d+)',
            r'id\s+(\d+)'
        ]

        for pattern in patterns:
            match = re.search(pattern, user_input)
            if match:
                return match.group(0)
        return None
    
    def should_escalate_to_human(self, user_input, intent):
        """Intelligent escalation logic based on multiple factors"""
        escalation_reasons = []
        
        # Check frustration level
        if self.user_frustration_level >= 3:
            escalation_reasons.append("High frustration detected")
        
        # Check for explicit human request
        if intent == 'human':
            escalation_reasons.append("Direct human request")
        
        # Check for repeated questions
        question_hash = hash(user_input.lower()[:50])
        self.repeated_questions[question_hash] += 1
        if self.repeated_questions[question_hash] >= 2:
            escalation_reasons.append("Repeated question")
        
        # Check for complex complaint
        if intent == 'complaint' and len(user_input.split()) > 15:
            escalation_reasons.append("Complex complaint")
        
        # Check for unknown intent multiple times
        if intent == 'unknown' and len([h for h in self.conversation_history if 'unknown' in str(h)]) >= 2:
            escalation_reasons.append("Multiple unclear requests")
        
        return len(escalation_reasons) > 0, escalation_reasons

    def get_response(self, user_input):
        """Generate context-aware, personalized responses"""
        start_time = datetime.now()
        
        # Detect intent and sentiment
        intent = self.detect_intent(user_input)
        sentiment = self.detect_sentiment(user_input)
        
        # Update metrics
        self.metrics['total_interactions'] += 1
        self.metrics['intents_detected'][intent] += 1
        
        # Check for human escalation
        should_escalate, reasons = self.should_escalate_to_human(user_input, intent)
        if should_escalate:
            self.metrics['escalations_to_human'] += 1
            return self._escalate_to_human(reasons)
        
        # Personalized response prefix based on sentiment and context
        response_prefix = self._get_response_prefix(sentiment, intent)
        
        # Generate response based on intent
        response = self._generate_intent_response(intent, user_input, response_prefix, sentiment)
        
        # Track response time
        response_time = (datetime.now() - start_time).total_seconds()
        self.metrics['response_times'].append(response_time)
        
        return response
    
    def _get_response_prefix(self, sentiment, intent):
        """Generate personalized response prefix"""
        if sentiment == 'negative' and intent not in ['goodbye', 'thanks']:
            if self.user_frustration_level >= 2:
                return "I sincerely apologize for the inconvenience you're experiencing. "
            return "I'm sorry to hear that you're experiencing difficulties. "
        elif sentiment == 'positive':
            return "Great! "
        return ""
    
    def _generate_intent_response(self, intent, user_input, response_prefix, sentiment):
        """Generate response based on detected intent"""
        if intent == 'greeting':
            return "Hello! Welcome to Customer Support. I'm here to help you with any questions or concerns. What can I do for you today?"

        elif intent == 'goodbye':
            return "Thank you for contacting us! If you need anything else, feel free to reach out. Have a great day!"

        elif intent == 'thanks':
            return "You're very welcome! Is there anything else I can help you with today?"

        elif intent == 'refund':
            return response_prefix + "I can help you with refunds. Please provide your order ID (e.g., ORD12345), and I'll process your refund request."

        elif intent == 'order_status':
            order_id = self.extract_order_id(user_input)
            if order_id:
                self.order_id = order_id
                return f"Let me check that for you. Your order {order_id} is currently being processed and should be shipped within 24 hours. You'll receive a tracking number via email."
            return "I'd be happy to check your order status. Please provide your order ID (e.g., ORD12345 or #12345)."

        elif intent == 'cancel':
            return response_prefix + "I can help you cancel your order. Please provide your order ID, and I'll initiate the cancellation process immediately."

        elif intent == 'shipping':
            return "Our shipping times are:\n• Standard: 5-7 business days\n• Express: 2-3 business days\n• Overnight: 1 business day\nWhich option would you like to know more about?"

        elif intent == 'payment':
            return "We accept the following payment methods:\n• Credit/Debit Cards (Visa, MasterCard, Amex)\n• PayPal\n• Apple Pay\n• Google Pay\nAll transactions are secure and encrypted."

        elif intent == 'product_info':
            return "I'd be happy to provide product information. Please tell me which product you're interested in, or provide the product name/ID."

        elif intent == 'complaint':
            self.current_context = 'complaint'
            return response_prefix + "I'm truly sorry to hear about this issue. Please provide details about the problem (product name, order ID, what went wrong), and I'll ensure this is resolved quickly."

        elif intent == 'help':
            return (
                "I'm here to assist you with:\n"
                "📦 Order tracking and status\n"
                "💰 Refunds and returns\n"
                "❌ Order cancellations\n"
                "🚚 Shipping information\n"
                "💳 Payment methods\n"
                "📝 Product information\n"
                "⚠️ Complaints and issues\n"
                "👤 Connect with human agent\n\n"
                "What would you like help with?"
            )

        elif intent == 'human':
            self.metrics['escalations_to_human'] += 1
            return "I'll connect you with a human agent right away. Please hold for a moment..."

        else:
            # Handle context-based responses
            if self.current_context == 'complaint':
                self.current_context = None
                return (
                    f"Thank you for providing those details. "
                    f"Your complaint has been registered (Ticket #C{self.metrics['total_interactions']:04d}). "
                    "Our support team will contact you within 24 hours to resolve this issue. "
                    "Is there anything else I can help you with?"
                )

            if sentiment == 'negative':
                return response_prefix + (
                    "I understand your frustration. Could you please provide more details about "
                    "what went wrong? I'm here to help resolve this for you."
                )
    
            return "I'm not sure I understood that correctly. Could you please rephrase your question or type 'help' to see what I can assist you with?"
    
    def _escalate_to_human(self, reasons):
        """Handle escalation to human agent"""
        reasons_str = ", ".join(reasons)
        return (
            f"I understand this situation requires personalized attention. "
            f"I'm connecting you with a human agent now who can better assist you. "
            f"(Escalation reason: {reasons_str})\n"
            f"Estimated wait time: 2-3 minutes. Thank you for your patience."
        )


    def log_conversation(self, user_input, bot_response, intent, sentiment):
        """Enhanced conversation logging with metadata"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.conversation_history.append({
            'timestamp': timestamp,
            'user': user_input,
            'bot': bot_response,
            'intent': intent,
            'sentiment': sentiment,
            'frustration_level': self.user_frustration_level
        })
    
    def collect_satisfaction_feedback(self):
        """Collect customer satisfaction score"""
        print("\n" + "="*60)
        print("How satisfied are you with this interaction?")
        print("1 - Very Dissatisfied")
        print("2 - Dissatisfied")
        print("3 - Neutral")
        print("4 - Satisfied")
        print("5 - Very Satisfied")
        
        while True:
            try:
                score = input("Your rating (1-5): ").strip()
                if score.isdigit() and 1 <= int(score) <= 5:
                    self.metrics['satisfaction_scores'].append(int(score))
                    return int(score)
                else:
                    print("Please enter a number between 1 and 5.")
            except:
                print("Invalid input. Please enter a number between 1 and 5.")
    
    def generate_metrics_report(self):
        """Generate comprehensive performance metrics"""
        session_duration = (datetime.now() - self.session_start_time).total_seconds() / 60
        
        report = "\n" + "="*60
        report += "\n📊 CHATBOT PERFORMANCE METRICS (Research Evaluation)\n"
        report += "="*60 + "\n"
        
        # Basic metrics
        report += f"\n📈 Session Statistics:\n"
        report += f"  • Total Interactions: {self.metrics['total_interactions']}\n"
        report += f"  • Session Duration: {session_duration:.2f} minutes\n"
        report += f"  • Human Escalations: {self.metrics['escalations_to_human']}\n"
        report += f"  • Escalation Rate: {(self.metrics['escalations_to_human']/max(1, self.metrics['total_interactions'])*100):.1f}%\n"
        
        # Response time
        if self.metrics['response_times']:
            avg_response = np.mean(self.metrics['response_times']) * 1000
            report += f"  • Avg Response Time: {avg_response:.2f}ms\n"
        
        # Intent distribution
        report += f"\n🎯 Intent Distribution:\n"
        for intent, count in sorted(self.metrics['intents_detected'].items(), key=lambda x: x[1], reverse=True):
            percentage = (count / max(1, self.metrics['total_interactions'])) * 100
            report += f"  • {intent.replace('_', ' ').title()}: {count} ({percentage:.1f}%)\n"
        
        # Sentiment analysis
        report += f"\n😊 Sentiment Analysis:\n"
        for sentiment, count in self.metrics['sentiment_distribution'].items():
            percentage = (count / max(1, self.metrics['total_interactions'])) * 100
            report += f"  • {sentiment.title()}: {count} ({percentage:.1f}%)\n"
        
        # Customer satisfaction
        if self.metrics['satisfaction_scores']:
            avg_satisfaction = np.mean(self.metrics['satisfaction_scores'])
            report += f"\n⭐ Customer Satisfaction:\n"
            report += f"  • Average Score: {avg_satisfaction:.2f}/5.00\n"
            report += f"  • Total Ratings: {len(self.metrics['satisfaction_scores'])}\n"
            
            # Satisfaction distribution
            for score in range(1, 6):
                count = self.metrics['satisfaction_scores'].count(score)
                if count > 0:
                    report += f"  • {score} stars: {count}\n"
        
        # Model performance
        report += f"\n🤖 AI Model Performance:\n"
        report += f"  • ML Model Active: {'Yes' if self.use_ml and self.model_trained else 'No'}\n"
        report += f"  • Context Tracking: Enabled\n"
        report += f"  • Sentiment Analysis: Enhanced\n"
        
        report += "\n" + "="*60 + "\n"
        
        return report
    
    def save_metrics_to_file(self):
        """Save metrics to JSON file for research analysis"""
        metrics_data = {
            'session_info': {
                'start_time': self.session_start_time.isoformat(),
                'end_time': datetime.now().isoformat(),
                'duration_minutes': (datetime.now() - self.session_start_time).total_seconds() / 60
            },
            'metrics': {
                'total_interactions': self.metrics['total_interactions'],
                'escalations_to_human': self.metrics['escalations_to_human'],
                'escalation_rate': self.metrics['escalations_to_human']/max(1, self.metrics['total_interactions']),
                'average_response_time_ms': np.mean(self.metrics['response_times']) * 1000 if self.metrics['response_times'] else 0,
                'intents_detected': dict(self.metrics['intents_detected']),
                'sentiment_distribution': dict(self.metrics['sentiment_distribution']),
                'satisfaction_scores': self.metrics['satisfaction_scores'],
                'average_satisfaction': np.mean(self.metrics['satisfaction_scores']) if self.metrics['satisfaction_scores'] else 0
            },
            'conversation_history': self.conversation_history
        }
        
        filename = f"chatbot_metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(metrics_data, f, indent=2)
        
        print(f"✓ Metrics saved to {filename}")

    def run(self):
        """Main chatbot loop with enhanced features"""
        print("=" * 60)
        print("🤖 ML-Enhanced Customer Support Chatbot")
        print("   Research Implementation v2.0")
        print("=" * 60)
        print("Bot: Hello! I'm your AI-powered virtual assistant.")
        print("     I use machine learning to better understand your needs.")
        print("     How can I help you today?")
        print("\n(Type 'bye' or 'quit' to exit)")
        print("="* 60 + "\n")

        while True:
            try:
                user_input = input("You: ").strip()

                if not user_input:
                    continue

                intent = self.detect_intent(user_input)
                sentiment = self.detect_sentiment(user_input)

                if intent == 'goodbye':
                    response = self.get_response(user_input)
                    print(f"Bot: {response}\n")
                    
                    # Collect feedback
                    satisfaction_score = self.collect_satisfaction_feedback()
                    
                    # Show metrics
                    print(self.generate_metrics_report())
                    
                    # Save to file
                    self.save_metrics_to_file()
                    break

                response = self.get_response(user_input)
                print(f"Bot: {response}\n")
                self.log_conversation(user_input, response, intent, sentiment)
                
            except KeyboardInterrupt:
                print("\n\nBot: Session interrupted. Saving metrics...")
                self.save_metrics_to_file()
                break
            except Exception as e:
                print(f"Bot: I encountered an error. Let me connect you with a human agent.")
                print(f"     Error details: {str(e)}")
                self.metrics['escalations_to_human'] += 1


def main():
    bot = CustomerSupportBot()
    bot.run()


if __name__ == "__main__":
    main()
