import unittest
from main_algorithm.preprocessing import Preprocessing
from typing import List, IO


class TestPreprocessing(unittest.TestCase):
    def setUp(self):
        self.preprocessing: Preprocessing = Preprocessing()

    def test_case_folding(self):
        self.assertEqual(self.preprocessing.case_folding("KECIL!123"), "kecil!123")

    def test_cleaning(self):
        self.assertEqual(self.preprocessing.cleaning('Dengan menyebut nama Allah Yang Maha Pemurah lagi Maha Penyayang.'), 'Dengan menyebut nama Allah Yang Maha Pemurah lagi Maha Penyayang')

    def test_filtering(self):
        my_tokens: List[str] = ['dengan', 'menyebut', 'nama',
                                'Allah', 'yang', 'maha', 'pemurah', 'lagi','maha','penyayang']
        self.assertEqual(self.preprocessing.filtering(my_tokens), [
                         'menyebut', 'nama', 'Allah', 'maha', 'pemurah', 'maha','penyayang'])

    def test_tokenisasi(self):
        my_string: str = 'Dengan menyebut nama Allah Yang Maha Pemurah lagi Maha Penyayang'
        self.assertEqual(self.preprocessing.tokenisasi(my_string), [
                         'Dengan', 'menyebut', 'nama', 'Allah','Yang','Maha','Pemurah','lagi','Maha','Penyayang'])

    def test_stemming(self):
        my_tokens: List[str] = ['menyebut', 'nama',
                                'allah', 'maha', 'pemurah','maha','penyayang']
        self.assertEqual(self.preprocessing.stemming(my_tokens), [
                         'sebut', 'nama', 'allah', 'maha','murah','maha','sayang'])

if __name__ == '__main__':
    unittest.main()
