import boto3
import streamlit as st

def get_dynamodb_table():
    """Returns the DynamoDB Table resource"""
    # Load credentials from Streamlit Secrets
    aws_access_key = st.secrets["AWS_ACCESS_KEY_ID"]
    aws_secret_key = st.secrets["AWS_SECRET_ACCESS_KEY"]
    aws_region = st.secrets["AWS_REGION"]

    # Create a boto3 session
    session = boto3.Session(
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=aws_region
    )

    # Initialize DynamoDB resource
    dynamodb = session.resource("dynamodb")
    
    # Return the table object
    return dynamodb.Table("Chore_Management")
