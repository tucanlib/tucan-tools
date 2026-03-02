import grades_exporter
import json
import os
import argparse
import mechanicalsoup
import getpass
import re
from playwright.sync_api import sync_playwright


current_path = os.path.dirname(os.path.abspath(__file__))
GRADES_JSON = os.path.join(current_path, 'grades.json')
CREDENTIALS_FILE = os.path.join(current_path, 'user-credentials.txt')
BASE_URL = 'https://www.tucan.tu-darmstadt.de'

def get_user_credentials():
    def get_by_file():
        with open(CREDENTIALS_FILE, 'r') as f:
            contents = f.readlines()
            if len(contents) != 2:
                return None
            return {
                "username": contents[0].strip(),
                "password": contents[1].strip()
            }
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

    raise(Exception('Could not retreive username/password. Are you doing this on purpose?'))

def get_grades(with_notenspiegel = True, force_new = False):
    try:
        if not os.path.exists(GRADES_JSON) or force_new:
            grades = grades_exporter.get_grades(with_notenspiegel = with_notenspiegel)
            with open(GRADES_JSON, 'w+') as f:
                json.dump(grades, f, indent=4)
        with open(GRADES_JSON, 'r') as f:
            return json.load(f)
    except:
        raise(Exception('Could not retreive grades. grades.json is malformed or the credentials you\'ve given are wrong - probably'))

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

def log_into_tucan(username, password, browser=mechanicalsoup.Browser(soup_config={"features":"html.parser"})):
    """log into tucan

    This originally used username and password
    with the move to the single sign on portal
    with mandatory 2FA this no longer possible.
    So instead we use playwright to log in and
    then transfer the cookies to mechanicalsoup for further use.
    """
    TARGET_PATTERN = (
        "https://www.tucan.tu-darmstadt.de/scripts/mgrqispi.dll"
        "?APPNAME=CampusNet&PRGNAME=MLSSTART&ARGUMENTS=**"
    )

    with sync_playwright() as p:
        playwright_browser = p.firefox.launch(headless=False)
        context = playwright_browser.new_context()
        page = context.new_page()

        # Start TUCaN login flow
        page.goto("https://www.tucan.tu-darmstadt.de")

        # Wait until redirected to the expected final URL pattern
        page.wait_for_url(TARGET_PATTERN, timeout=180000)  # 3 minutes

        start_url = page.url
        cookies = context.cookies()
        playwright_browser.close()


    browser = mechanicalsoup.Browser(soup_config={"features":"html.parser"})
    browser.session.cookies.update({cookie['name']: cookie['value'] for cookie in cookies})
    start_page = browser.get(start_url)

    return (browser, start_page)
