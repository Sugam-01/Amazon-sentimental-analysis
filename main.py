import streamlit as st
import pandas as pd
import requests
from io import BytesIO

# flask --app api.py run --port=5000
prediction_endpoint = "http://127.0.0.1:5000/predict"

st.title("Text Sentiment Predictor")

uploaded_file = st.file_uploader(
    "Choose a CSV file for bulk prediction - Upload the file and click on Predict",
    type="csv",
)

# Text input for sentiment prediction
user_input = st.text_input("Enter text and click on Predict", "")

# Prediction on single sentence
if st.button("Predict"):
    if uploaded_file is not None:
        # Read the uploaded file into memory
        file_content = uploaded_file.read()
        files = {"file": ("uploaded_file.csv", file_content)}

        response = requests.post(prediction_endpoint, files=files)

        if response.status_code == 200:
            response_bytes = BytesIO(response.content)
            response_df = pd.read_csv(response_bytes)

            st.download_button(
                label="Download Predictions",
                data=response_bytes,
                file_name="Predictions.csv",
                key="result_download_button",
            )
        else:
            st.error("Failed to get predictions. Please check the server.")
    else:
        response = requests.post(prediction_endpoint, data={"text": user_input})

        if response.status_code == 200:
            response = response.json()
            st.write(f"Predicted sentiment: {response['prediction']}")
        else:
            st.error("Failed to get prediction. Please check the server.")
