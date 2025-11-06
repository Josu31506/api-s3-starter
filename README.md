
# API S3 (Serverless) — desde cero

Funciones:
- `GET /s3/lista-buckets`
- `POST /s3/bucket/lista-objetos` (body: `{"bucket":"...","prefix":"opcional/"}`)
- `POST /s3/crear-bucket` (body: `{"bucket":"mi-bucket-unico","region":"us-east-1"}`)
- `POST /s3/crear-directorio` (body: `{"bucket":"mi-bucket","directorio":"catalogo-productos/imagenes-chicas"}`)
- `POST /s3/subir-archivo` (body: `{"bucket":"...","directorio":"...","filename":"...","content_base64":"..."}`)

## Deploy
```
mv serverless.sample.yml serverless.yml
AWS_PROFILE=deploy npx -y serverless@latest deploy --stage dev
AWS_PROFILE=deploy npx -y serverless@latest deploy --stage test
AWS_PROFILE=deploy npx -y serverless@latest deploy --stage prod
```

## Curl (Linux)
```bash
BASE_DEV="https://ID.execute-api.us-east-1.amazonaws.com/dev"

# 1) Crear bucket (usa nombre ÚNICO globalmente)
curl -s -X POST "$BASE_DEV/s3/crear-bucket"   -H 'Content-Type: application/json'   -d '{"bucket":"mi-bucket-2025-demo-xxxxx","region":"us-east-1"}' | jq

# 2) Crear directorio (prefix con '/')
curl -s -X POST "$BASE_DEV/s3/crear-directorio"   -H 'Content-Type: application/json'   -d '{"bucket":"mi-bucket-2025-demo-xxxxx","directorio":"catalogo-productos/imagenes-chicas"}' | jq

# 3) Subir archivo (base64)
FILE=galleta01-small.png
B64=$(base64 -w 0 "$FILE")
curl -s -X POST "$BASE_DEV/s3/subir-archivo"   -H 'Content-Type: application/json'   -d @- <<JSON | jq
{"bucket":"mi-bucket-2025-demo-xxxxx",
 "directorio":"catalogo-productos/imagenes-chicas",
 "filename":"galleta01-small.png",
 "content_base64":"$B64"}
JSON

# 4) Listar objetos
curl -s -X POST "$BASE_DEV/s3/bucket/lista-objetos"   -H 'Content-Type: application/json'   -d '{"bucket":"mi-bucket-2025-demo-xxxxx","prefix":"catalogo-productos/"}' | jq

# 5) Listar buckets
curl -s "$BASE_DEV/s3/lista-buckets" | jq
```
