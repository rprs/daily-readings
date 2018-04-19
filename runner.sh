# ~/.bashrc: executed by bash(1) for non-login shells.

# Set ourselves in the correct directory
cd ~/src/daily_readings

# Python fetches the content from the website
python ./main.py

# convert the recently created txt to .mobi
today_date=$(date +"%Y-%m-%d")
mobi_file="dr$today_date.mobi"
txt_file="dr$today_date.txt"
ebook-convert $txt_file $mobi_file --formatting-type=markdown --paragraph-type=unformatted

# send file by email
mail -s "daily_readings" -r $1 $2 -A $mobi_file < emailbody.txt 

# move the file so we only keep the last file
mv $mobi_file last_file.mobi
mv $txt_file last_readings.txt