import unittest
from main_algorithm.data_model import DataModel


class TestDataModel(unittest.TestCase):

    def setUp(self):
        self.data_model = DataModel('1','12','Ini terjemahan1.')

    def test_should_get_nomor_surat(self):
        self.assertEqual(self.data_model.get_nomor_surat(), '1')

    def test_should_get_nomor_ayat(self):
        self.assertEqual(self.data_model.get_nomor_ayat(), '12')

    def test_should_get_raw_text(self):
        self.assertEqual(self.data_model.get_content(),'Ini terjemahan1.')

    def test_should_get_cleaned(self):
        self.assertEqual(self.data_model.get_cleaned(),'ini terjemahan')

    def test_should_get_tokens(self):
        self.assertEqual(self.data_model.get_tokens(),['ini','terjemahan'])

    def test_should_get_preprocess(self):
        self.assertEqual(self.data_model.get_preprocessing(),['terjemah'])

if __name__ == '__main__':
    unittest.main()
