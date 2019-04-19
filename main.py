"""File that to extract readings from the source of the website."""
import collections
import datetime
import urllib2
from bs4 import BeautifulSoup

Reading = collections.namedtuple('Reading', 'title text')

def get_date_for_today():
    """Finds the system's date"""
    return datetime.date.today().strftime('%m%d%y')

def get_source_from_web(date):
    """Pulls the website source for hte daily readings"""
    url_prefix = 'http://www.usccb.org/bible/readings/'
    url_suffix = '.cfm'
    url = ''.join([url_prefix, date, url_suffix])

    # Retrieve the page source
    response = urllib2.urlopen(url)
    page_source = response.read()
    return page_source

def convert_web_source_into_soup(page_source):
    """Simply calls beatiful Soup with the html."""
    soup = BeautifulSoup(page_source, 'html5lib')
    return soup


def get_readings_from_content(content):
    """retrieves the readings from the beautiful soup."""
    # Get readings from page source
    texts = []
    for reading in content.find_all('div', class_='poetry'):
        for br_tag in reading.find_all('br'):
            br_tag.replace_with('\n')
        heading = reading.find_all('h4')
        if heading:
            splitted_readings = reading.text.partition(heading[0].text)
            texts.append(splitted_readings[0])
            texts.append(splitted_readings[2])
        else:
            texts.append(reading.text)
    titles = []
    for title in content.find_all('h4'):
        titles.append(title.text)

    # Make sure we got same number of titles and readings
    if len(titles) != len(texts):
        print 'ERROR: titles and readings are different.'

    # Return the readings in objects
    readings = []
    for title, text in zip(titles, texts):
        readings.append(Reading(
            ''.join(['\n\n\n## ', title.strip(), '\n\n']),
            text.strip()))
    return readings

def get_title_from_content(content):
    """Extracts the title of the readings."""
    for title in content.find_all('h3'):
        # We assume that Lectionary will always be part of the title.
        # So far it has.
        if 'Lectionary' in title.text:
            for br_tag in title.find_all('br'):
                br_tag.replace_with('\n')
            return title.text

def write_to_file(title, readings):
    """Saves the readings in a file."""
    date = datetime.date.today().strftime('%Y-%m-%d')
    file_title = ''.join(['dr', date, '.txt'])
    _file = open(file_title, 'w+')
    _file.write(title.encode('utf8'))
    for reading in readings:
        _file.write(reading.title.encode('utf8'))
        _file.write(reading.text.encode('utf8'))
    _file.close()


def main():
    """main function when we call python <this_file>."""
    date = get_date_for_today()
    source = get_source_from_web(date)
    soup = convert_web_source_into_soup(source)
    readings = get_readings_from_content(soup)
    title = get_title_from_content(soup)
    title = ''.join(['# ', title])
    write_to_file(title, readings)

main()
