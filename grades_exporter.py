#!/usr/bin/env python3

'''
Retrieves the grades from tucan (pain!)

Please don't look further - I wrote this code at deep night,
because a friend of mine (who got his CS bachelor given for free)
could not get my other script to work :D

So this is late night code and will propably stay that way.
'''


import mechanicalsoup
import sys
import re
import json
import helper

def get_grades(username, password):
    BASE_URL = helper.get_tucan_baseurl()

    # Lasciate ogni speranza, oh voi ch'entrate
    (browser, start_page) = helper.log_into_tucan_()

    # Prüfungsergebnisse page
    ergebnisse_page_link = BASE_URL + start_page.soup.select('li[title="Prüfungsergebnisse"] a')[0].attrs['href']
    ergebnisse_page = browser.get(ergebnisse_page_link)

    # Straight outta tucan skripts.js
    def get_link_for_ergebnisse(dispatcher, applicationName, programName, sessionNo, menuId, args):
        return dispatcher + "?APPNAME=" + applicationName + "&PRGNAME=" + programName + "&ARGUMENTS=-N" + sessionNo + ",-N" + menuId + ',' + args

    # To show all the grades you have to select an item in a select box.
    # Unfortunately the used library is no headless browser, so it has to be done manually
    def get_link_for_all_ergebnisse(page):
        args = page.soup.select('select#semester')[0].attrs['onchange'].replace('reloadpage.createUrlAndReload(', '').replace(')', '').replace('this.value', '999').replace('\'', '').split(',')
        return get_link_for_ergebnisse(*args)

    ergebnisse_page = browser.get(BASE_URL + get_link_for_all_ergebnisse(ergebnisse_page))

    # Reomove all "Bestanden" courses since they don't have grades
    grades = [x for x in ergebnisse_page.soup.select('table tr') if "bestanden" not in x.text]
    grade_tds = []
    for grade in grades:
        tds = grade.select('td')
        if tds is None or len(tds) <= 0 or len(tds[-1].select('a')) <= 0:
            continue
        grade_tds.append(tds)

    ### Parsing is done now - now the relaxing part starts...

    def get_notenspiegel(link):
        html = browser.get(link)
        try:
            # Get all notenspiegel items (the first two tds are discarded)
            notenspiegel = [0 if x.text.strip() == '---' else int(x.text.strip()) for x in html.soup.select('td.tbdata')[2:]]
            return notenspiegel
        except:
            return None

    def sanitize_title(title):
        # Removes the ID from the course and does some sanitation
        title = title.split('<br>')[0].replace('\n', ' ').replace('&nbsp;', ' ').strip()
        return re.sub(r'\d{2}-\d{2}-\d{4}(?:-.{2})?', '', title).strip()

    grades = []
    for grade_data in grade_tds:
        # The link to the notenspiegel is in the last column of the table
        notenspiegel_link = BASE_URL + grade_data[-1].find('a').attrs['href']
        notenspiegel_data = get_notenspiegel(notenspiegel_link)
        if notenspiegel_data is None:
            print("Failed to get notenspiegel for: {}".format(grade_data[0].text.replace('\n', ' ').strip()))
            continue
        grade = float(grade_data[2].text.strip().replace(',','.'))
        sanitized_title = sanitize_title(str(grade_data[0]).split('<br/>')[0].replace('<td>', ''))
        title = grade_data[0].text.strip()
        grades.append({
            "originalTitle": title,
            "title": sanitized_title,
            "grade": grade,
            "notenspiegel": notenspiegel_data
        })
    return grades
