import streamlit as st
from login import login_page
from signup import signup_page
from prediction import prediction_page
from health_prediction import predict_heart, predict_diabetes, get_user_predictions
from feedback import get_feedback

# Set page configuration
st.set_page_config(
    page_title="AI Smart Health Monitoring System",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject custom CSS for background and styling
st.markdown("""
    <style>
    body, .stApp {
        margin: 0;
        padding: 0;
        background: transparent !important; /* Ensure body and main container are transparent */
    }
    .block-container {
        background: transparent !important; /* Make the main block container transparent */
        box-shadow: none !important; /* Remove any shadow that might appear */
    }
    .background {
        background-image: url('https://images.unsplash.com/photo-1603398938378-e54eab446dde?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'); /* Replace with a direct image URL */
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
    }
    .main-container {
        background: transparent !important; /* Ensure main container is transparent */
        position: relative; /* Ensure it sits above the background */
        z-index: 1; /* Ensure it is above the background */
    }
    .title {
        font-size: 2.5rem;
        font-weight: bold;
        color: #4B0082;
        text-align: center;
        margin-bottom: 20px;
    }
    label {
        color: black !important; /* Change label text color to black */
    }
    </style>
    <div class="background"></div>
""", unsafe_allow_html=True)

# Initialize session state for navigation
if "page" not in st.session_state:
    st.session_state.page = "login"  # Default page is login
if "username" not in st.session_state:
    st.session_state.username = None

# Conditionally add an image to the sidebar only on the prediction page
if st.session_state.page == "prediction":
    st.sidebar.image(
        "https://plus.unsplash.com/premium_photo-1673953510107-d5aee40d80a7?q=80&w=1887&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D", 
        use_container_width=True
    )

# Navigation logic
if st.session_state.page == "login":
    login_page()
elif st.session_state.page == "signup":
    signup_page()
elif st.session_state.page == "prediction":
    prediction_page()
