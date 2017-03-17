#!/usr/local/bin/python
# coding=utf-8
import sys
from xml.etree import ElementTree as et

__author__ = 'Rizky Maulana Nugraha <lana.pcfre@gmail.com>'


workspace_filename = sys.argv[1]

tree = et.parse(workspace_filename)

# find run configuration
component_index = None
component_element = None

for index, child in enumerate(tree.findall('component')):
    child_is_run_manager = child.attrib['name'] == 'RunManager'
    if child_is_run_manager:
        component_index = index
        component_element = child
        break
else:
    print 'Not Found'

if component_index:
    root = tree.getroot()
    root.remove(component_element)

    injected_workspace_filename = sys.argv[2]

    injected_subtree = et.parse(injected_workspace_filename)
    injected_component = injected_subtree.getroot()

    root.insert(component_index, injected_component)

tree.write(workspace_filename)
