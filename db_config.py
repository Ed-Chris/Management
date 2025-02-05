import streamlit as st
import boto3

# Retrieve AWS credentials from Streamlit Secrets
AWS_REGION = st.secrets["AWS_REGION"]
AWS_ACCESS_KEY = st.secrets["AWS_ACCESS_KEY_ID"]
AWS_SECRET_KEY = st.secrets["AWS_SECRET_ACCESS_KEY"]

# Initialize DynamoDB Resource
dynamodb = boto3.resource(
    "dynamodb",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)

# Define the DynamoDB table
TABLE_NAME = "Chore_Management"
table = dynamodb.Table(TABLE_NAME)
