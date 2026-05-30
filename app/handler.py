import json
import os
import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["USERS_TABLE_NAME"])

def lambda_handler(event, context):
    path = event.get("rawPath", "/")

    if path == "/health":
        return response(200, {
            "status": "ok",
            "service": "trouble-lab"
        })

    if path == "/users":
        result = table.scan()
        return response(200, {
            "users": result.get("Items", [])
        })

    return response(404, {
        "message": "Not Found"
    })

def response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(body, ensure_ascii=False)
    }