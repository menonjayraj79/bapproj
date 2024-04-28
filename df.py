import pandas as pd
# Load datasets
Acomplete = pd.read_excel('Acomplete.xlsx')
Bcomplete = pd.read_excel('Bcomplete.xlsx')
Ccomplete = pd.read_excel('Ccomplete.xlsx')
Dcomplete = pd.read_excel('Dcomplete.xlsx')
Ecomplete = pd.read_excel('Ecomplete.xlsx')

print(Acomplete.head())
print(Bcomplete.head())
print(Ccomplete.head())
print(Dcomplete.head())
print(Ecomplete.head())
# Create a Dash application