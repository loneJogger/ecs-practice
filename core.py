import sheets
import dynamo

print()

emails = sheets.getLitHoldEmails()
print('number of lit hold members: ' + str(len(emails)))

session = dynamo.initSession()
data = dynamo.getLitHoldUsers(session)
print('number of db entries:' + str(len(data)))


print()
