import streamlit as st
import boto3
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder

# AWS DynamoDB setup
dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
table = dynamodb.Table("Chore_Management")

# Fetch all chores from DynamoDB
response = table.scan()
chores = response.get("Items", [])

st.title("📅 View Chores")

if not chores:
    st.warning("No chores found in the database.")
    st.stop()

# Convert to DataFrame
df = pd.DataFrame(chores)

# Handle missing or incorrect date formats
for col in ["start_date", "end_date", "done_date"]:
    df[col] = pd.to_datetime(df[col], dayfirst=True, errors="coerce")

# Sort by start_date
df = df.sort_values(by="start_date", ascending=True)

# Reorder columns for better readability
column_order = ["person", "chore", "start_date", "end_date", "done_date", "status"]
df = df[column_order]

# Format dates for better display in AgGrid
for col in ["start_date", "end_date", "done_date"]:
    df[col] = df[col].dt.strftime("%Y-%m-%d")  # Convert dates to string format

# Dropdown for selecting a person (Includes "All" option)
people = sorted(set(df["person"].dropna()))
people.insert(0, "All")
selected_person = st.selectbox("👤 Select a Person", people)

# Filter chores based on selection
if selected_person != "All":
    df = df[df["person"] == selected_person]

# 📌 **Interactive Table View**
st.subheader("📝 Chore Details")

# Configure AgGrid
gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_pagination()
gb.configure_side_bar()
gb.configure_selection("single", use_checkbox=True)
gb.configure_column("start_date", type=["dateColumnFilter", "customDateTimeFormat"], custom_format_string="yyyy-MM-dd")
gb.configure_column("end_date", type=["dateColumnFilter", "customDateTimeFormat"], custom_format_string="yyyy-MM-dd")
gb.configure_column("done_date", type=["dateColumnFilter", "customDateTimeFormat"], custom_format_string="yyyy-MM-dd")

grid_options = gb.build()

# Display AgGrid table
AgGrid(df, gridOptions=grid_options)
