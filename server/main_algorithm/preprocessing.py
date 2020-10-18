import string
from main_algorithm.file_utility import read_file_txt
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

class Preprocessing:
    def __init__(self, stopword = 'resources/stopword.txt'):
        stopword_path: str = 'resources/stopword.txt'
        read_content: str = read_file_txt(stopword_path, splitter='\n')
        self.stopwords = read_content

    def case_folding(self,source):
        return source.lower()

    def cleaning(self,source):
        punctuation_list = string.punctuation
        source = source.strip()
        result = ''
        source_last_char_index = len(source) - 1
        for i, char in enumerate(source):
            if char in punctuation_list:
                if i != source_last_char_index:
                    next_char = source[i + 1]
                    if (next_char not in punctuation_list and next_char != ' '):
                        result += ' '
            else:
                result += char

        return result

    def tokenization(self,source):
        return source.split()

    def filtering(self,source):
        return [word for word in source if word not in self.stopwords]

    def stemming(self,source):
        factory = StemmerFactory()
        stemmer = factory.create_stemmer()
        return [stemmer.stem(word) for word in source if word.isascii()]
    
    def preprocessing(self, data_model):
        raw_document = [doc.get_tafsir() for doc in data_model]
        term = []
        sentences = []
        for sentence in raw_document:
            sentences.append(sentence)
            term.append(
                self.stemming(
                    self.filtering(
                        self.tokenization(
                            self.cleaning(
                                self.case_folding(sentence)
                        )
                    )
                )
            )
            )
        return term, sentences