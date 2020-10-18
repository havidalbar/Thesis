import os
import pickle
import pandas as pd
import time
import json
import numpy as np
from main_algorithm.file_utility import read_file_txt, read_file_xlsx
from main_algorithm.preprocessing import Preprocessing
from main_algorithm.output import Output
from collections import OrderedDict, Counter
from main_algorithm.vector_space_model import VectorSpaceModel
from main_algorithm.fcm import fcm_clustering, silhouette
from typing import Dict, List, Set


if __name__ == '__main__':
    mulai = time.time()
    # file_name = "resources/results-4-gabungan"
    # full_file = open(f"{file_name}.json")
    # full_data = json.loads(full_file.read())
    # print(full_data['count_all_term'])
    # lists = sorted(full_data['count_all_term'].items())
    # x, y = zip(*lists)
    # plt.plot(x, y)
    # plt.show()
    # query = 'Sembah Allah Allah'
    # pickle_filename: str = 'resources/vector_space_model_surah_cek.pickle'
    # pickle_filename_cluster = 'resources/clusterSurahCek.pickle'
    # cluster_file = open(pickle_filename_cluster, 'rb')
    # list_cluster = pickle.load(cluster_file)
    # cluster_file.close()
    # result_data_file = open(pickle_filename, 'rb')
    # weight = pickle.load(result_data_file)
    # result_data_file.close()
    # df = pd.DataFrame(weight.normalisasi2d(weight.getTfIdf()), columns=weight.getFeatures())
    # df['klaster'] = list_cluster
    # evaluator_result = weight.indexing(query, list_cluster)
    # print(evaluator_result)
    # count_cluster = Counter(list_cluster)
    # print(count_cluster)
    # df = df.sort_values(by=['klaster'])
    # silo = silhouette(df)
    # print(list_cluster)
    print("Eksekusi Selama",time.time()-mulai)