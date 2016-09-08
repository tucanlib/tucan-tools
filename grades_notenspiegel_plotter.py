#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import json
import os
import re
import helper

OUTPUT_DIR = 'output'

grades = helper.get_grades()

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def autolabel_bars(rects):
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width()/2., 0.5 + height,
                '%d' % int(height),
                ha='center', va='bottom')

def sanitize_title_for_filename(title):
    title = title.replace(' ', '-').replace(':', '-').lower()
    return title

def print_notenspiegel_plot(grade):
    plt.cla()
    plt.clf()
    plt.style.use('seaborn-whitegrid')

    title = grade['title']
    sanitized_title = sanitize_title_for_filename(title)
    notenspiegel = grade['notenspiegel']
    ind = np.arange(len(notenspiegel))
    ind = np.array([1.0, 1.3, 1.7, 2.0, 2.3, 2.7, 3.0, 3.3, 3.7, 4.0, 5.0])
    width = 0.20
    bars = plt.bar(ind, notenspiegel, width)
    autolabel_bars(bars)
    plt.xticks(0.1 + ind, ind)

    # Nice naming, eh?
    for (index, grade_) in enumerate(ind):
        if grade['grade'] == grade_:
            bars[index].set_color('g')

    plt.xlabel("grades")
    plt.ylabel("# students")

    plt.tick_params(
        axis='both',
        which='both',
        top='off',
        left='off',
        labelleft='off',
        right='off'
    )
    plt.grid(False)
    plt.title(title, loc='left')
    plt.savefig('{}/{}.png'.format(OUTPUT_DIR, sanitized_title))

for grade in grades:
    print_notenspiegel_plot(grade)