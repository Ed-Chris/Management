import streamlit as st
import boto3
from datetime import datetime

# AWS DynamoDB setup
dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
table = dynamodb.Table("Chore_Management")

# Fetch all chores from DynamoDB
response = table.scan()
chores = response.get("Items", [])

# Get a list of all unique people (ensuring everyone is in the dropdown)
all_people = sorted(set(chore["person"] for chore in chores))

# Store people in session state for persistence
if "person_list" in st.session_state:
    all_people = sorted(set(all_people + st.session_state["person_list"]))
else:
    st.session_state["person_list"] = all_people  

# Dropdown to select a person
selected_person = st.selectbox("Select a person", all_people)

# Filter only **Pending** chores for the selected person
filtered_chores = [
    chore for chore in chores if chore["person"] == selected_person and chore["status"] == "Pending"
]

# If no pending chores, display a message
if not filtered_chores:
    st.info(f"No pending chores for {selected_person}.")
else:
    st.write(f"### Update Chores for {selected_person}")
    updated_chores = []
    
    for chore in filtered_chores:
        checked = st.checkbox(f"{chore['chore']} (Due: {chore['end_date']})", value=False)

        if checked:
            # Mark as completed
            chore["status"] = "Completed"
            chore["done_date"] = datetime.today().strftime("%Y-%m-%d")
            updated_chores.append(chore)

    # Save button
    if st.button("Save Updates") and updated_chores:
        with table.batch_writer() as batch:
            for chore in updated_chores:
                batch.put_item(Item=chore)
        st.success("Chores updated successfully!")
        st.rerun()  # Refresh the page
