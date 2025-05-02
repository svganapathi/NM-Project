import streamlit as st
import re
import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Function to get chatbot response using regex or fallback
def get_chatbot_response(user_input):
    user_input = user_input.lower().strip()

    responses = {
        r"(hi|hello|hey)": "Hello! Welcome to our customer support chatbot. How can I assist you today?",
        r"track.*order|order.*status": "Please provide your order ID, and I'll check the status for you!",
        r"return.*policy|how.*return": "You can return items within 30 days. Need help with a return?",
        r"contact.*support|talk.*human": "You can reach our human support team at support@example.com or call 1-800-123-4567.",
        r"product.*info|tell.*products": "We offer a wide range of products! Could you specify which product or category you're interested in?",
        r"thank.*|thanks": "You're welcome! Happy to help.",
        r"bye|goodbye": "Goodbye! Feel free to reach out anytime.",
        r"payment.*issue|problem.*payment": "Sorry to hear about your payment issue. Please check your payment method or contact support@example.com for assistance.",
        r"delivery.*time|when.*deliver": "Delivery times depend on your location. Please provide your order ID or zip code.",
        r"account.*login|can\'t.*login": "If you're having trouble logging in, try resetting your password or contact support@example.com.",
        r"product.*available|in.*stock": "Could you specify the product name or ID? I'll check its availability for you.",
        r"cancel.*order|how.*cancel": "To cancel an order, please provide your order ID. Cancellations are possible within 24 hours of purchase.",
        r"discount.*code|promo.*code": "Check our website for promotions or use a valid promo code at checkout.",
        r"refund.*status|where.*refund": "Please provide your order ID, and I'll check your refund status.",
        r"change.*address|update.*address": "To update your shipping address, please provide your order ID.",
        r"warranty.*info|product.*warranty": "Most products include a 1-year warranty. Please specify the product for details.",
        r"modify.*order|change.*order": "To modify your order, provide the order ID. Changes allowed within 24 hours.",
        r"gift.*card|use.*gift.*card": "Gift cards can be used at checkout. Provide the code to check balance or usage.",
        r"technical.*support|tech.*issue": "Describe your issue or contact our tech team at techsupport@example.com.",
        r"store.*location|find.*store": "Please provide your city or zip code to find the nearest store.",
        r"bulk.*order|wholesale": "For wholesale orders, contact our sales team at sales@example.com.",
        r"track.*package|where.*package": "Please provide your tracking number or order ID.",
        r"size.*guide|product.*size": "Check the size guide on the product page. Need help with a specific item?",
        r"loyalty.*program|rewards": "Our loyalty program offers points for purchases. Provide your account ID to check.",
        r"international.*shipping|ship.*overseas": "We offer international shipping to selected countries. Where are you located?",
    }

    for pattern, response in responses.items():
        if re.search(pattern, user_input):
            return response

    return search_like_response(user_input)

# Keyword-based fallback response
def search_like_response(user_input):
    search_db = {
        "track order": "To track your order, visit your account or provide your order ID here.",
        "returns": "You can return items within 30 days. For help, visit our returns portal.",
        "support": "Contact us via email or phone for real-time support.",
        "payment": "Check if your card is valid and contact support for failed payments.",
        "delivery": "Estimated delivery times vary by region. Enter zip code for more details.",
        "login issues": "Try resetting your password or clearing your browser cache.",
        "refund": "Refunds are typically processed in 3–5 business days.",
        "invoice": "Invoices are sent by email. Provide your order ID for a copy.",
        "store locations": "Visit our store locator page and enter your ZIP or city.",
        "product size": "Use the size chart on the product page to ensure the right fit."
    }

    vectorizer = TfidfVectorizer().fit(search_db.keys())
    user_vec = vectorizer.transform([user_input])
    db_vecs = vectorizer.transform(search_db.keys())
    similarities = cosine_similarity(user_vec, db_vecs).flatten()
    top_index = similarities.argmax()

    if similarities[top_index] > 0.2:
        return list(search_db.values())[top_index]

    return "I'm sorry, I couldn't find anything relevant. Could you try rephrasing your question?"

# Streamlit config
st.set_page_config(
    page_title="Chatbot",
    page_icon="🤖",
    layout="centered"
)

# Main app
def main():
    st.title("Smart Customer Support 🤖")
    st.subheader("Helping You Quickly with Orders, Returns, and More!")

    # Suggested prompts
    with st.expander("💡 Suggested Questions", expanded=True):
        cols = st.columns(3)
        suggestions = [
            "Track my order",
            "Return policy",
            "Talk to a human",
            "Where's my refund?",
            "Change delivery address",
            "Cancel my order",
            "Do you ship internationally?",
            "What's the delivery time?"
        ]
        for i, suggestion in enumerate(suggestions):
            if cols[i % 3].button(suggestion):
                st.session_state["pre_filled_input"] = suggestion

    # Chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I'm your support assistant. How can I help you today?"}
        ]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Input
    user_input = st.chat_input("Type your question here...", key="chat_input")
    if "pre_filled_input" in st.session_state:
        user_input = st.session_state.pop("pre_filled_input")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                time.sleep(1)
                response = get_chatbot_response(user_input)
                st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})

# Run it
if __name__ == "__main__":
    main()
