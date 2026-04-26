# 🍽️ Restaurant AI Chatbot — Spice Garden Lahore

An AI-powered chatbot for restaurants that answers customer questions
about menu, pricing, deals, reservations, and more — trained on the
restaurant's own data using RAG (Retrieval Augmented Generation).

## 🚀 Live Demo
👉 [Try it here](https://restaurant-chatbot-8utyn3zorhp2hejlp54dsl.streamlit.app/)

## 💡 What it does
- Answers questions about menu items and prices
- Provides information about deals and offers
- Handles reservation inquiries
- Shares parking, delivery, and general info
- Stays strictly on-topic — won't answer unrelated questions

## 🏗️ How it works
1. Restaurant data loaded into ChromaDB as vector embeddings
2. Customer question triggers similarity search for relevant context
3. GPT-3.5 generates response grounded only in retrieved context
4. Chatbot never makes up information not in the restaurant data

## 🛠️ Tech Stack
- LangChain — RAG pipeline and retrieval chain
- ChromaDB — vector storage for restaurant knowledge base
- OpenAI GPT-3.5 — response generation
- OpenAI Embeddings — converting text to vectors
- Streamlit — chat interface and deployment

## 📁 Project Structure
restaurant-chatbot/
├── data/
│   └── restaurant_info.txt
├── app.py
├── chatbot.py
├── ingest.py
└── requirements.txt

## 🔧 Run Locally
1. Clone the repo
   git clone https://github.com/kinza03/restaurant-chatbot.git
2. Install dependencies
   pip install -r requirements.txt
3. Add your OpenAI API key in .env file
   OPENAI_API_KEY=your-key-here
4. Build knowledge base
   python ingest.py
5. Run the app
   streamlit run app.py

## 💼 Business Use Case
Reusable template for restaurant businesses to replace repetitive
WhatsApp and phone enquiries with an intelligent 24/7 AI assistant.
Adaptable for any restaurant in under 2 hours by updating the data file.

## 👩‍💻 Author
Kinza — BSCS Student & AI Engineer
GitHub: https://github.com/kinza03