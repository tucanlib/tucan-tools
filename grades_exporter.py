'''
Retrieves the grades from tucan
'''

import mechanicalsoup
import sys
import re
import json
import helper

def get_grades(with_notenspiegel = True):
    BASE_URL = helper.get_tucan_baseurl()

    # Lasciate ogni speranza, oh voi ch'entrate
    (browser, start_page) = helper.log_into_tucan_()

    # Prüfungsergebnisse page
    ergebnisse_page_link = BASE_URL + start_page.soup.select('li[title="Prüfungsergebnisse"] a')[0].attrs['href']
    ergebnisse_page = browser.get(ergebnisse_page_link)

    # To show all the grades you have to select an item in a select box.
    # Unfortunately the used library is no headless browser, so it has to be done manually
    def get_link_for_all_ergebnisse(page):
        (dispatcher, applicationName, programName, sessionNo, menuId, args) = page.soup.select('select#semester')[0].attrs['onchange'].replace('reloadpage.createUrlAndReload(', '').replace(')', '').replace('this.value', '999').replace('\'', '').split(',')

        # Straight outta tucan skript.js
        return dispatcher + "?APPNAME=" + applicationName + "&PRGNAME=" + programName + "&ARGUMENTS=-N" + sessionNo + ",-N" + menuId + ',' + args

    ergebnisse_page = browser.get(BASE_URL + get_link_for_all_ergebnisse(ergebnisse_page))

    # Remove all "Bestanden" courses since they don't have grades
    grades = [x for x in ergebnisse_page.soup.select('table tr') if "bestanden" not in x.text]
    grade_tds = []
    for grade in grades:
        tds = grade.select('td')
        # Ignore "faulty" lines (that don't have a notenspiegel for example)
        # TODO: this should be more generic - because not all grades have a notenspiegel (for example the bachelor thesis)
        if tds is None or len(tds) <= 0:# or len(tds[-1].select('a')) <= 0:
            continue
        grade_tds.append(tds)

    def get_notenspiegel(link):
        html = browser.get(link)
        try:
            # Get all notenspiegel items (the first two tds are discarded)
            notenspiegel = [0 if x.text.strip() == '---' else int(x.text.strip()) for x in html.soup.select('td.tbdata')[2:]]
            return notenspiegel
        except:
            return None

    def get_grade(grade_as_string):
        try:
            return float(grade_as_string.strip().replace(',','.'))
        except:
            return None

    grades = []
    for grade_data in grade_tds:
        # Title
        title = grade_data[0].text.strip()
        sanitized_title = helper.sanitize_title(str(grade_data[0]).split('<br/>')[0].replace('<td>', ''))
        # Grade
        grade = get_grade(grade_data[2].text)
        if grade is None:
            print('Error retrieving grade for: {}'.format(title))
            continue

        r = {
            "originalTitle": title,
            "title": sanitized_title,
            "grade": grade
        }

        # Notenspiegel
        if with_notenspiegel:
            if len(grade_data[-1].select('a')) <= 0:
                print(f"No notenspiegel found for {title}")
                continue

            notenspiegel_link = BASE_URL + grade_data[-1].find('a').attrs['href']
            notenspiegel_data = get_notenspiegel(notenspiegel_link)
            if notenspiegel_data is None:
                print(f"Error retrieving notenspiegel for: {sanitized_title}")
                continue
            r['notenspiegel'] = notenspiegel_data

        grades.append(r)
    return grades
