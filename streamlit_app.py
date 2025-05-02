import streamlit as st
import re
import time

# Function to handle chatbot responses based on user input
def get_chatbot_response(user_input):
    user_input = user_input.lower().strip()
    
    # Dictionary of patterns and responses
    responses = {
        r"(hi|hello|hey)": "Hello! Welcome to our customer support chatbot. How can I assist you today?",
        r"track.*order|order.*status": "Please provide your order ID, and I'll check the status for you!",
        r"return.*policy|how.*return": "Our return policy allows returns within 30 days of purchase. Please visit our website or provide your order ID for detailed instructions.",
        r"contact.*support|talk.*human": "You can reach our human support team at support@example.com or call 1-800-123-4567.",
        r"product.*info|tell.*products": "We offer a wide range of products! Could you specify which product or category you're interested in?",
        r"thank.*|thanks": "You're welcome! Happy to help.",
        r"bye|goodbye": "Goodbye! Feel free to reach out anytime."
    }
    
    # Check for matching patterns
    for pattern, response in responses.items():
        if re.search(pattern, user_input):
            return response
    
    # Default response for unrecognized queries
    return "I'm sorry, I didn't understand that. Could you please clarify or ask something else?"

# Streamlit app configuration
st.set_page_config(
    page_title="Intelligent Customer Support Chatbot",
    page_icon="🤖",
    layout="centered"
)

# Main Streamlit app
def main():
    st.title("Revolutionizing Customer Support")
    st.subheader("Intelligent Chatbot for Automated Assistance")
    
    # Initialize session state for chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I'm your intelligent customer support chatbot. How can I help you today?"}
        ]
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Input field for user query
    user_input = st.chat_input("Type your question here...")
    
    if user_input:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # Get and display chatbot response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                time.sleep(1)  # Simulate processing delay
                response = get_chatbot_response(user_input)
                st.markdown(response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

# Run the app
if __name__ == "__main__":
    main()
