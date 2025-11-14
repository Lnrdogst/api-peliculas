import boto3
import uuid
import os
import json


def log_json(tipo, datos):
    print(json.dumps({
        "tipo": tipo,
        "log_datos": datos
    }, ensure_ascii=False))


def lambda_handler(event, context):
    log_json("INFO", {
        "mensaje": "Evento recibido en CrearPelicula",
        "event": event
    })

    try:
        body = event.get("body", {})

        if isinstance(body, str):
            body = json.loads(body)

        tenant_id = body["tenant_id"]
        pelicula_datos = body["pelicula_datos"]

        nombre_tabla = os.environ["TABLE_NAME"]

        # Proceso
        uuidv4 = str(uuid.uuid4())
        pelicula = {
            "tenant_id": tenant_id,
            "uuid": uuidv4,
            "pelicula_datos": pelicula_datos
        }

        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table(nombre_tabla)
        response = table.put_item(Item=pelicula)

        log_json("INFO", {
            "mensaje": "Película creada correctamente",
            "tenant_id": tenant_id,
            "pelicula": pelicula,
            "dynamodb_response": response
        })

        # Salida (json)
        return {
            "statusCode": 200,
            "body": json.dumps({
                "mensaje": "Película creada correctamente",
                "pelicula": pelicula
            })
        }

    except Exception as e:
        log_json("ERROR", {
            "mensaje": "Error al crear la película",
            "detalle_error": str(e),
            "body_recibido": event.get("body")
        })

        return {
            "statusCode": 500,
            "body": json.dumps({
                "mensaje": "Error al crear la película",
                "detalle_error": str(e)
            })
        }