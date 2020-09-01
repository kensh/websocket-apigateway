import json
import boto3
import os
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')
TABLE_NAME = os.environ['TABLE_NAME']
table = dynamodb.Table(TABLE_NAME)


def lambda_handler(event, context):

    post_data = json.loads(event.get('body', '{}')).get('data')
    domain_name = event.get('requestContext',{}).get('domainName')
    stage       = event.get('requestContext',{}).get('stage')
    apigatewaymanagementapi = boto3.client('apigatewaymanagementapi', endpoint_url=F"https://{domain_name}/{stage}")

    try:
        items = scan()
        for item in items:
            response = apigatewaymanagementapi.post_to_connection(
                Data=post_data,
                ConnectionId=item['connectionId']
            )

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": "Failed to send: {0}".format(str(e, encoding = 'utf-8'))
        }),
    }

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Data sent."
        }),
    }

def query(connectionId):
    result = table.query(
        KeyConditionExpression=Key('connectionId').eq(connectionId)
    )
    return result['Items']

def scan():
    try:
        result = table.scan(
            ProjectionExpression='connectionId',
        )
        return result['Items']

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": "Failed to get recipients: {0}".format(str(e, encoding = 'utf-8'))
        }),
    }

