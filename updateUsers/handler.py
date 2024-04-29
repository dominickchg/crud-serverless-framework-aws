import boto3, json, os

client = boto3.resource('dynamodb')

IS_OFFLINE = os.getenv('IS_OFFLINE', False)
if IS_OFFLINE:
    boto3.Session(
        aws_access_key_id = 'DEFAULTACCESSKEY',
        aws_secret_access_key = 'DEFAULTSECRET',
    )
    client = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')

table = client.Table('usersTable')

def updateUsers(event, context):
    userId = event['pathParameters']['id']

    body = json.loads(event['body'])

    params = {
        'TableName': "usersTable",
        'Key': { 'pk': userId },
        'UpdateExpression': 'set #Nombre = :Nombre',
        'ExpressionAttributeNames': { '#Nombre': 'Nombre' },
        'ExpressionAttributeValues': { ':Nombre': body['Nombre'] },
        'ReturnValues': 'ALL_NEW'
    }

    response = table.update_item(**params)

    return {
        'statusCode': 200,
        'body': json.dumps({'user': response['Attributes']})
    }