from .preprocessing import Preprocessing
from main_algorithm.file_utility import read_file_txt
from slugify import slugify

class DataModel:
    def __init__(self, nomor_surat: str, nomor_ayat: str, tafsir: str):
        self.nomor_surat: str = nomor_surat
        self.nomor_ayat: str = nomor_ayat
        self.tafsir: str = tafsir
        stopword_path: str = 'resources/stopword.txt'
        read_tafsir: str = read_file_txt(stopword_path, splitter='\n')
        preprocess = Preprocessing(read_tafsir)
        self.cleaned: str = preprocess.cleaning(
            preprocess.case_folding(tafsir))
        self.filtering = preprocess.filtering(
                preprocess.tokenisasi(
                    self.cleaned
                )
            )
        self.preprocessing: str = preprocess.stemming(
            preprocess.filtering(
                preprocess.tokenisasi(
                    preprocess.cleaning(
                        preprocess.case_folding(
                            tafsir)
                    )
                )
            )
        )

    def get_slug(self):
        return slugify(str(self.nomor_surat) + ' ' + str(self.nomor_ayat))

    def get_nomor_surat(self):
        return self.nomor_surat

    def get_nomor_ayat(self):
        return self.nomor_ayat

    def get_tafsir(self):
        return self.tafsir

    def get_cleaned(self):
        return self.cleaned

    def get_preprocessing(self):
        return self.preprocessing
    
    def get_filtering(self):
        return self.filtering

    def asdict(self, output_keys=['nomor_ayat', 'nomor_surat', 'tafsir','cleaned'], cosine=None, cluster=None):
        converter_dict: Dict[str, str] = {
            'slug': self.get_slug(),
            'nomor_ayat': str(self.nomor_ayat),
            'nomor_surat': str(self.nomor_surat),
            'tafsir': str(self.tafsir),
            'cleaned': str(self.cleaned),
            'cosine': cosine,
            'cluster': cluster
        }

        result: Dict[str, str] = {}
        for output_key in output_keys:
            value: str = converter_dict.get(output_key, None)
            if value is not None:
                result[output_key] = value

        return result
