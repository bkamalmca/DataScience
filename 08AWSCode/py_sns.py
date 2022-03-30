import json
import urllib
import boto3
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

def send_to_sns():
    print('Loading function...')
    print(os.getenv('aws_access_key_id'))
    print(os.getenv('aws_secret_access_key'))
    
    
    # sns = boto3.client('sns')
    sns = boto3.client('sns', aws_access_key_id=os.getenv('aws_access_key_id'), 
                       aws_secret_access_key=os.getenv('aws_secret_access_key'),
                       aws_session_token=os.getenv('aws_session_token'))
    sns.publish(
         TopicArn='arn:aws:sns:us-east-1:xxx:EDS-EMAIL-MSG',
         Subject="EDS Test",
         Message="EDS Message"
        )
    
    return ('Sent a message to an Amazon SNS topic.')