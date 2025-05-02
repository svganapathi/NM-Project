from flask import Flask, request, jsonify, send_from_directory
import joblib
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re

# Initialize Flask app
app = Flask(__name__, static_folder='static', template_folder='templates')

# Download NLTK data
nltk.download('punkt')
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

# Load pre-trained model and vectorizer
model = joblib.load('intent_classifier.pkl')
vectorizer = joblib.load('tfidf_vectorizer.pkl')

# Predefined responses for intents
responses = {
    'billing': 'Please provide your billing ID, and I can assist with your payment query.',
    'technical': 'It sounds like a technical issue. Could you describe the error in detail?',
    'product': 'Can you specify which product you have a question about?',
    'other': 'I’m not sure how to help with that. Let me connect you to a human agent.'
}

# Text preprocessing function
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    tokens = word_tokenize(text)
    tokens = [t for t in tokens if t not in stop_words]
    return ' '.join(tokens)

# Route for chatbot API
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('message', '')
    
    # Preprocess input
    processed_input = preprocess_text(user_input)
    
    # Vectorize input
    input_vector = vectorizer.transform([processed_input])
    
    # Predict intent
    intent = model.predict(input_vector)[0]
    
    # Get response
    response = responses.get(intent, 'Sorry, I didn’t understand that. Could you rephrase?')
    
    return jsonify({'response': response, 'intent': intent})

# Route for serving the frontend
@app.route('/')
def index():
    return send_from_directory(app.template_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
