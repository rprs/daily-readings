from main import get_source_from_web

""" List of dates that show a corner case that we need to handle."""
test_cases = [
    '032918',
    '041518',
    '041618',
    '040118',
    '033118',
    '041718',
    '041818',
    '051018',
    '081518'
]

def download_pages_for_testing():
    """Function to download the url content for the tests cases.

    This is done once and then the files are saved in the test_pages directory.
    """
    for date in test_cases:
        url_content = get_source_from_web(date)
        file_name = ''.join(['test_pages/', date, '.txt'])
        with open(file_name, 'w') as f:
            f.write(url_content)
            # python 3 equivalent
            # print(url_content, file=f)


def test_get_srouce_from_web():
    print(get_source_from_web())
    assert 1 == 1

# Only use this when you need to download new test cases (new dates that have a weird format for the daily reading).
# To run: `python test_main.py`
# download_pages_for_testing()
