from __future__ import print_function, division
from object_classes.html import HTMLWriter
from object_classes.transaction import Transaction
from settings.dformat import dateFormat,fileFormat
from utils.local import getWeekRange, writeSettings, calcNumRecurring
from datetime import datetime, timedelta
import json
import copy
import os

if not os.path.isfile('./current.json'):
    dRange = getWeekRange(datetime.today())
    newSettings = {
        "last total":0.00,
        "start date":dRange[0].strftime(dateFormat),
        "end date":dRange[1].strftime(dateFormat),
        "transactions":[
            Transaction(
                {
                    "date":dRange[0].strftime(dateFormat),
                    'type':'R',
                    'name':'Sample Transaction',
                    'amount':0.00
                }
            )
        ]
    }
    writeSettings(newSettings,'./current.json')

if not os.path.isfile('./test.json'):
    f = open('./test.json','w')
    f.write('[\n')
    f.write('    { "type":"R", "name":"Sample Transaction", "amount":0.00 }\n')
    f.write(']')
    f.close()

# Load in current transactions
f = open('./current.json','r')
current = json.loads(f.read())
f.close()

# Parse transactions into transaction objects
current['transactions'] = [Transaction(x) for x in current['transactions']]

# If we don't have a valid start or end date, calculate a new one
if current['start date'] == '' or current['end date'] == '':
    dayRange = getWeekRange(datetime.now())
    current['start date'] = dayRange[0].strftime(dateFormat)
    current['end date'] = dayRange[1].strftime(dateFormat)

# Init global vars
# (datetime) Starting date for our report range
startDate   = datetime.strptime(current['start date'], dateFormat)
# (datetime) Ending date for our report range
endDate     = datetime.strptime(current['end date'], dateFormat)

# (datetime) The current date, only want the date not the time; hence all the
# datetime function wizardry.
today       = datetime.strptime(
    datetime.today().strftime(dateFormat),dateFormat
)

# (Boolean) Whether to archive entries or not
arcive      = False

# If we're past the current end date, re-adust the end date
if today.date() > endDate.date():
    # Flag archiving
    arcive      = True

    # Adjust end date
    dayRange    = getWeekRange(today)
    endDate     = dayRange[0] - timedelta(days=1)

# Load in recurring transactions from file
f = open('./recurring.json','r')
recurring = json.loads(f.read())
f.close()

# (Int) The numer of times to apply our recurring transactions
numRecurring        = calcNumRecurring(startDate,endDate)
# (datetime) The current date
curDate             = startDate
# (Transaction) a list of recurring transactions expanded out for each week
expandedRecurring   = []

# Expand out transactions based on the number of weeks passed since last run
for _ in range(0, numRecurring):
    for r in recurring:
        expandedRecurring.append(copy.deepcopy(r))
        expandedRecurring[-1]['date'] = curDate.strftime(dateFormat)
    curDate += timedelta(days=7)
recurring = [Transaction(x, True) for x in expandedRecurring]

# Aggregate recurring transactions and user defined transactions together
aggregated = sorted(
    recurring + current['transactions'], 
    key=lambda x: x.date
)

# (Float) holds last total temporarily and is only written in case of archving
lastTotal = current['last total']

# Create html writer
writer = HTMLWriter()
writer.createHeader(startDate, endDate)

# Print report header
lastTotal = writer.processTransaction(
    Transaction({
        'date':startDate.strftime(dateFormat),
        'name':f'Total From {(startDate - timedelta(days=1)).strftime(dateFormat)}',
        'type':'R',
        'amount':lastTotal
    }),
    lastTotal
)

# Add transactions to the report
for transaction in aggregated:
    lastTotal = writer.processTransaction(
        transaction,
        lastTotal
    )

# Print the report ending transaction
lastTotal = writer.processTransaction(
    Transaction({
        'date':endDate.strftime(dateFormat),
        'name':f'Report Total Ending On {endDate.strftime(dateFormat)}',
        'type':'R',
        'amount':lastTotal
    }),
    lastTotal
)

# If archiving flag was set, archive data and clear out transactions
if arcive:
    # Archive data as csv
    f = open(f'./data/{endDate.strftime(fileFormat)}.csv','w')
    for transaction in aggregated:
        f.write(transaction.getCSVEntry())
    f.close()

    # Adjust new date range
    newDateRange                = getWeekRange(today)
    current['start date']       = newDateRange[0].strftime(dateFormat)
    current['end date']         = newDateRange[1].strftime(dateFormat)

    # Write out total as last total
    current['last total']       = lastTotal

    # clear out transactions
    current['transactions']     = []

# Print out report, write settings, and exit
writer.createPDF(f'./reports/{endDate.strftime(fileFormat)}.pdf')

# Once we're done, print out and write back to file
writeSettings(current, './current.json')