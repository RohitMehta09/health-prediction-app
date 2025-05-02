import streamlit as st
import plotly.express as px
from health_prediction import predict_heart, predict_diabetes, get_user_predictions
from feedback import get_feedback

def prediction_page():
    if "username" not in st.session_state or not st.session_state.username:
        st.session_state.page = "login"  # Redirect to login if not logged in
        st.experimental_rerun()

    username = st.session_state.username

    # Inject custom CSS for background and transitions
    st.markdown("""
        <style>
        body {
            margin: 0;
            padding: 0;
            background-image: url('https://source.unsplash.com/1600x900/?health,technology');
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            font-family: Arial, sans-serif;
        }
        .sidebar {
            background-color: rgba(255, 255, 255, 0.8);
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.25);
        }
        .sub-header {
            font-size: 1.5rem;
            color: #4CAF50;
            text-align: center;
            margin-bottom: 20px;
            animation: fadeIn 2s;
        }
        .risk-box {
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            font-size: 1.2rem;
            margin-top: 20px;
            animation: fadeIn 1.5s;
        }
        .high-risk {
            background-color: rgba(255, 0, 0, 0.1);
            color: red;
        }
        .low-risk {
            background-color: rgba(0, 255, 0, 0.1);
            color: green;
        }
        @keyframes fadeIn {
            from {
                opacity: 0;
            }
            to {
                opacity: 1;
            }
        }
        </style>
    """, unsafe_allow_html=True)

    # Sidebar with Logout
    st.sidebar.markdown('<div class="sidebar">', unsafe_allow_html=True)
    st.sidebar.title(f"Welcome, {username}!")
    if st.sidebar.button("🚪 Logout"):
        st.session_state.username = None
        st.session_state.page = "login"  # Redirect to login page
    st.sidebar.markdown('</div>', unsafe_allow_html=True)

    # Tabs for predictions and logs
    tab1, tab2, tab3 = st.tabs(["❤️ Heart Disease", "🩸 Diabetes", "📊 Logs"])

    # ---------- HEART DISEASE ----------
    with tab1:
        st.markdown('<div class="sub-header">❤️ Heart Disease Risk Prediction</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        with col1:
            age = st.number_input("Age", min_value=1, max_value=120, value=30)
            sex = st.selectbox("Sex", ("M", "F"))
            cp = st.selectbox("Chest Pain Type", ("Typical Angina", "Atypical Angina", "Non-anginal Pain", "Asymptomatic"))
            trestbps = st.number_input("Resting Blood Pressure", value=120)
            chol = st.number_input("Cholesterol", value=200)

        with col2:
            fbs = st.selectbox("Fasting Blood Sugar > 120 mg/dl", ("Yes", "No"))
            restecg = st.selectbox("Resting ECG", ("Normal", "ST-T Abnormality", "Left Ventricular Hypertrophy"))
            thalach = st.number_input("Max Heart Rate", value=150)
            exang = st.selectbox("Exercise Induced Angina", ("Yes", "No"))
            oldpeak = st.slider("Oldpeak", 0.0, 6.0, step=0.1)
            slope = st.selectbox("ST Slope", ("Upsloping", "Flat", "Downsloping"))
            ca = st.selectbox("Major Vessels Colored by Fluoroscopy", (0, 1, 2, 3))
            thal = st.selectbox("Thalassemia", ("Normal", "Fixed Defect", "Reversible Defect"))

        input_dict = {
            "age": age,
            "sex": sex,
            "cp": cp,
            "trestbps": trestbps,
            "chol": chol,
            "fbs": fbs,
            "restecg": restecg,
            "thalach": thalach,
            "exang": exang,
            "oldpeak": oldpeak,
            "slope": slope,
            "ca": ca,
            "thal": thal
        }

        if st.button("🔍 Predict Heart Disease"):
            result, prob = predict_heart(username, input_dict)
            feedback = get_feedback("heart", result)

            # Display Risk Level
            risk_class = "high-risk" if result == 1 else "low-risk"
            st.markdown(f'<div class="risk-box {risk_class}">{feedback["Risk Level"]}</div>', unsafe_allow_html=True)

            # Display Precautions or Suggestions
            if "Precautions" in feedback:
                st.markdown("### ⚠️ Precautions")
                for precaution in feedback["Precautions"]:
                    st.markdown(f"- {precaution}")
            if "Suggestions" in feedback:
                st.markdown("### 💡 Suggestions")
                for suggestion in feedback["Suggestions"]:
                    st.markdown(f"- {suggestion}")

            # Display Consultation Advice
            if "Consultation" in feedback:
                st.markdown("### 👨‍⚕️ Consultation Advice")
                st.markdown(f"- {feedback['Consultation']}")

    # ---------- DIABETES ----------
    with tab2:
        st.markdown('<div class="sub-header">🩸 Diabetes Risk Prediction</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        with col1:
            preg = st.number_input("Pregnancies", min_value=0, max_value=20, value=1)
            glucose = st.number_input("Glucose Level", min_value=0, value=120)
            bp = st.number_input("Blood Pressure", min_value=0, value=70)

        with col2:
            skin = st.number_input("Skin Thickness", min_value=0, value=20)
            insulin = st.number_input("Insulin", min_value=0, value=80)
            bmi = st.number_input("BMI", min_value=0.0, value=25.0)
            dpf = st.number_input("Diabetes Pedigree Function", min_value=0.0, value=0.5)
            age_d = st.number_input("Age", min_value=1, value=30)

        input_dict = {
            "pregnancies": preg,
            "glucose": glucose,
            "bp": bp,
            "skin": skin,
            "insulin": insulin,
            "bmi": bmi,
            "dpf": dpf,
            "age": age_d
        }

        if st.button("🔍 Predict Diabetes"):
            result, prob = predict_diabetes(username, input_dict)
            feedback = get_feedback("diabetes", result)

            # Display Risk Level
            risk_class = "high-risk" if result == 1 else "low-risk"
            st.markdown(f'<div class="risk-box {risk_class}">{feedback["Risk Level"]}</div>', unsafe_allow_html=True)

            # Display Precautions or Suggestions
            if "Precautions" in feedback:
                st.markdown("### ⚠️ Precautions")
                for precaution in feedback["Precautions"]:
                    st.markdown(f"- {precaution}")
            if "Suggestions" in feedback:
                st.markdown("### 💡 Suggestions")
                for suggestion in feedback["Suggestions"]:
                    st.markdown(f"- {suggestion}")

            # Display Consultation Advice
            if "Consultation" in feedback:
                st.markdown("### 👨‍⚕️ Consultation Advice")
                st.markdown(f"- {feedback['Consultation']}")

    # ---------- LOGS ----------
    with tab3:
        st.markdown('<div class="sub-header">📊 Your Prediction Logs</div>', unsafe_allow_html=True)
        logs_df = get_user_predictions(username)
        if not logs_df.empty:
            st.dataframe(logs_df)
            chart = px.histogram(logs_df, x="timestamp", color="model", barmode="group")
            st.plotly_chart(chart, use_container_width=True)
        else:
            st.info("No predictions logged yet.")