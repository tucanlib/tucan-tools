#!/usr/bin/env python3
"""
This script extracts the grades from the 'Leistungsspiegel' page.
The other script extracts the grades from the 'Prüfungen' page
"""

from tucan_tools import helper


def convert_to_float(x):
    try:
        return float(x.strip().replace(',', '.'))
    except:
        return -1.0


class Grade(object):

    def __init__(self, title, grade, cp):
        self.title = title
        self.grade = grade
        self.cp = cp


def get_grades():
    BASE_URL = helper.get_tucan_baseurl()

    (browser, start_page) = helper.log_into_tucan_()

    # Leistungsspiegel page
    leistungsspiegel_page_link = BASE_URL + start_page.soup.select('li[title="Leistungsspiegel"] a')[0].attrs['href']
    leistungsspiegel_page = browser.get(leistungsspiegel_page_link)
    grades_raw = leistungsspiegel_page.soup.select('tr')
    grades_raw = [x for x in grades_raw if "Bestanden" in str(x) and len(x.select('td.tbdata')) > 5]
    grades = []
    for grade_data in grades_raw:
        tds = grade_data.select('td.tbdata')
        title = tds[1].find('a').text.strip()
        cp = convert_to_float(tds[3].text)
        grade = convert_to_float(tds[5].text)
        grades.append(Grade(title=title, grade=grade, cp=cp))
    return grades

