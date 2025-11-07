import base64
import boto3

def lambda_handler(event, context):
    body = event.get("body") or {}
    bucket = (body.get("bucket") or "").strip()
    directorio = (body.get("directorio") or "").strip()
    filename = (body.get("filename") or "").strip()
    content_b64 = body.get("content_base64")
    content_type = body.get("content_type")  # opcional
    public = bool(body.get("public", False))

    if not all([bucket, directorio, filename, content_b64]):
        return {"statusCode": 400, "error": "Debe enviar 'bucket', 'directorio', 'filename' y 'content_base64'"}

    if directorio and not directorio.endswith('/'):
        directorio = directorio + '/'

    key = f"{directorio}{filename}"

    data = base64.b64decode(content_b64)

    put_args = dict(Bucket=bucket, Key=key, Body=data)
    if content_type:
        put_args["ContentType"] = content_type
    if public:
        put_args["ACL"] = "public-read"

    s3 = boto3.client("s3")
    s3.put_object(**put_args)

    s3_url = f"s3://{bucket}/{key}"
    http_url = f"https://{bucket}.s3.amazonaws.com/{key}"
    return {"statusCode": 200, "bucket": bucket, "key": key, "s3_url": s3_url, "http_url": http_url, "public": public}