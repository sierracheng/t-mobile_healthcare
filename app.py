import streamlit as st
import pandas as pd


# Configure the page layout to fit the screen size
st.set_page_config(layout="wide")
file_path = "processed_data.csv"
df = pd.read_csv(file_path)

st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {display: none;}
    </style>
""", unsafe_allow_html=True)

def update_csv():
    df["Highlight"] = df.index.map(lambda i: st.session_state.highlight_status[i])
    df.to_csv(file_path, index=False)

def generate_detail_link(patient_name):
    return f"/patient_detail?patient_name={patient_name}"  # Using Streamlit page structure

# Custom CSS for sidebar with icons
st.markdown(
    """
    <style>
    /* Style the sidebar container */
    .sidebar-container {
        padding-top: 20px;
    }

    /* Style for the CareLink title */
    .sidebar-container h2 {
        font-weight: bold;
        color: #333;
        margin-bottom: 20px;
    }

    /* Tab styles */
    .sidebar-tab {
        display: flex;
        align-items: center;
        padding: 10px;
        margin-bottom: 5px;
        border-radius: 5px;
        font-size: 16px;
        font-weight: bold;
        cursor: pointer;
        color: #333;
        background-color: #f0f0f0;
        transition: background-color 0.3s ease, color 0.3s ease;
    }

    /* Tab icons */
    .sidebar-tab svg {
        margin-right: 10px;
        font-size: 20px;
    }

    /* Hover effect */
    .sidebar-tab:hover {
        background-color: #e0e0e0;
    }

    /* Active tab */
    .sidebar-tab.active {
        background-color: #333;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar with styled tabs
with st.sidebar:
    st.markdown('<div class="sidebar-container">', unsafe_allow_html=True)
    st.markdown('<h2>CareLink</h2>', unsafe_allow_html=True)

    # Create tabs using Streamlit session state to track the active tab
    if "active_tab" not in st.session_state:
        st.session_state.active_tab = "Patients"  # Default tab

    # Define tabs and icons
    tabs = {
        "Patients": "👥",
        "Messages": "💬",
        "Notifications": "🔔",
    }

    for tab_name, icon in tabs.items():
        active_class = "active" if st.session_state.active_tab == tab_name else ""
        if st.markdown(
            f'<div class="sidebar-tab {active_class}" onclick="window.location.reload();">'
            f'{icon} {tab_name}</div>',
            unsafe_allow_html=True,
        ):
            st.session_state.active_tab = tab_name

    st.markdown("</div>", unsafe_allow_html=True)

# Main content
st.markdown("<h2 style='margin-bottom: 20px;'>Highlighted Patients</h2>", unsafe_allow_html=True)

# Highlighted Patients Section
highlighted_patients = df[df["Highlight"] == True].reset_index(drop=True)  # Reset the index for proper iteration

if not highlighted_patients.empty:
    cols = st.columns(len(highlighted_patients))
    for i in range(len(highlighted_patients)):
        patient = highlighted_patients.loc[i]
        with cols[i]:
            # Card Design
            status_color = "#ff6b6b" if patient["Status"] == "Elevated" else "#38c172" if patient["Status"] == "Normal" else "#f9c74f"
            card_bg_color = "#ffecec" if patient["Status"] == "Elevated" else "#eafaf1" if patient["Status"] == "Normal" else "#fff4e3"
            st.markdown(
                f"""
                <div style="background-color: {card_bg_color}; border-top: 5px solid {status_color}; 
                            border-radius: 10px; padding: 15px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h3 style="margin: 0;">{patient['Patient Name']}</h3>
                        <span style="font-size: 18px; cursor: pointer;">⭐</span>
                    </div>
                    <p><strong>Age:</strong> {patient['Age']}</p>
                    <p><strong>Status:</strong> 
                        <span style="color: {status_color}; font-weight: bold;">{patient['Status'].upper()}</span>
                    </p>
                    <p><strong>Condition:</strong> {patient['Diabetes']}</p>
                    <p style="font-style: italic; color: #666;">
                        <a href="{generate_detail_link(patient['Patient Name'])}" target="_self" style="text-decoration: none; color: blue; cursor: pointer;">
                            View Details
                        </a>
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )
else:
    st.write("No highlighted patients available.")


# Initialize session state for reminders and highlights
if "reminder_status" not in st.session_state:
    st.session_state.reminder_status = {i: False for i in range(len(df))}  # Track sent status
if "highlight_status" not in st.session_state:
    st.session_state.highlight_status = {i: df.loc[i, "Highlight"] for i in range(len(df))}  # Track highlight

# Custom CSS for proper table styling
st.markdown(
    """
    <style>
        .patient-table {
            width: 100%;
            border-collapse: collapse;
        }
        .patient-row {
            display: flex;
            align-items: center;
            padding: 10px 5px;
            border-bottom: 1px solid #ddd;
        }
        .patient-column {
            flex: 1;
            text-align: center;
        }
        .status-badge {
            padding: 4px 8px;
            border-radius: 10px;
            font-weight: bold;
            display: inline-block;
        }
        .status-normal { color: green; border: 1px solid green; }
        .status-elevated { color: red; border: 1px solid red; }
        .status-no-data { color: gray; border: 1px solid gray; background-color: #e0e0e0; }
        .reminder-btn {
            padding: 5px 10px;
            border: none;
            background-color: #007bff;
            color: white;
            font-size: 12px;
            border-radius: 5px;
            cursor: pointer;
        }
        .reminder-btn:disabled {
            background-color: #d0d0d0;
            cursor: not-allowed;
        }
        .highlight-button {
            font-size: 18px;
            cursor: pointer;
            background: none;
            border: none;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Display the Patients List Table
st.markdown("## Patients List")

# Create column layout for headers
header_cols = st.columns([1.5, 1, 1, 0.5, 1.2, 1, 1.5, 1.5, 2, 1])
headers = ["Status", "Patient Name", "Gender", "Age", "Last Visit", "Diabetes", "sysBP", "diaBP", "Reminder", "Highlight"]
for col, header in zip(header_cols, headers):
    col.markdown(f"**{header}**")

# Iterate through patient data and display rows
for i in range(len(df)):
    cols = st.columns([1.5, 1, 1, 0.5, 1.2, 1, 1.5, 1.5, 2, 1])  # Define column layout per row

    # Status Badge
    status = df.loc[i, "Status"]
    status_color = (
        "green" if status == "Normal" else
        "red" if status == "Elevated" else
        "gray"
    )
    status_badge = f'<span style="color: {status_color}; font-weight: bold; border: 1px solid {status_color}; padding: 4px 8px; border-radius: 10px;">{status.upper()}</span>'
    cols[0].markdown(status_badge, unsafe_allow_html=True)

    # Patient details
    cols[1].markdown(df.loc[i, "Patient Name"])
    cols[2].markdown(df.loc[i, "Gender"])
    cols[3].markdown(df.loc[i, "Age"])
    cols[4].markdown(df.loc[i, "Last Visit"])
    cols[5].markdown(df.loc[i, "Diabetes"])
    cols[6].markdown(df.loc[i, "sysBP"])
    cols[7].markdown(df.loc[i, "diaBP"])

    # Reminder Button (inside the column)
    if not st.session_state.reminder_status[i]:
        if cols[8].button("Send Reminder", key=f"reminder_{i}", help="Click to send a reminder"):
            st.session_state.reminder_status[i] = True
            st.rerun()  # Refresh UI to update button
    else:
        cols[8].markdown('<span style="color: gray;">Sent Successfully</span>', unsafe_allow_html=True)

    # Highlight Star Toggle (inside the column)
    star_symbol = "⭐" if st.session_state.highlight_status[i] else "☆"
    if cols[9].button(star_symbol, key=f"highlight_{i}"):
        st.session_state.highlight_status[i] = not st.session_state.highlight_status[i]
        update_csv()  # Update CSV immediately
        st.rerun()  # Refresh UI to update the star
