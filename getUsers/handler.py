import boto3, json, os, uuid

client = boto3.resource('dynamodb')

IS_OFFLINE = os.getenv('IS_OFFLINE', False)
if IS_OFFLINE:
    boto3.Session(
        aws_access_key_id = 'DEFAULTACCESSKEY',
        aws_secret_access_key = 'DEFAULTSECRET',
    )
    client = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')

table = client.Table('usersTable')

def getUsers(event, context):
    userId = event['pathParameters']['id']

    params = {
        'ExpressionAttributeValues': { ":pk": userId },
        'KeyConditionExpression': "pk = :pk",
        'TableName': "usersTable",
    }

    response = table.query(**params)

    return {
        'statusCode': 200,
        'body': json.dumps(response['Items'])
    }