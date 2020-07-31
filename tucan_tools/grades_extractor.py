#!/usr/bin/env python3
from tucan_tools import helper


def main():
    grades = helper.get_grades(with_notenspiegel=False, force_new=True)

    for grade_data in grades:
        grade = grade_data['grade']
        title = grade_data['title']
        print("{}\t{}".format(grade, title))


if __name__ == '__main__':
    main()
