import os
import pickle
import pandas as pd
import time
from main_algorithm.file_utility import read_file_txt, read_file_xlsx
from main_algorithm.preprocessing import Preprocessing
from main_algorithm.output import Output
from main_algorithm.vector_space_model import VectorSpaceModel
from main_algorithm.fcm import fcm_clustering, silhouette
from typing import Dict, List, Set


if __name__ == '__main__':
    mulai = time.time()
    pickle_filename: str = 'resources/vector_space_model.pickle'
    vsm = VectorSpaceModel(600)
    query = 'jalan allah'
    result_data_file = open(pickle_filename, 'rb')
    weight = pickle.load(result_data_file)
    result_data_file.close()
    df = pd.DataFrame(weight.normalisasi2d(weight.getTfIdf()), columns=weight.getFeatures())
    u, partition_coefficient, partition_entropy, list_error_obj, uawal = fcm_clustering(df, debug=False)
    # mencetak matriks U akhir
    print("Matriks U Akhir")
    print(u, "\n")
    print('partition_coefficient', partition_coefficient)
    print('partition_entropy', partition_entropy)
    list_cluster = []

    for i, u_row in enumerate(u):
        max_prob = max(u_row)
        for j, uik in enumerate(u_row):
            if uik == max_prob:
                list_cluster.append(j + 1)
    print()
    pickle_filename_cluster = 'resources/cluster.pickle'
    cluster_file = open(pickle_filename_cluster, 'wb')
    pickle.dump(list_cluster, cluster_file)
    cluster_file.close()
    evaluator_result = weight.indexing(query, list_cluster)
    
    
    df['klaster'] = list_cluster
    df = df.sort_values(by=['klaster'])
    silo = silhouette(df)
    print('sil', silo)
    
    probability_term_same_cluster = weight.calculateTermInSameCluster(list_cluster)
    # print(probability_term_same_cluster)

    # # output
    # out = Output()
    # list_nomor_surat = [weight.get_data_model_output()[idx].get_nomor_surat() for idx in range(len(weight.get_data_model_output()))]
    # list_nomor_ayat = [weight.get_data_model_output()[idx].get_nomor_ayat() for idx in range(len(weight.get_data_model_output()))]
    # list_merge = []
    # list_merge.append(list_nomor_surat)
    # list_merge.append(list_nomor_ayat)
    # list_sentence = [weight.get_data_model_output()[idx].get_tafsir() for idx in range(len(weight.get_data_model_output()))]
    # list_cleaned = [weight.get_data_model_output()[idx].get_cleaned() for idx in range(len(weight.get_data_model_output()))]
    # list_filtering = [weight.get_data_model_output()[idx].get_filtering() for idx in range(len(weight.get_data_model_output()))]
    # list_preprocessing = [weight.get_data_model_output()[idx].get_preprocessing() for idx in range(len(weight.get_data_model_output()))]

    # transposed_tf = [
    #     [weight.getTf()[j][i] for j in range(len(weight.getTf()))]
    #     for i in range(len(weight.getTf()[0]))
    # ]

    # out.write_preprocessing(nd_title=list_merge, sentence=list_sentence,
    #                         cleaned=list_cleaned, filtering=list_filtering,
    #                         term=list_preprocessing)

    # out.write_doc_weighting(tf=transposed_tf, nd_title=list_merge,
    #                         term=weight.getFeatures(), df=weight.getDf(),
    #                         idf=weight.getIdf(), tfidf=weight.normalisasi2d(weight.getTfIdf()))

    # out.write_doc_clustering(tfidf_norm=weight.normalisasi2d(weight.getTfIdf()), nd_title=list_merge,
    #                          term=weight.getFeatures(), error_obj=list_error_obj,
    #                          cluster=list_cluster, probability=probability_term_same_cluster,
    #                          uawal=uawal, uakhir=u, silo=silo)

    # out.write_doc_information_retrieval(tfidf_norm=weight.normalisasi2d(weight.getTfIdf()), nd_title=list_merge,
    #                                     term=weight.getFeatures(),docs=weight.get_doc_output(), query=query)

    # out.save("resources/output.xls")
    print("Eksekusi Selama",time.time()-mulai)


