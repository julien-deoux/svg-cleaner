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

def clean_namespaces(element: ET.Element, parent: ET.Element):
    for child in list(element):
        clean_namespaces(child, element)
    new_attrib = {}
    for attr in element.attrib:
        if -1 == attr.find(':'):
            new_attrib[attr] = element.attrib[attr]
    element.attrib = new_attrib
    if -1 != element.tag.find('}'):
        parts = element.tag.split('}')
        if '{http://www.w3.org/2000/svg' == parts[0]:
            element.tag = parts[1]
        else:
            parent.remove(element)

def clean_invisibles(element: ET.Element, parent: ET.Element):
    if 'style' in element.attrib and element.attrib['style'] == "display:none":
        parent.remove(element)
    else:
        for child in list(element):
            clean_invisibles(child, element)

clean_namespaces(root, None)
clean_invisibles(root, None)
tree.write('output.svg')
