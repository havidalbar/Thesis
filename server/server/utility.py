import os
import pandas as pd
import pickle
from main_algorithm.vector_space_model import VectorSpaceModel
from main_algorithm.fcm import fcm_clustering

def load_model_pickle():
    # pickle_filename: str = 'main_algorithm/resources/explore/albaqarah/filter/klaster/7high/vector_space_model_surah_albaqarah.pickle'
    # pickle_filename: str = 'main_algorithm/resources/explore/almulk/filter/klaster/5high/vector_space_model_surah_almulk.pickle'
    pickle_filename: str = 'main_algorithm/resources/vector_space_model_surah_gabungan.pickle'
    result_data_file = open(pickle_filename, 'rb')
    result_model = pickle.load(result_data_file)
    result_data_file.close()
                
    # pickle_filename_cluster = 'main_algorithm/resources/explore/albaqarah/filter/klaster/7high/clusterSurahAlBaqarah.pickle'
    # pickle_filename_cluster = 'main_algorithm/resources/explore/almulk/filter/klaster/5high/clusterSurahAlMulk.pickle'
    pickle_filename_cluster = 'main_algorithm/resources/clusterSurahGabungan.pickle'
    cluster_file = open(pickle_filename_cluster, 'rb')
    list_cluster = pickle.load(cluster_file)
    cluster_file.close()
        
    return result_model, list_cluster
