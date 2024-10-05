import streamlit as st
import pandas as pd

# Data for the first chore schedule (Bins, Kitchen, Common Area)
data1 = {
    "Start Date": ["01-10-2024", "08-10-2024", "15-10-2024", "22-10-2024"],
    "End Date": ["07-10-2024", "14-10-2024", "21-10-2024", "28-10-2024"],
    "Chore": [
        "Blue & Green Bins, Cleaning Kitchen and Common Area",
        "Blue & Green Bins, Cleaning Kitchen and Common Area",
        "Blue & Green Bins, Cleaning Kitchen and Common Area",
        "Blue & Green Bins, Cleaning Kitchen and Common Area"
    ],
    "Person": [
        "Yedu & Abhijay",
        "Gagan, Nidhin & Bhatiyar",
        "Navneet & Mahweer",
        "Keshav & Mohammed"
    ]
}

# Data for the second chore schedule (Top Floor Washroom)
data2 = {
    "Start Date": ["01-10-2024", "08-10-2024", "15-10-2024", "22-10-2024", "29-10-2024"],
    "End Date": ["07-10-2024", "14-10-2024", "21-10-2024", "28-10-2024", "04-11-2024"],
    "Chore": ["Top Floor Washroom"] * 5,  # Same chore for all rows
    "Person": ["Yedu", "Bhatiyar", "Navneet", "Mahweer", "Nidhin"]
}

# Create DataFrames
df1 = pd.DataFrame(data1)
df2 = pd.DataFrame(data2)

# Streamlit app layout
st.title("Chore Schedules")

# Section 1: Bins, Kitchen, Common Area
st.header("Bins, Kitchen, and Common Area Chores")
st.dataframe(df1)

# Section 2: Top Floor Washroom Chores
st.header("Top Floor Washroom Chores")
st.dataframe(df2)
