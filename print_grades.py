#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import grades_exporter

def strip_non_ascii(string):
    stripped = (c for c in string if 0 < ord(c) < 127)
    return ''.join(stripped)

grades = grades_exporter.get_grades(with_notenspiegel = False)
for grade in grades:
    print(strip_non_ascii("{}\t{}".format(grade['grade'], grade['title'])))
