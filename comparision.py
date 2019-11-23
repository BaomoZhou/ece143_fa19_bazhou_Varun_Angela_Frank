# -*- coding: utf-8 -*-
import pandas as pd

sold_id = []
new_id = []
same_id = []

data_yst = pd.read_csv('test_yst.csv')
data_td = pd.read_csv('test_td.csv')

ID_yst = data_yst['Item ID']
ID_td = data_td['Item ID']

for item in ID_td:
    if item not in ID_yst.values:
        new_id.append(item)
    else:
        same_id.append(item)
for item in ID_yst:
    if item not in ID_td.values:
        sold_id.append(item)
    
print(sold_id)
print(new_id)
print(same_id)