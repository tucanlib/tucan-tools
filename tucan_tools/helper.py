import getpass
import json
import os
import re
from os.path import expanduser

import mechanicalsoup

from tucan_tools import grades_exporter

home = expanduser("~")
cache_path = os.path.join(home, '.cache', 'tucan_tools')
config_path = os.path.join(home, '.config', 'tucan_tools')

os.makedirs(cache_path, exist_ok=True)
os.makedirs(config_path, exist_ok=True)

GRADES_JSON = os.path.join(cache_path, 'grades.json')
CREDENTIALS_FILE = os.path.join(config_path, 'credentials.json')
BASE_URL = 'https://www.tucan.tu-darmstadt.de'


def get_user_credentials():
    def get_by_file():
        with open(CREDENTIALS_FILE, 'r') as f:
            credentials = json.load(f)
            if 'username' not in credentials or 'password' not in credentials:
                raise Exception(f'Invalid credentials file ({CREDENTIALS_FILE})')
            return credentials

    def ask_user():
        username = None
        password = None
        while username is None:
            username = input('Tucan Username: ')
        while password is None:
            password = getpass.getpass('Tucan Password: ')
        return {
            "username": username.strip(),
            "password": password.strip()
        }

    def get_from_env_variables():
        password = os.environ.get('TUCAN_TOOLS_PASSWORD', None)
        user = os.environ.get('TUCAN_TOOLS_USER', None)
        if password and user:
            return {
                'username': user,
                'password': password
            }
        else:
            return None

    for strategy_fn in [get_from_env_variables, get_by_file, ask_user]:
        try:
            credentials = strategy_fn()
            if credentials:
                return credentials
        except:
            pass

    raise (Exception('Could not retreive username/password. Are you doing this on purpose?'))


def get_cached_grade():
    with open(GRADES_JSON, 'r') as f:
        return json.load(f)


def get_grades(with_notenspiegel=True, force_new=False):
    try:
        if not os.path.exists(GRADES_JSON) or force_new:
            grades = grades_exporter.get_grades(with_notenspiegel=with_notenspiegel)
            with open(GRADES_JSON, 'w+') as f:
                json.dump(grades, f, indent=4)
        return get_cached_grade()
    except:
        raise (Exception(
            'Could not retreive grades. grades.json is malformed or the credentials you\'ve given are wrong - probably'
        ))


def get_available_grades():
    return [1.0, 1.3, 1.7, 2.0, 2.3, 2.7, 3.0, 3.3, 3.7, 4.0, 5.0]


def get_avg_from_notenspiegel_without_failed(notenspiegel):
    return get_avg_from_notenspiegel(notenspiegel[:-1])


def get_avg_from_notenspiegel(notenspiegel):
    n = [x * get_available_grades()[index] for (index, x) in enumerate(notenspiegel)]
    if sum(notenspiegel) == 0:
        return -1
    return sum(n) / sum(notenspiegel)


def sanitize_title(title):
    # Remove multiple whitespaces
    title = re.sub(r'\s{2,}', ' ', title)
    # Removes the ID from the course and does some sanitation
    title = title.split('<br>')[0].replace('\n', ' ').replace('&nbsp;', ' ').strip()
    return sanitize_title_(title)


def sanitize_title_(title):
    return remove_course_semester(remove_course_nr(title)).strip()


def remove_course_nr(title):
    return re.sub(r'\d{2}-\d{2}-\d{4}(?:-.{2})?', '', title).strip()


def remove_course_semester(title):
    return re.sub(r'\(.*?20.*?\)$', '', title.strip()).strip()


def sanitize_filename(title):
    removestr = ['\t', '\n', '(', ')', ':', '\t', ' ', '/']
    for s in removestr:
        title = title.replace(s, '-')
    return title.lower()


def get_tucan_baseurl():
    return BASE_URL


# ...
def log_into_tucan_():
    credentials = get_user_credentials()
    return log_into_tucan(credentials['username'], credentials['password'])


def log_into_tucan(username, password, browser=mechanicalsoup.Browser(soup_config={"features": "html.parser"})):
    SELECTORS = {
        "LoginUser": '#field_user',
        "LoginPass": '#field_pass',
        "LoginForm": '#cn_loginForm'
    }

    def get_redirection_link(page):
        return BASE_URL + page.soup.select('a')[2].attrs['href']

    browser = mechanicalsoup.Browser(soup_config={"features": "html.parser"})
    login_page = browser.get(BASE_URL)
    # HTML redirects, because why not
    login_page = browser.get(get_redirection_link(login_page))
    login_page = browser.get(get_redirection_link(login_page))
    login_form = login_page.soup.select(SELECTORS['LoginForm'])[0]

    login_form.select(SELECTORS['LoginUser'])[0]['value'] = username
    login_form.select(SELECTORS['LoginPass'])[0]['value'] = password

    login_page = browser.submit(login_form, login_page.url)
    redirected_url = "=".join(login_page.headers['REFRESH'].split('=')[1:])

    start_page = browser.get(BASE_URL + redirected_url)
    start_page = browser.get(get_redirection_link(start_page))
    return browser, start_page
