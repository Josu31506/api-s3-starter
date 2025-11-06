import boto3, os, json

def _get_body(event):
    body = event.get('body') if isinstance(event, dict) else None
    if isinstance(body, str) and body:
        try:
            return json.loads(body)
        except Exception:
            pass
    return body if isinstance(body, dict) else (event if isinstance(event, dict) else {})

def lambda_handler(event, context):
    data = _get_body(event) or {}
    bucket = data.get('bucket')
    region = data.get('region') or os.getenv('AWS_REGION', 'us-east-1')
    if not bucket:
        return {'statusCode':400,'body':json.dumps({'error':"Falta 'bucket'."})}

    s3 = boto3.client('s3', region_name=region)

    try:
        if region == 'us-east-1':
            s3.create_bucket(Bucket=bucket)
        else:
            s3.create_bucket(Bucket=bucket, CreateBucketConfiguration={'LocationConstraint': region})
    except Exception as e:
        return {'statusCode':500,'body':json.dumps({'error':str(e)})}

    return {'statusCode':200,'body':json.dumps({'message':'Bucket creado','bucket':bucket,'region':region})}
