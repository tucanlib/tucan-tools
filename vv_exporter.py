#!/usr/bin/env python3

import re
import json
import helper
import warnings
from bs4 import BeautifulSoup

warnings.simplefilter('ignore', UserWarning)

# These links are problematic because they contain links to the whole VV of all departments of the TU Darmstadt. If all the VVs would be crawled, the crawl time need would be very high.
# Also these links contain links that are recursive (it would crawl the
# VVs again and again and again and again and again and again and ...)
BLACKLIST = (
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


def main():
    (browser, page) = helper.log_into_tucan_()
    vv = get_vv(browser, page, helper.get_tucan_baseurl())
    with open('modules.json', 'w+') as f:
        json.dump(vv, f, indent=4, sort_keys = True)


def details_from_element(element):
    link = element.find('a')
    title = link.text.strip()
    link = BASE_URL + link.attrs['href']
    return {
        'title': title,
        'link': link,
        'isParent': "PRGNAME=REGISTRATION" in link,
        'isModule': "PRGNAME=MODULEDETAILS" in link,
        'children': []
    }


def get_table_with_caption(tables, caption):
    for table in tables:
        if caption in table.select('caption')[0].text:
            return table
    return None


def get_links_of_table_with_caption(page, caption):
    tables = page.select('table.tb')
    table = get_table_with_caption(tables, caption)
    if not table:
        return
    return set(BASE_URL + x.attrs['href'] for x in table.select('tr a'))


def extract_rooms_and_times_of_module(course_page):
    tables = course_page.select('table.tb')
    table = get_table_with_caption(tables, 'Termine')
    if not table:
        return
    for link in table.select('a'):
        link.attrs['href'] = ''
    return table


def get_all_links(page):
    SELECTOR = '#pageContent ul li, #pageContent table tr'
    links = [details_from_element(x) for x in page.soup.select(
        SELECTOR) if x.text.strip() not in BLACKLIST and len(x.select('a')) > 0]
    return links

# ....


def sanitize_detail(detail):
    replacements = [
        ('\t', ''),
        ('<br/>', '\n'),
        ('\n', '<br/>'),
        (':', '\b'),
        ('\b', ':'),
        ('\r', ''),
        ('////', '<br/>')
    ]

    reg_replacements = [
        (r'^:', ''),
        (r']$', ''),
        (r'(<br\/>)*$', ''),
        (r'^(<br\/>)*', ''),
        (r'\s{2,}', ''),
        (r'(<br\/>)*$', '')
    ]

    detail_text = detail['details'].replace('<br/>', '////')
    detail_text = BeautifulSoup(detail_text, "html.parser").text
    detail['title'] = detail['title'].replace(':', '').strip()

    for r in replacements:
        detail_text = detail_text.replace(r[0], r[1]).strip()

    for r in reg_replacements:
        detail_text = re.sub(r[0], r[1], detail_text).strip()

    detail['details'] = detail_text
    return detail


def extract_module_details(html, browser):
    details_raw = html.select('#pageContent table:nth-of-type(1) .tbdata td')
    details = [sanitize_detail({"title": x.split('</b>')[0].strip(), "details": x.split('</b>')[1].strip()})
               for x in str(details_raw).split('<b>')[1:]]

    # Extract the appointments and rooms of the module
    # TODO cleanup
    try:
        links = get_links_of_table_with_caption(html, 'Kurse')
        kurse_pages = [browser.get(link).soup for idx, link in enumerate(links)]
        kurs_appointments = [extract_rooms_and_times_of_module(x) for x in kurse_pages][-1]
        if len(kurs_appointments.select('tr')) > 2:
            details.append({'title': 'Kurstermine', 'details': str(kurs_appointments)})
    except Exception as e:
        print('(Could not extract Kurstermine) - {}'.format(e))
    return details


def extract_cp(link):
    for detail in link['details']:
        if 'Credits' in detail['title']:
            cp = detail['details'].split(',')[0]
            try:
                cp = int(cp)
            except:
                pass
            return cp
    return 0


def print_link(link):
    print(('\t' * link['depth']) + '> {}'.format(link['title']))


def crawl(browser, link):
    # If it's a parent module, crawl it's children
    if link['isParent']:
        print_link(link)
        page = browser.get(link['link'])
        # Only go through all links that are parents or modules (there are other links in the page, too)
        for l in [x for x in get_all_links(page) if x['isParent'] or x['isModule']]:
            l['depth'] = link['depth'] + 1
            link['children'].append(crawl(browser, l))
    # If it's a normal module (= Kurs), extract the data from the module page
    elif link['isModule']:
        module_page = browser.get(link['link'])
        link['details'] = extract_module_details(module_page.soup, browser)
        link['credits'] = extract_cp(link)
        print_link(link)
    return link


def walk_modules(vv, fn, only_children=True):
    if len(vv['children']) == 0 or not only_children:
        vv = fn(vv)
    for child in vv['children']:
        child = walk_modules(child, fn, only_children)
    return vv


def get_vv(browser, start_page, base_url):
    # anmeldung page
    anmeldung_page_link = base_url + start_page.soup.select('li[title="Anmeldung"] a')[0].attrs['href']

    vv = crawl(browser, {
        'title': 'Start',
        'link': anmeldung_page_link,
        'isParent': True,
        'isModule': False,
        'children': [],
        "depth": 0}
    )

    def remove_unneccesary_data(module):
        for e in ['link', 'isParent', 'depth', 'isModule']:
            del module[e]
        return module
    vv = walk_modules(vv, remove_unneccesary_data, only_children=False)
    return vv['children']

if __name__ == '__main__':
    main()
