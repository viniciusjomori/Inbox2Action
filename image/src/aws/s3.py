import boto3
import os

s3_client = boto3.client('s3')
bucket_name = os.getenv('AWS_BUCKET_NAME')

def get_content(path):
    response = s3_client.get_object(
        Bucket=bucket_name,
        Key=path
    )
    return response['Body'].read().decode('utf-8')