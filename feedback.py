def get_feedback(model, prediction):
    if model == "heart":
        if prediction == 1:
            return {
                "Risk Level": '<span style="color:black;">⚠️ High Risk</span>',
                "Precautions": [
                    '<span style="color:black;">Avoid saturated fats and reduce salt intake.</span>',
                    '<span style="color:black;">Quit smoking and limit alcohol.</span>',
                    '<span style="color:black;">Exercise regularly and manage stress.</span>'
                ],
                "Consultation": '<span style="color:black;">Consider consulting a cardiologist and getting an ECG done.</span>'
            }
        else:
            return {
                "Risk Level": '<span style="color:black;">✅ Low Risk</span>',
                "Suggestions": [
                    '<span style="color:black;">Maintain a healthy diet and exercise regularly.</span>',
                    '<span style="color:black;">Continue regular health checkups.</span>'
                ]
            }
    elif model == "diabetes":
        if prediction == 1:
            return {
                "Risk Level": '<span style="color:black;">⚠️ High Risk</span>',
                "Precautions": [
                    '<span style="color:black;">Limit sugar and refined carbohydrates.</span>',
                    '<span style="color:black;">Monitor your blood sugar regularly.</span>',
                    '<span style="color:black;">Maintain a healthy weight and stay active.</span>'
                ],
                "Consultation": '<span style="color:black;">Schedule a visit with an endocrinologist.</span>'
            }
        else:
            return {
                "Risk Level": '<span style="color:black;">✅ Low Risk</span>',
                "Suggestions": [
                    '<span style="color:black;">Stay active and eat a balanced diet.</span>',
                    '<span style="color:black;">Get regular blood sugar screenings.</span>'
                ]
            }
