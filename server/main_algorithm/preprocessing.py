import string
from collections import Counter,OrderedDict
from typing import IO, Iterable, List, Set
from main_algorithm.file_utility import read_file_txt
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

class Preprocessing:
    def __init__(self, stopword = 'resources/stopword.txt'):
        stopword_path: str = 'resources/stopword.txt'
        read_content: str = read_file_txt(stopword_path, splitter='\n')
        self.stopwords = read_content
        self.punctuation_list = string.punctuation

    def case_folding(self,source):
        return source.lower()

    def cleaning(self,source):
        source_to_process = source.strip()
        result = ''
        source_last_char_index = len(source_to_process) - 1
        for i, char in enumerate(source_to_process):
            if char in self.punctuation_list or char.isnumeric():
                if i != source_last_char_index:
                    next_char = source_to_process[i + 1]
                    if (next_char not in self.punctuation_list and
                            not next_char.isnumeric() and next_char != ' '):
                        result += ' '
            else:
                result += char

        return result

    def tokenisasi(self,source):
        return source.split()

    def filtering(self,source):
        return [word for word in source if word not in self.stopwords]

    def stemming(self,source):
        factory = StemmerFactory()
        stemmer = factory.create_stemmer()
        return [stemmer.stem(word) for word in source if word and word.isascii()]
    
    def preprocessing(self, data_model):
        raw_document = [doc.get_tafsir() for doc in data_model]
        term = []
        sentences = []
        for sentence in raw_document:
            sentences.append(sentence)
            term.append(
                self.filtering(
                self.stemming(
                    self.filtering(
                        self.tokenisasi(
                            self.case_folding(
                                self.cleaning(sentence)
                            )
                        )
                    )
                )
            )
            )
        return term, sentences