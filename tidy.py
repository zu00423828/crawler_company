import pandas as pd
import re

from sqlalchemy import false
df = pd.read_excel('data/pack-tw.xlsx')
print(df.head())
df['comp_address'].replace(
    to_replace="\d+", value='', limit=1, regex=True, inplace=True)
df['comp_phone'] = df['comp_phone'].str.replace(
    "+886", '0', regex=False).str.replace('-', '')
print(df[['name', 'comp_phone', 'comp_address']])

s = '+886123456789'
print(s.replace('+886', '0'))
