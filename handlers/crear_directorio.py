import boto3, json

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
    directorio = data.get('directorio')

    if not bucket or not directorio:
        return {'statusCode':400,'body':json.dumps({'error':"Falta 'bucket' o 'directorio'."})}

    if not directorio.endswith('/'):
        directorio += '/'

    s3 = boto3.client('s3')
    s3.put_object(Bucket=bucket, Key=directorio)

    return {'statusCode':200,'body':json.dumps({'message':'Directorio creado','bucket':bucket,'directorio':directorio})}
