import json
import boto3
import pandas as pd
from io import BytesIO, StringIO

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    print("Req data", json.dumps(event))
    series = pd.Series([2, 4, 6, 8])
    
    # print(dir(pandas))
    
    i = 0
    while i < event['count']:
        print(event["message"])
        i += 1
    
    try:
        bucket_name = 'xxx-s3' # event["Records"][0]["s3"]["bucket"]["name"]
        s3_file_name = 'xxx/input/Graylist_20220307.csv' # event["Records"][0]["s3"]["object"]["key"]
        resp = s3_client.get_object(Bucket=bucket_name, Key=s3_file_name)
        
        df_s3_data = pd.read_csv(StringIO(resp['Body'].read().decode('utf-8')))

        print(df_s3_data.head(2))
        
        # write to s3 from local
        s3 = boto3.resource('s3')
        bucket = s3.Bucket('dgx-ds-use1-dev-landing-s3')
        key = 'test.csv'
        df_s3_data.to_csv('/tmp/test.csv')
        bucket.upload_file('/tmp/test.csv', key)

    except Exception as err:
        print(err)
    
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda and pandas.. ' + str(series.max()))
        
    }
