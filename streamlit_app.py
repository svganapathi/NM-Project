import streamlit as st
import re
import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Main pattern-based response function
def get_chatbot_response(user_input):
    user_input = user_input.lower().strip()

    # Responses dictionary with expanded entries
    responses = {
        r"(hi|hello|hey)": "Hello! Welcome to our customer support chatbot. How can I assist you today?",
        r"track.*order|order.*status": "Please provide your order ID, and I'll check the status for you!",
        r"return.*policy|how.*return": "Our return policy allows returns within 30 days of purchase. Please visit our website or provide your order ID for detailed instructions.",
        r"contact.*support|talk.*human": "You can reach our human support team at support@example.com or call 1-800-123-4567.",
        r"product.*info|tell.*products": "We offer a wide range of products! Could you specify which product or category you're interested in?",
        r"thank.*|thanks": "You're welcome! Happy to help.",
        r"bye|goodbye": "Goodbye! Feel free to reach out anytime.",
        r"payment.*issue|problem.*payment": "Sorry to hear about your payment issue. Please check your payment method or contact support@example.com for assistance.",
        r"delivery.*time|when.*deliver": "Delivery times depend on your location. Please provide your order ID or zip code for an estimated delivery date.",
        r"account.*login|can\'t.*login": "If you're having trouble logging in, try resetting your password or contact support@example.com for help.",
        r"product.*available|in.*stock": "Could you specify the product name or ID? I'll check its availability for you.",
        r"cancel.*order|how.*cancel": "To cancel an order, please provide your order ID. Note that cancellations are possible within 24 hours of purchase.",
        r"discount.*code|promo.*code": "Check our website for current promotions or enter a valid promo code at checkout. Need help? Let me know!",
        r"refund.*status|where.*refund": "Please provide your order ID, and I'll check the status of your refund.",
        r"change.*address|update.*address": "To update your shipping address, please provide your order ID. Note that changes are possible before the order ships.",
        r"warranty.*info|product.*warranty": "Most products come with a 1-year warranty. Please provide the product name or order ID for specific warranty details.",
        r"modify.*order|change.*order": "To modify your order, please provide your order ID. Modifications are possible within 24 hours of purchase.",
        r"gift.*card|use.*gift.*card": "Gift cards can be applied at checkout. Please provide the gift card code for balance or usage details.",
        r"technical.*support|tech.*issue": "For technical issues, please describe the problem or contact our tech support team at techsupport@example.com.",
        r"store.*location|find.*store": "Please provide your city or zip code, and I'll find the nearest store location for you.",
        r"bulk.*order|wholesale": "For bulk or wholesale orders, please contact our sales team at sales@example.com with your requirements.",
        r"track.*package|where.*package": "Please provide your tracking number or order ID, and I'll help you track your package.",
        r"size.*guide|product.*size": "Size guides are available on our website. Please specify the product for detailed sizing information.",
        r"loyalty.*program|rewards": "Our loyalty program offers points for every purchase. Visit our website or provide your account ID to check your rewards.",
        r"international.*shipping|ship.*overseas": "We offer international shipping to select countries. Please provide your country for shipping details.",
        r"app.*crash|app.*not.*working": "Try reinstalling the app or updating it to the latest version. If the issue persists, contact techsupport@example.com.",
        r"reset.*password|forgot.*password": "You can reset your password using the 'Forgot Password' option on the login page.",
        r"subscription.*plan|change.*plan": "We offer monthly and yearly subscription plans. Would you like help upgrading or changing your plan?",
        r"complaint|issue.*service": "We're sorry to hear that. Please describe your issue so we can assist or escalate it appropriately.",
        r"invoice.*copy|resend.*invoice": "Sure! Please provide your order ID or registered email, and I’ll send a copy of your invoice.",
        r"open.*hours|business.*hours": "Our customer support is available from 9 AM to 6 PM, Monday through Friday.",
        r"shipping.*cost|delivery.*fee": "Shipping fees depend on your location and selected delivery option. Would you like to enter your zip code?",
        r"order.*confirmation|didn’t.*receive.*confirmation": "Please check your spam folder. If you still haven't received confirmation, provide your email or order ID.",
        r"out.*of.*stock|when.*available": "That item may be temporarily unavailable. Could you share the product name or ID so I can check its restock status?",
        r"how.*long.*refund": "Refunds typically take 3–5 business days after processing. Let me check your order if you'd like."
    }

    # Check regex-based responses first
    for pattern, response in responses.items():
        if re.search(pattern, user_input):
            return response

    # Search-style fallback
    return search_like_response(user_input)

# Simulated search-style fallback using keywords
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

# Streamlit UI setup
st.set_page_config(
    page_title="Intelligent Customer Support Chatbot",
    page_icon="🤖",
    layout="centered"
)

def main():
    st.title("Revolutionizing Customer Support")
    st.subheader("Intelligent Chatbot for Automated Assistance")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I'm your intelligent customer support chatbot. How can I help you today?"}
        ]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_input = st.chat_input("Type your question here...")

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

# Run the app
if __name__ == "__main__":
    main()
