import joblib
import pandas as pd  
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
        print(f"🔍 Mencari model di: {MODEL_PATH}")
        
        if not os.path.exists(MODEL_PATH):
            print(f"⚠️  FILE TIDAK DITEMUKAN!")
            return

        try:
            data = joblib.load(MODEL_PATH)
            if isinstance(data, dict):
                self.model = data.get('model')
                self.scaler = data.get('scaler')
                self.feature_names = data.get('feature_names')
            else:
                self.model = data
            
            print("✅ ML Model Berhasil Dimuat (Versi Pandas)!")
        except Exception as e:
            print(f"❌ Error saat load joblib: {e}")

    def _calculate_academic_performance_encoded(self, gpa):
        if gpa >= 3.5: category = 'Excellent'
        elif 3.0 <= gpa < 3.5: category = 'Good'
        elif 2.0 <= gpa < 3.0: category = 'Fair'
        else: category = 'Poor'
        
        mapping = {'Poor': 0, 'Fair': 1, 'Good': 2, 'Excellent': 3}
        return mapping.get(category, 0)

    def predict_stress(self, input_data: dict) -> str:
        if not self.model: return "Error: Model not ready"

        try:
            # 1. Feature Engineering
            gpa = input_data['gpa']
            academic_encoded = self._calculate_academic_performance_encoded(gpa)

            # 2. Bikin DataFrame (Cara Pandas)
            # Ini sesuai banget sama cara dosen/notebook kamu
            new_data = {
                'Study_Hours_Per_Day': [input_data['study_hours']],
                'Extracurricular_Hours_Per_Day': [input_data['extracurricular_hours']],
                'Sleep_Hours_Per_Day': [input_data['sleep_hours']],
                'Social_Hours_Per_Day': [input_data['social_hours']],
                'Physical_Activity_Hours_Per_Day': [input_data['physical_hours']],
                'GPA': [gpa],
                'Academic_Performance_Encoded': [academic_encoded]
            }
            
            df = pd.DataFrame(new_data)

            # 3. Urutkan Kolom (Penting biar match sama model)
            if self.feature_names is not None:
                # Pastikan nama kolom di DataFrame sama persis dengan yang diminta model
                # Kalau ada kolom yang beda nama dikit aja, Pandas bakal error/nambah kolom NaN
                try:
                    df = df[self.feature_names]
                except KeyError:
                    # Fallback kalau nama kolom di model beda case/typo
                    pass 

            # 4. Scaling
            if self.scaler:
                final_input = self.scaler.transform(df)
            else:
                final_input = df

            # 5. Predict
            prediction_idx = self.model.predict(final_input)[0]
            label_map = {0: "Low", 1: "Moderate", 2: "High"}
            
            return label_map.get(prediction_idx, "Unknown")

        except Exception as e:
            print(f"❌ Prediction Error: {e}")
            return f"Error: {str(e)}"

ml_service = StressModelService()