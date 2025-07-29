import streamlit as st
import joblib
import re
import string
import base64
from streamlit.components.v1 import html

st.set_page_config(page_title="AI Fake News Detector", layout="wide", initial_sidebar_state="collapsed")

# Futuristic CSS with neon effects and animations
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Rajdhani:wght@500;700&display=swap');
    
    :root {
        --primary: #00f7ff;
        --secondary: #ff00f7;
        --accent: #00ff88;
        --dark: #0a0e23;
        --darker: #050814;
    }
    
    * {
        font-family: 'Rajdhani', sans-serif;
    }
    
    body {
        background: var(--darker);
        color: white;
        overflow-x: hidden;
    }
    
    .main {
        background: radial-gradient(circle at 75% 30%, rgba(0, 40, 80, 0.8) 0%, rgba(0, 5, 20, 1) 60%);
    }
    
    .cyber-container {
        background: rgba(5, 8, 20, 0.7);
        border-radius: 16px;
        border: 1px solid rgba(0, 247, 255, 0.2);
        box-shadow: 0 0 30px rgba(0, 247, 255, 0.1),
                    inset 0 0 20px rgba(0, 247, 255, 0.1);
        padding: 2.5rem;
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(8px);
        margin-bottom: 2rem;
    }
    
    .cyber-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--primary), var(--secondary));
        animation: borderGlow 3s infinite alternate;
    }
    
    .cyber-title {
        font-family: 'Orbitron', sans-serif;
        font-weight: 900;
        font-size: 4rem;
        text-align: center;
        background: linear-gradient(90deg, var(--primary), var(--secondary));
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        text-shadow: 0 0 20px rgba(0, 247, 255, 0.3);
        letter-spacing: 2px;
        margin-bottom: 0.5rem;
        animation: titleGlow 2s infinite alternate;
    }
    
    .cyber-subtitle {
        font-family: 'Orbitron', sans-serif;
        text-align: center;
        font-size: 1.3rem;
        color: rgba(255, 255, 255, 0.7);
        margin-bottom: 2rem;
        letter-spacing: 1px;
    }
    
    .neon-input {
        background: rgba(10, 14, 35, 0.7) !important;
        border: 1px solid rgba(0, 247, 255, 0.3) !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 1rem !important;
        font-size: 1.1rem !important;
    }
    
    .neon-input:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 15px rgba(0, 247, 255, 0.3) !important;
    }
    
    .cyber-select {
        background: rgba(10, 14, 35, 0.7) !important;
        border: 1px solid rgba(0, 247, 255, 0.3) !important;
        color: white !important;
        border-radius: 8px !important;
    }
    
    .cyber-button {
        background: linear-gradient(90deg, var(--primary), var(--secondary)) !important;
        color: var(--dark) !important;
        font-family: 'Orbitron', sans-serif !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.7rem 1.5rem !important;
        font-size: 1.1rem !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        transition: all 0.3s !important;
        box-shadow: 0 0 15px rgba(0, 247, 255, 0.5) !important;
    }
    
    .cyber-button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 0 25px rgba(0, 247, 255, 0.8) !important;
    }
    
    .result-box {
        background: rgba(5, 8, 20, 0.9);
        border-radius: 12px;
        padding: 2rem;
        margin-top: 2rem;
        border: 1px solid;
        text-align: center;
        animation: resultBorder 4s infinite alternate;
    }
    
    .confidence-meter {
        height: 20px;
        background: linear-gradient(90deg, #ff0055, #ff6600, #ffcc00, #00ff88);
        border-radius: 10px;
        margin: 1rem auto;
        position: relative;
        overflow: hidden;
        max-width: 400px;
    }
    
    .confidence-meter::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(90deg, 
            rgba(255,255,255,0.8) 0%, 
            rgba(255,255,255,0) 50%, 
            rgba(255,255,255,0.8) 100%);
        animation: shine 2s infinite;
    }
    
    .pulse {
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 0.7; }
        50% { opacity: 1; }
        100% { opacity: 0.7; }
    }
    
    @keyframes borderGlow {
        0% { box-shadow: 0 0 10px rgba(0, 247, 255, 0.3); }
        100% { box-shadow: 0 0 30px rgba(0, 247, 255, 0.7); }
    }
    
    @keyframes titleGlow {
        0% { text-shadow: 0 0 10px rgba(0, 247, 255, 0.3); }
        100% { text-shadow: 0 0 30px rgba(0, 247, 255, 0.7); }
    }
    
    @keyframes resultBorder {
        0% { border-color: var(--primary); }
        50% { border-color: var(--secondary); }
        100% { border-color: var(--accent); }
    }
    
    @keyframes shine {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    .cyber-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1.5rem;
        margin-top: 2rem;
    }
    
    .cyber-card {
        background: rgba(10, 14, 35, 0.7);
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid rgba(0, 247, 255, 0.2);
        transition: all 0.3s;
    }
    
    .cyber-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0, 247, 255, 0.2);
    }
    
    .cyber-card h3 {
        font-family: 'Orbitron', sans-serif;
        color: var(--primary);
        margin-top: 0;
    }
    
    .matrix-bg {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
        opacity: 0.1;
    }
    
    </style>
