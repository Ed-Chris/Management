import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
from db_config import get_dynamodb_table

# 🔹 **Get DynamoDB Table**
table = get_dynamodb_table()

# 🔹 **Fetch all chores from DynamoDB**
try:
    response = table.scan()
    chores = response.get("Items", [])
except Exception as e:
    st.error(f"⚠️ Error fetching data: {e}")
    st.stop()

st.title("📅 View Chores")

if not chores:
    st.warning("No chores found in the database.")
    st.stop()

# 🔹 **Convert to DataFrame**
df = pd.DataFrame(chores)

# 🔹 **Handle missing or incorrect date formats**
date_columns = ["start_date", "end_date", "done_date"]

for col in date_columns:
    # Convert strings to datetime with explicit format
    df[col] = pd.to_datetime(df[col], format="%d-%m-%Y", errors="coerce", dayfirst=True)

    # Handle UNIX timestamps (if any)
    df[col] = pd.to_datetime(df[col], unit="s", errors="coerce").fillna(df[col])

# 🔹 **Debugging: Check missing values**
#st.write(f"Missing start_date count: {df['start_date'].isna().sum()}")

# 🔹 **Sort by `start_date`**
df = df.sort_values(by="start_date", ascending=True)

# 🔹 **Reorder columns for better readability**
column_order = ["person", "chore", "start_date", "end_date", "done_date", "status"]
df = df[column_order]

# 🔹 **Format dates for display in AgGrid**
for col in date_columns:
    df[col] = df[col].dt.strftime("%Y-%m-%d")  # Convert dates to string format

# 🔹 **Dropdown for selecting a person (Includes "All" option)**
people = sorted(set(df["person"].dropna()))
people.insert(0, "All")
selected_person = st.selectbox("👤 Select a Person", people)

# 🔹 **Filter chores based on selection**
if selected_person != "All":
    df = df[df["person"] == selected_person]

# 📌 **Interactive Table View**
st.subheader("📝 Chore Details")

# 🔹 **Configure AgGrid**
gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_pagination()
gb.configure_side_bar()
gb.configure_selection("single", use_checkbox=True)

# 🔹 **Format date columns in AgGrid**
for col in date_columns:
    gb.configure_column(col, type=["dateColumnFilter", "customDateTimeFormat"], custom_format_string="yyyy-MM-dd")

grid_options = gb.build()

# 🔹 **Display AgGrid table**
AgGrid(df, gridOptions=grid_options)
