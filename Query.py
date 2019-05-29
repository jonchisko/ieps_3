# imports
import sqlite3
from sqlite3 import Error
from bs4 import BeautifulSoup
import os
from test2 import process_string
import time
import sys
import pickle

# class
class QueryMe:

    def __init__(self):
        # open files
        direktorij = "data_websites"
        print("Preparing files, please wait ...")
        t1 = time.time()
        self.cur = self.create_conn("index.db").cursor()

        file = "text_files_pickle"

        if os.path.isfile(file):
            print("Pickled text dict exists!")
            f = open(file, "rb")
            self.text_files = pickle.load(f)
            f.close()
        else:
            print("Pickled text dict does not exist, creating one. This might take up to one minute!")
            self.text_files = {filename : self.file2string(direktorij+"/"+filename) for filename in os.listdir(direktorij)}
            print("Saving pickle text dict!")
            f = open(file, "wb")
            pickle.dump(self.text_files, f)
            f.close()

        print("Took me: {0:.2f} seconds".format(time.time()-t1))
        print("Ready for searching ...")

    """def __delete__(self, instance):
        self.text_files = None"""


    def find_queries(self, queries_string):
        queries_list = queries_string.split(" ")

    def create_conn(self, db_file):
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            print(e)
            return None


    def select_row(self, conn, words):
        #cur = self.conn.cursor()

        file_dict = dict()
        for word in words:
            self.cur.execute("SELECT * FROM Posting WHERE word = '{0}'".format(word))
            t1 = time.time()
            for row in self.cur.fetchall():
                if row[1] not in file_dict:
                    file_dict[row[1]] = {"freq": row[2], "index": set()}
                    for x in row[3].split(" "):
                        file_dict[row[1]]["index"].add(int(x))
                else:
                    file_dict[row[1]]["freq"] += row[2]
                    for x in row[3].split(" "):
                        file_dict[row[1]]["index"].add(int(x))
        seznam = sorted(file_dict.items(), key=lambda x: x[1]["freq"], reverse=True)

        #filename, frekvenca, indeksi
        resitev = []
        for j, element in enumerate(seznam):
            filename, slovar = element
            text = self.text_files[filename]
            freq = slovar["freq"]
            indeksi = slovar["index"]
            if freq > 0:
                snip = ""
                indeksi = sorted(indeksi)
                for i, ind in enumerate(indeksi):
                    if len(indeksi) == 1:
                        start = ind - 3 if ind - 3 >= 0 else 0
                        if start != 0:
                            snip += "..."
                        end = ind + 3 + 1 if ind + 3 + 1 <= len(text) else len(text)
                        snip += " ".join(text[start:end])
                        if end != len(text):
                            snip += " ..."
                        break
                    if i == 0:
                        start = ind - 3 if ind - 3 >= 0 else 0
                        diff = indeksi[i + 1] - ind
                        if diff > 3:
                            token = " ".join(text[start:ind + 3 + 1]) + " ..."
                            snip += token if start == 0 else "... " + token
                        else:
                            token = " ".join(text[start:indeksi[i + 1]])
                            snip += token if start == 0 else "... " + token
                    elif i > 0 and i != len(indeksi) - 1:
                        # indeksi[i-1]+3 ind-3
                        # e1 e2 e3 e4 e5 e6 e7 e8    e9   e10 e11 e12 e13 e14
                        # 1  2  3  4  5   6 i  i+1   i+2  i+3 i+4 i+5 i+6 i+7
                        # indeksi[i+1]-3 ind+3
                        # -5 ce sosednji do +1 ce je vmes 6 besed
                        diff = ind - (indeksi[i - 1] + 3)
                        start = ind - diff + 1
                        if diff <= 0:
                            start = ind
                        if diff > 4:
                            start = ind - 3 #if ind - 3 >= 0 else 0

                        diff = indeksi[i + 1] - ind
                        if diff > 7:
                            snip += " " + " ".join(text[start:ind + 3 + 1]) + " ..."
                        elif diff >= 0:
                            snip += " " + " ".join(text[start:ind + 3 + 1])
                        else:
                            snip += " " + " ".join(text[start:indeksi[i + 1]])

                    else:
                        diff = ind - (indeksi[i - 1] + 3)
                        start = ind - diff + 1
                        if diff <= 0:
                            start = ind
                        if diff > 4:
                            start = ind - 3 #if ind - 3 >= 0 else 0
                        if ind + 3 + 1 >= len(text):
                            end = len(text)
                            snip += " " + " ".join(text[start:end])
                        else:
                            end = ind + 3 + 1
                            snip += " " + " ".join(text[start:end]) + " ..."
                resitev.append((freq, filename, snip))
        return resitev



    def ind_search(self, queries):
        #conn = self.create_conn("index.db")
        queries = [x.lower() for x in process_string(queries, "")[0]]
        return self.select_row("a", queries)


    def doSearch(self, query, seq_ind):
        t1 = time.time()
        if seq_ind == "seq":
            s = self.sequential_search(query)
        elif seq_ind == "ind":
            s = self.ind_search(query)
        else:
            print("Wrong search type specificed, use 'seq' for sequential or 'ind' for db!")
            return
        t2 = time.time()
        print("Results for a query:", query)
        print("Results found in {0:.2f} ms.".format((t2-t1)*1000))

        # print it
        print("Frequencies Document                                  Snippet")
        print("----------- ----------------------------------------- -----------------------------------------------------------")
        for e in s:
            print("%-5s       %-41s %s" % (e[0], e[1], e[2]))


    def file2string(self, filename):
        with open(filename, "rt", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
            _, actual_text = process_string(soup.text, filename.split("/")[-1])
        return actual_text

    def sequential_search(self, queries):
        results = []
        query_set = set( x.lower() for x in process_string(queries, "")[0] )
        for file in self.text_files:
            freq = 0
            snip = ""
            to_add = 0
            last_snip_ind = 0
            text = self.text_files[file]
            i=-1
            for i in range(len(text)):
                if text[i].lower() in query_set:
                    freq += 1
                    start = i-3 if i-3 >= 0 else 0
                    to_add = 4 #
                    if last_snip_ind == 0:
                        token = " ".join(text[start:i])
                        snip += token if start == 0 else "... " + token
                    else:
                        if i - last_snip_ind > 4:
                            snip += " ... "
                            snip += " ".join(text[start:i])
                        else:
                            snip += " ".join(text[last_snip_ind+1:i])
                if to_add > 0:
                    snip += " " + text[i]
                    last_snip_ind = i
                    to_add -= 1
            if last_snip_ind != i:
                snip += " ..."
            if freq > 0:
                results.append( (freq, file, snip) )
        results = sorted(results, key=lambda x: x[0], reverse=True)
        return results





if __name__ == '__main__':

    #nizi = ["predelovalne dejavnosti", "trgovina", "social services", "davki", "delo informacije", "sistem SPOT"]

    """
    rabis "data_websites" folder s spletnimi stranmi
    rabis index.db
    zgornje dve stvari rabis imeti na isti lokaciji kot kodo
    seq
    ind
    """

    sekve_baza = sys.argv[1]
    nizi = " ".join(sys.argv[2:])
    QS = QueryMe()
    QS.doSearch(nizi, seq_ind=sekve_baza)
