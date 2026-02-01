import streamlit as st
import google.generativeai as genai
import time

# 1. Config & Setup
st.set_page_config(page_title="Iron Lady Growth Strategist", page_icon="🦁", layout="wide")

# --- CUSTOM CSS FOR "UI DESIGN" LOOK ---
# --- CUSTOM CSS FOR "UI DESIGN" LOOK ---
st.markdown("""
<style>
    /* Import modern font */
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;700&display=swap');

    
    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif;
        font-size: 25px; 
    }

    /* Main Background - Deep Luxury Black */
    .stApp {
        background-color: #0e1117;
        background-image: radial-gradient(circle at 50% 0%, #2b1c1c 0%, #0e1117 60%);
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #161a23;
        border-right: 1px solid #333;
    }
    /* Increase Sidebar Font Size specifically */
    section[data-testid="stSidebar"] .stMarkdown {
        font-size: 18px; 
    }

    /* Chat Input Styling */
    .stChatInput input {
        background-color: #2b303b !important;
        color: white !important;
        border: 1px solid #444 !important;
        border-radius: 12px !important;
        font-size: 18px !important; /* <--- Increased Input Text Size */
    }

    /* User Message Style (Right side) */
    div[data-testid="stChatMessage"] {
        background-color: transparent;
        font-size: 20px; /* <--- Chat Text Size */
    }
    div[data-testid="stChatMessage"]:nth-child(odd) {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 15px; /* Added more padding for readability */
    }

    /* Titles and Headers */
    h1 {
        color: #FFD700 !important;
        font-weight: 700 !important;
        text-shadow: 0px 0px 10px rgba(255, 215, 0, 0.3);
        font-size: 48px !important; /* <--- Made Title Bigger */
    }
    h2, h3 {
        color: #E0E0E0 !important;
        font-size: 32px !important; /* <--- Made Subtitles Bigger */
    }
    
    p {
        line-height: 1.6; /* Adds space between lines for better readability */
    }

    /* Remove default Streamlit Menu */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
</style>
""", unsafe_allow_html=True)

# 2. Sidebar for Context
with st.sidebar:
    st.markdown("## 🦁 IRON LADY")
    st.markdown("---")
    st.write("**Mission:** Enabling 1 Million Women to Reach the Top.")
    st.write("This AI is designed to help you break through career ceilings using the 'Business War' methodology.")
    st.markdown("---")
    api_key = st.text_input("Enter Google Gemini API Key", type="password")
    st.info("💡 **Tip:** Ask about 'Leadership Essentials' or '100 Board Members'.")

# 3. Main Title Area
col1, col2 = st.columns([1, 8])
with col1:
    st.write("") # Spacer
with col2:
    st.title("Iron Lady Strategist")
    st.markdown("#### *Stop Balancing. Start Maximizing.*")

# 4. Chat Logic
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "model", "parts": ["**Welcome, Leader.** I am here to help you smash glass ceilings. \n\nTell me: **What is your current role and what is stopping you from reaching the C-Suite?**"]}
    ]

# 5. Display Chat History
for msg in st.session_state.messages:
    role = "user" if msg["role"] == "user" else "assistant"
    # Add an avatar: User gets a generic icon, Bot gets a Lion
    avatar = "👤" if role == "user" else "🦁"
    with st.chat_message(role, avatar=avatar):
        st.write(msg["parts"][0])

# 6. Handle User Input
if prompt := st.chat_input("Type your career challenge here..."):
    if not api_key:
        st.error("🔒 Please enter your Google API Key in the sidebar to unlock the Strategist.")
        st.stop()

    # Configure Gemini
    genai.configure(api_key=api_key)
    
    # SYSTEM PROMPT
    system_instruction = """
    You are the "Iron Lady Growth Strategist."
    You help women smash glass ceilings.
    Tone: Unapologetic, direct, empowering, high-energy.
    Philosophy: "Maximize, don't Balance."
    
    Offerings to recommend based on user input:
    - Mid-career/Stuck? -> "100 Board Members Program".
    - Senior/C-Suite ambition? -> "Master of Business Warfare".
    - Confidence/Politics issues? -> "Leadership Essentials".
    
    Formatting:
    - Use **Bold** for key impact words.
    - Use bullet points for strategy steps.
    - Keep paragraphs short and punchy.
    
    Always end with a provocative question to make them think bigger.
    """
    
    # Model Setup
    model = genai.GenerativeModel("gemini-flash-latest", system_instruction=system_instruction)

    # Display User Message
    st.session_state.messages.append({"role": "user", "parts": [prompt]})
    with st.chat_message("user", avatar="👤"):
        st.write(prompt)

    # Generate Response
    try:
        chat = model.start_chat(history=st.session_state.messages[:-1]) 
        response = chat.send_message(prompt)
        
        msg = response.text
        st.session_state.messages.append({"role": "model", "parts": [msg]})
        with st.chat_message("assistant", avatar="🦁"):
            st.write(msg)
        
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg:
            st.warning("⚠️ High traffic. The Strategist is analyzing... (Please wait 30s)")
        else:
            st.error(f"System Error: {e}")