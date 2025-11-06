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
    prefix = data.get('prefix')  # opcional

    if not bucket:
        return {'statusCode':400,'body':json.dumps({'error':"Falta 'bucket'."})}

    s3 = boto3.client('s3')
    kwargs = {'Bucket': bucket}
    if prefix:
        kwargs['Prefix'] = prefix

    resp = s3.list_objects_v2(**kwargs)
    contents = resp.get('Contents', [])
    objetos = [o.get('Key') for o in contents]

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({'bucket': bucket, 'prefix': prefix, 'lista_objetos': objetos})
    }
