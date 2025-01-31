import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import urllib.parse

# Load patient detailed data
st.set_page_config(layout="wide")
detail_file_path = "processed_data.csv"
detail_df = pd.read_csv(detail_file_path)

# Load patient history data
history_file_path = "patient_history_data.csv"
history_df = pd.read_csv(history_file_path)

# Hide sidebar navigation
st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {display: none;}
    </style>
""", unsafe_allow_html=True)

# Ensure patient names are treated as strings
detail_df["Patient Name"] = detail_df["Patient Name"].astype(str)
history_df["Patient Name"] = history_df["Patient Name"].astype(str)
history_df["Measurement Date"] = pd.to_datetime(history_df["Measurement Date"], errors='coerce')

# Get query parameters
patient_name = st.query_params.get("patient_name")

# Retrieve patient detailed data
patient_detail = detail_df[detail_df["Patient Name"] == patient_name]
# Retrieve patient historical data
patient_history = history_df[history_df["Patient Name"] == patient_name]

if not patient_detail.empty:
    patient = patient_detail.iloc[0]  # Extract single row

    # Display patient details in a card
    st.markdown(
        f"""
        <div style="background-color: #f9f9f9; padding: 20px; border-radius: 10px; box-shadow: 0px 2px 4px rgba(0,0,0,0.1);">
            <h2>{patient['Patient Name']}</h2>
            <p><strong>Age:</strong> {patient['Age']}</p>
            <p><strong>Gender:</strong> {patient['Gender']}</p>
            <p><strong>Status:</strong> {patient['Status']}</p>
            <p><strong>Diabetes:</strong> {patient['Diabetes']}</p>
            <p><strong>Last Visit:</strong> {patient['Last Visit']}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    if not patient_history.empty:
        # Display blood pressure chart
        st.markdown("### Blood Pressure History")
        patient_history = patient_history.sort_values(by="Measurement Date")
        
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(patient_history["Measurement Date"], patient_history["sysBP"], marker='o', linestyle='-', color='red', label='Systolic BP')
        ax.plot(patient_history["Measurement Date"], patient_history["diaBP"], marker='o', linestyle='-', color='green', label='Diastolic BP')
        ax.set_xlabel("Date")
        ax.set_ylabel("Blood Pressure (mmHg)")
        ax.set_title("Blood Pressure Trends")
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.6)
        
        st.pyplot(fig)
    else:
        st.write("No historical blood pressure data available.")
    
    # Button to go back
    st.page_link("app.py", label="⬅️ Back to Dashboard")
else:
    st.error("Patient not found.")
