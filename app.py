import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="Data Sweeper", page_icon="🛠️", layout="wide")

# Custom CSS for background, text, and button colors
st.markdown("""
    <style>
        .stApp {
            background-color: black !important;
            color: white !important;
        }
        
        /* Set text color to bright white */
        body, .stTextInput, .stCheckbox, .stRadio, .stButton, .stDownloadButton, label {
            color: #ffffff !important;  /* Brighter white */
            font-weight: bold !important;  /* Make it stand out */
        }

        /* Style buttons */
        div.stButton > button, div.stDownloadButton > button {
            background-color: white !important;
            color: black !important;
            border-radius: 8px;
            border: none;
            padding: 8px 16px;
            font-weight: bold;
        }

        /* Hover effect */
        div.stButton > button:hover, div.stDownloadButton > button:hover {
            background-color: grey !important;
            color: black !important;
        }

        /* Improve visibility of checkboxes, radio buttons, and labels */
        .stCheckbox > label, .stRadio > label {
            font-size: 16px !important;
            color: #ffffff !important; /* Brighter text */
        }

        /* Increase visibility of all labels */
        label {
            font-size: 16px !important;
            color: #ffffff !important; /* Brighter text */
        }
    </style>
""", unsafe_allow_html=True)

# Title and Description with Emojis
st.title("💿 DataSweeper Sterling Integrator 🛠️")
st.write("✨ This application allows you to upload a **CSV** or **Excel** file and use the following commands to **clean** and **transform** your data! 🚀")

# File uploader
st.subheader("📂 Upload Your File")
uploaded_file = st.file_uploader("📌 Upload a CSV or Excel file", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_file:
    for file in uploaded_file:
        file_ext = os.path.splitext(file.name)[-1].lower()
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error("❌ Invalid file type. Please upload a CSV or Excel file.")
            continue

        # File details
        st.subheader(f"📊 Preview: {file.name}")
        st.dataframe(df)  # Shows the full dataset

        # Data cleaning options
        st.subheader("🧹 Data Cleaning Options")
        if st.checkbox(f"✅ Clean data from {file.name}"):
            col1, col2 = st.columns(2)

            with col1: 
                if st.button(f"🗑️ Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True) 
                    st.success("🎉 Duplicates Removed!")
            with col2:
                if st.button(f"🩹 Fill Missing Values for {file.name}"):
                    numeric_columns = df.select_dtypes(include=['number']).columns
                    df[numeric_columns] = df[numeric_columns].fillna(df[numeric_columns].mean())    
                    st.success("✨ Missing Values Filled!")

        st.subheader("📌 Select Columns to Keep")
        columns = st.multiselect(f"📂 Select Columns for {file.name}", df.columns, default=df.columns) 
        df = df[columns]  

        # Data Visualization
        st.subheader("📊 Data Visualization")
        if st.checkbox(f"📉 Show visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include=['number']).iloc[:, :2])

        # Conversion Option
        st.subheader("🔄 Conversion Options")
        conversion_type = st.radio(f"📁 Convert {file.name} to:", ("📜 CSV", "📊 Excel"))
        if st.button(f"⚡ Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "📜 CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            else:  # Excel
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            
            buffer.seek(0)

            st.download_button(
                label=f"⬇️ Download {file.name} as {conversion_type} file",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )
            st.success("🎉 File processed successfully! 🚀")

