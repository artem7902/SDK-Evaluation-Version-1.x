import os
import sys
import unittest
from dicttoxml import dicttoxml

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tests.TestConfig import config
from Glasswall import Glasswall

PATH_TO_LIB           = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))) + "/Lib/libglasswall.classic.so"
TEST_FILE_PATH        = os.path.dirname(os.path.abspath(__file__)) + "/test_data/test-doc-file.doc"
TEST_FILE_OUTPUT_PATH = os.path.dirname(os.path.abspath(__file__)) + "/test_data/test-doc-file-output.doc"


class TestStringMethods(unittest.TestCase):

    def setUp(self):
        self._glasswall = Glasswall(PATH_TO_LIB)
        self.xml_config = dicttoxml(obj=config, custom_root="config", attr_type=False).decode("utf-8")
        try:
            set_config_result = self._glasswall.GWFileConfigXML(self.xml_config)
            if set_config_result.returnStatus !=1:
                raise Exception('Error has been raised during set config operation {}'.format(set_config_result.returnStatus))
        finally:
            self._glasswall.GWFileDone()

    def test_file_protect(self):
        file_path = TEST_FILE_PATH
        file_type = 'doc'
        try:
            gw_engine_response = self._glasswall.GWFileProtect(file_path, file_type)
        finally:
            self._glasswall.GWFileDone()
        self.assertEqual(gw_engine_response.returnStatus, 1)

    def test_file_protect_lite(self):
        file_path = TEST_FILE_PATH
        file_type = 'doc'
        try:
            gw_engine_response = self._glasswall.GWFileProtectLite(file_path, file_type)
        finally:
            self._glasswall.GWFileDone()
        self.assertEqual(gw_engine_response.returnStatus, 1)

    def test_file_to_file_protect(self):
        file_path   = TEST_FILE_PATH
        output_path = TEST_FILE_OUTPUT_PATH
        file_type   = 'doc'
        try:
            gw_engine_response = self._glasswall.GWFileToFileProtect(file_path, file_type, output_path)
        finally:
            self._glasswall.GWFileDone()
        self.assertEqual(gw_engine_response.returnStatus, 1)
        self.assertTrue(os.path.isfile(output_path))

    def test_file_to_file_protect_lite(self):
        file_path   = TEST_FILE_PATH
        output_path = TEST_FILE_OUTPUT_PATH
        file_type   = 'doc'
        try:
            gw_engine_response = self._glasswall.GWFileToFileProtectLite(file_path, file_type, output_path)
        finally:
            self._glasswall.GWFileDone()
        self.assertEqual(gw_engine_response.returnStatus, 1)
        self.assertTrue(os.path.isfile(output_path))

    def test_file_protect_and_report(self):
        file_path   = TEST_FILE_PATH
        file_type   = 'doc'
        try:
            gw_engine_response = self._glasswall.GWFileProtectAndReport(file_path, file_type)
        finally:
            self._glasswall.GWFileDone()
        self.assertEqual(gw_engine_response.returnStatus, 1)


    def test_memory_to_memory_protect(self):
        file      = open(TEST_FILE_PATH, "rb")
        file_type = 'doc'
        bytes     = file.read()
        try:
            gw_engine_response = self._glasswall.GWMemoryToMemoryProtect(bytes, file_type)
        finally:
            self._glasswall.GWFileDone()
        self.assertEqual(gw_engine_response.returnStatus, 1)

    def tearDown(self) -> None:
        try:
            os.remove(TEST_FILE_OUTPUT_PATH)
        except:
            pass