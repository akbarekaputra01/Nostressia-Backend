import joblib
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models_ml", "current_stress_model.joblib")

class StressModelService:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.feature_names = None
        self.load_model()

    def load_model(self):
        # Gunakan logging print sederhana untuk debugging saat startup
        print(f"INFO: Loading model from {MODEL_PATH}")
        if not os.path.exists(MODEL_PATH):
            print(f"ERROR: Model file not found at {MODEL_PATH}")
            return

        try:
            data = joblib.load(MODEL_PATH)
            if isinstance(data, dict):
                self.model = data.get('model')
                self.scaler = data.get('scaler')
                self.feature_names = data.get('feature_names')
            else:
                self.model = data
            print("INFO: ML Model loaded successfully (Optimized Runtime)")
        except Exception as e:
            print(f"ERROR: Failed to load model artifacts: {e}")

    def _calculate_academic_performance_encoded(self, gpa: float) -> int:
        """Categorize GPA based on defined academic standards."""
        if gpa >= 3.5: category = 'Excellent'
        elif 3.0 <= gpa < 3.5: category = 'Good'
        elif 2.0 <= gpa < 3.0: category = 'Fair'
        else: category = 'Poor'
        
        mapping = {'Poor': 0, 'Fair': 1, 'Good': 2, 'Excellent': 3}
        return mapping.get(category, 0)

    def predict_stress(self, input_data: dict) -> str:
        if not self.model:
            return "Error: Model not initialized"

        try:
            # 1. Feature Engineering
            gpa = float(input_data['gpa'])
            academic_encoded = self._calculate_academic_performance_encoded(gpa)

            # 2. Data Preparation (Using Dictionary instead of DataFrame for memory efficiency)
            raw_features = {
                'Study_Hours_Per_Day': input_data['study_hours'],
                'Extracurricular_Hours_Per_Day': input_data['extracurricular_hours'],
                'Sleep_Hours_Per_Day': input_data['sleep_hours'],
                'Social_Hours_Per_Day': input_data['social_hours'],
                'Physical_Activity_Hours_Per_Day': input_data['physical_hours'],
                'GPA': gpa,
                'Academic_Performance_Encoded': academic_encoded
            }

            # 3. Feature Ordering (Crucial for model consistency)
            if self.feature_names:
                ordered_values = [raw_features[col] for col in self.feature_names]
            else:
                # Fallback ordering based on training schema
                ordered_values = [
                    raw_features['Study_Hours_Per_Day'],
                    raw_features['Extracurricular_Hours_Per_Day'],
                    raw_features['Sleep_Hours_Per_Day'],
                    raw_features['Social_Hours_Per_Day'],
                    raw_features['Physical_Activity_Hours_Per_Day'],
                    raw_features['GPA'],
                    raw_features['Academic_Performance_Encoded']
                ]

            # 4. Convert to Numpy Array (2D)
            final_input = np.array([ordered_values])

            # 5. Scaling
            if self.scaler:
                final_input = self.scaler.transform(final_input)

            # 6. Inference
            prediction_idx = self.model.predict(final_input)[0]
            label_map = {0: "Low", 1: "Moderate", 2: "High"}
            
            return label_map.get(prediction_idx, "Unknown")

        except Exception as e:
            print(f"ERROR: Prediction failed: {e}")
            return f"Error: {str(e)}"

ml_service = StressModelService()