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
    st.title("📝 Sign Up for AI Smart Health Monitoring System")

    # Signup form
    username = st.text_input("Choose a Username")
    email = st.text_input("Enter Your Email")
    password = st.text_input("Choose a Password", type="password")
    signup_button = st.button("Send OTP")

    if signup_button:
        if username and email and password:  # Ensure all fields are filled
            otp = send_otp(email)
            if otp:
                st.success("OTP sent to your email. Please check your inbox.")
                entered_otp = st.text_input("Enter the OTP sent to your email")
                verify_button = st.button("Verify OTP")

                if verify_button:
                    if entered_otp == otp:
                        if register_user(username, email, password):
                            st.success("Account created successfully! Please log in.")
                            st.session_state.page = "login"  # Redirect to login page
                        else:
                            st.error("Username or email already exists. Please try again.")
                    else:
                        st.error("Invalid OTP. Please try again.")
        else:
            st.error("Please fill in all fields.")

    # Link to login page
    st.markdown("Already have an account? [Log in here](#)", unsafe_allow_html=True)
    if st.button("Log In"):
        st.session_state.page = "login"