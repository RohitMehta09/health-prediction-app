from user_auth import authenticate_user
import streamlit as st

def login_page():
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
            background-image: url('https://plus.unsplash.com/premium_photo-1670459707416-26dad95d99af?q=80&w=1897&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'); /* Replace with a direct image URL */
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

    # Main container for login form
    st.markdown('<div class="main-container">', unsafe_allow_html=True)

    # Title
    st.markdown('<div class="title">🔑 Login to AI Smart Health Monitoring System</div>', unsafe_allow_html=True)

    # Login form
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login", key="login_button")

    if login_button:
        if authenticate_user(username, password):
            st.session_state.username = username
            st.session_state.page = "prediction"  # Redirect to prediction page
        else:
            st.error("Invalid username or password. Please try again.")

    # Link to signup page
    st.markdown("Don't have an account? [Sign up here](#)", unsafe_allow_html=True)
    if st.button("Sign Up", key="signup_button"):
        st.session_state.page = "signup"

    # Close main container
    st.markdown('</div>', unsafe_allow_html=True)
