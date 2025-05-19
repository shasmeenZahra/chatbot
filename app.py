import random
import streamlit as st
import difflib
from datetime import datetime
import time

# --- Page Setup ---
st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="centered")

# --- What You Can Ask ---
with st.expander("❓ What You Can Ask Me"):
    st.markdown("""
    - Hello / Hi  
    - What's your name?  
    - Who created you?  
    - Tell me a joke  
    - Goodbye  
    - How are you?  
    - What can you do?  
    - Where are you from?  
    - What is your purpose?  
    """)

# --- Custom Styling ---
st.markdown("""
<style>
body, .stApp {
    background-color: #e6f2ff;
    color: #333;
    font-family: Arial, sans-serif;
}
.message {
    padding: 10px;
    margin: 5px 0;
    border-radius: 10px;
}
.user {
    background-color: #d9fdd3;
    text-align: right;
}
.bot {
    background-color: #ffe6e6;
    text-align: left;
}
.typing {
    font-style: italic;
    color: #999;
}
</style>
""", unsafe_allow_html=True)

# --- Session States ---
if "user_responses" not in st.session_state:
    st.session_state.user_responses = {}

if "chat_memory" not in st.session_state:
    st.session_state.chat_memory = []

if "bot_name" not in st.session_state:
    st.session_state.bot_name = "Chatbot"

if "bot_personality" not in st.session_state:
    st.session_state.bot_personality = "Friendly"

# --- Personality Modes ---
personalities = {
    "Friendly": {
        "greet": "Hey there! 😊",
        "bye": "See you later, friend! 👋",
        "unknown": "Hmm... I didn't get that. Wanna try again?"
    },
    "Professional": {
        "greet": "Hello. How can I assist you today?",
        "bye": "Goodbye. Have a productive day!",
        "unknown": "I'm not sure how to respond to that. Could you rephrase?"
    },
    "Funny": {
        "greet": "Yo human! Ready for some AI nonsense? 😜",
        "bye": "Peace out! 🤘",
        "unknown": "My AI brain just did a flip. Try again maybe?"
    }
}

# --- Predefined Responses ---
responses = {
    "hello": ["Hi there! How can I help you?", "Hello! Hope you're having a great day! 😊"],
    "hi": ["Hi there! How can I help you?", "Hello! Hope you're having a great day! 😊"],
    "what's your name": ["I'm {name}! 🤖"],
    "who created you": ["I was created by Shasmeen zahra! 👩‍💻"],
    "tell me a joke": [
        "Why don’t scientists trust atoms? Because they make up everything! 😂",
        "Why did the scarecrow win an award? Because he was outstanding in his field! 🌾",
        "استاد: بچوں سب سے زیادہ تیز چیز کیا ہے؟\nطالب علم: دعا\nاستاد: وہ کیسے؟\nطالب علم: دعا مانگتے ہی امی کے ہاتھ کی چپل آ جاتی ہے! 😂"
    ],
    "goodbye": ["Bye! Have a great day! 😊"],
    "how are you": ["I'm doing great! How about you? 😊"],
    "what can you do": ["I can chat, tell jokes, learn, and make your day better! 🤖"],
    "where are you from": ["I live in the magical cloud ☁️"],
    "what is your purpose": ["To assist, entertain and chat with awesome people like you! 😊"]
}

# --- Sidebar Options ---
with st.sidebar:
    st.header("⚙️ Settings")
    st.session_state.bot_name = st.text_input("🤖 Bot Name", value=st.session_state.bot_name)
    st.session_state.bot_personality = st.selectbox("🎭 Bot Personality", list(personalities.keys()))
    if st.button("🧹 Clear Chat"):
        st.session_state.chat_memory.clear()
    if st.button("📄 Export Chat"):
        filename = f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            for msg in reversed(st.session_state.chat_memory):
                f.write(msg.replace("<div class='message ", "").replace("</div>", "\n").split(">")[-1])
        st.success(f"Chat saved as {filename}")

# --- Chatbot Logic ---
def chatbot_response(user_input):
    user_input = user_input.lower()
    st.session_state.chat_memory.insert(0, f"<div class='message user'>You: {user_input}</div>")

    # Trained user responses
    if user_input in st.session_state.user_responses:
        response = random.choice(st.session_state.user_responses[user_input])
        st.session_state.chat_memory.insert(0, f"<div class='message bot'>{st.session_state.bot_name}: {response}</div>")
        return response

    # Default responses
    match = difflib.get_close_matches(user_input, responses.keys(), n=1, cutoff=0.6)
    if match:
        response = random.choice(responses[match[0]])
        response = response.replace("{name}", st.session_state.bot_name)
        st.session_state.chat_memory.insert(0, f"<div class='message bot'>{st.session_state.bot_name}: {response}</div>")
        return response

    unknown = personalities[st.session_state.bot_personality]["unknown"]
    st.session_state.chat_memory.insert(0, f"<div class='message bot'>{st.session_state.bot_name}: {unknown}</div>")
    return unknown

# --- UI ---
st.title(f"{st.session_state.bot_name} 🤖")
st.markdown("Chat with your AI assistant below:")

user_message = st.text_input("You:")

if user_message:
    if user_message.lower() == "exit":
        bye_msg = personalities[st.session_state.bot_personality]["bye"]
        st.markdown(f"<div class='message bot'>{st.session_state.bot_name}: {bye_msg}</div>", unsafe_allow_html=True)

    elif user_message.lower().startswith("train:"):
        try:
            parts = user_message[6:].split("=")
            user_msg = parts[0].strip().lower()
            bot_response = parts[1].strip()
            if user_msg and bot_response:
                st.session_state.user_responses.setdefault(user_msg, []).append(bot_response)
                st.markdown(f"<div class='message bot'>{st.session_state.bot_name}: Thanks! I've learned that. 😊</div>", unsafe_allow_html=True)
        except:
            st.markdown(f"<div class='message bot'>{st.session_state.bot_name}: Oops! Use `train: message = response` format.</div>", unsafe_allow_html=True)
    else:
        # Typing effect
        with st.spinner("Typing..."):
            time.sleep(0.8)
            reply = chatbot_response(user_message)
            st.markdown(f"<div class='message bot'>{st.session_state.bot_name}: {reply}</div>", unsafe_allow_html=True)

# --- Chat History ---
st.subheader("💬 Chat History")
for msg in reversed(st.session_state.chat_memory):
    st.markdown(msg, unsafe_allow_html=True)
