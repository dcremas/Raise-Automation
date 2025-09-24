from pypdf import PdfReader
from datetime import date

ATTACHMENTS = '/Users/dustincremascoli/Automation/Raise/ATTACHMENTS_RAISE/'

date_tod = date.today().strftime("%Y-%m-%d")
year_tod, month_tod, day_tod = date_tod[:4], date_tod[5:7], date_tod[8:]

file_name = 'Shop_Your_Way_-_Gift_' + year_tod + '-' + month_tod + '-' + day_tod + '.pdf'

reader = PdfReader(ATTACHMENTS + file_name)
text = ""
for page in reader.pages:
    text += page.extract_text()
