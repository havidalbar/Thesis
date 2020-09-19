import numpy as np
import math
import pandas as pd
from typing import Dict, List, Iterable, Set
import copy
from main_algorithm.data_model import DataModel


def one_normalize(array_data):
    result = array_data / sum(array_data)
    return result


def fcm_clustering(dataframe, class_count=4, w=2, max_iter=100, error_threshold=0.001, debug=True):
    """
    Method ini merupakan method yang mengclusterkan data menggunakan konsep Fuzzy C-Means.
    :param dataframe: data masukan yang akan diclusterisasi dalam bentuk dataframe pandas
    
    :param class_count: jumlah cluster yang diinginkan
    :param w: bilangan pemangkat (pembobot)
    :param max_iter: jumlah iterasi maksimal jika error tidak terpenuhi
    :param error_threshold: batas error yang
    
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

        # menghitung partition entropy
        partition_entropy = -1/data_count * sum([
            sum([u[data_index][class_index] * math.log2(u[data_index][class_index])
                for data_index in range(data_count)])
            for class_index in range(class_count)
        ])

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

    return u, partition_coefficient, partition_entropy, error_obj, uawal, class_count, w, max_iter, error_threshold, v_list, d_list, u_all, randomawal


def Euclidean_distance(data1, data2):
    data1 = data1.drop('klaster')
    data2 = data2.drop('klaster')
    return np.sqrt(np.sum((data1-data2)**2))


def silhouette(data):
    a = []
    b = []

    for i, row1 in data.iterrows():
        sum_b = {}
        count_a = 0
        sum_a = 0
        count_b = {}
        for j, row2 in data.iterrows():
            if row1.klaster == row2.klaster:
                count_a = count_a + 1
                sum_a += Euclidean_distance(row1, row2)
            else:
                klaster = row2.klaster
                if klaster in sum_b:
                    sum_b[klaster] += Euclidean_distance(row1, row2)
                    count_b[klaster] += 1
                else:
                    sum_b[klaster] = Euclidean_distance(row1, row2)
                    count_b[klaster] = 1
        for key in sum_b:
            sum_b[key] = sum_b[key]/count_b[key]
        b.append((sum_b[min(sum_b, key=sum_b.get)]))
        a.append(1/(count_a - 1) * sum_a)

    sil = (np.array(b)-np.array(a))/np.maximum(np.array(a), np.array(b))
    dict_sil = {}
    for i in range(len(sil)):
        klaster = data.klaster[i]
        if klaster in dict_sil:
            dict_sil[klaster] += sil[i]
        else:
            dict_sil[klaster] = sil[i]
    count = data["klaster"].value_counts()
    score = [dict_sil[key]/count[key] for key in dict_sil]
    return np.average(score)
