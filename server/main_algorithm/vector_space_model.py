import math
import pickle
import numpy as np
from collections import OrderedDict, Counter
from main_algorithm.data_model import DataModel
from main_algorithm.preprocessing import Preprocessing
from main_algorithm.file_utility import read_file_xlsx

class VectorSpaceModel:
    def __init__(self, n_ayat, pickle_filename: str = 'resources/vector_space_model_surah_gabungan.pickle'):
        self.documents = []
        self.features = []
        self.tf = [[]]
        self.idf = []
        self.tf_idf = [[]]
        self.data_model = self.extract_documents(n_ayat)
        self.result_model = None
        self.data_model_output = None
        self.data_clustering = None
        self.list_doc_output = None
        vsm_model_file = open(pickle_filename, 'wb')
        pickle.dump(self, vsm_model_file)
        vsm_model_file.close()

    def extract_documents(self, n_ayat):
        result: List[DataModel] = []
        alquran_path: str = 'resources/surahGabungan.xlsx'
        sentences: str = read_file_xlsx(alquran_path)
        for i, element in enumerate(sentences.iloc[0:n_ayat, :3].values):
            result.append(
                DataModel(sentences.iloc[i][0], sentences.iloc[i][1], sentences.iloc[i][2]))
        self.weighting(result)
        return result

    def setText(self, source):
        self.documents = source

    def getFeatures(self):
        self.features = list(OrderedDict(
            (word, None) for document in self.documents for word in document).keys())
        return self.features

    def getTf(self):
        self.tf = [[document.count(feature) for document in self.documents]
                   for feature in self.getFeatures()]
        return self.tf
    
    def getDf(self):
        self.df = [sum(1 for tf in termTfs if tf > 0) for termTfs in self.getTf()]
        return self.df

    def getIdf(self):
        self.idf = [math.log10(
            len(termTfs) / sum(1 for tf in termTfs if tf > 0)) for termTfs in self.getTf()]
        return self.idf

    def getTfIdf(self):
        self.tf_idf = [
            [(1 + math.log10(tf)) * idf if tf > 0 else tf for tf in termTfs]
            for termTfs, idf in zip(self.getTf(), self.getIdf())
        ]
        return self.tf_idf

    def weighting(self, data_model):
        pre = Preprocessing()
        term, sentences = pre.preprocessing(data_model)
        self.setText([sentence for sentence in term])

    def normalisasi2d(self, weighting_2d_array):
        transposed_weighting_2d_array = [
            [weighting_2d_array[j][i]
                for j in range(len(weighting_2d_array))]
            for i in range(len(weighting_2d_array[0]))
        ]

        for i, row in enumerate(transposed_weighting_2d_array):
            divider = math.sqrt(sum([math.pow(element, 2) for element in row]))
            transposed_weighting_2d_array[i] = [
                element / divider for element in row]

        return transposed_weighting_2d_array

    def indexing(self, query, cluster):
        query_vocab = []
        for word in query.lower().split():
            if word not in query_vocab:
                query_vocab.append(word)

        query_wc = [query.lower().split().count(word) for word in query_vocab]
        tf_idf = self.normalisasi2d(self.getTfIdf())
        list_index = [self.getFeatures().index(word)
                                       for word in query_vocab if word in self.getFeatures()]
        relevance_scores = {}
        for doc_id in range(len(self.data_model)):
            cosine = 0
            for idx, idx_word in enumerate(list_index):
                cosine += query_wc[idx] * tf_idf[doc_id][idx_word]
            relevance_scores[doc_id] = cosine
        sorted_value = OrderedDict(
            sorted(relevance_scores.items(), key=lambda x: x[1], reverse=True))
        top_all = {k: sorted_value[k] for k in list(
            sorted_value)[:len(self.data_model)]}
        temp = {k: v for k, v in sorted(
            top_all.items(), key=lambda item: item[0])}
        temp_data_model = []
        temp_cosine = []
        temp_result_model = []
        temp_cluster = []
        self.data_clustering = temp
        for key, value in temp.items():
            temp_data_model.append(self.data_model[key])
            if value != 0.0:
                temp_result_model.append(self.data_model[key])
                temp_cosine.append(value)
                temp_cluster.append(cluster[key])
        list_doc_sort = np.column_stack((temp_result_model, temp_cosine, temp_cluster))
        list_doc_sort = np.array(sorted(list_doc_sort, key=lambda item: item[1], reverse=True))
        self.result_model = [[doc[0] for doc in list_doc_sort], [doc[1] for doc in list_doc_sort], [doc[2] for doc in list_doc_sort]]
        self.data_model_output = temp_data_model
        return self.result_model

    def get_result_documents(self):
        return self.result_model
    
    def get_data_model_output(self):
        return self.data_model_output
    
    def get_data_clustering(self):
        return self.data_clustering
    
    def get_doc_output(self):
        return self.list_doc_output

    def calculateTermInSameCluster(self, list_cluster):
        temp_cosine = []
        temp_data_model = []
        for key, value in self.data_clustering.items():
            temp_data_model.append(self.data_model[key])
            temp_cosine.append(value)
        list_doc_sort = np.column_stack((temp_data_model, temp_cosine, list_cluster))
        list_doc_sort = sorted(list_doc_sort, key=lambda item: item[1], reverse=True)
        self.list_doc_output = list_doc_sort
        dict_doc_sort = []
        for doc in list_doc_sort:
            dict_doc_sort.append({"cluster": doc[2], "term": doc[0].get_preprocessing()})
        feature_list = []
        cluster_counters = dict()

        for doc in dict_doc_sort:
            if cluster_counters.get(doc["cluster"]) == None:
                cluster_counters[doc["cluster"]] = Counter()

            cluster_counters[doc["cluster"]] += Counter(doc["term"])
            feature_list.append(doc["term"])
        feature_counters = Counter(np.hstack(feature_list))

        result = dict()
        for keys, element in cluster_counters.items():
            counter_temp = element + feature_counters
            for key in counter_temp.keys():
                counter_temp[key] = element.get(key, 0) / feature_counters.get(key, 0)
            result[keys] = counter_temp

        return result
    
    def get_document_by_slug(self, slug: str):
        for doc in self.data_model:
            if doc.get_slug() == slug:
                return doc

        return None
