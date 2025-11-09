from __future__ import print_function, division
from json import loads

class ListItem:
    def __init__(self, json):
        self.name = json['name']
        self.amount = round(json['amount'])
        self.quantity = 1
        if 'quantity' in json:
            self.quantity = json['quantity']
    
    def get_total_value(self):
        return self.amount * self.quantity
    
    def __str__(self):
        compound = self.name
        if self.quantity > 1:
            compound += f" (x{self.quantity})"
        amount = self.amount * self.quantity
        return f'{compound:.<40}${amount:6.2f}'

f = open('./wishlist.json', 'r')
total = 0.0
for li in [ ListItem(x) for x in loads(f.read()) ]:
    total += li.get_total_value()
    print(li)
tax = round(total * 0.0825)
print("-"*47)
print(f'{"Tax":.<40}${tax:6.2f}')
print(f'{"Total":.<40}${round(tax+total):6.2f}')