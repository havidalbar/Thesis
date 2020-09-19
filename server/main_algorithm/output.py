import xlwt


class Output:
    def __init__(self):
        self.book = xlwt.Workbook()
        self.sheet = self.book.add_sheet("Preprocessing")
        self.sheet.write(0, 0, "Preprocessing")

        self.sheet2 = self.book.add_sheet("Term Weighting")
        self.sheet2.write(0, 0, "Term Weighting")

        self.sheet3 = self.book.add_sheet("FCM Clustering")
        self.sheet3.write(0, 0, "FCM CLUSTERING")

        self.sheet4 = self.book.add_sheet("Information Retrieval")
        self.sheet4.write(0, 0, "Information Retrieval")

        self.column_number = 0
        self.row_number = 2

    def write_preprocessing(self, nd_title, sentence, cleaned, filtering, term):
        self.row_number = 2
        self.column_number = 0

        # print title tf
        self.sheet.write(self.row_number, self.column_number, "Sentence")
        self.row_number += 1

        # print no_surat & ayat
        for row_title in nd_title:
            for row_col in row_title:
                self.sheet.write(self.row_number, self.column_number, str(row_col))
                self.row_number += 1
            self.row_number = 3
            self.column_number = 1

        self.row_number = 3
        self.column_number = 2
        for element in sentence:
            self.sheet.write(self.row_number, self.column_number, element)
            self.row_number += 1

        ##-----------------------clean and casefold-------------------#
        self.column_number = 0
        self.row_number += 3
        # print title clean and casefold
        self.sheet.write(self.row_number, self.column_number, "Cleaning and CaseFolding")
        self.row_number += 1

        temp_row = self.row_number
        # print no_surat & ayat
        for row_title in nd_title:
            for row_col in row_title:
                self.sheet.write(self.row_number, self.column_number, str(row_col))
                self.row_number += 1
            self.row_number = temp_row
            self.column_number = 1

        # # print cleaned
        self.column_number = 2
        for element in cleaned:
            self.sheet.write(self.row_number, self.column_number, element)
            self.row_number += 1

        ##-----------------------filtering-------------------#
        self.column_number = 0
        self.row_number += 3
        # print title filtering
        self.sheet.write(self.row_number, self.column_number, "Filtering")
        self.row_number += 1

        temp_row = self.row_number
        # print no_surat & ayat
        for row_title in nd_title:
            for row_col in row_title:
                self.sheet.write(self.row_number, self.column_number, str(row_col))
                self.row_number += 1
            self.row_number = temp_row
            self.column_number = 1

        # # print filtering
        self.column_number = 2
        for element in filtering:
            temp = str(element)+","
            self.sheet.write(self.row_number, self.column_number, temp)
            self.row_number += 1

        ##-----------------------stemming-------------------#
        self.column_number = 0
        self.row_number += 3
        # print title stemming
        self.sheet.write(self.row_number, self.column_number, "Stemming")
        self.row_number += 1

        temp_row = self.row_number
        # print no_surat & ayat
        for row_title in nd_title:
            for row_col in row_title:
                self.sheet.write(self.row_number, self.column_number, str(row_col))
                self.row_number += 1
            self.row_number = temp_row
            self.column_number = 1

        # # print stemming
        self.column_number = 2
        for element in term:
            temp = str(element) + ","
            self.sheet.write(self.row_number, self.column_number, temp)
            self.row_number += 1
        self.row_number += 1

    def write_doc_weighting(self,nd_title, term, tf, df, idf, tfidf, tfidfnorm):
        self.row_number = 2
        self.column_number = 0

        #print title tf
        self.sheet2.write(self.row_number, self.column_number, "TF")
        self.row_number += 1

        #print no_surat & ayat
        for row_title in nd_title:
            for row_col in row_title:
                self.sheet2.write(self.row_number, self.column_number, str(row_col))
                self.row_number +=1
            self.row_number = 3
            self.column_number = 1

        #print term
        self.row_number = 2
        self.column_number = 2
        for element in term:
            self.sheet2.write(self.row_number, self.column_number, element)
            self.column_number += 1

        #print value tf
        self.row_number = 3
        self.column_number = 2
        for word_frequency in tf:
            for element in word_frequency:
                self.sheet2.write(self.row_number, self.column_number, element)
                self.column_number += 1
            self.column_number = 2
            self.row_number += 1

        # print title df
        self.column_number = 1
        self.sheet2.write(self.row_number, self.column_number, "DF")
        self.column_number += 1
        # print value df
        for element in df:
            self.sheet2.write(self.row_number, self.column_number, element)
            self.column_number += 1

        self.row_number += 1
        # print title idf
        self.column_number = 1
        self.sheet2.write(self.row_number, self.column_number, "IDF")
        self.column_number += 1
        # print value idf
        for element in idf:
            self.sheet2.write(self.row_number, self.column_number, element)
            self.column_number += 1
        self.row_number += 2

        ##-----------------------------print tfidf----------------------------#
        self.column_number = 0
        self.row_number += 3
        # print title tf
        self.sheet2.write(self.row_number, self.column_number, "TFIDF")
        self.row_number += 1

        temp_row = self.row_number
        # print no_surat & ayat
        for row_title in nd_title:
            for row_col in row_title:
                self.sheet2.write(self.row_number, self.column_number, str(row_col))
                self.row_number += 1
            self.row_number = temp_row
            self.column_number = 1

        self.row_number -= 1
        # # print term
        self.column_number = 2
        for element in term:
            self.sheet2.write(self.row_number, self.column_number, element)
            self.column_number += 1
        self.row_number += 1

        # print value tfidf
        self.column_number = 2
        for word_frequency in tfidf:
            for element in word_frequency:
                self.sheet2.write(self.row_number, self.column_number, element)
                self.column_number += 1
            self.column_number = 2
            self.row_number += 1

        # print title df
        self.column_number = 1
        self.sheet2.write(self.row_number, self.column_number, "DF")
        self.column_number += 1
        # print value df
        for element in df:
            self.sheet2.write(self.row_number, self.column_number, element)
            self.column_number += 1

        self.row_number += 1
        # print title idf
        self.column_number = 1
        self.sheet2.write(self.row_number, self.column_number, "IDF")
        self.column_number += 1
        # print value idf
        for element in idf:
            self.sheet2.write(self.row_number, self.column_number, element)
            self.column_number += 1
        self.row_number += 2
        
        
                ##-----------------------------print tfidf----------------------------#
        self.column_number = 0
        self.row_number += 3
        # print title tf
        self.sheet2.write(self.row_number, self.column_number, "TFIDF")
        self.row_number += 1

        temp_row = self.row_number
        # print no_surat & ayat
        for row_title in nd_title:
            for row_col in row_title:
                self.sheet2.write(self.row_number, self.column_number, str(row_col))
                self.row_number += 1
            self.row_number = temp_row
            self.column_number = 1

        self.row_number -= 1
        # # print term
        self.column_number = 2
        for element in term:
            self.sheet2.write(self.row_number, self.column_number, element)
            self.column_number += 1
        self.row_number += 1

        # print value tfidf
        self.column_number = 2
        for word_frequency in tfidfnorm:
            for element in word_frequency:
                self.sheet2.write(self.row_number, self.column_number, element)
                self.column_number += 1
            self.column_number = 2
            self.row_number += 1

        # print title df
        self.column_number = 1
        self.sheet2.write(self.row_number, self.column_number, "DF")
        self.column_number += 1
        # print value df
        for element in df:
            self.sheet2.write(self.row_number, self.column_number, element)
            self.column_number += 1

        self.row_number += 1
        # print title idf
        self.column_number = 1
        self.sheet2.write(self.row_number, self.column_number, "IDF")
        self.column_number += 1
        # print value idf
        for element in idf:
            self.sheet2.write(self.row_number, self.column_number, element)
            self.column_number += 1
        self.row_number += 2

    def write_doc_clustering(self,nd_title, term, tfidf_norm, error_obj, cluster, probability, uawal, uakhir, silo, random):
        self.row_number = 2
        self.column_number = 0

        #print title tfidf norm
        self.sheet3.write(self.row_number, self.column_number, "Random Awal")
        self.row_number += 1

        self.column_number = 2
        for dt in random:
            for el in dt:
                self.sheet3.write(self.row_number, self.column_number, el)
                self.column_number += 1
            self.column_number = 2
            self.row_number += 1

        # #print no_surat & ayat
        # for row_title in nd_title:
        #     for row_col in row_title:
        #         self.sheet3.write(self.row_number, self.column_number, str(row_col))
        #         self.row_number +=1
        #     self.row_number = 3
        #     self.column_number = 1

        # #print term
        # self.row_number = 2
        # self.column_number = 2
        # for element in term:
        #     self.sheet3.write(self.row_number, self.column_number, element)
        #     self.column_number += 1

        # #print value tfidfnorm
        # self.row_number = 3
        # self.column_number = 2
        # for word_frequency in tfidf_norm:
        #     for element in word_frequency:
        #         self.sheet3.write(self.row_number, self.column_number, element)
        #         self.column_number += 1
        #     self.column_number = 2
        #     self.row_number += 1

        ##-----------------------------print proses clustering----------------------------#
        self.column_number = 0
        self.row_number += 2
        # print title proses
        self.sheet3.write(self.row_number, self.column_number, "Proses Clustering")
        self.row_number += 1

        self.sheet3.write(self.row_number, self.column_number, "Matriks U Awal Clustering")
        self.row_number += 1

        self.column_number = 2
        for row_u in uawal:
            for col_u in row_u:
                self.sheet3.write(self.row_number, self.column_number, col_u)
                self.column_number += 1
            self.row_number += 1
            self.column_number = 2
        self.row_number += 2

        self.column_number = 2
        for element in error_obj:
            self.sheet3.write(self.row_number, self.column_number, element)
            self.row_number += 1
        self.row_number += 2

        self.column_number = 0
        self.sheet3.write(self.row_number, self.column_number, "Matriks U Akhir Clustering")
        self.row_number += 1

        self.column_number = 2
        for row_u in uakhir:
            for col_u in row_u:
                self.sheet3.write(self.row_number, self.column_number, col_u)
                self.column_number += 1
            self.row_number += 1
            self.column_number = 2

        self.column_number = 0
        self.sheet3.write(self.row_number, self.column_number, "Silhouette Coefficient:")

        self.row_number += 1
        self.sheet3.write(self.row_number, self.column_number, silo)


        ##-----------------------------print hasil clustering----------------------------#
        self.column_number = 0
        self.row_number += 2
        # print title tf
        self.sheet3.write(self.row_number, self.column_number, "Hasil Clustering")
        self.row_number += 1

        temp_row = self.row_number
        # print no_surat & ayat
        for row_title in nd_title:
            for row_col in row_title:
                self.sheet3.write(self.row_number, self.column_number, str(row_col))
                self.row_number += 1
            self.row_number = temp_row
            self.column_number = 1
        temp_term = self.row_number - 1

        self.row_number -= 1
        # print title cluster
        self.column_number = 2
        self.sheet3.write(self.row_number, self.column_number, "Cluster")
        # print value cluster
        self.row_number += 1
        for idx in range(len(cluster)):
            self.sheet3.write(self.row_number, self.column_number, str(cluster[idx]))
            self.row_number += 1

        # self.row_number = temp_term
        # # # print term
        # self.column_number = 3
        # for element in term:
        #     self.sheet3.write(self.row_number, self.column_number, element)
        #     self.column_number += 1
        # self.row_number += 2

        # # print value tfidf
        # self.row_number -= 1
        # self.column_number = 3
        # for word_frequency in tfidf_norm:
        #     for element in word_frequency:
        #         self.sheet3.write(self.row_number, self.column_number, element)
        #         self.column_number += 1
        #     self.column_number = 3
        #     self.row_number += 1


        # ##-----------------------------print hasil clustering----------------------------#
        # self.column_number = 0
        # self.row_number += 2
        # # print title tf
        # self.sheet3.write(self.row_number, self.column_number, "Probability Each Term in Same Cluster")
        # self.row_number += 1
        # self.column_number -= 1

        # # # print probability
        # list_term_sort = []
        # list_cluster_sort = []
        # list_prob_sort = []
        # for cluster, value in probability.items():
        #     for term, probability in value.items():
        #         if probability != 0.0:
        #             list_term_sort.append(term)
        #             list_cluster_sort.append(cluster)
        #             list_prob_sort.append(probability)
        # self.row_number += 1
        # # # print term
        # self.column_number = 0
        # self.sheet3.write(self.row_number, self.column_number, "Term")

        # self.column_number = 1
        # for element in list_term_sort:
        #     self.sheet3.write(self.row_number, self.column_number, element)
        #     self.column_number += 1
        # self.row_number += 1

        # self.column_number = 0
        # self.sheet3.write(self.row_number, self.column_number, "Probability")
        # self.column_number = 1
        # for element in list_prob_sort:
        #     self.sheet3.write(self.row_number, self.column_number, element)
        #     self.column_number += 1
        # self.row_number += 1

        # self.column_number = 0
        # self.sheet3.write(self.row_number, self.column_number, "Cluster")
        # self.column_number = 1
        # for element in list_cluster_sort:
        #     self.sheet3.write(self.row_number, self.column_number, element)
        #     self.column_number += 1
        # self.row_number += 1

    def write_doc_information_retrieval(self,nd_title, term, tfidf_norm, docs, query):
        self.row_number = 2
        self.column_number = 0

        #print title tfidf norm
        self.sheet4.write(self.row_number, self.column_number, "TFIDF Normal")
        self.row_number += 1

        #print no_surat & ayat
        for row_title in nd_title:
            for row_col in row_title:
                self.sheet4.write(self.row_number, self.column_number, str(row_col))
                self.row_number +=1
            self.row_number = 3
            self.column_number = 1

        #print term
        self.row_number = 2
        self.column_number = 2
        for element in term:
            self.sheet4.write(self.row_number, self.column_number, element)
            self.column_number += 1

        #print value tfidfnorm
        self.row_number = 3
        self.column_number = 2
        for word_frequency in tfidf_norm:
            for element in word_frequency:
                self.sheet4.write(self.row_number, self.column_number, element)
                self.column_number += 1
            self.column_number = 2
            self.row_number += 1

        list_ayat_sort = []
        list_surat_sort = []
        list_term_sort = []
        list_clean_sort = []
        list_cluster_sort = []
        list_cosine_sort = []
        for idx in range(len(docs)):
            if docs[idx][1] != 0:
                list_surat_sort.append(docs[idx][0].get_nomor_surat())
                list_ayat_sort.append(docs[idx][0].get_nomor_ayat())
                list_term_sort.append(docs[idx][0].get_preprocessing())
                list_clean_sort.append(docs[idx][0].get_cleaned())
                list_cluster_sort.append(docs[idx][2])
                list_cosine_sort.append(docs[idx][1])

        self.row_number += 2
        ##-----------------------------print hasil retrieval----------------------------#
        self.column_number = 0
        # print title retrieval
        self.sheet4.write(self.row_number, self.column_number, "Hasil Retrieval")
        self.row_number += 1
        self.sheet4.write(self.row_number, self.column_number, ("Query:" + query))
        self.column_number += 4
        self.sheet4.write(self.row_number, self.column_number, "Term:")
        self.column_number -= 4
        self.row_number += 1

        # print no_surat & ayat
        temp = self.row_number
        for element in list_surat_sort:
            self.sheet4.write(self.row_number, self.column_number, str(element))
            self.row_number += 1
        self.column_number += 1

        self.row_number = temp
        for element in list_ayat_sort:
            self.sheet4.write(self.row_number, self.column_number, str(element))
            self.row_number += 1
        self.column_number += 1

        self.row_number = temp - 1
        self.sheet4.write(self.row_number, self.column_number, "Cosine:")
        self.row_number += 1
        for element in list_cosine_sort:
            self.sheet4.write(self.row_number, self.column_number, str(element))
            self.row_number += 1
        self.column_number += 1

        self.row_number = temp - 1
        self.sheet4.write(self.row_number, self.column_number, "Cluster:")
        self.row_number += 1

        for element in list_cluster_sort:
            self.sheet4.write(self.row_number, self.column_number, str(element))
            self.row_number += 1

        self.column_number += 1
        self.row_number = temp
        for element in list_term_sort:
            temp = str(element)+","
            self.sheet4.write(self.row_number, self.column_number, temp)
            self.row_number += 1

        self.column_number = 0
        self.row_number += 1

        # print no_surat & ayat
        temp = self.row_number
        for element in list_surat_sort:
            self.sheet4.write(self.row_number, self.column_number, str(element))
            self.row_number += 1
        self.column_number += 1

        self.row_number = temp
        for element in list_ayat_sort:
            self.sheet4.write(self.row_number, self.column_number, str(element))
            self.row_number += 1
        self.column_number += 1

        # print clean tafsir
        self.row_number = temp
        for element in list_clean_sort:
            self.sheet4.write(self.row_number, self.column_number, str(element))
            self.row_number += 1
        self.row_number += 2

    
    def save(self, filename):
        self.book.save(filename)
