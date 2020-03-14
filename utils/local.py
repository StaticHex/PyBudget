from __future__ import print_function, division
from datetime import datetime, timedelta
from settings.dformat import dateFormat, taxRate
from utils.jutils import formatCurrency


def getWeekRange(date):
    today = date.weekday()
    start = 0
    end = 6
    if today < 6:
        start = today + 1
        end = 6 - (today + 1)
    ds = date - timedelta(days=start)
    de = date + timedelta(days=end)
    return (ds,de) 

def applyTax(amount):
    tax = amount * taxRate
    return amount + tax

def calcNumRecurring(startD, endD):
    # Make sure we're dealing with datetime objects
    if isinstance(startD, str):
        startD = datetime.strptime(startD,dateFormat)
    if isinstance(endD, str):
        endD = datetime.strptime(endD, dateFormat)
    dt = endD - startD
    return (dt.days // 7) + 1

def writeSettings(data, path=''):
    f = path and open(path, 'w') or open('./settings2.json','w')
    idt = '    '
    f.write('{\n')
    f.write(f'{idt}"last total":{data["last total"]},\n')
    f.write(f'{idt}"start date":"{data["start date"]}",\n')
    f.write(f'{idt}"end date":"{data["end date"]}",\n')
    f.write(f'{idt}"transactions":[\n')
    transString = ""
    for t in data['transactions']:
        transString += f'        {str(t)},\n'
    transString = f'{transString[:-2]}{transString[-1:]}'
    f.write(transString)
    f.write(f'{idt}]\n')
    f.write('}')

def formatCurrencyAsString(amount):
    amtStr = formatCurrency(amount)
    if '-' in amtStr:
        amtStr = f'{amtStr[0]}${amtStr[1:]}'
    else:
        amtStr = f'${amtStr}'
    return amtStr