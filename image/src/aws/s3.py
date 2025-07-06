import boto3

s3_client = boto3.client('s3')

def from_sns(message):
    object = message['receipt']['action']['objectKey']
    bucket_name = message['receipt']['action']['bucketName']

    response = s3_client.get_object(
        Bucket=bucket_name,
        Key=object
    )
    return response['Body'].read().decode('utf-8')