from __future__ import print_function, division
from enum       import Enum

class TransactionType (Enum):
    REPORT='R',
    WITHDRAWL='W',
    DEPOSIT='D'