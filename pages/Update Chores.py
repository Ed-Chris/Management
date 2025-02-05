import streamlit as st
import pandas as pd
from datetime import datetime
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

# 🔹 **Get a list of all unique people (ensuring everyone is in the dropdown)**
all_people = sorted(set(chore["person"] for chore in chores if "person" in chore))

# 🔹 **Store people in session state for persistence**
if "person_list" in st.session_state:
    all_people = sorted(set(all_people + st.session_state["person_list"]))
else:
    st.session_state["person_list"] = all_people  

# 🔹 **Dropdown to select a person**
selected_person = st.selectbox("👤 Select a person", all_people)

# 🔹 **Filter only "Pending" chores for the selected person**
filtered_chores = [
    chore for chore in chores if chore.get("person") == selected_person and chore.get("status") == "Pending"
]

# 🔹 **If no pending chores, display a message**
if not filtered_chores:
    st.info(f"No pending chores for {selected_person}.")
    st.stop()

# 📌 **Update Chores Section**
st.write(f"### ✅ Update Chores for {selected_person}")

updated_chores = []

for chore in filtered_chores:
    chore_name = chore.get("chore", "Unnamed Chore")
    end_date = chore.get("end_date", "Unknown Date")

    checked = st.checkbox(f"{chore_name} (Due: {end_date})", value=False)

    if checked:
        # Mark as completed
        chore["status"] = "Completed"
        chore["done_date"] = datetime.today().strftime("%Y-%m-%d")
        updated_chores.append(chore)

# 🔹 **Save button**
if st.button("💾 Save Updates") and updated_chores:
    try:
        with table.batch_writer() as batch:
            for chore in updated_chores:
                batch.put_item(Item=chore)
        st.success("✅ Chores updated successfully!")
        st.rerun()  # Refresh the page
    except Exception as e:
        st.error(f"⚠️ Error updating chores: {e}")
