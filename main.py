import datetime
from bs4 import BeautifulSoup
import urllib2

class Reading:
    def __init__(self, title, text):
        self.title = title
        self.text = text

def get_date_for_today():
    return datetime.date.today().strftime('%m%d%y')

def get_source_from_web(date):
    url_prefix = 'http://www.usccb.org/bible/readings/'
    url_suffix = '.cfm'
    url = ''.join([url_prefix, date, url_suffix])

    # Retrieve the page source
    response = urllib2.urlopen(url)
    page_source = response.read()
    return page_source

def convert_web_source_into_soup(page_source):
    soup = BeautifulSoup(page_source, 'html5lib')
    return soup


def get_readings_from_content(content):
    # Get readings from page source
    texts = []
    for r in content.find_all('div', class_='poetry'):
        for br in r.find_all('br'):
            br.replace_with('\n')
        h = r.find_all('h4')
        if h:
            splitted_readings = r.text.partition(h[0].text)
            texts.append(splitted_readings[0])
            texts.append(splitted_readings[2])
        else:
            texts.append(r.text)
    titles = []
    for t in content.find_all('h4'):
        titles.append(t.text)

    # Make sure we got same number of titles and readings
    if len(titles) != len(texts):
        print 'ERROR: titles and readings are differenti.'

    # Return the readings in objects
    readings = []
    for title, text in zip(titles, texts):
        readings.append(Reading(title, text))
    return readings

def get_title_from_content(content):
    for t in content.find_all('h3'):
        # We assume that Lectionary will always be part of the title.
        # So far it has.
        if 'Lectionary' in t.text:
            for br in t.find_all('br'):
                br.replace_with('\n')
            return t.text

def format_readings(readings):
    for r in readings:
        r.text = r.text.strip()
        r.title = r.title.strip()
        if 'Psalm' not in r.title and 'Alleluia' not in r.title:
            r.text = r.text.replace('.\n', '.\n\n')
            r.text = r.text.replace('"\n', '"\n\n')
        if r != readings[-1]:
            r.text += '\n\n\n\n'
        r.title = ''.join(['## ', r.title, '\n\n\n'])

def write_to_file(title, readings):
    date = datetime.date.today().strftime('%Y-%m-%d')
    file_title = ''.join(['dr', date, '.txt'])
    f = open(file_title, 'w+')
    f.write(title.encode('utf8'))
    for r in readings:
        f.write(r.title.encode('utf8'))
        f.write(r.text.encode('utf8'))
    f.close()


def main():
    date = get_date_for_today()
    source = get_source_from_web(date)
    soup = convert_web_source_into_soup(source)
    readings = get_readings_from_content(soup)
    format_readings(readings)
    title = get_title_from_content(soup)
    title = ''.join(['# ', title, '\n\n\n\n'])
    write_to_file(title, readings)

main()
