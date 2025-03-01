import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import timedelta

# Load patient detailed data
st.set_page_config(layout="wide")

# Hide sidebar navigation
st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {display: none;}
    </style>
""", unsafe_allow_html=True)

# Load patient data
detail_file_path = "processed_data.csv"
history_file_path = "patient_history_data.csv"

detail_df = pd.read_csv(detail_file_path)
history_df = pd.read_csv(history_file_path)

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
# Button to go back
st.page_link("app.py", label="⬅️ Back to Dashboard")
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
            <p><strong>Condition:</strong> {patient['condition']}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if not patient_history.empty:
        # Find the most recent date for this patient
        patient_max_date = patient_history["Measurement Date"].max()

        # User can select the data range: Closest 7 Days or Closest 30 Days
        st.markdown("### Blood Pressure History")
        date_range_option = st.radio("Select Date Range:", ["Last 7 Days", "Last 30 Days"], horizontal=True)

        # Determine the threshold date based on the patient's last recorded date
        if date_range_option == "Last 7 Days":
            date_threshold = patient_max_date - timedelta(days=7)
        else:  # "Last 30 Days"
            date_threshold = patient_max_date - timedelta(days=30)

        # Filter history data based on the selected date range
        filtered_history = patient_history[patient_history["Measurement Date"] >= date_threshold]

        # If no data within the selected period, show all available data
        if filtered_history.empty:
            filtered_history = patient_history.copy()

        # Sort filtered data by date
        filtered_history = filtered_history.sort_values(by="Measurement Date")

        # Plot blood pressure trends
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(filtered_history["Measurement Date"], filtered_history["sysBP"], marker='o', linestyle='-', color='red', label='Systolic BP')
        ax.plot(filtered_history["Measurement Date"], filtered_history["diaBP"], marker='o', linestyle='-', color='green', label='Diastolic BP')

        ax.set_xlabel("Date")
        ax.set_ylabel("Blood Pressure (mmHg)")
        ax.set_title("Blood Pressure Trends")
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.6)

        # **Smart Date Label Display for X-axis**
        date_labels = filtered_history["Measurement Date"].dt.strftime('%Y-%m-%d')  # Format dates
        if len(date_labels) > 10:  # If too many labels, reduce displayed labels
            step = 5 if len(date_labels) > 20 else 3  # Show every 5th or 3rd label based on data length
            ax.set_xticks(filtered_history["Measurement Date"][::step])
            ax.set_xticklabels(date_labels[::step], rotation=45, ha="right")  # Rotate for better readability
        else:
            ax.set_xticks(filtered_history["Measurement Date"])
            ax.set_xticklabels(date_labels, rotation=30, ha="right")  # Rotate slightly for clarity

        st.pyplot(fig)
    else:
        st.write("No historical blood pressure data available.")

else:
    st.error("Patient not found.")
