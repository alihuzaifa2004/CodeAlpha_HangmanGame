# 🎮 Hangman Pro X (Streamlit Edition)

A sleek, animated, production-ready implementation of the classic Hangman word game built entirely with Python and Streamlit. This version features structural optimization, real-time reactive rendering, responsive corner pop-up notifications, custom dark mode overrides, and synchronized Lottie vector micro-animations.

---

## ✨ Key Features

* **🎮 Micro-Animation Engine:** Features stateful vector tracking using `streamlit-lottie` to dynamically cycle through idle, success, error, and end-state animations without display duplication.
* **⚡ Smart Asset Caching:** Leverages Streamlit’s native `@st.cache_data` pipeline to store assets in memory, cutting redundant HTTP requests on user clicks and ensuring lag-free gameplay.
* **🔔 Real-Time Action Toasts:** Uses lightweight asynchronous toast modules (`st.toast`) to dispatch instantaneous feedback windows in the corner of the layout.
* **🛡️ Exploit Mitigation:** Built-in hardware validation tracking that safely disables virtual letter buttons instantly once guessed, locking out duplicate penalties.
* **🎯 Analytics Dashboard Bar:** Displays an integrated dashboard metric readout featuring tracking parameters such as current strikes ($X/6$) and exact structural lifelines.

---

## 🛠️ Architecture Design & State Management

Streamlit apps execute top-to-bottom on every single user interaction. In standard scripts, a button click can flush intermediate variables. **Hangman Pro X** manages application longevity by relying heavily on optimized session data:

* **`st.session_state.guessed`**: Transformed from a standard linear list sequence ($O(n)$ access lookup) into a constant time Python hash set framework ($O(1)$ lookup time efficiency).
* **`st.session_state.last_result`**: Acts as an atomic tracking bit, preventing animation race-conditions by serving as a dedicated gateway for asset evaluation.
* **`.stApp` Overrides**: Directly modifies Streamlit's target viewport wrapper in the DOM layer rather than manipulating standard root headers to maintain dark-canvas aesthetics seamlessly.

---

## 💾 Installation & Local Setup

### 1. Clone the Project Workspace
```bash
git clone https://github.com/alihuzaifa2004/CodeAlpha_HangmanGame
cd hangman-pro-x
```

### 2. Prepare the Environment & Dependencies
Ensure your environment running Python 3.8+ has the correct graphic and application frameworks ready:
```bash
pip install streamlit streamlit-lottie requests
```

### 3. Deploy the Application
Initialize your local server node directly from the command-line interface:
```bash
streamlit run app.py
```

---

## 📂 Project Architecture

```text
hangman-pro-x/
├── main.py              # Main reactive monolithic application script
├── README.md           # Deployment documentation and systemic specifications
└── requirements.txt    # Production-level dependency blueprints
```

---

## 🎨 Layout Configuration Customization

The interface relies on embedded styling structures to achieve its signature cyberpunk color grid. If you want to customize the look, modify the variables within the inline CSS dictionary block inside `app.py`:

| Component Class | Target Hex Element | Structural Responsibility |
| :--- | :--- | :--- |
| `.stApp` | `#0f172a` | Root layout viewport wrapper tone (Deep Slate) |
| `.title` | `#38bdf8` | Main heading accent tone (Sky Blue) |
| `.card` | `#111827` | Inner viewport background canvas layer |
| `.word` | `#22c55e` | Revealed hidden letters indicator (Emerald green) |
| `.counter-highlight` | `#ef4444` | Warning thresholds and mistake markers |

---

## 🚀 Game Logic Rules

1. **Target Evaluation Matrix:** The engine compiles the puzzle sequence from a randomized word arrays pool.
2. **Execution Caps:** A user has access to exactly **6 dynamic lifelines** before terminal state structures drop.
3. **Win/Loss Threshold Bounds:** * **Victory:** Sparked if the total matching array set precisely maps to the target sequence letters ($orall 	ext{ char } \in 	ext{ word}$ exists inside `guessed`).
    * **Defeat:** Triggered automatically when mistake variables peak ($\ge 6$).
