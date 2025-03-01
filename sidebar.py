import streamlit as st


# Ensure session state is set

def render_sidebar(defaultTab):
    """Render the sidebar navigation bar across pages."""
    
    st.markdown('<div class="sidebar-container">', unsafe_allow_html=True)
    st.markdown('<h2>CareLink</h2>', unsafe_allow_html=True)
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

    if "active_tab" not in st.session_state:
        st.session_state.active_tab = defaultTab #"Patients"  # Default tab

    # Define tabs and icons
    tabs = {
        "Patients": "👥",
        "Watchlist": "⭐",
        "Messages": "💬",
        "Notifications": "🔔",
    }

    for tab_name, icon in tabs.items():
        url = "/" if tab_name == "Patients" else "/watchlist" if tab_name == "Watchlist" else "#"
        active_class = "active" if st.session_state.active_tab == tab_name else ""
        
        st.markdown(
            f'<a href="{url}" target="_self" class="sidebar-tab {active_class}" style="text-decoration: none; display: block; padding: 10px; color: black; font-weight: bold;">'
            f'{icon} {tab_name}</a>',
            unsafe_allow_html=True,
        )


    st.markdown("</div>", unsafe_allow_html=True)
