import grades_exporter
import json
import os

def get_grades():
    if not os.path.exists('grades.json'):
        grades_exporter.export()
    with open('grades.json', 'r') as f:
        return json.load(f)

