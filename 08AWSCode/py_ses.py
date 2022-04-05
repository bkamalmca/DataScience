import json
import urllib
import boto3
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

def send_to_ses():
    print('Loading function...')
    print(os.getenv('aws_access_key_id'))
    print(os.getenv('aws_secret_access_key'))
    
    
    # sns = boto3.client('sns')
    ses = boto3.client('ses', aws_access_key_id=os.getenv('aws_access_key_id'), 
                       aws_secret_access_key=os.getenv('aws_secret_access_key'),
                       aws_session_token=os.getenv('aws_session_token'))
    
    body = """
        Hello and welcome to the SES Lambda Python Demo.
        """

    ses.send_email(
        Source = 'xxx@gmail.com',
        Destination = {
        'ToAddresses': [
            'target@gmail.com'
            ]
        },
        Message = {
            'Subject': {
            'Data': 'SES Demo',
            'Charset': 'UTF-8'
            },
            'Body': {
            'Text':{
                'Data': body,
                'Charset': 'UTF-8'
                }
            }
        }
    )
    
    return ('Sent a message to an Amazon SES')