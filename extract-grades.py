#!/usr/bin/env python3

'''
Please don't look further - I wrote this code at deep night, because a friend of mine (who got his CS bachelor given for free) could not get my other script to work :D
So this is late night code and will propably stay that way.
'''

import argparse
import mechanicalsoup
import sys
import re
import json

BASE_URL = 'https://www.tucan.tu-darmstadt.de'

parser = argparse.ArgumentParser(description='Login')
parser.add_argument("username")
parser.add_argument("password")
args = parser.parse_args()

SELECTORS = {
    "LoginUser": '#field_user',
    "LoginPass": '#field_pass',
    "LoginForm": '#cn_loginForm'
}

def get_redirection_link(page):
    return BASE_URL + page.soup.select('a')[2].attrs['href']

browser = mechanicalsoup.Browser(soup_config={"features":"html.parser"})
login_page = browser.get(BASE_URL)
login_page = browser.get(get_redirection_link(login_page))
login_page = browser.get(get_redirection_link(login_page))
login_form = login_page.soup.select(SELECTORS['LoginForm'])[0]

# specify username and password
login_form.select(SELECTORS['LoginUser'])[0]['value'] = args.username
login_form.select(SELECTORS['LoginPass'])[0]['value'] = args.password

# submit form
login_page = browser.submit(login_form, login_page.url)
redirected_url = "=".join(login_page.headers['REFRESH'].split('=')[1:])

start_page = browser.get(BASE_URL + redirected_url)
start_page = browser.get(get_redirection_link(start_page))

ergebnisse_page_link = BASE_URL + start_page.soup.select('li[title="Prüfungsergebnisse"] a')[0].attrs['href']
ergebnisse_page = browser.get(ergebnisse_page_link)

def get_link_for_ergebnisse(dispatcher, applicationName, programName, sessionNo, menuId, args):
    return dispatcher + "?APPNAME=" + applicationName + "&PRGNAME=" + programName + "&ARGUMENTS=-N" + sessionNo + ",-N" + menuId + ',' + args

new_link = ergebnisse_page.soup.select('select#semester')[0].attrs['onchange'].replace('reloadpage.createUrlAndReload(', '').replace(')', '').replace('this.value', '999').replace('\'', '').split(',')

ergebnisse_page = browser.get(BASE_URL + get_link_for_ergebnisse(*new_link))
grades = [x for x in ergebnisse_page.soup.select('table tr') if "bestanden" not in x.text]
grade_tds = []
for grade in grades:
    tds = grade.select('td')
    if tds is None or len(tds) <= 0:
        continue
    if len(tds[-1].select('a')) <= 0:
        continue
    grade_tds.append(tds)

def get_avg_from_notenspiegel(notenspiegel):
    grades = [1.0,1.3,1.7,2.0,2.3,2.7,3.0,3.3,3.7,4.0,5.0]
    n = [x * grades[index] for (index, x) in enumerate(notenspiegel)]
    return sum(n) / sum(notenspiegel)

def get_notenspiegel(link):
    notenspiegel_regexp = re.compile(r'<td class="tbdata">(.*?)<\/td>')
    durschschnitt_regexp = re.compile(r'Durchschnitt\: (.*?)<\/div>')
    html = browser.get(link).text
    try:
        notenspiegel = [int(x.strip()) for x in notenspiegel_regexp.findall(html)[1:]]
        avg = get_avg_from_notenspiegel(notenspiegel)
        return {
            "notenspiegel": notenspiegel,
            "avg": avg
        }
    except:
        return None

def sanitize_title(title):
    title = title.split('<br>')[0].replace('\n', ' ').replace('&nbsp;', ' ').strip()
    return re.sub(r'\d{2}-\d{2}-\d{4}(?:-iv)?', '', title).strip()

grades = []
for grade_data in grade_tds:
    notenspiegel_link = BASE_URL + grade_data[-1].find('a').attrs['href']
    notenspiegel_data = get_notenspiegel(notenspiegel_link)
    if notenspiegel_data is None:
        print("Failed to get notenspiegel for: {}".format(grade_data[0].text.strip()))
        continue
    grades.append({
        "originalTitle": grade_data[0].text.strip(),
        "title": sanitize_title(str(grade_data[0]).split('<br/>')[0].replace('<td>', '')),
        "grade": float(grade_data[2].text.strip().replace(',','.')),
        "notenspiegel": notenspiegel_data['notenspiegel'],
        "avg": notenspiegel_data['avg']
    })

diffs = []
for grade_data in grades:
    grade = grade_data['grade']
    avg = grade_data['avg']
    title = grade_data['title']
    diff = avg - grade
    diffs.append(diff)
    print("grade: {}\tavg: {}\tdiff: {}\t({})".format(grade, avg, round(diff, 1), title))

print('\n' * 3)
print('#Courses: {}'.format(len(grades)))
print('avg diff: {}'.format(round(sum(diffs) / len(diffs), 2)))

with open('grades.json', 'w+') as f:
    json.dump(grades, f, indent=4)
