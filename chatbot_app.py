import random
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
import pandas as pd

data = {
    "text": ["Hi", "Hello", "Goodbye", "Thanks", "I need help", "Can you help me?", "Bye", "Thank you"],
    "intent": ["greeting", "greeting", "goodbye", "thanks", "support", "support", "goodbye", "thanks"]
}
df = pd.DataFrame(data)

X_train, X_test, y_train, y_test = train_test_split(df["text"], df["intent"], test_size=0.25, random_state=42)

pipeline_lr = make_pipeline(TfidfVectorizer(), LogisticRegression())
pipeline_rf = make_pipeline(TfidfVectorizer(), RandomForestClassifier())

pipeline_lr.fit(X_train, y_train)
pipeline_rf.fit(X_train, y_train)

st.set_page_config(page_title="Smart Chatbot", page_icon="🤖")
st.title("🤖 Customer Support Chatbot")
model_choice = st.radio("Choose Model", ["Logistic Regression", "Random Forest"])
user_input = st.text_input("You:", placeholder="Type your message here...")

if user_input:
    model = pipeline_lr if model_choice == "Logistic Regression" else pipeline_rf
    prediction = model.predict([user_input])[0]
    st.write(f"**Intent Detected:** {prediction}")