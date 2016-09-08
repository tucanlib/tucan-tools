#!/usr/bin/env python3

'''
Why does this have to be such a pain :/
BeautifulSoup and me won't become friends, it's too stubbornly misunderstanding...
'''

import mechanicalsoup
import sys
import re
import json
import helper
import collections
from pprint import pprint
from bs4 import BeautifulSoup

BLACKLIST=(
    'Weitere Veranstaltungen',
    'Leistungen für den Masterstudiengang',
    'Zusätzliche Leistungen',
    'Anmelden',
    'Gesamtkatalog aller Module an der TU Darmstadt',
    'Informatik fachübergreifend',
    'Module des Sprachenzentrums mit Fachprüfungen',
    'Fachübergreifende Veranstaltungen',
    'Veranstaltung'
)

BASE_URL = helper.get_tucan_baseurl()

def details_from_element(element):
    link = element.find('a')
    title = link.text.strip()
    link = BASE_URL + link.attrs['href']
    return  {'title': title, 'link': link, 'isParent': "PRGNAME=REGISTRATION" in link,  'isModule': "PRGNAME=MODULEDETAILS" in link, 'children': []}

def get_all_links(page):
    links = [details_from_element(x) for x in page.soup.select('#pageContent ul li, #pageContent table tr') if x.text.strip() not in BLACKLIST and len(x.select('a')) > 0]
    return links

def sanitize_detail(detail):
    replacements = [
        ('\t', ''),
        ('<br/>', '\n'),
        ('\n', '<br/>'),
        (':', '\t'),
        ('\t', ':')
    ]

    detail_text = detail['details']
    detail_text = BeautifulSoup(detail_text, "html.parser").text
    detail['title'] = detail['title'].replace(':', '').strip()

    for r in replacements:
        detail_text = detail_text.replace(r[0], r[1]).strip()

    detail_text = re.sub(r'^:', '', detail_text).strip()
    detail_text = re.sub(r'(<br\/>)*$', '', detail_text).strip()
    detail_text = re.sub(r'(<br\/>)*', '', detail_text).strip()
    detail['details'] = detail_text
    return detail

def extract_module_details(html):
    details = []
    details_raw = html.select('#pageContent table:nth-of-type(1) .tbdata td')
    return [sanitize_detail({"title": x.split('</b>')[0].strip(), "details": x.split('</b>')[1].strip()}) for x in str(details_raw).split('<b>')[1:]]

def extract_cp(link):
    for detail in link['details']:
        if 'Credits' in detail['title']:
            return detail['details'].split(',')[0]
    return 0

def print_link(link):
    print(('\t' * link['depth']) + '> {}'.format(link['title']) )

def crawl(browser, link):
    if link['isParent']:
        print_link(link)
        page = browser.get(link['link'])
        for l in [x for x in get_all_links(page) if x['isParent'] or x['isModule']]:
            l['depth'] = link['depth'] + 1
            link['children'].append(crawl(browser, l))
    elif link['isModule']:
        module_page = browser.get(link['link'])
        link['details'] = extract_module_details(module_page.soup)
        link['credits'] = extract_cp(link)
        print_link(link)
    return link

def walk_modules(vv, fn, only_children = True):
    if len(vv['children']) == 0 or not only_children:
        vv = fn(vv)
    for child in vv['children']:
        child = walk_modules(child, fn)
    return vv

def get_vv():
    BASE_URL = helper.get_tucan_baseurl()
    (browser, start_page) = helper.log_into_tucan_()

    # anmeldung page
    anmeldung_page_link = BASE_URL + start_page.soup.select('li[title="Anmeldung"] a')[0].attrs['href']

    vv = crawl(browser, {'title': 'Start',
        'link': anmeldung_page_link, 'isParent': True,  'isModule': False, 'children': [], "depth": 0})

    def remove_unneccesary_data(module):
        del module['link']
        del module['isParent']
        return module

    vv = walk_modules(vv, remove_unneccesary_data, only_children = False)

    with open('modules.json', 'w+') as f:
        json.dump(vv['children'], f, indent=4)

if __name__ == '__main__':
    get_vv()
