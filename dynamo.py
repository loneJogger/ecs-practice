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
def compareSheetToTable(sheet, table):

    tableList = []
    for entry in table:
        tableList.append(entry['email'])

    changes = []

    for email in sheet:
        if email not in tableList:
            changes.append({
                "email" : email,
                "type" : "add"
            })

    for email in tableList:
        if email not in sheet:
            changes.append({
                "email" : email,
                "type" : "deactivate"
            })

    return changes

# write changes to bring DB into line with sheet
def writeChanges(session, changes):

    dynamoDB = session.resource('dynamodb', region_name='us-east-1')
    table = dynamoDB.Table(settings.TABLE)

    for change in changes:
        if change['type'] == "add":
            table.put_item(
                Item={
                    'email' : change['email'],
                    'active' : True,
                    'files' : {}
                }
            )
        elif change['type'] == "deactivate":
            table.update_item(
                Key={
                    'email' : change['email']
                },
                UpdateExpression='SET active = :val',
                ExpressionAttributeValues={
                    ':val' : False
                }
            )

    print('DB update complete!')
