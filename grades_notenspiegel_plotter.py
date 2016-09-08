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
        plt.text(rect.get_x() + rect.get_width()/2., 1.02 * height,
                '%d' % int(height),
                ha='center', va='bottom')

def get_notenspiegel_index(grade):
    for (index, grade_) in enumerate(available_grades):
        if grade == grade_:
            return index
    return -1

def plot_notenspiegel(title, notenspiegel):
    plt.cla()
    plt.clf()
    plt.style.use('seaborn-whitegrid')

    sanitized_title = helper.sanitize_filename(title)
    ind = np.arange(len(notenspiegel))
    ind = np.array(available_grades)
    width = 0.20
    bars = plt.bar(ind, notenspiegel, width)
    autolabel_bars(bars)
    plt.xticks(0.1 + ind, ind)

    # Nice naming, eh?
    # Color the bar with your grade in green
    notenspiegel_index = get_notenspiegel_index(grade['grade'])
    if notenspiegel_index != -1:
        bars[notenspiegel_index].set_color('g')

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

def create_notenspiegel_plot(grade):
    plot_notenspiegel(grade['title'], grade['notenspiegel'])

for grade in grades:
    create_notenspiegel_plot(grade)


notenspiegel = [0] * len(available_grades)
for grade in grades:
    grade_ = grade['grade']
    notenspiegel_index = get_notenspiegel_index(grade['grade'])
    if notenspiegel_index != -1:
        notenspiegel[notenspiegel_index] = notenspiegel[notenspiegel_index] + 1

plot_notenspiegel('_NOTENSPIEGEL', notenspiegel)
