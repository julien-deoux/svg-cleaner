#!/bin/python3
import sys
import os
import getopt
import xml.etree.ElementTree as ET

HELP = '''Usage: python3 ./svg_cleaner.py (-a | --angular) [SVG_FILE]
Options :
    -h, --help                  Prints this help message
    -a, --angular               Enables Angular mode (removes flow* tags)'''

# Arguments par défaut
angular_mode = False

# Récupération des options
try:
    opts, args = getopt.getopt(sys.argv[1:], 'ah', ['--angular', '--help'])
except getopt.GetoptError:
    print(HELP)
    sys.exit(1)
for opt, arg in opts:
    if opt in ('-a', '--angular'):
        angular_mode = True
    if opt in ('-h', '--help'):
        print(HELP)
        sys.exit(0)
if len(args) >= 1:
    filename = os.path.abspath(args[0])
    args = args[1:]
else:
    print(HELP)
    sys.exit(1)

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

def clean_flow(element: ET.Element, parent: ET.Element):
    if element.tag.startswith('flow'):
        parent.remove(element)
    else:
        for child in list(element):
            clean_flow(child, element)

clean_namespaces(root, None)
clean_invisibles(root, None)
if angular_mode:
    clean_flow(root, None)
tree.write(sys.stdout.buffer)
print()