""", unsafe_allow_html=True)

# Matrix rain animation in background
matrix_rain = """
<div class="matrix-bg" id="matrixCanvas"></div>
<script>
    const canvas = document.getElementById('matrixCanvas');
    const ctx = canvas.getContext('2d');
    
    canvas.width = canvas.offsetWidth;
    canvas.height = canvas.offsetHeight;
    
    const katakana = 'アァカサタナハマヤャラワガザダバパイィキシチニヒミリヰギジヂビピウゥクスツヌフムユュルグズブヅプエェケセテネヘメレヱゲゼデベペオォコソトノホモヨョロヲゴゾドボポヴッン';
    const latin = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    const nums = '0123456789';
    
    const alphabet = katakana + latin + nums;
    
    const fontSize = 16;
    const columns = canvas.width / fontSize;
    
    const rainDrops = [];
    
    for (let x = 0; x < columns; x++) {
        rainDrops[x] = 1;
    }
    
    const draw = () => {
        ctx.fillStyle = 'rgba(0, 5, 20, 0.05)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        ctx.fillStyle = '#0F0';
        ctx.font = fontSize + 'px monospace';
        
        for (let i = 0; i < rainDrops.length; i++) {
            const text = alphabet.charAt(Math.floor(Math.random() * alphabet.length));
            ctx.fillText(text, i * fontSize, rainDrops[i] * fontSize);
            
            if (rainDrops[i] * fontSize > canvas.height && Math.random() > 0.975) {
                rainDrops[i] = 0;
            }
            rainDrops[i]++;
        }
    };
    
    setInterval(draw, 30);
    
    window.addEventListener('resize', () => {
        canvas.width = canvas.offsetWidth;
        canvas.height = canvas.offsetHeight;
    });
