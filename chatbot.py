"""
Advanced Rule-Based Chatbot for Customer Support
Features:
- Continuous conversation loop
- Multiple intent recognition
- Context-aware responses
- Conversation history
- Sentiment detection
- Comprehensive customer support topics
"""

import re
from datetime import datetime


class CustomerSupportBot:
    def __init__(self):
        self.conversation_history = []
        self.user_name = None
        self.order_id = None
        self.current_context = None

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

    def detect_intent(self, user_input):
        user_input = user_input.lower()
        for intent, keywords in self.patterns.items():
            for keyword in keywords:
                if keyword in user_input:
                    return intent
        return 'unknown'

    def detect_sentiment(self, user_input):
        positive_words = ['good', 'great', 'excellent', 'happy', 'satisfied', 'love', 'awesome']
        negative_words = ['bad', 'terrible', 'awful', 'hate', 'angry', 'frustrated', 'upset', 'disappointed']

        user_input = user_input.lower()

        positive_count = sum(1 for word in positive_words if word in user_input)
        negative_count = sum(1 for word in negative_words if word in user_input)

        if negative_count > positive_count:
            return 'negative'
        elif positive_count > negative_count:
            return 'positive'
        return 'neutral'

    def extract_order_id(self, user_input):
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

    # 🔧 FIXED BLOCK (ONLY THIS WAS TOUCHED)
    def get_response(self, user_input):
        intent = self.detect_intent(user_input)
        sentiment = self.detect_sentiment(user_input)

        if sentiment == 'negative' and intent not in ['goodbye', 'thanks']:
            response_prefix = "I'm sorry to hear that you're experiencing difficulties. "
        else:
            response_prefix = ""

        if intent == 'greeting':
            return "Hello! Welcome to Customer Support. I'm here to help you. What can I do for you today?"

        elif intent == 'goodbye':
            return "Thank you for contacting us! Have a great day! 👋"

        elif intent == 'thanks':
            return "You're welcome! Is there anything else I can help you with?"

        elif intent == 'refund':
            return response_prefix + "I can help you with refunds. Please provide your order ID."

        elif intent == 'order_status':
            order_id = self.extract_order_id(user_input)
            if order_id:
                self.order_id = order_id
                return f"Your order {order_id} is currently being processed."
            return "Please provide your order ID (e.g., ORD12345)."

        elif intent == 'cancel':
            return response_prefix + "I can help cancel your order. Please provide your order ID."

        elif intent == 'shipping':
            return "Standard shipping takes 5-7 business days."

        elif intent == 'payment':
            return "We accept credit cards, debit cards, and PayPal."

        elif intent == 'product_info':
            return "Please tell me which product you want information about."

        elif intent == 'complaint':
            self.current_context = 'complaint'
            return response_prefix + "I’m sorry about that. Which product is affected?"

        elif intent == 'help':
            return (
                "I can help you with:\n"
                "• Order status\n"
                "• Refunds\n"
                "• Cancellations\n"
                "• Shipping\n"
                "• Payments\n"
                "• Complaints\n"
            )

        elif intent == 'human':
            return "Connecting you to a human agent. Please wait..."

        else:
            # Handle complaint follow-up
            if self.current_context == 'complaint':
                self.current_context = None
                return (
                    f"Thank you for the details. "
                    f"Your complaint regarding '{user_input}' has been registered. "
                    "Our support team will contact you shortly."
                )

            if sentiment == 'negative':
                return response_prefix + (
                    "I'm really sorry you're feeling this way. "
                    "Could you please tell me what went wrong with the service or order?"
                )
    
            return "I'm not sure I understood that correctly. Could you please rephrase or type 'help'."


    def log_conversation(self, user_input, bot_response):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.conversation_history.append({
            'timestamp': timestamp,
            'user': user_input,
            'bot': bot_response
        })

    def run(self):
        print("=" * 60)
        print("Customer Support Chatbot")
        print("=" * 60)
        print("Bot: Hello! I'm your virtual assistant. How can I help you today?")
        print("(Type 'bye' or 'quit' to exit)\n")

        while True:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            if self.detect_intent(user_input) == 'goodbye':
                response = self.get_response(user_input)
                print(f"Bot: {response}")
                break

            response = self.get_response(user_input)
            print(f"Bot: {response}")
            self.log_conversation(user_input, response)


def main():
    bot = CustomerSupportBot()
    bot.run()


if __name__ == "__main__":
    main()
