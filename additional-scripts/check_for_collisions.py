#!/usr/bin/env python3
import sys
import json
from pprint import pprint
from attrdict import AttrDict
import hashlib

def main():
    root = {'title': 'root', 'children': get_modules()}
    hashes = AttrDict()
    def get_hash(module, parent):
        if 'title' not in module:
            return
        title = module['title']
        if parent and 'title' in parent:
            title += ' ' + parent['title']
        m = hashlib.md5()
        m.update(title.encode('utf-8'))
        h = m.digest()
        if h in hashes:
            print("Collision!\n\t'{}'\n\t'{}'\n".format(title, hashes[h]))
        hashes[h] = title
    walk_modules(root, get_hash)

# Duplication
def walk_modules(module: dict, fn, parent = None):
    if not module:
        return
    fn(module, parent)
    for children in module['children']:
        walk_modules(children, fn, module)

def get_modules(file:str = 'modules.json') -> dict:
    with open(file) as f:
        return json.load(f)

if __name__ == '__main__':
    main()