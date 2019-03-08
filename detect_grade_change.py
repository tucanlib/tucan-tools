#!/usr/bin/env python3

import os
import notify2
import datetime
from glob import glob
from time import time
import sys


def get_args():
    import argparse
    parser = argparse.ArgumentParser(description='desc')
    parser.add_argument('--grades_path', type=str, default='grades')
    parser.add_argument('--keep_grades', type=int, default=20)
    args = parser.parse_args()
    return args


def main():
    args = get_args()
    import helper

    grades = helper.get_grades(False, force_new=True)
    os.makedirs(args.grades_path, exist_ok=True)
    last = get_last_grades(args.grades_path)
    current = write_grades(grades, args.grades_path)
    diff = [x for x in current.splitlines() if x not in last.splitlines()]
    if len(diff):
        show_notification('TuCan Grades changed', '\n'.join(diff))

    files = sorted(glob(args.grades_path + '/*.txt'))
    if len(files) > args.keep_grades:
        for file in files[:-args.keep_grades]:
            os.remove(file)


def get_timestamp():
    return datetime.datetime.fromtimestamp(time()).strftime('%Y%m%d__%H_%M_%S')


def get_filename(grades_path):
    return '{}/{}.txt'.format(grades_path, get_timestamp())


def get_last_grades(grades_path):
    files = sorted(glob(grades_path + '/*.txt'))
    if not len(files):
        return ''

    with open(files[-1]) as f:
        return f.read()


def write_grades(grades, grades_path):
    current = ''
    with open(get_filename(grades_path), 'w') as f:
        for grade_data in grades:
            grade = grade_data['grade']
            title = grade_data['title']
            s = "{}\t{}\n".format(grade, title.encode('utf-8'))
            current += s
            f.write(s)
    return current


def show_notification(title, description):
    notify2.init('TuCan Grades')
    n = notify2.Notification(title, description)
    n.show()


if __name__ == '__main__':
    main()
