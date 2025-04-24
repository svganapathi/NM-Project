import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline

intents = {
    "greeting": ["Hi", "Hello", "Hey"],
    "goodbye": ["Bye", "Goodbye", "See you"],
    "thanks": ["Thanks", "Thank you"],
    "support": ["I need help", "Can you help me?", "Support"]
}

X_train, y_train = [], []
for tag, patterns in intents.items():
    for pattern in patterns:
        X_train.append(pattern)
        y_train.append(tag)

model = make_pipeline(TfidfVectorizer(), LogisticRegression())
model.fit(X_train, y_train)

print("Chatbot is ready! Type 'quit' to exit.")
while True:
    user_input = input("You: ")
    if user_input.lower() == 'quit':
        print("Bot: Goodbye!")
        break
    prediction = model.predict([user_input])[0]
    print(f"Bot: Detected intent - {prediction}")