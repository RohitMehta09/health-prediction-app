from user_auth import authenticate_user
import streamlit as st

def login_page():
    # Inject custom CSS for background and styling
    st.markdown("""
        <style>
        body {
            margin: 0;
            padding: 0;
        }
        .background {
            background-image: url('https://source.unsplash.com/1600x900/?health,technology');
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
        
        .title {
            font-size: 2.5rem;
            color: #4CAF50;
            text-align: center;
            margin-bottom: 20px;
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
    st.markdown("Don't have an account? Sign up here", unsafe_allow_html=True)
    if st.button("Sign Up", key="signup_button"):
        st.session_state.page = "signup"

    # Close main container
    st.markdown('</div>', unsafe_allow_html=True)