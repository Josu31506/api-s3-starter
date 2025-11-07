import boto3

def lambda_handler(event, context):
    body = event.get("body") or {}
    bucket = (body.get("bucket") or "").strip()
    directorio = (body.get("directorio") or "").strip()

    if not bucket or not directorio:
        return {"statusCode": 400, "error": "Debe enviar 'bucket' y 'directorio' en el body"}

    if not directorio.endswith('/'):
        directorio = directorio + '/'

    s3 = boto3.client("s3")
    # Crear un 'folder' S3 = subir objeto 0 bytes con sufijo '/'
    s3.put_object(Bucket=bucket, Key=directorio)

    return {"statusCode": 200, "bucket": bucket, "directorio": directorio, "message": "Directorio creado"}