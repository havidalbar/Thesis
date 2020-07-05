import unittest
from main_algorithm.file_utility import read_file_txt, read_file_xlsx
from typing import List


class TestFileUtility(unittest.TestCase):
    def test_read_file_stopword(self):
        test_data_filename: str = 'resources/stopword.txt'
        read_content: str = read_file_txt(test_data_filename)
        self.assertEqual(read_content[:10], 'ada\nadalah')
        read_content: List[str] = read_file_txt(test_data_filename, splitter='\n')
        self.assertEqual(read_content[:2], ['ada', 'adalah'])
        self.assertEqual(len(read_content), 758)

    def test_read_file_quran(self):
        test_data_filename: str = 'resources/quran.xlsx'
        read_content: str = read_file_xlsx(test_data_filename)
        self.assertEqual(read_content.iloc[:1,2].values, 'Dengan menyebut nama Allah Yang Maha Pemurah lagi Maha Penyayang.')
        read_content: List[str] = read_file_xlsx(test_data_filename)
        self.assertEqual(len(read_content), 6236)


if __name__ == '__main__':
    unittest.main()
