import boto3

AWS_REGION = "us-east-1"  # Set your correct AWS region
TABLE_NAME = "Chore_Management"

# Initialize DynamoDB Client
dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
table = dynamodb.Table(TABLE_NAME)
