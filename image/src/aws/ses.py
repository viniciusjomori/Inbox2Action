import boto3
import os

ses_client = boto3.client('ses', region_name='us-east-1')
bcc = os.getenv('EMAIL_ADDRESS_BCC')
bcc = bcc.split(', ')

def send_email(to, content, subject):
    ses_client.send_email(
        Source=os.getenv('EMAIL_ADDRESS_SENDER'),
        Destination={
            'ToAddresses': to,
            'BccAddresses': bcc
        },
        Message={
            'Subject': {
                'Data': subject,
                'Charset': 'UTF-8'
            },
            'Body': {
                'Html': {
                    'Data': content,
                    'Charset': 'UTF-8'
                }
            }
        }
    )