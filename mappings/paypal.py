# -*- coding: utf-8 -*-

__author__ = 'dwrobel'

from datetime import datetime

from csv2ofx.csvutils import fromCSVCol
from csv2ofx.utils import setlocale

# "Date"        "Time"      "Time Zone"
# "29-01-2015"	"15:27:38"	"PST"
def toOFXDate(row, grid):
    date = fromCSVCol(row, grid, 'Date')
    time = fromCSVCol(row, grid, 'Time')
    timezone = fromCSVCol(row, grid, 'Time Zone')
    return datetime.strptime(date + time, "%d-%m-%Y%H:%M:%S").strftime('%Y%m%d')

def isReceived(row, grid):
    return True if float(getAmount(row, grid)) > 0 else False

def getAmount(row, grid):
    return fromCSVCol(row, grid, 'Net').replace(",", ".")

def getPayee(row, grid):
    type = fromCSVCol(row, grid, 'Type')
    payee = fromCSVCol(row, grid, 'Name')

    if type in ['Currency Conversion', 'Transfer']:
        payeeFormat = "{type} {payee}"
    elif type in ['Charge From Credit Card', 'Credit to Credit Card']:
        payeeFormat = "{payee}"
    elif type.lower().endswith('received'):
        payeeFormat = '{type} from "{payee}"'
    elif type and payee:
        payeeFormat = '{type} to "{payee}"'
    else:
        payeeFormat = '{type}{payee}'

    return payeeFormat.format(**locals())

def getMemo(row, grid):
    auctionSite = fromCSVCol(row, grid, 'Auction Site')
    itemID = fromCSVCol(row, grid, 'Item ID')
    itemTitle = fromCSVCol(row, grid, 'Item Title')
    return '{}{}{}{}'.format( auctionSite + ' ' if auctionSite else '', 'Item ID: ' + itemID if itemID else '', '|' if (itemID and itemTitle) else '', itemTitle)

paypal = {

    '_params': {
        'delimiter': '\t',
        'skip_initial_space': True
    },

    'OFX': {
        'skip': lambda row, grid: False,
        'BANKID': lambda row, grid: "PayPal",
        'ACCTID': lambda row, grid: fromCSVCol(row, grid, 'Currency'),
        'DTPOSTED': lambda row, grid: toOFXDate(row, grid),
        'TRNAMT': lambda row, grid: getAmount(row, grid),
        'FITID': lambda row, grid: fromCSVCol(row, grid, 'Transaction ID'),
        'PAYEE': lambda row, grid: getPayee(row, grid),
        'MEMO': lambda row, grid: getMemo(row, grid),
        'CURDEF': lambda row, grid: 'Currency',
        'CHECKNUM': lambda row, grid: ''
    },
}