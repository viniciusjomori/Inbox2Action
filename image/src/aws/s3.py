import boto3

s3_client = boto3.client('s3')

def get_content(event):
    object = event['Records'][0]['s3']['object']['key']
    bucket_name = event['Records'][0]['s3']['bucket']['name']

    response = s3_client.get_object(
        Bucket=bucket_name,
        Key=object
    )
    return response['Body'].read().decode('utf-8')