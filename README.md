# Daily readings

Code to generate a .mobi file with the daily readins from
http://www.usccb.org/bible/readings/index.cfm

## to run program

`python3 main.py`

## to convert output of pogram to a .mobi ebook.

`ebook-convert dr2020.md dr2020.mobi --authors=bible.usccb.org --title="2020 Daily Readings" --max-toc-links=0 --level1-toc "//h:h1" --level2-toc "//h:h2"  --use-auto-toc --formatting-type=markdown --paragraph-type=off`

## To send it over email.

`mail -s "convert" -r <EMAIL_FROM> <EMAIL_TO> -A dr2020.mobi < emailbody.txt`

## to auto format python code

`autopep8 --in-place --aggressive --aggressive --aggressive main.py`

