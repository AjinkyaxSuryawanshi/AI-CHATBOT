"""
Training Script for ML-Enhanced Chatbot
Loads training data from CSV and trains the model
"""

import pickle
import csv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB


def load_training_data(csv_file='data/training_data.csv'):
    """Load training data from CSV file"""
    training_data = []
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            training_data.append((row['text'], row['intent']))
    
    return training_data


def train_model(training_data):
    """Train the ML model"""
    texts = [text for text, _ in training_data]
    labels = [label for _, label in training_data]
    
    # Create and train vectorizer and classifier
    vectorizer = TfidfVectorizer(max_features=500, ngram_range=(1, 2))
    intent_classifier = MultinomialNB()
    
    X = vectorizer.fit_transform(texts)
    intent_classifier.fit(X, labels)
    
    return vectorizer, intent_classifier


def save_model(vectorizer, classifier, model_file='chatbot_model.pkl'):
    """Save the trained model"""
    model_data = {
        'vectorizer': vectorizer,
        'classifier': classifier
    }
    
    with open(model_file, 'wb') as f:
        pickle.dump(model_data, f)
    
    print(f"✓ Model saved to {model_file}")


def main():
    """Main training pipeline"""
    print("="*60)
    print("Training ML Model for Customer Support Chatbot")
    print("="*60 + "\n")
    
    # Load training data
    print("Loading training data from CSV...")
    training_data = load_training_data()
    print(f"✓ Loaded {len(training_data)} training examples")
    
    # Train model
    print("\nTraining model...")
    vectorizer, classifier = train_model(training_data)
    print("✓ Model trained successfully")
    
    # Save model
    print("\nSaving model...")
    save_model(vectorizer, classifier)
    
    print("\n" + "="*60)
    print("Training completed successfully!")
    print("="*60)


if __name__ == "__main__":
    main()
