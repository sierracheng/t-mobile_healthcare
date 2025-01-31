#!/bin/bash
pip install -r requirements.txt  # Install dependencies
streamlit run streamlit_app.py --server.port=8051 --server.address=0.0.0.0