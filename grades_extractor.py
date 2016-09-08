#!/usr/bin/env python3
import helper

grades = helper.get_grades()

diffs = []
diffs_without_failed = []
for grade_data in grades:
    grade = grade_data['grade']
    if grade == 5.0:
        continue
    avg = helper.get_avg_from_notenspiegel(grade_data['notenspiegel'])
    if avg <= 0:
        continue
    avg_without_failed = helper.get_avg_from_notenspiegel_without_failed(grade_data['notenspiegel'])
    title = grade_data['title']
    diff = avg - grade
    diff_without_failed = avg_without_failed - grade
    diffs.append(diff)
    diffs_without_failed.append(diff_without_failed)
    print("grade: {}\tavg: {}\tdiff: {}\tdiff without 5,0: {}\t\t({})".format(grade, round(avg, 2), round(diff, 1), round(diff_without_failed, 1), title))

def get_diff_avg_for_notenspiegel(diffs):
    return sum(diffs) / len(diffs)

print('\n' * 3)
print('#Courses: {}'.format(len(grades)))

avg_of_diff_to_avgs = get_diff_avg_for_notenspiegel(diffs)
avg_of_diff_to_avgs_without_failed = get_diff_avg_for_notenspiegel(diffs_without_failed)

print('avg diff: {}'.format(round(avg_of_diff_to_avgs, 2)))
print('avg diff without failed: {}'.format(round(avg_of_diff_to_avgs_without_failed, 2)))
