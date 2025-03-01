import streamlit as st
import pandas as pd
from sidebar import render_sidebar


# Configure the page
st.set_page_config(layout="wide")
st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {display: none;}
    </style>
""", unsafe_allow_html=True)


file_path = "processed_data.csv"
df = pd.read_csv(file_path)

# Hide sidebar navigation

# Sidebar with styled tabs
with st.sidebar:
    render_sidebar("Watchlist")
    # st.markdown('<div class="sidebar-container">', unsafe_allow_html=True)
    # st.markdown('<h2>CareLink</h2>', unsafe_allow_html=True)

    # # Create tabs using Streamlit session state to track the active tab
    # if "active_tab" not in st.session_state:
    #     st.session_state.active_tab = "Patients"  # Default tab

    # # Define tabs and icons
    # tabs = {
    #     "Patients": "👥",
    #     "Watchlist": "⭐",
    #     "Messages": "💬",
    #     "Notifications": "🔔",
    # }
    # for tab_name, icon in tabs.items():
    #     url = "/" if tab_name == "Patients" else "/watchlist" if tab_name == "Watchlist" else "#"
    #     active_class = "active" if st.session_state.active_tab == tab_name else ""
    #     st.markdown(
    #         f'<a href="{url}" target="_self" class="sidebar-tab {active_class}" style="text-decoration: none; display: block; padding: 10px; color: black; font-weight: bold;">'
    #         f'{icon} {tab_name}</a>',
    #         unsafe_allow_html=True,
    #     )

    # st.markdown("</div>", unsafe_allow_html=True)

def generate_detail_link(patient_name):
    return f"/patient_detail?patient_name={patient_name}"  # Using Streamlit page structure

# Title for Watchlist Page
st.markdown("<h2 style='margin-bottom: 20px;'>Watchlist</h2>", unsafe_allow_html=True)

# # Highlighted Patients Section
highlighted_patients = df[df["Highlight"] == True].reset_index(drop=True)  # Reset the index for proper iteration

if not highlighted_patients.empty:
    cols = st.columns(len(highlighted_patients))
    for i in range(len(highlighted_patients)):
        patient = highlighted_patients.loc[i]
        with cols[i]:
            # Card Design
            status_color = "#ff6b6b" if patient["Status"] == "CRITICAL ALERT" else "#38c172" if patient["Status"] == "STABLE" else "#f9c74f"
            card_bg_color = "#ffecec" if patient["Status"] == "CRITICAL ALERT" else "#eafaf1" if patient["Status"] == "STABLE" else "#fff4e3"
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