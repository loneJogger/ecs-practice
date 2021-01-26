import sheets
import dynamo

print()

sheet = sheets.getLitHoldEmails()
print('number of lit hold members: ' + str(len(sheet)))

session = dynamo.initSession()
table = dynamo.getLitHoldUsers(session)

changes = dynamo.compareSheetToTable(sheet, table)
dynamo.writeChanges(session, changes)

print()
