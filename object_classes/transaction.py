from __future__         import print_function, division
from datetime           import datetime, timedelta
from utils.jutils       import padString, formatCurrency
from utils.local        import applyTax
from settings.dformat   import dateFormat
from data_classes.ttype import TransactionType
import math

class Transaction:
    __typeMap = {
        'R':TransactionType.REPORT,
        'W':TransactionType.WITHDRAWL,
        'D':TransactionType.DEPOSIT
    }
    def __init__(self, jdata, recurring=False):
        self.__applyTax = '^' in jdata['type'] and True or False
        self.__applyRounding = '_' not in jdata['type'] and True or False  
        self.name   = jdata['name']
        self.type   = Transaction.__typeMap[
            jdata['type'].replace('^','').replace('_','')
        ]
        self.amount = jdata['amount']
        if self.__applyTax:
            self.amount = applyTax(self.amount)
        if self.__applyRounding:
            if self.type == TransactionType.WITHDRAWL:
                self.amount = math.ceil(self.amount)
            if self.type == TransactionType.DEPOSIT:
                self.amount = math.floor(self.amount)
        self.date   = 'date' in jdata and datetime.strptime(
            jdata['date'], 
            dateFormat
        ) or datetime.now()
        self.recurring = recurring
    
    def __parseDate(self, strDate):
        return datetime.strptime(strDate, dateFormat)

    def getCSVEntry(self):
        typ = self.type.value[0]
        date = self.date.strftime(dateFormat)
        amt = formatCurrency(self.amount)
        name = self.name
        recur = self.recurring and 'True' or 'False'
        return f'{recur},{date},{typ},{name},{amt}\n'

    def __str__(self):
        ty = self.type.value[0]
        dt = self.date.strftime(dateFormat)
        amt = formatCurrency(self.amount)
        name = self.name
        ob = '{'
        cb = '}'
        return f'{ob}"date":"{dt}", "type":"{ty}", "name":"{name}", "amount":{amt}{cb}'
