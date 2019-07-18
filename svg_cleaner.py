#!/bin/python3
import sys
import os
import xml.etree.ElementTree as ET

if 2 != len(sys.argv):
    print('Usage: python3 ./svg_cleaner.py [svg_file]')
    sys.exit(1)

filename = sys.argv[1]

if not os.path.isfile(filename):
    print('file %s not found', filename)
    sys.exit(2)

tree = ET.parse(filename)
root = tree.getroot()

def clean_namespaces(element: ET.Element):
    for child in list(element):
        clean_namespaces(child)
    if -1 != element.tag.find('}'):
        element.tag = element.tag.split('}')[1]
    new_attrib = {}
    for attr in element.attrib:
        if -1 != attr.find('}'):
            new_attr = attr.split('}')[1]
        else:
            new_attr = attr
            new_attrib[new_attr] = element.attrib[attr]
    element.attrib = new_attrib

clean_namespaces(root)
tree.write('output.svg')
