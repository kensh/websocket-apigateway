import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')
TABLE_NAME = os.environ['TABLE_NAME']
table = dynamodb.Table(TABLE_NAME)


def lambda_handler(event, context):
    
    print(json.dumps(event))


    try:
        # raise Exception('this is dummy error!')
        
        connectionId = event['requestContext']['connectionId']
        item = {
             'connectionId': connectionId
        }

        table.put_item(Item=item)
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": "Failed to connect: {0}".format(str(e, encoding = 'utf-8'))
        }),
    }

    return {
        "statusCode": 200, # to fail the connection, return not 200
        "body": json.dumps({
            "message": "Connected."
        }),
    }
