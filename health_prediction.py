import pickle
import numpy as np
import sqlite3
from datetime import datetime
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_diabetes
import pickle
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split

import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

# Load the UCI Heart Disease Dataset
data = pd.read_csv("heart.xls")  # Replace with the actual path to the dataset
categorical_columns = ['Sex', 'ChestPainType', 'RestingECG', 'ExerciseAngina', 'ST_Slope']
data = pd.get_dummies(data, columns=categorical_columns, drop_first=True)
# Define features and target
X = data.drop("HeartDisease", axis=1)  # Replace "target" with the actual target column name
y = data["HeartDisease"]

# Split the dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the SVM model
heart_model = SVC(probability=True)
heart_model.fit(X_train, y_train)

# Save the trained model
with open("SVM_heart_model.pkl", "wb") as f:
    pickle.dump(heart_model, f)
print("Heart disease model trained and saved successfully.")
# Example: Train and save the Logistic Regression model
def train_and_save_diabetes_model():
    # Load example dataset (replace this with your actual dataset)
    data = load_diabetes()
    X = data.data
    y = (data.target > data.target.mean()).astype(int)  # Convert target to binary classification
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the model
    diabetes_model = LogisticRegression()
    diabetes_model.fit(X_train, y_train)

    # Save the trained model
    with open("Logistic Regression_diabetes_model.pkl", "wb") as f:
        pickle.dump(diabetes_model, f)
    print("Diabetes model trained and saved successfully.")

# Uncomment the following line to train and save the diabetes model
# train_and_save_diabetes_model()

# Load the heart disease model
try:
    with open("SVM_heart_model.pkl", "rb") as f:
        heart_model = pickle.load(f)
        print(f"Heart disease model loaded successfully: {type(heart_model)}")  # Debugging
except Exception as e:
    print(f"Error loading heart disease model: {e}")
    heart_model = None

# Load the diabetes model
try:
    with open("Logistic Regression_diabetes_model.pkl", "rb") as f:
        diabetes_model = pickle.load(f)
        print(f"Diabetes model loaded successfully: {type(diabetes_model)}")  # Debugging
except (EOFError, FileNotFoundError, pickle.UnpicklingError) as e:
    print(f"Error loading diabetes disease model: {e}")
    diabetes_model = None

# Initialize and connect to user data DB
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

# Create predictions table (if it doesn't exist)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        model TEXT,
        date TEXT,
        input_data TEXT,
        prediction INTEGER
    )
''')
conn.commit()

def predict_heart(username, input_dict):
    if heart_model is None:
        raise ValueError("Heart disease model is not loaded. Please check the model file.")

    # Preprocess input features
    sex = 1 if input_dict["sex"] == "M" else 0
    cp = ["Typical Angina", "Atypical Angina", "Non-anginal Pain", "Asymptomatic"].index(input_dict["cp"])
    fbs = 1 if input_dict["fbs"] == "Yes" else 0
    restecg = ["Normal", "ST-T Abnormality", "Left Ventricular Hypertrophy"].index(input_dict["restecg"])
    exang = 1 if input_dict["exang"] == "Yes" else 0
    slope = ["Upsloping", "Flat", "Downsloping"].index(input_dict["slope"])
    thal = ["Normal", "Fixed Defect", "Reversible Defect"].index(input_dict["thal"])

    features = [
        input_dict["age"],
        sex,
        cp,
        input_dict["trestbps"],
        input_dict["chol"],
        fbs,
        restecg,
        input_dict["thalach"],
        exang,
        input_dict["oldpeak"],
        slope,
        input_dict["ca"],
        thal,
        0,  # dummy
        0   # dummy
    ]

    features = np.array(features).reshape(1, -1)
    prediction = int(heart_model.predict(features)[0])
    prob = float(heart_model.predict_proba(features)[0][prediction])

    save_prediction(username, "Heart", input_dict, prediction)
    return prediction, prob

def predict_diabetes(username, input_dict):
    if diabetes_model is None:
        raise ValueError("Diabetes model is not loaded. Please check the model file.")

    # Preprocess input features
    features = [
        input_dict["pregnancies"],
        input_dict["glucose"],
        input_dict["bp"],
        input_dict["skin"],
        input_dict["insulin"],
        input_dict["bmi"],
        input_dict["dpf"],
        input_dict["age"],
        0,
        0
    ]

    features = np.array(features).reshape(1, -1)
    prediction = int(diabetes_model.predict(features)[0])
    prob = float(diabetes_model.predict_proba(features)[0][prediction])

    save_prediction(username, "Diabetes", input_dict, prediction)

    return prediction, prob

def save_prediction(username, model, input_data, prediction):
    cursor.execute('''
        INSERT INTO predictions (username, model, date, input_data, prediction)
        VALUES (?, ?, ?, ?, ?)
    ''', (username, model, datetime.now().strftime("%Y-%m-%d %H:%M"), str(input_data), prediction))
    conn.commit()

def get_user_predictions(username):
    cursor.execute("SELECT * FROM predictions WHERE username = ? ORDER BY date DESC", (username,))
    data = cursor.fetchall()
    if data:
        df = pd.DataFrame(data, columns=["id", "username", "model", "timestamp", "input_data", "prediction"])
        return df
    return pd.DataFrame()