# coding=utf-8
import sys
import os

from lxml.etree import XMLParser

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import unittest
import shutil

from lxml import etree as et

from inject_python_interpreter import inject_python_interpreter
from inject_run_configurations import inject_run_configurations


class TestInjection(unittest.TestCase):

    @classmethod
    def project_dir(cls, *args):
        current_path = os.path.dirname(__file__)
        project_path = os.path.join(current_path, '../../../../../../../')
        project_path = os.path.abspath(project_path)
        return os.path.join(project_path, *args)

    @classmethod
    def tmp_dir(cls, *args):
        return cls.project_dir('deployment/ansible/tmp/', *args)

    @classmethod
    def sample_dir(cls, *args):
        return cls.project_dir(
            'deployment/ansible/development/roles/pycharm/files/test/sample',
            *args)

    @classmethod
    def elements_equal(cls, e1, e2):
        if e1.tag != e2.tag:
            return False
        if e1.text != e2.text:
            return False
        if e1.tail != e2.tail:
            return False
        if e1.attrib != e2.attrib:
            return False
        if len(e1) != len(e2):
            return False
        return all(cls.elements_equal(c1, c2) for c1, c2 in zip(e1, e2))

    def test_inject_python_interpreter(self):
        """Test injection working as expected."""
        sample_file = self.sample_dir('jdk.table.xml')
        temp_file = self.tmp_dir('jdk.table.xml')
        shutil.copy(sample_file, temp_file)

        injected_interpreter = self.sample_dir('geonode-celery.xml')
        self.assertEqual(
            inject_python_interpreter(temp_file, injected_interpreter),
            0)

        control_file = self.sample_dir('modified-jdk.table.xml')

        parser = XMLParser(remove_blank_text=True)

        self.assertTrue(
            self.elements_equal(
                et.parse(temp_file, parser).getroot(),
                et.parse(control_file, parser).getroot()))

    def test_inject_run_configurations(self):
        """Test injection working as expected."""
        sample_file = self.sample_dir('workspace.xml')
        temp_file = self.tmp_dir('workspace.xml')
        shutil.copy(sample_file, temp_file)

        injected_configurations = self.sample_dir(
            'workspace-configuration.xml')
        self.assertEqual(
            inject_run_configurations(temp_file, injected_configurations),
            0)

        control_file = self.sample_dir('modified-workspace.xml')

        parser = XMLParser(remove_blank_text=True)

        self.assertTrue(
            self.elements_equal(
                et.parse(temp_file, parser).getroot(),
                et.parse(control_file, parser).getroot()))
