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

def get_grades():
    BASE_URL = helper.get_tucan_baseurl()

    # Lasciate ogni speranza, oh voi ch'entrate
    (browser, start_page) = helper.log_into_tucan_()

    # Prüfungsergebnisse page
    ergebnisse_page_link = BASE_URL + start_page.soup.select('li[title="Leistungsspiegel"] a')[0].attrs['href']
    ergebnisse_page = browser.get(ergebnisse_page_link)
    print(ergebnisse_page.soup)

if __name__ == '__main__':
    get_grades()