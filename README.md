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
- Responds in the user's language — English, Urdu, Roman Urdu
- Stays strictly on-topic — won't answer unrelated questions

## 🏗️ How it works
1. Restaurant data (menu, FAQs, policies) is loaded and split into chunks
2. Chunks are converted to embeddings using OpenAI and stored in Pinecone
3. When a customer asks a question, similarity search retrieves the most relevant context
4. GPT-3.5 generates a response grounded only in that retrieved context
5. The chatbot never makes up information not in the restaurant data

## 🛠️ Tech Stack
- LangChain — RAG pipeline and retrieval chain
- Pinecone — cloud vector storage for permanent knowledge base
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
3. Add your API keys in .env file
   OPENAI_API_KEY=your-openai-key
   PINECONE_API_KEY=your-pinecone-key
4. Build the knowledge base
   python ingest.py
5. Run the app
   streamlit run app.py

## 💼 Business Use Case
Built as a reusable template for restaurant businesses to replace
repetitive WhatsApp and phone enquiries with an intelligent 24/7
AI assistant. Adaptable for any restaurant in under 2 hours by
simply updating the data file. Uses Pinecone for permanent cloud
storage — no data resets, always available.

## 👩‍💻 Author
Kinza Sabir — AI Engineer
GitHub: https://github.com/kinza03