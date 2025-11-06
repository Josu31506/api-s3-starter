import boto3
import json

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    resp = s3.list_buckets()
    buckets = [b.get('Name') for b in resp.get('Buckets', [])]
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({'lista_buckets': buckets})
    }
