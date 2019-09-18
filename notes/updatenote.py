import boto3
import json
import os
from notes import decimalencoder
from datetime import datetime

dynamodb_client = boto3.client('dynamodb', region_name='us-west-2')
dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
table = dynamodb.Table(os.environ['TABLE_NAME'])


# PUT /notes/{id}
def lambda_handler(event, context):
    data = json.loads(event['body'])

    try:
        response = table.update_item(
            Key={
                'userId': event['requestContext']['authorizer']['claims']['sub'],
                'noteId': event['pathParameters']['id']
            },
            UpdateExpression='SET content = :content, attachment = :attachment, lastUpdatedAt = :lastUpdatedAt',
            ExpressionAttributeValues={
                ':attachment':  data.get('attachment', None),
                ':content': data.get('content', None),
                ':lastUpdatedAt': str(datetime.now().timestamp())
            },
            ReturnValues='ALL_NEW'
        )

        print("Update Note Response: {}".format(response))

        return success({"status": "true"})

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
