# Revolutionizing Customer Support with an Intelligent Chatbot

This project implements an intelligent customer support chatbot using Streamlit for automated assistance. The chatbot handles common customer queries with predefined responses and can be extended with advanced AI models.

## Features

- Interactive web interface powered by Streamlit
- Rule-based responses for common customer support queries
- Chat history persistence during the session
- Easily extensible for integration with advanced NLP or AI models

## Prerequisites

- Python 3.8+
- Streamlit
- Git (for deployment)

## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. Create a virtual environment and activate it:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Running Locally

1. Start the Streamlit app:

   ```bash
   streamlit run chatbot_app.py
   ```

2. Open your browser and navigate to http://localhost:8501.

## Deployment to Streamlit Cloud

1. Push your project to a GitHub repository.
2. Sign in to Streamlit Cloud.
3. Create a new app and link it to your GitHub repository.
4. Specify chatbot_app.py as the main script.
5. Deploy the app and access it via the provided URL.

## Extending the Chatbot

To enhance the chatbot with AI capabilities:

- Add more response patterns in the get_chatbot_response function.
- Incorporate NLP libraries like transformers or spacy for advanced intent recognition.

## License

MIT License @svganapathi
