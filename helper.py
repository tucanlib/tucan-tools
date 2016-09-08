import grades_exporter
import json
import os

GRADES_JSON = 'grades.json'

def get_grades():
    try:
        if not os.path.exists(GRADES_JSON):
            grades = grades_exporter.get_grades()
            with open(GRADES_JSON, 'w+') as f:
                json.dump(grades, f, indent=4)

        with open(GRADES_JSON, 'r') as f:
            return json.load(f)
    except:
        raise(Exception('Could not retreive grades. grades.json is malformed or the credentials you\'ve are wrong - probably'))

def get_available_grades():
    return [1.0, 1.3, 1.7, 2.0, 2.3, 2.7, 3.0, 3.3, 3.7, 4.0, 5.0]

def get_avg_from_notenspiegel_without_failed(notenspiegel):
    return get_avg_from_notenspiegel(notenspiegel[:-1])

def get_avg_from_notenspiegel(notenspiegel):
    n = [x * get_available_grades()[index] for (index, x) in enumerate(notenspiegel)]
    return sum(n) / sum(notenspiegel)

def sanitize_filename(title):
    title = title.replace(' ', '-').replace(':', '-').lower()
    return title