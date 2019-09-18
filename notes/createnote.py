import boto3
import json
import os
import uuid
from notes import decimalencoder
from datetime import datetime

dynamodb_client = boto3.client('dynamodb', region_name='us-west-2')
dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
table = dynamodb.Table(os.environ['TABLE_NAME'])


# POST /notes
def lambda_handler(event, context):
    data = json.loads(event['body'])

    noteitem = {
        'userId': event['requestContext']['authorizer']['claims']['sub'],
        'noteId': str(uuid.uuid4()),
        'content': data.get('content', None),
        'attachment': data.get('attachment', None),
        'createdAt': str(datetime.now().timestamp())
    }

    try:
        response = table.put_item(Item=noteitem)

        print("Response: {}".format(response))

        return success(noteitem)

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
