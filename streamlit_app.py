import streamlit as st
import re
import time

# Function to handle chatbot responses
def get_chatbot_response(user_input):
    user_input = user_input.lower().strip()
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
        r"international.*shipping|ship.*overseas": "We offer international shipping to select countries. Please provide your country for shipping details."
    }
    for pattern, response in responses.items():
        if re.search(pattern, user_input):
            return response
    return "I'm sorry, I didn't understand that. Could you please clarify or ask something else?"

# Predefined suggestions
SUGGESTIONS = [
    "Hi",
    "Track my order",
    "What is the return policy",
    "Contact support",
    "Tell me about your products",
    "Thanks",
    "Goodbye",
    "Payment issue",
    "Delivery time",
    "Can't login",
    "Is this product available",
    "Cancel my order",
    "Promo code",
    "Refund status",
    "Change address",
    "Warranty info",
    "Modify order",
    "Use gift card",
    "Technical support",
    "Find a store",
    "Bulk order",
    "Track package",
    "Size guide",
    "Loyalty program",
    "International shipping"
]

# Streamlit page configuration
st.set_page_config(page_title="Intelligent Customer Support Chatbot", page_icon="🤖", layout="centered")

# Main app
def main():
    st.title("Revolutionizing Customer Support")
    st.subheader("Intelligent Chatbot for Automated Assistance")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I'm your intelligent customer support chatbot. How can I help you today?"}
        ]
    if "input_text" not in st.session_state:
        st.session_state.input_text = ""

    # Input box with Google-style suggestions
    user_input = st.text_input("Type your question:", value=st.session_state.input_text, key="input_text")

    # Dynamic autocomplete suggestions
    if user_input:
        filtered = [s for s in SUGGESTIONS if user_input.lower() in s.lower()]
        if filtered:
            st.markdown("**Suggestions:**")
            for suggestion in filtered[:5]:
                if st.button(suggestion, key=suggestion):
                    st.session_state.input_text = suggestion
                    st.experimental_rerun()

    # Manual send button
    if st.button("Send") and st.session_state.input_text.strip():
        input_to_process = st.session_state.input_text.strip()
        st.session_state.messages.append({"role": "user", "content": input_to_process})
        with st.chat_message("user"):
            st.markdown(input_to_process)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                time.sleep(1)
                response = get_chatbot_response(input_to_process)
                st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})
        st.session_state.input_text = ""
        st.experimental_rerun()

    # Chat history display
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Run app
if __name__ == "__main__":
    main()
