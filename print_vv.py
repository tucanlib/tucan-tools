#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import helper
import sys

search_for_professor = sys.argv[1] if len(sys.argv) > 1 else None

with open('modules.json', 'r+') as f:
    vv = json.load(f)

def get_professor(module):
    if 'details' not in module:
        return None
    for detail in module['details']:
        if 'Modulverantwortliche' in detail['title']:
            return detail['details']


def print_module(module, depth):
    title = helper.sanitize_title_(module['title'])
    prefix = '  ' * depth
    print("{}{}".format(prefix, title))
    for m in module['children']:
        print_module(m, depth + 1)

def traverse_modules(module, fn):
    fn(module)
    if 'children' in module:
        for child in module['children']:
            traverse_modules(child, fn)

if search_for_professor is not None:
    print("Searching for professor: {}\n".format(search_for_professor))
    def it(item):
        professor = get_professor(item)
        if professor is not None and search_for_professor.lower() in professor.lower():
            print("{:<40}\n\t{}\n".format(item['title'], professor))
    for module in vv:
        traverse_modules(module, it)
else:
    for module in vv:
        print_module(module, 0)

