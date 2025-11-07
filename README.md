# S11 - api-s3 (Sem 11)

## Despliegue (3 stages)
```bash
# Dev
serverless deploy --stage dev
# Test
serverless deploy --stage test
# Prod
serverless deploy --stage prod
```

Anota la URL base que te imprime Serverless, por ejemplo:
`https://xxxxxx.execute-api.us-east-1.amazonaws.com` y úsala como `BASE_URL`.

## CURL: ejemplos
```bash
BASE_URL="https://xxxxxx.execute-api.us-east-1.amazonaws.com"
STAGE="dev"

# 1) Listar buckets (GET)
curl "$BASE_URL/$STAGE/s3/lista-buckets"

# 2) Listar objetos de un bucket (POST)
curl -X POST "$BASE_URL/$STAGE/s3/bucket/lista-objetos" \
  -H 'Content-Type: application/json' \
  -d '{"bucket":"<tu-bucket>"}'

# 3) Crear bucket (POST) - usa un nombre único y minúsculas
curl -X POST "$BASE_URL/$STAGE/s3/bucket/crear" \
  -H 'Content-Type: application/json' \
  -d '{"bucket":"<nuevo-bucket-unico-12345>"}'

# 4) Crear "directorio" (POST)
curl -X POST "$BASE_URL/$STAGE/s3/bucket/crear-directorio" \
  -H 'Content-Type: application/json' \
  -d '{"bucket":"<tu-bucket>", "directorio":"catalogo-productos/imagenes-chicas"}'

# 5) Subir archivo base64 (POST)
# Linux: codifica a base64 en una sola línea (-w 0). En macOS usa: base64 -b 0
B64=$(base64 -w 0 galleta01-small.png)

curl -X POST "$BASE_URL/$STAGE/s3/bucket/subir-archivo" \
  -H 'Content-Type: application/json' \
  -d '{"bucket":"<tu-bucket>","directorio":"catalogo-productos/imagenes-chicas","filename":"galleta01-small.png","content_type":"image/png","content_base64":"'"$B64"'","public":true}'
```

> Tip: Repite los mismos `curl` cambiando `STAGE=test` y `STAGE=prod`.