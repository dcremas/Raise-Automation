#/bin/zsh

# A place to run python scripts from commands.

time_start=$(date +%s)

python 01_GMAIL_CONNECT.py

python 02_PDF_EXCEL_ALL.py

python 03_EXCEL_CONNECT.py

time_stop=$(date +%s)

diff=$(( time_stop - time_start ))

echo "The script took $diff seconds to complete."

exit 0
