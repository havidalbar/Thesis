import os
import pandas as pd
import pickle
from main_algorithm.vector_space_model import VectorSpaceModel
from main_algorithm.fcm import fcm_clustering

def load_model_pickle():
    pickle_filename: str = 'main_algorithm/resources/vector_space_model.pickle'
    # result_model = VectorSpaceModel(7)
    result_data_file = open(pickle_filename, 'rb')
    result_model = pickle.load(result_data_file)
    result_data_file.close()
    # df = pd.DataFrame(result_model.normalisasi2d(result_model.getTfIdf()), columns=result_model.getFeatures())
    # u, partition_coefficient, partition_entropy, list_error_obj, uawal = fcm_clustering(df, debug=False)
    # list_cluster = []
    # for i, u_row in enumerate(u):
    #     max_prob = max(u_row)
    #     for j, uik in enumerate(u_row):
    #         if uik == max_prob:
    #             list_cluster.append(j + 1)
                
    #jika pickle cluster tidak ada
    pickle_filename_cluster = 'main_algorithm/resources/cluster.pickle'
    # cluster_file = open(pickle_filename_cluster, 'wb')
    # pickle.dump(list_cluster, cluster_file)
    # cluster_file.close()
    
    #jika pickle cluster ada
    cluster_file = open(pickle_filename_cluster, 'rb')
    list_cluster = pickle.load(cluster_file)
    cluster_file.close()
        
    return result_model, list_cluster
