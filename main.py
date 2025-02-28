import streamlit as st
import base64
import time

# Set page config - must be the first Streamlit command
st.set_page_config(
    page_title="The SlangLab",
    page_icon="🔥",
    layout="wide",
)

# Function to add custom CSS
def local_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&display=swap');

        html, body, [class*="st"] {
            font-family: 'Poppins', sans-serif;
        }
        .main-title {
            font-size: 4rem !important;
            font-weight: 800 !important;
            background: linear-gradient(90deg, #FC466B 0%, #3F5EFB 100%);
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            margin-bottom: 0px !important;
            text-align: center;
            animation: fadeInDown 1s ease-out;
        }
        .sub-title {
            font-size: 1.5rem !important;
            opacity: 0.8;
            text-align: center;
            margin-bottom: 30px;
            animation: fadeInUp 1.5s ease-out;
        }
        @keyframes fadeInDown {
            0% { opacity: 0; transform: translateY(-20px); }
            100% { opacity: 1; transform: translateY(0); }
        }
        @keyframes fadeInUp {
            0% { opacity: 0; transform: translateY(20px); }
            100% { opacity: 1; transform: translateY(0); }
        }
        .button-container {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-bottom: 30px;
        }
        .stButton > button {
            border-radius: 20px;
            font-weight: 600;
            padding: 20px 30px !important;
            border: none;
            transition: all 0.3s ease;
            width: 100%;
            height: 100px !important;
            font-size: 1.2rem !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        }
        .chatbot-btn > button {
            background: linear-gradient(90deg, #FC466B 0%, #3F5EFB 100%);
            color: white;
        }
        .chatbot-btn > button:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
        }
        .quiz-btn > button {
            background: linear-gradient(90deg, #3F5EFB 0%, #FC466B 100%);
            color: white;
        }
        .quiz-btn > button:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
        }
        .slang-card {
            background-color: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 20px;
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            margin-bottom: 20px;
            animation: fadeIn 1s ease-out;
        }
        @keyframes fadeIn {
            0% { opacity: 0; }
            100% { opacity: 1; }
        }
        .divider {
            margin: 30px 0;
            text-align: center;
            font-size: 2rem;
        }
        .footer {
            text-align: center;
            font-size: 0.8rem;
            opacity: 0.7;
            padding-top: 50px;
        }
    </style>
    """, unsafe_allow_html=True)

def set_background():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: linear-gradient(135deg, #121212 0%, #2d3436 100%);
            background-size: cover;
            color: white;
        }}
        """,
        unsafe_allow_html=True
    )

def main():
    set_background()
    local_css()

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown('<h1 class="main-title">The SlangLab</h1>', unsafe_allow_html=True)
        st.markdown('<p class="sub-title">Translate Gen Z slang with style</p>', unsafe_allow_html=True)

        slang_examples = [
            {"slang": "no cap", "meaning": "not lying, telling the truth"},
            {"slang": "bussin", "meaning": "really good, especially food"},
            {"slang": "slay", "meaning": "to do something really well"},
            {"slang": "sus", "meaning": "suspicious, sketchy"},
            {"slang": "bet", "meaning": "agreement or confirmation"}
        ]

        for i, example in enumerate(slang_examples):
            st.markdown(
                f"""
                <div class="slang-card">
                    <b>🔥 "{example['slang']}"</b> → {example['meaning']}
                </div>
                """,
                unsafe_allow_html=True
            )
            time.sleep(0.2)

        st.markdown('<div class="divider">🔥</div>', unsafe_allow_html=True)

        st.markdown('<div class="button-container">', unsafe_allow_html=True)

        col_btn1, col_btn2 = st.columns(2)

        with col_btn1:
            st.markdown('<div class="chatbot-btn">', unsafe_allow_html=True)
            if st.button("💬 Chat with SlangBot"):
                st.switch_page("pages/app.py")
            st.markdown('</div>', unsafe_allow_html=True)

        with col_btn2:
            st.markdown('<div class="quiz-btn">', unsafe_allow_html=True)
            if st.button("🧠 Test Your Slang"):
                st.switch_page("pages/quiz.py")
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown(
            '<div class="footer">Stay lit, fam! © The SlangLab 2025</div>',
            unsafe_allow_html=True
        )

if __name__ == "__main__":
    main()
