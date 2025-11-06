import boto3, json, base64, mimetypes

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
    filename = data.get('filename')
    content_b64 = data.get('content_base64')

    if not all([bucket, directorio, filename, content_b64]):
        return {'statusCode':400,'body':json.dumps({'error':"Faltan 'bucket','directorio','filename' o 'content_base64'."})}

    if not directorio.endswith('/'):
        directorio += '/'

    key = f"{directorio}{filename}"
    content = base64.b64decode(content_b64)
    content_type = mimetypes.guess_type(filename)[0] or 'application/octet-stream'

    s3 = boto3.client('s3')
    s3.put_object(Bucket=bucket, Key=key, Body=content, ContentType=content_type)

    return {'statusCode':200,'body':json.dumps({'message':'Archivo subido','bucket':bucket,'key':key,'contentType':content_type})}