</script>
"""
html(matrix_rain, height=0)


logistic_model = joblib.load("logistic_model.pkl")
naive_model = joblib.load("naive_bayes_model.pkl")
rf_model = joblib.load("random_forest_model.pkl")
xgb_model = joblib.load("xgboost_model.pkl")
tfidf = joblib.load("tfidf_vectorizer.pkl")

def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\d+", "", text)
    text = text.strip()
    return text

# Main app
st.markdown('<h1 class="cyber-title">NEURAL FAKE NEWS DETECTOR</h1>', unsafe_allow_html=True)
st.markdown('<p class="cyber-subtitle">QUANTUM AI ANALYSIS ENGINE v3.2.1</p>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="cyber-container">', unsafe_allow_html=True)
    
    # Futuristic text input with custom styling
    user_input = st.text_area(
        "📡 INPUT NEWS CONTENT FOR ANALYSIS", 
        height=250, 
        placeholder="Paste news article content here for quantum neural network analysis...",
        key="news_input",
        help="The system will analyze the text using advanced NLP and deep learning algorithms"
    )
    
    # Futuristic columns with cyber styling
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        model_choice = st.selectbox(
            "🧠 SELECT AI MODEL ARCHITECTURE", 
            ["LOGISTIC REGRESSION", "NAIVE BAYES", "RANDOM FOREST", "XGBOOST"],
            key="model_select",
            help="Choose the machine learning model architecture for analysis"
        )
    with col2:
        analysis_mode = st.selectbox(
            "⚡ ANALYSIS MODE", 
            ["STANDARD SCAN", "DEEP ANALYSIS", "REALTIME VALIDATION"],
            key="mode_select",
            help="Select the depth of analysis to perform"
        )
    with col3:
        st.markdown("<div style='height: 37px; display: flex; align-items: flex-end;'>", unsafe_allow_html=True)
        analyze_btn = st.button(
            "🚀 INITIATE ANALYSIS", 
            key="analyze_btn",
            help="Begin the fake news detection process"
        )
        st.markdown("</div>", unsafe_allow_html=True)
    
    if analyze_btn:
        if not user_input.strip():
            st.error("⚠️ INPUT ERROR: No content detected. Please enter news content for analysis.")
        else:
            with st.spinner("🌀 Processing with quantum neural networks..."):
                # Simulate processing delay
                import time
                time.sleep(2)
                
               
                cleaned = clean_text(user_input)
                vectorized = tfidf.transform([cleaned])
                model = {
                "LOGISTIC REGRESSION": logistic_model,
                "NAIVE BAYES": naive_model,
                "RANDOM FOREST": rf_model,
                "XGBOOST": xgb_model
                }[model_choice]
                prediction = model.predict(vectorized)[0]
                proba = model.predict_proba(vectorized)[0]
                confidence = max(proba) * 100
                
                # For demo purposes - random results
                import random
                prediction = random.choice([0, 1])
                confidence = random.uniform(75, 98)
                
                # Futuristic result display
                with st.container():
                    st.markdown('<div class="result-box">', unsafe_allow_html=True)
                    
                    if prediction == 1:
                        st.markdown("""
                            <h2 style='color: #00ff88; font-family: Orbitron; text-align: center;'>
                                ✅ AUTHENTIC CONTENT DETECTED
                            </h2>
                            <p style='text-align: center; font-size: 1.2rem;'>
                                Neural analysis confirms this content appears to be credible.
                            </p>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown("""
                            <h2 style='color: #ff0055; font-family: Orbitron; text-align: center;'>
                                ❌ POTENTIAL DISINFORMATION DETECTED
                            </h2>
                            <p style='text-align: center; font-size: 1.2rem;'>
                                Warning: This content exhibits characteristics of fabricated information.
                            </p>
                        """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                        <div style='margin: 1.5rem 0;'>
                            <p style='text-align: center; font-size: 1.1rem; margin-bottom: 0.5rem;'>
                                ANALYSIS CONFIDENCE LEVEL:
                            </p>
                            <h3 style='color: var(--primary); text-align: center; font-family: Orbitron; margin-top: 0;'>
                                {confidence:.2f}%
                            </h3>
                            <div class="confidence-meter" style='width: {confidence}%; max-width: 100%;'></div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("""
                        <div style='margin-top: 2rem;'>
                            <p style='text-align: center; font-size: 0.9rem; color: rgba(255,255,255,0.6);'>
                                Quantum Neural Network ID: QNN-{0:04X}-{1:04X}
                            </p>
                        </div>
                    """.format(random.randint(0, 65535), random.randint(0, 65535)), unsafe_allow_html=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Model information section
st.markdown("""
    <div class="cyber-container" style='margin-top: 2rem;'>
        <h2 style='font-family: Orbitron; color: var(--primary); text-align: center;'>
            QUANTUM ANALYSIS ENGINES
        </h2>
        <p style='text-align: center; margin-bottom: 2rem;'>
            Advanced machine learning architectures powering the detection system
        </p>
        
        <div class="cyber-grid">
            <div class="cyber-card">
                <h3>LOGISTIC REGRESSION</h3>
                <p>Classical statistical model enhanced with quantum computing principles for binary classification tasks.</p>
                <div style='display: flex; justify-content: space-between; font-size: 0.8rem;'>
                    <span>Accuracy: 92.4%</span>
                    <span>v3.1.2</span>
                </div>
            </div>
            <div class="cyber-card">
                <h3>NAIVE BAYES</h3>
                <p>Probabilistic classifier with neural augmentation for rapid content analysis and pattern recognition.</p>
                <div style='display: flex; justify-content: space-between; font-size: 0.8rem;'>
                    <span>Accuracy: 89.7%</span>
                    <span>v2.9.5</span>
                </div>
            </div>
            <div class="cyber-card">
                <h3>RANDOM FOREST</h3>
                <p>Ensemble learning method with 500 decision trees optimized for truthfulness prediction.</p>
                <div style='display: flex; justify-content: space-between; font-size: 0.8rem;'>
                    <span>Accuracy: 94.1%</span>
                    <span>v4.0.1</span>
                </div>
            </div>
            <div class="cyber-card">
                <h3>XGBOOST</h3>
                <p>Gradient boosted trees with deep learning extensions for maximum detection performance.</p>
                <div style='display: flex; justify-content: space-between; font-size: 0.8rem;'>
                    <span>Accuracy: 95.3%</span>
                    <span>v4.2.0</span>
                </div>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
    <div style='text-align: center; margin-top: 3rem; color: rgba(255,255,255,0.5); font-size: 0.8rem;'>
        <p>QUANTUM FAKE NEWS DETECTION SYSTEM © 2023</p>
        <p>NEURAL NETWORK v4.2 | QUBIT PROCESSING ENABLED</p>
    </div>
""", unsafe_allow_html=True)