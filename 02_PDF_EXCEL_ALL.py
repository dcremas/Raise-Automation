import os
from datetime import datetime, date
import pdfplumber
import pandas as pd

directory = os.listdir('FILES_RAISE')
directory.sort()

date_tod = date.today().strftime("%Y-%m-%d")
year_tod, month_tod, day_tod = date_tod[:4], date_tod[5:7], date_tod[8:]

headings = {0: 'Invoice_Number', 1: 'Statement_Date', 2: 'Escrow_Balance', 3: 'Invoiced_Amount'}

excel_file = f'FILES_EXCEL/data_{month_tod}-{day_tod}-{year_tod}.xlsx'

for idx, file in enumerate(directory):

	if idx == 0:
		with pdfplumber.open(f"FILES_RAISE/{file}") as pdf:
			for page in pdf.pages:
				tables = page.extract_tables()
				for table in tables:
					if table:
						df = pd.DataFrame(table)
	else:
		with pdfplumber.open(f"FILES_RAISE/{file}") as pdf:
			for page in pdf.pages:
				tables = page.extract_tables()
				for table in tables:
					if table:
						df = pd.concat([df, pd.DataFrame(table)], ignore_index=True)

df.rename(columns=headings, inplace=True)
df = df[df['Invoice_Number'].str.contains('SYW')]
df = df[df[['Statement_Date']].notnull().all(1)]
df['Escrow_Balance'] = (
	df['Escrow_Balance'].str.replace('$', '', regex=False)
	.str.replace(',', '', regex=False)
	.str.replace('(', '-', regex=False)
	.str.replace(')', '', regex=False)
	)
df['Escrow_Balance'] = df['Escrow_Balance'].astype(float)
df['Invoiced_Amount'] = (
	df['Invoiced_Amount'].str.replace('$', '', regex=False)
	.str.replace(',', '', regex=False)
	.str.replace('(', '-', regex=False)
	.str.replace(')', '', regex=False)
	)
df['Invoiced_Amount'] = df['Invoiced_Amount'].astype(float)
df['Statement_Date'] = pd.to_datetime(df['Statement_Date'], format='%b %d, %Y')

with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
	df.to_excel(writer, sheet_name='Data', index=False)
