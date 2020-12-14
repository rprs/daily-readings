# Daily readings

Code to generate a .mobi file with the daily readins from
http://www.usccb.org/bible/readings/index.cfm

## to run program

`python3 main.py`

## to convert output of pogram to a .mobi ebook.

`ebook-convert dr2021.md dr2021.mobi --authors=bible.usccb.org --title="2021 Daily Readings" --max-toc-links=0 --level1-toc "//h:h1" --level2-toc "//h:h2"  --use-auto-toc --formatting-type=markdown --paragraph-type=off`

## To send it over email.

NOTE: Cannot send it directly to the kindle. Even if the file is attached, the
amazon tool complains that there is not a file attached. Resending the file
manually works. Suggestion is to send file to oneself first, then to the knidle
email.

`mail -s "convert" -r <EMAIL_FROM> <EMAIL_TO> -A dr2021.mobi < emailbody.txt`

## to auto format python code

`autopep8 --in-place --aggressive --aggressive --aggressive main.py`

