import streamlit as st
from extract import extract_fields, predict_disease
from PIL import Image
import os

st.set_page_config(page_title="Health OCR & Disease Prediction", layout="centered")

st.title("🏥 Health OCR & Disease Prediction System")

# -----------------------
# Step 1: Select Mode
# -----------------------
mode = st.radio("Choose input method:", ["Upload Image", "Enter Manually"])

# Default data dictionary
data = {
    "name": "",
    "age": "",
    "weight": "",
    "sugar": "",
    "bp": "",
    "fever": "",
    "heartbeat": "",
    "pulse": ""
}

# ===============================================
# 📤 MODE 1: IMAGE UPLOAD (OCR)
# ===============================================
if mode == "Upload Image":
    uploaded_file = st.file_uploader("Upload Medical Form Image", type=["jpg", "png", "jpeg"])

    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, caption="Uploaded Image", width=350)
        img.save("temp.png")

        st.subheader("🔍 Extracting Data...")
        extracted = extract_fields("temp.png")

        st.success("OCR extraction completed!")

        st.subheader("✏️ Review & Edit Extracted Information")
        for key in data.keys():
            default = extracted.get(key, "")
            if not default:
                default = "Not Found"

            data[key] = st.text_input(f"{key.capitalize()}:", value=default)

# ===============================================
# ✍ MODE 2: MANUAL INPUT
# ===============================================
elif mode == "Enter Manually":
    st.subheader("🔡 Enter Patient Details Manually")
    for key in data.keys():
        data[key] = st.text_input(f"{key.capitalize()}:")
        

# ===============================================
# BUTTON 1: SHOW DATA
# ===============================================
if st.button("📋 Show Patient Data"):
    st.subheader("📋 Patient Information")

    for key, value in data.items():
        shown_value = value if value else "Not Provided"
        st.markdown(
            f"""
            <div style='padding:10px; margin:5px 0; background:#eeeeee; border-radius:8px;'>
                <b>{key.capitalize()}</b>: {shown_value}
            </div>
            """,
            unsafe_allow_html=True
        )

    st.session_state["data_ready"] = True


# ===============================================
# BUTTON 2: PREDICT DISEASE
# ===============================================
if st.session_state.get("data_ready", False):

    if st.button("🧠 Predict Disease"):
        st.subheader("🧠 Disease Prediction")

        try:
            prediction = predict_disease(data)
        except:
            prediction = "Unable to predict — missing fields."

        st.markdown(
            f"""
            <div style="padding:15px; background:#e8f5e9; border-radius:10px; border:2px solid #4caf50;">
                <b>{prediction}</b>
            </div>
            """,
            unsafe_allow_html=True
        )

        # -----------------------
        # SIMPLE TEXT REPORT (No PDF)
        # -----------------------
        st.subheader("📄 Download Report")

        report_text = "HEALTH REPORT\n\n"
        for key, value in data.items():
            report_text += f"{key.capitalize()}: {value}\n"
        report_text += f"\nDisease Prediction: {prediction}\n"

        st.download_button(
            label="⬇ Download Report",
            data=report_text,
            file_name="Health_Report.txt",
            mime="text/plain"
        )
