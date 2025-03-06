
# GROWTH MINDSET CHALLENGE APP

import streamlit as st
import pandas as pd
import os
from io import BytesIO
import time


st.set_page_config(page_title="Data Sweeper", layout="wide")


st.markdown(
    """
    <style>
    .stApp { background-color: #1E1E1E; color: white; font-family: Arial, sans-serif; }
    .stTitle { color: #FFA500; }
    .upload-box { border: 2px dashed #FFA500; padding: 10px; text-align: center; margin-bottom: 10px; }
    .upload-status { color: #FFA500; font-weight: bold; margin-top: 10px; }
    .progress-bar { width: 100%; height: 10px; background-color: #333; border-radius: 5px; margin-top: 5px; }
    .progress { height: 100%; background-color: #FFA500; border-radius: 5px; }
    </style>
    """,
    unsafe_allow_html=True
)


st.title("📀 Data Sweeper - Sterling Integrator")
st.write("Easily convert and clean your data files between CSV and Excel formats.")


st.markdown('<div class="upload-box">📤 Drag and drop your files below</div>', unsafe_allow_html=True)
uploaded_files = st.file_uploader(
    "Upload Your Files (Accepts CSV or Excel):",
    type=["csv", "xlsx"],
    accept_multiple_files=True
)

if uploaded_files:
    total_files = len(uploaded_files)
    progress_bar = st.progress(0)
    uploaded_count = 0
    
    for file in uploaded_files:
        uploaded_count += 1
        file_ext = os.path.splitext(file.name)[-1].lower()
        
        try:
            if file_ext == ".csv":
                df = pd.read_csv(file)
            elif file_ext == ".xlsx":
                df = pd.read_excel(file, engine="openpyxl")  # Engine specified
            else:
                st.error(f"Unsupported File Type: {file_ext}")
                continue
        except Exception as e:
            st.error(f"Error reading file {file.name}: {e}")
            continue
        

        progress_bar.progress(uploaded_count / total_files)
        st.markdown(f"<p class='upload-status'>✅ {uploaded_count} of {total_files} files uploaded</p>", unsafe_allow_html=True)
        time.sleep(0.5)


        st.subheader(f"📌 Preview: {file.name}")
        st.dataframe(df.head())


        st.subheader("🛠 Data Cleaning Options")
        if st.checkbox(f"Enable Cleaning for {file.name}"):
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button(f"Remove Duplicates: {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.success("✅ Duplicates removed!")
            
            with col2:
                if st.button(f"Fill Missing Values: {file.name}"):
                    numeric_cols = df.select_dtypes(include=["number"]).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.success("✅ Missing values filled with column mean!")


        st.subheader("🎯 Select Columns to Keep")
        selected_columns = st.multiselect(
            f"Choose columns for {file.name}", df.columns, default=df.columns
        )
        df = df[selected_columns]


        st.subheader("📊 Data Visualization")
        if st.checkbox(f"Show visualization for {file.name}"):
            numeric_data = df.select_dtypes(include="number")
            if not numeric_data.empty:
                st.bar_chart(numeric_data.iloc[:, :2])
            else:
                st.warning("No numeric data available for visualization.")


        st.subheader("🔄 Conversion Options")
        conversion_type = st.radio(
            f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name
        )
        
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            else:
                df.to_excel(buffer, index=False, engine="openpyxl")  # Fixed
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)

            st.download_button(
                label=f"Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )

st.success("🎉 All files processed successfully!")