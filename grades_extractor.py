#!/usr/bin/env python3
import helper

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
# you like?
avg_of_diff_to_avgs = sum(diffs) / len(diffs)
print('avg diff: {}'.format(round(avg_of_diff_to_avgs, 2)))
