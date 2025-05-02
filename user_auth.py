import streamlit as st
import sqlite3
from sqlite3 import Connection
import hashlib
import random
import smtplib
from email.mime.text import MIMEText

DB_NAME = "users.db"

def get_connection() -> Connection:
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def create_user_table():
    conn = get_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        email TEXT UNIQUE,
                        password TEXT
                    )''')
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def send_otp(email):
    otp = random.randint(100000, 999999)
    try:
        # Configure your email credentials
        sender_email = "mehtarohit.0911@gmail.com"
        sender_password = "zgidkhndfsppxjcz"  # Replace with your app password
        smtp_server = "smtp.gmail.com"
        smtp_port = 587

        # Create the email content
        msg = MIMEText(f"Your OTP for signup is: {otp}")
        msg["Subject"] = "Signup OTP Verification"
        msg["From"] = sender_email
        msg["To"] = email

        # Send the email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, email, msg.as_string())

        return otp
    except Exception as e:
        st.error(f"Failed to send OTP: {e}")
        return None

def register_user(username, email, password):
    conn = get_connection()
    hashed_password = hash_password(password)
    print(f"Registering user: {username}, {email}, {hashed_password}")  # Debugging
    try:
        conn.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", 
                     (username, email, hashed_password))
        conn.commit()
        print("User registered successfully!")  # Debugging
        return True
    except sqlite3.IntegrityError as e:
        print(f"IntegrityError: {e}")  # Debugging
        return False
    finally:
        conn.close()

def authenticate_user(username, password):
    conn = get_connection()
    hashed_password = hash_password(password)
    print(f"Logging in user with hashed password: {hashed_password}")  # Debugging
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_password))
    user = cursor.fetchone()
    conn.close()
    return user

def login_ui():
    st.sidebar.subheader("🔐 User Login")
    choice = st.sidebar.radio("Login or Sign Up", ("Login", "Sign Up"))

    if choice == "Login":
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")
        if st.sidebar.button("Login"):
            user = login_user(username, password)
            if user:
                st.session_state["user"] = username
                st.success(f"Welcome back, {username}!")
            else:
                st.error("Invalid credentials")

    elif choice == "Sign Up":
        new_user = st.sidebar.text_input("Create Username")
        email = st.sidebar.text_input("Email")
        new_password = st.sidebar.text_input("Create Password", type="password")
        if st.sidebar.button("Send OTP"):
            otp = send_otp(email)
            if otp:
                st.session_state["otp"] = otp
                st.success("OTP sent to your email. Please verify.")
        if "otp" in st.session_state:
            entered_otp = st.sidebar.text_input("Enter OTP")
            if st.sidebar.button("Verify OTP"):
                if entered_otp == str(st.session_state["otp"]):
                    if register_user(new_user, email, new_password):
                        st.success("User created successfully. Please log in.")
                        del st.session_state["otp"]
                    else:
                        st.error("Username or email already exists. Try another.")
                else:
                    st.error("Invalid OTP. Please try again.")
def print_users_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    conn.close()

print_users_table()

def get_logged_in_user():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    username = st.session_state.get("user", None)
    if username:
        cursor.execute("SELECT email FROM users WHERE username = ?", (username,))
        user_data = cursor.fetchone()
        conn.close()
        if user_data:
            return username, user_data[0]  # Return username and email
    conn.close()
    return None, None

def logout_user():
    if "user" in st.session_state:
        del st.session_state["user"]