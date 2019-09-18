import boto3
import json
import os
from notes import decimalencoder

dynamodb_client = boto3.client('dynamodb', region_name='us-west-2')
dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
table = dynamodb.Table(os.environ['TABLE_NAME'])


# GET /notes/{id}
def lambda_handler(event, context):
    try:
        response = table.get_item(
            Key={
                'userId': event['requestContext']['authorizer']['claims']['sub'],
                'noteId': event['pathParameters']['id']
            }
        )

        if response['Item']:
            return success(response['Item'])
        else:
            return failure({"status": "false", "error": "Item not found."})

    except Exception as error:
        return failure({"status": "false", "error": str(error)})


def buildresponse(statuscode, body):
    return {
        "statusCode": statuscode,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": "true"
        },
        "body": json.dumps(body, cls=decimalencoder.DecimalEncoder)
    }


def success(body):
    return buildresponse(200, body)


def failure(body):
    return buildresponse(500, body)
