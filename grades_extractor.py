#!/usr/bin/env python3
import helper
import json

grades = helper.get_grades()

diffs = []
for grade_data in grades:
    grade = grade_data['grade']
    avg = grade_data['avg']
    title = grade_data['title']
    diff = avg - grade
    diffs.append(diff)
    print("grade: {}\tavg: {}\tdiff: {}\t({})".format(grade, round(avg, 2), round(diff, 1), title))

print('\n' * 3)
print('#Courses: {}'.format(len(grades)))
print('avg diff: {}'.format(round(sum(diffs) / len(diffs), 2)))

with open('grades.json', 'w+') as f:
    json.dump(grades, f, indent=4)
