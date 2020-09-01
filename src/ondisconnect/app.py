import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')
TABLE_NAME = os.environ['TABLE_NAME']
table = dynamodb.Table(TABLE_NAME)


def lambda_handler(event, context):

    connectionId = event['requestContext']['connectionId']

    try:
        item = {
             'connectionId': connectionId
        }

        table.delete_item(
            Key=item
        )
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": "Failed to disconnect: {0}".format(str(e, encoding = 'utf-8'))
        }),
    }

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Disconnected."
        }),
    }

