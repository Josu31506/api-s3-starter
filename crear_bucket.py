import os
import boto3
from botocore.exceptions import ClientError

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

def lambda_handler(event, context):
    # Entrada
    body = event.get("body") or {}
    bucket = (body.get("bucket") or "").strip()

    if not bucket:
        return {"statusCode": 400, "error": "Debe enviar 'bucket' en el body"}

    s3 = boto3.client("s3", region_name=AWS_REGION)

    try:
        params = {"Bucket": bucket}
        # LocationConstraint no se usa en us-east-1
        if AWS_REGION != "us-east-1":
            params["CreateBucketConfiguration"] = {"LocationConstraint": AWS_REGION}
        s3.create_bucket(**params)
    except ClientError as e:
        return {"statusCode": 400, "bucket": bucket, "error": str(e)}

    return {"statusCode": 200, "bucket": bucket, "message": "Bucket creado"}