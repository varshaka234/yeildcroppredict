import streamlit as st
import pandas as pd
import pickle

# Load trained model
with open("model/final_pipeline_model.pkl", "rb") as f:
    model = pickle.load(f)

st.set_page_config(page_title="🌾 Crop Yield Prediction", layout="wide")

st.title("🌾 Crop Yield Prediction App")
st.write("This app predicts the expected crop yield based on environmental and agricultural conditions.")

# Layout with two columns (input narrower, output wider)
col1, col2 = st.columns([1.5, 2])

with col1:
    st.subheader("📋 Input Crop Details")

    # Grid layout for inputs
    c1, c2 = st.columns(2)

    with c1:
        crop = st.selectbox("Crop", ["Select your crop", "Barley", "Cotton", "Maize", "Rice", "Soybean", "Wheat"])
        soil_type = st.selectbox("Soil Type", ["Select your soil type", "Chalky", "Clay", "Loam", "Peaty", "Sandy", "Silt"])
        rainfall = st.number_input(
            "Rainfall (mm) [Range: 101 - 999]", min_value=0.0, max_value=1000.0,
            value=None, placeholder="Enter rainfall"
        )

    with c2:
        region = st.selectbox("Region", ["Select your region", "East", "West", "North", "South"])
        weather = st.selectbox("Weather Condition", ["Select weather", "Cloudy", "Rainy", "Sunny"])
        temperature = st.number_input(
            "Temperature (°C) [Range: 16 - 40]", min_value=-10.0, max_value=50.0,
            value=None, placeholder="Enter temperature"
        )

    days_to_harvest = st.number_input(
        "Days to Harvest [Range: 60 - 149]", min_value=1, max_value=365,
        value=None, placeholder="Enter days"
    )

with col2:
    st.subheader("Prediction Result")
    st.markdown("### (Tonnes per Hectare)")

    prediction_box = st.empty()

    if st.button("Predict Yield", use_container_width=True):
        # Validate categorical selections
        if crop.startswith("Select") or soil_type.startswith("Select") or region.startswith("Select") or weather.startswith("Select"):
            st.error("⚠ Please select valid values for all fields before predicting.")
        # Validate numeric thresholds
        elif not (60 <= days_to_harvest <= 149):
            st.error("⚠ Days to Harvest must be between 60 and 149.")
        elif not (16 <= temperature <= 40):
            st.error("⚠ Temperature must be between 16 and 40 °C.")
        elif not (101 <= rainfall <= 999):
            st.error("⚠ Rainfall must be between 101 and 999 mm.")
        else:
            # Prepare input DataFrame
            input_data = pd.DataFrame([{
                "Crop": crop,
                "Region": region,
                "Soil_Type": soil_type,
                "Weather_Condition": weather,
                "Temperature_Celsius": temperature,
                "Rainfall_mm": rainfall,
                "Days_to_Harvest": days_to_harvest
            }])

            prediction = model.predict(input_data)[0]

            # Show prediction and inputs in styled card (no clipboard issue)
            # Show prediction and inputs in styled card
            prediction_html = f"""
            <div style="padding:20px; border-radius:12px; background:#f0fdf4; border:2px solid #2e7d32; width:90%; margin:auto;">
                <h2 style="text-align:center; color:#2e7d32;">Predicted Yield</h2>
                <p style="text-align:center; font-size:50px; font-weight:bold; color:#1b5e20; margin:0;">
                    {prediction:.2f}
                </p>
                <hr>
                <h4 style="color:#1b5e20; margin-top:15px;">📋 Your Input</h4>
                <div style="background:#ffffff; padding:10px 15px; border-radius:8px; border:1px solid #ddd; color:#1b1b1b;">
                    <ul style="margin:0; padding-left:20px; font-size:15px;">
                        <li><b>Crop:</b> {crop}</li>
                        <li><b>Region:</b> {region}</li>
                        <li><b>Soil Type:</b> {soil_type}</li>
                        <li><b>Weather:</b> {weather}</li>
                        <li><b>Temperature:</b> {temperature} °C</li>
                        <li><b>Rainfall:</b> {rainfall} mm</li>
                        <li><b>Days to Harvest:</b> {days_to_harvest}</li>
                    </ul>
                </div>
            </div>
            """
            prediction_box.markdown(prediction_html, unsafe_allow_html=True)