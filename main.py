"""File that to extract readings from the source of the website."""
from bs4 import BeautifulSoup
from dataclasses import dataclass, field
from typing import List
import collections
import datetime
import urllib.request


@dataclass
class DailyReadings:
    day_title: str
    date: datetime
    readings_titles: List[str] = field(default_factory=list)
    versiculos: List[str] = field(default_factory=list)
    readings: List[str] = field(default_factory=list)

    def to_string(self):
        text = '## {0} {1}\n\n'.format(
            self.date.strftime('%Y-%m-%d'), self.day_title)
        for i in range(len(self.readings)):
            text += '### {0} {1}\n\n'.format(
                self.readings_titles[i], self.versiculos[i])
            text += '{0}\n\n'.format(self.readings[i])
        return text


def get_source_from_web(date):
    """Pulls the website source for hte daily readings"""
    url_prefix = 'https://bible.usccb.org/bible/readings/'
    url_suffix = '.cfm'
    url = ''.join([url_prefix, date, url_suffix])

    # Retrieve the page source
    try:
        response = urllib.request.urlopen(url)
    except urllib.error.HTTPError as err:
        print('Could not open url {0}: {1}'.format(url, err))
        raise
    page_source = response.read()
    return page_source


def soupify(page_source):
    """Simply calls beatiful Soup with the html."""
    soup = BeautifulSoup(page_source, 'html5lib')
    return soup


def strip_empty_lines(text):
    return '\n'.join([t for t in text.splitlines() if t])


def get_lecture_titles(content):
    return [t.text for t in content.find_all('h3')]


def get_versiculos(content):
    return [t.text.strip() for t in content.find_all('div', class_='address')]


def get_readings(content):
    """retrieves the readings from the beautiful soup."""
    texts = []
    lecture_titles = get_lecture_titles(content)
    readings = content.find_all('div', class_='content-body')
    for t, r in zip(lecture_titles, readings):
        if 'psalm' in t.lower() or 'alleluia' in t.lower():
            for br_tag in r.find_all('br'):
                br_tag.replace_with('\n')
            texts.append(psalm_with_breaks(strip_empty_lines(r.text.strip())))
        else:
            texts.append(r.text.strip())
    return texts


def get_day_title(content):
    """Extracts the title of the readings."""
    # Gets the content of the html attribute <title>,
    # removes the ' | USCCB' trailing text by sliting the text on '|'
    # and removing the trailing space (.[:-1])
    return content.find('title').text.split('|', 1)[0][:-1]


def psalm_with_breaks(psalm):
    """Adds line breaks so the psalm is readable."""
    lines = psalm.splitlines()
    result = ''
    first_line = True
    lines_size = len(lines)
    for i in range(lines_size):
        result += lines[i]
        if i + 1 < lines_size:
            result += '\n'
            if lines[i + 1].startswith('R. '):
                result += '\n'
            if lines[i].startswith('R. '):
                result += '\n'
    return result


def write_to_file(date, lectures):
    """Saves the readings in a file."""
    file_title = ''.join(['dr', date.strftime('%Y'), '.md'])
    _file = open(file_title, 'w+')
    _file.write('# {0} Daily readings\n\n'.format(date.strftime('%Y')))
    for lecture in lectures:
        _file.write(lecture.to_string())
    _file.close()


def get_lectures_for_date(date):
    source = get_source_from_web(date.strftime('%m%d%y'))
    soup = soupify(source)
    title = get_day_title(soup)
    versiculos = get_versiculos(soup)
    readings = get_readings(soup)
    titles = get_lecture_titles(soup)
    return DailyReadings(title, date, titles, versiculos, readings)


def main():
    """main function when we call python <this_file>."""
    start_date = datetime.date(2020, 1, 1)
    end_date = datetime.date(2021, 1, 1)
    date = start_date
    # Used these date (and range 5 in the loop) for testing purposes.
    # date = datetime.date(2020, 9, 25)
    d = datetime.timedelta(1)
    lectures = []
    # for i in range(5):
    while date < end_date:
        print('tackling date: {0}'.format(date.strftime('%Y-%m-%d')))
        if date == datetime.date(2020, 6, 4):
            # For some reson, the webpage does not have levtures for this day.
            date = date + d
            continue
        lectures.append(get_lectures_for_date(date))
        date = date + d
    write_to_file(start_date, lectures)


main()
