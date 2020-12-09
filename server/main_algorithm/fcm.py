import copy
import pandas as pd
import numpy as np
import math
from main_algorithm.data_model import DataModel


def one_normalize(array_data):
    result = array_data / sum(array_data)
    return result


def fcm_clustering(dataframe, class_count=2, w=2, max_iter=3, error_threshold=0.00001, debug=True):
    """
    Method ini merupakan method yang mengclusterkan data menggunakan konsep Fuzzy C-Means.
    :param dataframe: data masukan yang akan diclusterisasi dalam bentuk dataframe pandas
    
    :param class_count: jumlah cluster yang diinginkan
    :param w: bilangan pemangkat (pembobot)
    :param max_iter: jumlah iterasi maksimal jika error tidak terpenuhi
    :param error_threshold: batas error yang diharapkan
    
    :param debug: boolean untuk menentukan mencetak hasil tiap iterasi
    :return: matriks U (list 2 dimensi) akhir setelah iterasi berhenti
    """
    data_count, feature_count = dataframe.shape
    partition_coefficient = []
    partition_entropy = []
    error_obj = []
    # membuat matriks U random dengan jumlah probabilitas 1 tiap baris
    u = np.absolute(np.random.randn(data_count, class_count))
    randomawal = copy.deepcopy(u)
    for (row_index, row_u) in enumerate(u):
        u[row_index] = one_normalize(row_u)

    uawal = u
    print()
    prev_obj_func_result = 0
    v_list = []
    d_list = []
    u_all = []
    pc_all = []
    pe_all = []
    must_continue = True
    current_iter = 1
    while must_continue and current_iter <= max_iter:
        u_powered = np.power(u, w)
        v = np.zeros((class_count, feature_count))
        d_square = np.zeros((data_count, class_count))
        new_u = np.zeros((data_count, class_count))

        for class_index in range(class_count):
            ui_power_w_array = u_powered[:, class_index]
            sum_of_ui_power_w_array = sum(ui_power_w_array)
            for feature_index in range(feature_count):
                # mencari v (pusat dari tiap cluster untuk tiap fitur)
                v[class_index][feature_index] = sum([
                    uik_element * dataframe.iloc[k_index][feature_index]
                    for k_index, uik_element in enumerate(ui_power_w_array)
                ]) / sum_of_ui_power_w_array
        v_list.append(v)

        for data_index in range(data_count):
            for class_index in range(class_count):
                # mencari d^1/2 dari sebuah data terhadap sebuah pusat cluster
                d_square[data_index][class_index] = pow(sum([
                    pow(dataframe.iloc[data_index][feature_index] - \
                        v[class_index][feature_index], 2)
                    for feature_index in range(feature_count)
                ]), 1 / 2)
                
        d_list.append(d_square)

        for data_index in range(data_count):
            for class_index in range(class_count):
                # memperbaiki matriks U
                new_u[data_index][class_index] = 1 / sum([
                    pow(d_square[data_index][class_index] / d_square[data_index][j], 2 / (w - 1))
                    for j in range(class_count)
                ])

        u_all.append(new_u)
        # menghitung fungsi objektif
        obj_func_result = sum([
            sum([pow(u[data_index][class_index], w) * pow(d_square[data_index][class_index],2) for data_index in
                 range(data_count)])
            for class_index in range(class_count)
        ])

        # menghitung partition coeficiton
        partition_coefficient = 1/data_count * sum([
            sum([pow(u[data_index][class_index], w)
                for data_index in range(data_count)])
            for class_index in range(class_count)
        ])
        pc_all.append(partition_coefficient)

        # menghitung partition entropy
        partition_entropy = -1/data_count * sum([
            sum([u[data_index][class_index] * math.log2(u[data_index][class_index])
                for data_index in range(data_count)])
            for class_index in range(class_count)
        ])
        pe_all.append(partition_entropy)

        # menghitung error
        error = abs(prev_obj_func_result - obj_func_result)
        if debug:
            error_obj.append(
                f'iteration {current_iter}, obj. funct = {obj_func_result}, error = {error}')
            print(
                f'iteration {current_iter}, obj. funct = {obj_func_result}, error = {error}')

        # memperbarui variabel dalam iterasi
        current_iter += 1
        u = new_u
        prev_obj_func_result = obj_func_result
        must_continue = prev_obj_func_result is None or error > error_threshold

    return u, pc_all, pe_all, error_obj, uawal, class_count, w, max_iter, error_threshold, v_list, d_list, u_all, randomawal


def silhouette_coef(data):
    list_ai = []
    list_bi = []

    for i, data1 in data.iterrows():
        suma = 0
        counta = 0
        dict_sumb = {}
        dict_countb = {}
        for j, data2 in data.iterrows():
            if data1.klaster == data2.klaster:
                counta = counta + 1
                cp_data1 = copy.deepcopy(data1)
                cp_data1 = cp_data1.drop('klaster')
                cp_data2 = copy.deepcopy(data2)
                cp_data2 = cp_data2.drop('klaster')
                suma += euclidean_distance(cp_data1, cp_data2)
            else:
                klaster = data2.klaster
                if klaster in dict_sumb:
                    cp_data1 = copy.deepcopy(data1)
                    cp_data1 = cp_data1.drop('klaster')
                    cp_data2 = copy.deepcopy(data2)
                    cp_data2 = cp_data2.drop('klaster')
                    dict_sumb[klaster] += euclidean_distance(cp_data1, cp_data2)
                    dict_countb[klaster] += 1
                else:
                    cp_data1 = copy.deepcopy(data1)
                    cp_data1 = cp_data1.drop('klaster')
                    cp_data2 = copy.deepcopy(data2)
                    cp_data2 = cp_data2.drop('klaster')
                    dict_sumb[klaster] = euclidean_distance(cp_data1, cp_data2)
                    dict_countb[klaster] = 1
        for key in dict_sumb:
            dict_sumb[key] = dict_sumb[key]/dict_countb[key]
        list_ai.append(1/(counta - 1) * suma)
        list_bi.append((dict_sumb[min(dict_sumb, key=dict_sumb.get)]))

    silhouette = (np.array(list_bi)-np.array(list_ai))/np.maximum(np.array(list_ai), np.array(list_bi))
    dict_silhouette = {}
    for i in range(len(silhouette)):
        klaster = data.klaster[i]
        if klaster in dict_silhouette:
            dict_silhouette[klaster] += silhouette[i]
        else:
            dict_silhouette[klaster] = silhouette[i]
    cluster_count = data["klaster"].value_counts()
    silhouette_score = [dict_silhouette[key]/cluster_count[key] for key in dict_silhouette]
    return np.average(silhouette_score)

def euclidean_distance(data1, data2):
    return np.sqrt(np.sum(pow((data1-data2),2)))
