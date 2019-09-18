import boto3
from boto3.dynamodb.conditions import Key, Attr
import json
import os
from notes import decimalencoder

dynamodb_client = boto3.client('dynamodb', region_name='us-west-2')
dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
table = dynamodb.Table(os.environ['TABLE_NAME'])


# GET /notes
def lambda_handler(event, context):
    try:
        print("CognitoIdentityId: {}".format(event['requestContext']['authorizer']['claims']['sub']))

        result = table.query(
            KeyConditionExpression=Key('userId').eq(str(event['requestContext']['authorizer']['claims']['sub']))
        )

        return success(result['Items'])

    except Exception as error:
        print("Error: {}".format(str(error)))
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
