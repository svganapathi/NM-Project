import streamlit as st
import joblib
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re

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

# Streamlit app
st.title("Customer Support Chatbot (Streamlit)")

# Initialize chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# User input
user_input = st.text_input("Type your message:", key="user_input")

if user_input:
    # Preprocess input
    processed_input = preprocess_text(user_input)
    
    # Vectorize input
    input_vector = vectorizer.transform([processed_input])
    
    # Predict intent
    intent = model.predict(input_vector)[0]
    
    # Get response
    bot_response = responses.get(intent, 'Sorry, I didn’t understand that. Could you rephrase?')
    
    # Update chat history
    st.session_state.chat_history.append(("You", user_input))
    st.session_state.chat_history.append(("Bot", bot_response))

# Display chat history
for sender, message in st.session_state.chat_history:
    if sender == "You":
        st.write(f"**You**: {message}")
    else:
        st.write(f"**Bot**: {message}")
