def get_feedback(model, prediction):
    if model == "heart":
        if prediction == 1:
            return {
                "Risk Level": '<span style="color:black;">⚠️ High Risk</span>',
                "Precautions": [
                    "Avoid saturated fats and reduce salt intake.",
                    "Quit smoking and limit alcohol.",
                    "Exercise regularly and manage stress."
                ],
                "Consultation": '<span style="color:black;">Consider consulting a cardiologist and getting an ECG done.</span>'
            }
        else:
            return {
                "Risk Level": '<span style="color:black;">✅ Low Risk</span>',
                "Suggestions": [
                    "Maintain a healthy diet and exercise regularly.",
                    "Continue regular health checkups."
                ]
            }
    elif model == "diabetes":
        if prediction == 1:
            return {
                "Risk Level": '<span style="color:black;">⚠️ High Risk</span>',
                "Precautions": [
                    "Limit sugar and refined carbohydrates.",
                    "Monitor your blood sugar regularly.",
                    "Maintain a healthy weight and stay active."
                ],
                "Consultation": "Schedule a visit with an endocrinologist."
            }
        else:
            return {
                "Risk Level": '<span style="color:black;">✅ Low Risk</span>',
                "Suggestions": [
                    "Stay active and eat a balanced diet.",
                    "Get regular blood sugar screenings."
                ]
            }
