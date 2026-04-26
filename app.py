import streamlit as st
import os
from chatbot import load_chain
from ingest import ingest_data

st.set_page_config(
    page_title="Spice Garden Lahore",
    page_icon="🍽️",
    layout="centered"
)

st.markdown("""
    <style>
    .restaurant-name {
        font-size: 1.8rem;
        font-weight: bold;
        color: #c0392b;
        text-align: center;
    }
    .restaurant-tagline {
        color: #888;
        font-size: 0.9rem;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="restaurant-name">Spice Garden Lahore</div>', unsafe_allow_html=True)
st.markdown('<div class="restaurant-tagline">Ask me anything — menu, deals, reservations, hours</div>', unsafe_allow_html=True)
st.markdown("---")

# Build knowledge base if it doesn't exist
if not os.path.exists("chroma_db"):
    with st.spinner("Setting up knowledge base..."):
        ingest_data()

if "chain" not in st.session_state:
    with st.spinner("Loading..."):
        st.session_state.chain = load_chain()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Assalam o Alaikum! Welcome to Spice Garden Lahore. I can help you with our menu, deals, reservations, and more. What would you like to know?"}
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if user_input := st.chat_input("Ask about our menu, hours, deals..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer = st.session_state.chain.invoke(user_input)
            st.write(answer)
    
    st.session_state.messages.append({"role": "assistant", "content": answer})

st.markdown("---")
st.markdown("**Quick questions:**")
col1, col2, col3 = st.columns(3)
suggestions = [
    "What are today's deals?",
    "How do I make a reservation?",
    "Do you offer delivery?"
]
for col, suggestion in zip([col1, col2, col3], suggestions):
    if col.button(suggestion, use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": suggestion})
        answer = st.session_state.chain.invoke(suggestion)
        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.rerun()