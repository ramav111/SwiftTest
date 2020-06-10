#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 10:18:47 2020

@author: hannahchiakaixin
The Top 3 itemids (in a list) from the ‘Official Shop’ of that particular 
brand that generated the highest Gross Sales Revenue 
from 10th May to 31st May 2019.
"""
import pandas as pd

pd.set_option("display.max.columns", None)
pd.set_option("display.precision", 7)

#is there a way to do this without hardcoding the file path?
#shop type + brand dataset
brands = pd.read_csv("/Users/hannahchiakaixin/Desktop/shopee/preter_1.csv")
#transactions dataset
orders = pd.read_csv("/Users/hannahchiakaixin/Desktop/shopee/preter_2.csv", 
                  parse_dates= ['date_id'], infer_datetime_format=True, 
                  dayfirst = True, index_col = ['shopid'])


#all brands (for use later)
all_brands = list(brands.brand.unique())

#  Clean dataset 1, the shopid column
brands = brands.astype({'shop_id': 'int64'})

brands = brands.set_index('shop_id').rename_axis('shopid', axis = 'rows')
#only take official shops
brands = brands.loc[brands.shop_type == 'Official Shop']
#clean dataset 2 remove all dates outside the range
orders = orders.loc[(orders['date_id'] > '2019-5-10') 
                    & (orders['date_id'] <= '2019-5-31')]

#merge datasets
df = brands.join(orders)
#remove null values & duplicates
df = df.dropna()
df = df.drop_duplicates()

#add column for gross sales revenue
df['gross_sales_rev'] = df.item_price_usd * df.amount

#create a merged dataset
two = df.groupby(['brand', 'itemid']).gross_sales_rev.sum()
two = two.sort_index().reset_index().set_index('brand')

submission = []
#iterate through each brand. use list for submission for efficiency
brand_names = list(two.index.unique())
for b in brand_names:
    #retireve all the rows for each brand 
    rows = two.loc[b]
    #locate the highest gross_sales_rev and return the itemid
    if rows.shape[0] > 3:
        rows = rows.sort_values('gross_sales_rev', ascending = False).head(3)
    if isinstance(rows, pd.Series):
        aslist = [b] + [rows.itemid]
    else:
        aslist = ([b] + list(rows.itemid))
    submission.append(aslist)
    #add it to the dataframe

#add missing brands
missing_brands = list(set(all_brands).difference(brand_names))

submission += [([m]+ ['N.A']) for m in missing_brands]
submission.sort()

#format submission
submission = pd.Series(submission).reset_index()
submission.columns = ['Index', 'Answers']
submission['Index'] = submission['Index'] + 1
submission.to_csv("preter1solved.csv", header = True, index = False)



# reset_index()
#having difficulty extracting just one index to get, for example, all the brands
# brand_names = two.index[level="brand"]
# print(brand_names)
# 


#the print line throws up an error for some reason
# print(two.index["brand"].nlargest(3))

