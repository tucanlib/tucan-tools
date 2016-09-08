#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import os
import re
import helper

OUTPUT_DIR = 'output'

grades = helper.get_grades()
available_grades = helper.get_available_grades()

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
    ind = np.array(available_grades)
    width = 0.20
    bars = plt.bar(ind, notenspiegel, width)
    autolabel_bars(bars)
    plt.xticks(0.1 + ind, ind)

    # Nice naming, eh?
    # Color the bar with your grade in green
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
