import streamlit as st
import os
from chatbot import load_chain

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

MENU_KEYWORDS = [
    "menu", "meniu", "مینیو", "meny", "dishes", "dish", "کھانا", "کھانے",
    "dikhao", "dikhayen", "دیکھاؤ", "دکھاؤ", "دیکھائیں", "دکھائیں",
    "what do you serve", "what food", "available dishes", "all dishes",
    "kya hai", "کیا ہے", "list", "show me", "tell me"
]

MENU_TEXT_EN = """
**Our Menu:**

**Starters:**
- Chicken Tikka: Rs. 850 (half), Rs. 1500 (full)
- Seekh Kebab: Rs. 750 (6 pieces)
- Crispy Calamari: Rs. 950

**Main Course:**
- Lahori Karahi (Chicken): Rs. 1800
- Mutton Handi: Rs. 2200
- Grilled Fish: Rs. 1650
- Vegetable Biryani: Rs. 950

**Deals:**
- Family Deal (serves 4): 1 Karahi + 2 Naan + Raita + Drinks = Rs. 3500
- Lunch Special (12-4 PM): Any main + drink = Rs. 1200
"""

MENU_TEXT_UR = """
**ہمارا مینیو:**

**اسٹارٹرز:**
- چکن ٹکہ: Rs. 850 (آدھا), Rs. 1500 (پورا)
- سیخ کباب: Rs. 750 (6 پیس)
- کرسپی کلماری: Rs. 950

**مین کورس:**
- لاہوری کڑاہی (چکن): Rs. 1800
- مٹن ہانڈی: Rs. 2200
- گرلڈ مچھلی: Rs. 1650
- سبزی بریانی: Rs. 950

**ڈیلز:**
- فیملی ڈیل (4 افراد): 1 کڑاہی + 2 نان + رائتہ + ڈرنکس = Rs. 3500
- لنچ اسپیشل (12-4 بجے): کوئی بھی مین + ڈرنک = Rs. 1200
"""

URDU_KEYWORDS = [
    "مینیو", "کھانا", "دیکھاؤ", "دکھاؤ", "دیکھائیں", "دکھائیں",
    "کیا", "ہے", "ہیں", "اپنا", "آپ", "ہمارا", "کریں", "بتائیں"
]

def is_menu_request(text):
    text_lower = text.lower()
    return any(keyword.lower() in text_lower for keyword in MENU_KEYWORDS)

def is_urdu(text):
    return any(keyword in text for keyword in URDU_KEYWORDS)

if "chain" not in st.session_state:
    with st.spinner("Loading..."):
        st.session_state.chain = load_chain()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Assalam o Alaikum! Welcome to Spice Garden Lahore 🍽️\n\nI can help you check menu items, today's deals, delivery info, or book a table instantly.\nWhat would you like to know today?"}
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if user_input := st.chat_input("Ask about our menu, hours, deals..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            if is_menu_request(user_input):
                if is_urdu(user_input):
                    answer = MENU_TEXT_UR
                else:
                    answer = MENU_TEXT_EN
            else:
                answer = st.session_state.chain.invoke(user_input)
            st.markdown(answer)

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
        if is_menu_request(suggestion):
            answer = MENU_TEXT_EN
        else:
            answer = st.session_state.chain.invoke(suggestion)
        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.rerun()