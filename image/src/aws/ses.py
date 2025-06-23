import boto3
import os

name = os.getenv('EMAIL_NAME')
address = os.getenv('EMAIL_ADDRESS')
bcc = os.getenv('EMAIL_ADDRESS_BCC')
bcc = bcc.split(', ')

ses_client = boto3.client('ses', region_name='us-east-1')

def send_email(to, content, subject):
    ses_client.send_email(
        Source=f'{name} <{address}>',
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