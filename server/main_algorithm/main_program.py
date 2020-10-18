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
    pickle_filename: str = 'resources/vector_space_model_surah_gabungan.pickle'
    vsm = VectorSpaceModel(1034)
    query = 'Allah'
    result_data_file = open(pickle_filename, 'rb')
    weight = pickle.load(result_data_file)
    result_data_file.close()
    df = pd.DataFrame(weight.normalisasi2d(weight.getTfIdf()), columns=weight.getFeatures())
    u, partition_coefficient, partition_entropy, list_error_obj, uawal, class_count, w, max_iter, threshold, v, d, u_all, randomawal = fcm_clustering(df, debug=True)
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
    pickle_filename_cluster = 'resources/clusterSurahGabungan.pickle'
    cluster_file = open(pickle_filename_cluster, 'wb')
    pickle.dump(list_cluster, cluster_file)
    cluster_file.close()
    evaluator_result = weight.indexing(query, list_cluster)
    
    probability_term_same_cluster, count_all_term = weight.calculateTermInSameCluster(list_cluster)
    # print(probability_term_same_cluster)
    
    df['klaster'] = list_cluster
    count_cluster = Counter(list_cluster)
    print(count_cluster)
    df = df.sort_values(by=['klaster'])
    silo = silhouette(df)
    print('sil', silo)
    results = {}
    results['klaster'] = class_count
    results['silhouette'] = silo
    results['w'] = w
    results['max_iterasi'] = max_iter
    results['threshold'] = threshold
    results['partition_coefficient'] = np.array(partition_coefficient).tolist()
    results['partition_entropy'] = np.array(partition_entropy).tolist()
    results['features'] = weight.getFeatures()
    results['tf'] = weight.getTf()
    results['idf'] = weight.getIdf()
    results['tfidf'] = weight.getTfIdf()
    results['tfidf_norm'] = weight.normalisasi2d(weight.getTfIdf())
    results['v'] = np.array(v).tolist()
    results['d'] = np.array(d).tolist()
    results['u_awal'] = uawal.tolist()
    results['u_all'] = np.array(u_all).tolist()
    results['u_akhir'] = u.tolist()
    results['randomawal'] = randomawal.tolist()
    results['error_obj'] = list_error_obj
    results['counter_cluster'] = count_cluster
    results['count_all_term'] = count_all_term
    results['probability_term_same_cluster'] = probability_term_same_cluster
    json.dump(results, open(f"resources/results-{class_count}-gabungan.json", "w"))
    
    # probability_term_same_cluster = weight.calculateTermInSameCluster(list_cluster)
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
    
    # transposed_tfidf = [
    #     [weight.getTfIdf()[j][i] for j in range(len(weight.getTfIdf()))]
    #     for i in range(len(weight.getTfIdf()[0]))
    # ]

    # out.write_preprocessing(nd_title=list_merge, sentence=list_sentence,
    #                         cleaned=list_cleaned, filtering=list_filtering,
    #                         term=list_preprocessing)

    # out.write_doc_weighting(tf=transposed_tf, nd_title=list_merge,
    #                         term=weight.getFeatures(), df=weight.getDf(),
    #                         idf=weight.getIdf(), tfidf = transposed_tfidf , tfidfnorm=weight.normalisasi2d(weight.getTfIdf()))

    # out.write_doc_clustering(tfidf_norm=weight.normalisasi2d(weight.getTfIdf()), nd_title=list_merge,
    #                          term=weight.getFeatures(), error_obj=list_error_obj,
    #                          cluster=list_cluster, probability=probability_term_same_cluster,
    #                          uawal=uawal, uakhir=u, silo=silo, random=randomawal)

    # out.write_doc_information_retrieval(tfidf_norm=weight.normalisasi2d(weight.getTfIdf()), nd_title=list_merge,
    #                                     term=weight.getFeatures(),docs=weight.get_doc_output(), query=query)

    # out.save("resources/outputSurahCekFix.xls")
    print("Eksekusi Selama",time.time()-mulai)


