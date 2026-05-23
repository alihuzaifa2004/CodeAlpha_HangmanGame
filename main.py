import streamlit as st
import random
import requests
import time


try:
    from streamlit_lottie import st_lottie
    LOTTIE_AVAILABLE = True
except ImportError:
    LOTTIE_AVAILABLE = False


st.set_page_config(
    page_title="Hangman Pro X",
    page_icon="🎮",
    layout="centered"
)

@st.cache_data(show_spinner=False)
def load_lottie(url):
    try:
        r = requests.get(url, timeout=3)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return None

# Load your animations
welcome_anim = load_lottie("https://lottie.host/e1bc61fc-5d20-4ccc-92bf-d91f17228e6a.json")
wrong_anim = load_lottie("https://lottie.host/c7fae277-0014-4b88-8345-8a4fabfc23b6.json")
dead_anim = load_lottie("https://lottie.host/bf2ad280-e56b-4554-9d30-93d5d8dd675c.json")
# New victory animation
win_anim = load_lottie("https://assets10.lottiefiles.com/packages/lf20_7w867mub.json") 

# CSS UI
st.markdown("""
<style>
.stApp {
    background-color: #0f172a;
}
.title {
    font-size: 42px;
    text-align: center;
    color: #38bdf8;
    font-weight: bold;
    margin-bottom: 5px;
}
.counter-box {
    text-align: center;
    font-size: 20px;
    color: #94a3b8;
    margin-bottom: 20px;
}
.counter-highlight {
    color: #ef4444;
    font-weight: bold;
}
.card {
    background: #111827;
    padding: 25px;
    border-radius: 15px;
    border: 2px solid #334155;
    text-align: center;
    margin: 20px 0;
}
.word {
    font-size: 38px;
    letter-spacing: 12px;
    color: #22c55e;
    font-family: monospace;
}
.success {color: #22c55e; font-size: 28px; text-align:center; font-weight: bold;}
.fail {color: #ef4444; font-size: 28px; text-align:center; font-weight: bold;}
</style>
""", unsafe_allow_html=True)

# WORD BANK
# ---------------------------------------------------
WORDS = ["python", "gaming", "laptop", "network", "streamlit", "developer", "hangman"]

# SESSION STATE INITIALIZATION
if "word" not in st.session_state:
    st.session_state.word = random.choice(WORDS)
if "guessed" not in st.session_state:
    st.session_state.guessed = set()
if "wrong" not in st.session_state:
    st.session_state.wrong = 0
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "last_result" not in st.session_state:
    st.session_state.last_result = None  # Tracks "correct", "wrong", or None for animation triggers

# GAME LOGIC CHECKS
won = all(letter in st.session_state.guessed for letter in st.session_state.word)
lost = st.session_state.wrong >= 6

if won or lost:
    st.session_state.game_over = True

# TITLE & COUNTER DISPLAY
st.markdown("<div class='title'>🎮 Hangman Pro X</div>", unsafe_allow_html=True)

# Visual Counter for remaining attempts
attempts_left = 6 - st.session_state.wrong
st.markdown(
    f"<div class='counter-box'>Strikes: <span class='counter-highlight'>{st.session_state.wrong}/6</span> | Attempts Remaining: <b>{attempts_left}</b></div>", 
    unsafe_allow_html=True
)

# CENTRAL ANIMATION ENGINE
if LOTTIE_AVAILABLE:
    # 1. End Game States take priority
    if won and win_anim:
        st_lottie(win_anim, height=220, key="win_game")
    elif lost and dead_anim:
        st_lottie(dead_anim, height=220, key="dead_game")
    
    # 2. Mid-game active event triggers
    elif st.session_state.last_result == "wrong" and wrong_anim:
        st_lottie(wrong_anim, height=220, key=f"wrong_strike_{st.session_state.wrong}")
    
    # 3. Default Idle/Welcome screen
    elif welcome_anim:
        st_lottie(welcome_anim, height=220, key="welcome")
else:
    st.caption("Install streamlit-lottie for animated visuals!")

# ---------------------------------------------------
# WORD DISPLAY
# ---------------------------------------------------
display_word = " ".join([c.upper() if c in st.session_state.guessed else "_" for c in st.session_state.word])
st.markdown(f"<div class='card word'>{display_word}</div>", unsafe_allow_html=True)

# ---------------------------------------------------
# STATUS MESSAGES
# ---------------------------------------------------
if won:
    st.markdown("<div class='success'>🎉 YOU WIN! GREAT JOB!</div>", unsafe_allow_html=True)
    st.balloons()
elif lost:
    st.markdown(f"<div class='fail'>💀 GAME OVER! The word was: {st.session_state.word.upper()}</div>", unsafe_allow_html=True)

# ---------------------------------------------------
# KEYBOARD INPUT
# ---------------------------------------------------
st.write("### Choose a letter:")
letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
cols = st.columns(13)

for i, letter in enumerate(letters):
    low_letter = letter.lower()
    is_disabled = low_letter in st.session_state.guessed or st.session_state.game_over
    
    if cols[i % 13].button(letter, key=f"btn_{letter}", disabled=is_disabled, use_container_width=True):
        st.session_state.guessed.add(low_letter)
        
        if low_letter in st.session_state.word:
            st.session_state.last_result = "correct"
            st.toast(f"Nice! '{letter}' is correct! ✨", icon="✅")
        else:
            st.session_state.wrong += 1
            st.session_state.last_result = "wrong"
            # Pop-up notification in the corner of the screen
            st.toast(f"Ouch! '{letter}' is wrong! (Strikes: {st.session_state.wrong}/6)", icon="❌")
            
        # Give the toast an instant moment to register physically before a clean redraw
        time.sleep(1) 
        st.rerun()

st.markdown("---")

# ---------------------------------------------------
# RESET GAME
# ---------------------------------------------------
if st.button("🔄 Restart Match", use_container_width=True, type="primary"):
    st.session_state.word = random.choice(WORDS)
    st.session_state.guessed = set()
    st.session_state.wrong = 0
    st.session_state.game_over = False
    st.session_state.last_result = None
    st.rerun()