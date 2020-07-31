#!/usr/bin/env python3
import hashlib
import json
import re

SEARCH_FOR_IN_PARENT = 'Praktika'


def print_module(module, parent, h):
    title = module['title']
    title = re.sub(r'.{2}-.{2}-.{4} ', '', title).strip()
    title = title.replace('(SoSe 2017)', '').strip()
    print("[{1} ({2}CP)](https://davidgengenbach.de/informatik-vv/sose17/?module={0})\n".format(str(h), title,
                                                                                                module['credits']))


def filter(module, parent):
    return SEARCH_FOR_IN_PARENT in parent['title']


def main():
    root = {'title': 'root', 'children': get_modules()}
    filtered = {}
    all_seminars = {}

    def yes(module, parent):
        if not parent or 'title' not in parent:
            return
        title = module['title']
        if parent and 'title' in parent:
            title += '_' + parent['title']
        m = hashlib.md5()
        m.update(title.encode('utf-8'))
        h = m.hexdigest()
        if filter(module, parent):
            seminar_type = parent['title']
            if not seminar_type in all_seminars:
                all_seminars[seminar_type] = []
            all_seminars[seminar_type].append((module, parent, h))

    walk_modules(root, yes)

    for type_name, seminars in all_seminars.items():
        print('## {}'.format(type_name))
        for module, parent, h in seminars:
            print_module(module, parent, h)


# Duplication
def walk_modules(module: dict, fn, parent=None):
    if not module:
        return
    module['parent'] = parent
    fn(module, parent)
    for children in module['children']:
        walk_modules(children, fn, module)


def get_modules(file: str = 'modules.json') -> dict:
    with open(file) as f:
        return json.load(f)


if __name__ == '__main__':
    main()
