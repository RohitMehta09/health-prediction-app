def get_feedback(model, prediction):
    if model == "heart":
        if prediction == 1:
            return {
                "Risk Level": "⚠️ High Risk",
                "Precautions": [
                    "Avoid saturated fats and reduce salt intake.",
                    "Quit smoking and limit alcohol.",
                    "Exercise regularly and manage stress."
                ],
                "Consultation": "Consider consulting a cardiologist and getting an ECG done."
            }
        else:
            return {
                "Risk Level": "✅ Low Risk",
                "Suggestions": [
                    "Maintain a healthy diet and exercise regularly.",
                    "Continue regular health checkups."
                ]
            }
    elif model == "diabetes":
        if prediction == 1:
            return {
                "Risk Level": "⚠️ High Risk",
                "Precautions": [
                    "Limit sugar and refined carbohydrates.",
                    "Monitor your blood sugar regularly.",
                    "Maintain a healthy weight and stay active."
                ],
                "Consultation": "Schedule a visit with an endocrinologist."
            }
        else:
            return {
                "Risk Level": "✅ Low Risk",
                "Suggestions": [
                    "Stay active and eat a balanced diet.",
                    "Get regular blood sugar screenings."
                ]
            }
