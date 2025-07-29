import streamlit as st
import joblib
from sentence_transformers import SentenceTransformer
import numpy as np
from streamlit_extras.let_it_rain import rain
import time

# Load custom CSS
def load_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700&display=swap');
        :root {
            --primary: #00f2ff;
            --secondary: #ff00e6;
            --accent: #00ff9d;
            --bg: #0a0a1a;
            --card-bg: #121230;
        }
        * { font-family: 'Orbitron', sans-serif; }
        body { background-color: var(--bg); color: white; }
        .stApp {
            background: linear-gradient(135deg, var(--bg) 0%, #0f0f2d 100%);
        }
        .stTextInput>div>div>input, .stTextArea>div>div>textarea {
            background-color: rgba(18, 18, 48, 0.8) !important;
            color: white !important;
            border: 1px solid var(--primary) !important;
            border-radius: 8px !important;
            box-shadow: 0 0 10px rgba(0, 242, 255, 0.3);
        }
        .stButton>button {
            background: linear-gradient(90deg, var(--primary) 0%, var(--secondary) 100%) !important;
            color: black !important;
            border: none !important;
            border-radius: 25px !important;
            padding: 10px 24px !important;
            font-weight: 700 !important;
            box-shadow: 0 0 15px rgba(0, 242, 255, 0.5);
            transition: all 0.3s ease !important;
        }
        .stButton>button:hover {
            transform: scale(1.05) !important;
            box-shadow: 0 0 20px rgba(0, 242, 255, 0.8) !important;
        }
        .stProgress>div>div>div {
            background: linear-gradient(90deg, var(--accent) 0%, var(--primary) 100%) !important;
            box-shadow: 0 0 10px rgba(0, 255, 157, 0.5);
        }
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
            color: var(--primary) !important;
            text-shadow: 0 0 10px rgba(0, 242, 255, 0.5);
            font-family: 'Orbitron', sans-serif !important;
        }
        .css-1aumxhk {
            background-color: var(--card-bg) !important;
            border: 1px solid var(--secondary) !important;
            border-radius: 12px !important;
            box-shadow: 0 0 15px rgba(255, 0, 230, 0.3);
        }
        .css-1aumxhk:hover {
            box-shadow: 0 0 25px rgba(255, 0, 230, 0.5) !important;
        }
        .prediction-card {
            background: linear-gradient(135deg, rgba(18, 18, 48, 0.8) 0%, rgba(10, 10, 26, 0.9) 100%) !important;
            border: 1px solid var(--accent) !important;
            border-radius: 16px !important;
            padding: 20px;
            margin: 10px 0;
            box-shadow: 0 0 20px rgba(0, 255, 157, 0.3);
        }
        .scanning-animation {
            position: relative;
            overflow: hidden;
        }
        .scanning-animation::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, transparent, var(--primary), transparent);
            animation: scan 2s linear infinite;
        }
        @keyframes scan {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(100%); }
        }
        [data-testid="stExpander"] div[role="button"] p {
        color: white !important;
    }
    
    /* FORCE ALL OTHER TEXT IN EXPANDER */
    [data-testid="stExpander"] div[role="button"] + div * {
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Load model and encoder
@st.cache_resource
def load_model():
    model = joblib.load("bert_fake_news_model.pkl")
    embedder = SentenceTransformer('all-MiniLM-L6-v2')
    return model, embedder

clf, model_sbert = load_model()

def predict_news(text):
    cleaned = text.strip().lower()
    embedded = model_sbert.encode([cleaned])
    pred = clf.predict(embedded)[0]
    proba = clf.predict_proba(embedded)[0]
    label = "REAL" if pred == 1 else "FAKE"
    confidence = proba[pred] * 100
    return label, confidence, proba

def show_prediction_animation():
    with st.empty():
        for _ in range(3):
            st.markdown("<div class='scanning-animation' style='height: 20px; margin: 20px 0;'></div>", unsafe_allow_html=True)
            time.sleep(0.3)
            st.empty()
            time.sleep(0.2)

def main():
    load_css()

    st.markdown("""
    <div style='text-align: center; margin-bottom: 30px;'>
        <h1 class='glow-text'>NEURAL NEWS VERIFIER</h1>
        <p style='color: var(--accent); font-size: 1.2em;'>Advanced AI-powered fake news detection system by Yogesh Chauhan</p>
        <div style='height: 2px; background: linear-gradient(90deg, transparent, var(--primary), var(--secondary), transparent); margin: 10px 0 20px;'></div>
    </div>
    """, unsafe_allow_html=True)

    if "example_text" not in st.session_state:
        st.session_state.example_text = ""

    st.markdown("### <span style='color: var(--primary)'>INPUT NEWS CONTENT</span>", unsafe_allow_html=True)
    user_input = st.text_area(
        "", 
        height=250,
        placeholder="Paste news article or headline here for analysis...",
        value=st.session_state.example_text,
        help="The system will analyze the text using advanced neural networks"
    )

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        predict_btn = st.button("🚀 INITIATE ANALYSIS", use_container_width=True)

    if predict_btn:
        if not user_input.strip():
            st.error("⚠️ INPUT REQUIRED: Please enter news content for verification")
        else:
            show_prediction_animation()
            label, confidence, proba = predict_news(user_input)
            st.session_state.example_text = user_input

            st.markdown(f"""
            <div class='prediction-card'>
                <h3 style='color: {'var(--accent)' if label == 'REAL' else 'var(--secondary)'}; text-align: center;'>
                    VERDICT: <span style='font-size: 1.5em;'>{label}</span>
                </h3>
                <div style='text-align: center; margin: 20px 0;'>
                    <div style='font-size: 2.5em; font-weight: bold; color: {'var(--primary)' if label == 'REAL' else '#ff4d4d'};'>
                        {confidence:.1f}%
                    </div>
                    <div style='color: #aaa;'>confidence level</div>
                </div>
                <div style='height: 10px; background: linear-gradient(90deg, 
                    {'var(--accent) 0%, var(--primary) 100%' if label == 'REAL' else 'var(--secondary) 0%, #ff4d4d 100%'}); 
                    border-radius: 5px; margin: 20px 0;'></div>
            </div>
            """, unsafe_allow_html=True)

            with st.expander("📊 DETAILED ANALYSIS METRICS", expanded=True):
               col1, col2 = st.columns(2)
    
    
               with col1:
                st.markdown("<p style='color: white; margin-bottom: 0.5rem;'>REAL Probability</p>", 
                   unsafe_allow_html=True)
                st.markdown(f"<div style='color: white; font-size: 2rem; font-weight: bold;'>{proba[1]*100:.2f}%</div>", 
                   unsafe_allow_html=True)
                st.progress(int(proba[1]*100))
    
    
                with col2:
                  st.markdown("<p style='color: white; margin-bottom: 0.5rem;'>FAKE Probability</p>", 
                   unsafe_allow_html=True)
                  st.markdown(f"<div style='color: white; font-size: 2rem; font-weight: bold;'>{proba[0]*100:.2f}%</div>", 
                   unsafe_allow_html=True)
                  st.progress(int(proba[0]*100))

    st.markdown("""
    <div style='text-align: center; margin-top: 50px; color: #fff; font-size: 0.8em;'>
        <div style='height: 1px; background: linear-gradient(90deg, transparent, var(--primary), transparent); margin: 20px 0;'></div>
        NEURAL NEWS VERIFIER | Advanced AI Detection System<br>
        Yogesh Chauhan
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
