import streamlit as st
import boto3

# Retrieve AWS credentials from Streamlit Secrets
AWS_REGION = st.secrets["AWS_REGION"]
AWS_ACCESS_KEY = st.secrets["AWS_ACCESS_KEY_ID"]
AWS_SECRET_KEY = st.secrets["AWS_SECRET_ACCESS_KEY"]

# Initialize DynamoDB Client
dynamodb_client = boto3.client(
    "dynamodb",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)

# Define the DynamoDB table name
TABLE_NAME = "Chore_Management"

# Streamlit UI
st.title("Chore Management")

# Fetch data from DynamoDB
try:
    response = dynamodb_client.scan(TableName=TABLE_NAME)
    chores = response.get("Items", [])
    
    if chores:
        st.write("### Chore List")
        for chore in chores:
            st.write(f"- **{chore['chore_name']['S']}** (Assigned to: {chore['assigned_to']['S']})")
    else:
        st.write("No chores found.")

except Exception as e:
    st.error(f"Error fetching chores: {e}")
