# import statments
import boto3
import settings

# create boto3 session
def initSession():
    session = boto3.Session(
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    )
    return session

# get all users in lit hold table
def getLitHoldUsers(session):

    dynamoDB = session.resource('dynamodb', region_name='us-east-1')
    table = dynamoDB.Table(settings.TABLE)
    response = table.scan()
    data = response['Items']
    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])
    return data

# compare table to sheet: if entry is listed do nothing, if entry is missing add them,
# if entry is not in sheet set as inactive
# def compareSheetToTable(sheet, table):
