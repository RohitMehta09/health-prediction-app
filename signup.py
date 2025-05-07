import streamlit as st
from user_auth import register_user
import random
import smtplib
from email.mime.text import MIMEText

# Function to send OTP via email
def send_otp(email):
    otp = str(random.randint(100000, 999999))  # Generate a 6-digit OTP
    subject = "Your OTP for AI Smart Health Monitoring System"
    body = f"Your OTP is: {otp}\n\nPlease use this OTP to complete your signup process."
    sender_email = "mehtarohit.0911@gmail.com"  # Replace with your email
    sender_password = "zgidkhndfsppxjcz"  # Replace with your email password

    # Send email
    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = email

        with smtplib.SMTP("smtp.gmail.com", 587) as server:  # Use Gmail's SMTP server
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, email, msg.as_string())
        return otp
    except Exception as e:
        st.error(f"Failed to send OTP: {e}")
        return None

def signup_page():
    # Inject custom CSS for background and styling
    st.markdown("""
        <style>
        body, .stApp {
            margin: 0;
            padding: 0;
            background: transparent !important;
        }
        .block-container {
            background: transparent !important;
            box-shadow: none !important;
        }
        .background {
            background-image: url('https://images.unsplash.com/photo-1584982751601-97dcc096659c?q=80&w=2072&auto=format&fit=crop');
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
            background: transparent !important;
            position: relative;
            z-index: 1;
        }
        .title {
            font-size: 2.5rem;
            font-weight: bold;
            color: #4B0082;
            text-align: center;
            margin-bottom: 20px;
        }
        label {
            color: black !important;
        }
        </style>
        <div class="background"></div>
    """, unsafe_allow_html=True)

    # Main container for signup form
    st.markdown('<div class="main-container">', unsafe_allow_html=True)

    # Title
    st.markdown('<div class="title">📝 Sign Up for AI Smart Health Monitoring System</div>', unsafe_allow_html=True)

    # Signup form
    username = st.text_input("Choose a Username")
    email = st.text_input("Enter Your Email")
    password = st.text_input("Choose a Password", type="password")
    signup_button = st.button("Send OTP")

    if signup_button:
        if username and email and password:  # Ensure all fields are filled
            otp = send_otp(email)
            if otp:
                st.session_state["otp"] = otp  # Store OTP in session state
                st.session_state["signup_data"] = {"username": username, "email": email, "password": password}
                st.success("OTP sent to your email. Please check your inbox.")
            else:
                st.error("Failed to send OTP. Please try again.")
        else:
            st.error("Please fill in all fields.")

    # OTP verification
    if "otp" in st.session_state:
        entered_otp = st.text_input("Enter the OTP sent to your email")
        verify_button = st.button("Verify OTP")

        if verify_button:
            if entered_otp == str(st.session_state["otp"]):  # Compare entered OTP with stored OTP
                signup_data = st.session_state.get("signup_data", {})
                if signup_data:
                    if register_user(signup_data["username"], signup_data["email"], signup_data["password"]):
                        st.success("Account created successfully! Redirecting to login page...")
                        st.session_state.page = "login"  # Redirect to login page
                        del st.session_state["otp"]  # Clear OTP from session state
                        del st.session_state["signup_data"]  # Clear signup data
                    else:
                        st.error("Username or email already exists. Please try again.")
            else:
                st.error("Invalid OTP. Please try again.")

    # Link to login page
    st.markdown("Already have an account? [Log in here](#)", unsafe_allow_html=True)
    if st.button("Log In"):
        st.session_state.page = "login"

    # Close main container
    st.markdown('</div>', unsafe_allow_html=True)
