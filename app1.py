import streamlit as st
import os
import sys
from src.pipeline.train_pipeline import TraininingPipeline
from src.pipeline.predict_pipeline import PredictionPipeline
from src.exception import CustomException

st.set_page_config(page_title="Wafer Fault Detection", layout="centered")

st.title("🔍 Wafer Fault Detection System")

# Section 1: Train model
st.header("🚀 Model Training")
if st.button("Start Training"):
    try:
        train_pipeline = TraininingPipeline()
        train_pipeline.run_pipeline()
        st.success("✅ Training Completed Successfully!")
    except Exception as e:
        st.error(f"❌ Training Failed: {str(e)}")
        raise CustomException(e, sys)

# Section 2: Prediction
st.header("📦 Upload File for Prediction")
uploaded_file = st.file_uploader("Upload your wafer sensor CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        # Save uploaded file temporarily
        file_path = os.path.join("prediction_artifacts", uploaded_file.name)
        os.makedirs("prediction_artifacts", exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Inject into request-like structure for prediction pipeline
        class DummyRequest:
            files = {"file": open(file_path, "rb")}

        st.info("⏳ Running prediction...")
        prediction_pipeline = PredictionPipeline(DummyRequest())
        prediction_file_detail = prediction_pipeline.run_pipeline()

        st.success("✅ Prediction Completed!")

        # Download prediction
        with open(prediction_file_detail.prediction_file_path, "rb") as f:
            st.download_button(
                label="⬇️ Download Prediction File",
                data=f,
                file_name=prediction_file_detail.prediction_file_name,
                mime="text/csv"
            )

    except Exception as e:
        st.error(f"❌ Prediction Failed: {str(e)}")
        raise CustomException(e, sys)
