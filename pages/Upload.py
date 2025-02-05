import streamlit as st
import pandas as pd
import boto3
import uuid  # For generating unique chore_id

# AWS DynamoDB Configuration
AWS_REGION = "us-east-1"  # Make sure this is your actual AWS region
TABLE_NAME = "Chore_Management"

# Initialize DynamoDB resource
dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
table = dynamodb.Table(TABLE_NAME)

st.title("Upload Chores Excel")

uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx"])

if uploaded_file:
    if st.button("Upload Data"):
        try:
            # Read the Excel file
            df = pd.read_excel(uploaded_file, engine="openpyxl")

            # Normalize column names
            df.columns = df.columns.str.strip().str.lower()  # Remove spaces & lowercase
            df.columns = df.columns.str.replace(r"[\n\t]", "", regex=True)  # Remove hidden characters

            # Debugging: Show column names
            st.write("Columns in file:", df.columns.tolist())

            # Define required columns
            required_cols = ["person", "chore", "start date", "end date", "status"]
            missing_cols = [col for col in required_cols if col not in df.columns]

            if missing_cols:
                st.error(f"Missing required columns: {missing_cols}")
            else:
                # Convert date columns to string format (DynamoDB does not support datetime)
                df["start date"] = df["start date"].astype(str)
                df["end date"] = df["end date"].astype(str)

                # Insert data into DynamoDB
                for _, row in df.iterrows():
                    item = {
                        "chore_id": str(uuid.uuid4()),  # Generate a unique chore_id
                        "person": row["person"],
                        "chore": row["chore"],
                        "start_date": row["start date"],
                        "end_date": row["end date"],
                        "status": row["status"],
                        "done_date": ""  # Initially empty, will be updated later
                    }

                    table.put_item(Item=item)

                st.success("Data successfully uploaded to DynamoDB! 🎉")

        except Exception as e:
            st.error(f"Error uploading file: {e}")
