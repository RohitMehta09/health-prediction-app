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

# Initialize session state for navigation
if "page" not in st.session_state:
    st.session_state.page = "login"  # Default page is login
if "username" not in st.session_state:
    st.session_state.username = None

# Navigation logic
if st.session_state.page == "login":
    login_page()
elif st.session_state.page == "signup":
    signup_page()
elif st.session_state.page == "prediction":
    prediction_page()