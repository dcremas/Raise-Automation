import os

ATTACHMENTS = '/Users/dustincremascoli/Automation/Raise/ATTACHMENTS_RAISE/'
FILES = os.listdir(ATTACHMENTS)

for file in FILES:
	file_modify = file.split('.')[0][:31] + '.pdf'
	src = f"{ATTACHMENTS}{file}"
	dst = f"{ATTACHMENTS}{file_modify}"
	os.rename(src, dst)
