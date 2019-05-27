# imports
import sqlite3
from sqlite3 import Error
from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup
import os
from test import process_string
from test import stop_words_slovene
import time

# class
class QueryMe:

    def __init__(self):
        # open files
        self.text_files = {filename : self.file2string("data_websites/"+filename) for filename in os.listdir("data_websites")}
        print("Ready ...")

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
        cur = conn.cursor()
        file_dict = dict()
        for word in words:
            cur.execute("SELECT * FROM Posting WHERE word='{0}'".format(word))
            for row in cur.fetchall():
                if row[1] not in file_dict:
                    file_dict[row[1]] = {"freq": row[2], "index": set()}
                    for x in row[3].split(","):
                        file_dict[row[1]]["index"].add(int(x))
                else:
                    file_dict[row[1]]["freq"] += row[2]
                    for x in row[3].split(","):
                        file_dict[row[1]]["index"].add(int(x))
        seznam = sorted(file_dict.items(), key=lambda x: x[1]["freq"], reverse=True)

        #filename, frekvenca, indeksi
        for j, element in enumerate(seznam):
            filename, slovar = element
            text = self.text_files[filename]
            freq = slovar["freq"]
            indeksi = slovar["index"]
            snip = ""
            indeksi = sorted(indeksi)
            for i, ind in enumerate(indeksi):
                a = 100
                if len(indeksi) == 1:
                    snip += text[ind]
                    break
                if i == 0:
                    start = ind - 3 if ind - 3 >= 0 else 0
                    diff = indeksi[i + 1] - ind
                    if diff > 3:
                        snip += " " + " ".join(text[start:ind + 3 + 1]) + " ... "
                    else:
                        snip += " " + " ".join(text[start:indeksi[i + 1]])
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
                    if diff > 3:
                        snip += " " + " ".join(text[start:ind + 3 + 1]) + " ... "
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
            print(snip)



    def ind_search(self, queries):
        conn = self.create_conn("index.db")
        queries = self.process_text(queries)
        return self.select_row(conn, queries)



    def process_text(self, s):
        razdeljen = s.split("\n")
        razdeljen = [x + " " for x in razdeljen if x and "/*" not in x and ";" not in x and "*/" not in x]
        obdelan_tekst = "".join(razdeljen)
        a = word_tokenize(obdelan_tekst)
        a = [x for x in a if
             x != "," and x != ";" and x != "(" and x != ")" and x != "." and x != ":"
             and x != "!" and x != "?" and x != "<" and x != ">" and x != "#"]
        vocab = [word.lower() for word in a if word.lower() not in stop_words_slovene]
        return vocab

    def file2string(self, filename):
        with open(filename, "rt", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
            _, actual_text = process_string(soup.text, filename.split("/")[-1])
        return actual_text

    def sequential_search(self, queries, files):
        results = []
        query_set = set(self.process_text(queries))
        for file in files:
            freq = 0
            snip = ""
            to_add = 0
            last_snip_ind = 0
            text = self.text_files[file]
            i=-1
            for i in range(len(text)):
                for quer in query_set:
                    if quer in text[i].lower():
                        freq += 1
                        start = i-3 if i > 3 else 0
                        to_add = 4 #

                        if i - last_snip_ind > 3:
                            snip += " ... "
                            snip += " ".join(text[start:i])
                        else:
                            snip += " " + " ".join(text[last_snip_ind+1:i])
                        break
                if to_add > 0:
                    snip += " "+text[i]
                    last_snip_ind = i
                    to_add -= 1
            if last_snip_ind != i:
                snip += " ..."
            results.append( (freq, file, snip) )
        results = sorted(results, key=lambda x: x[0], reverse=True)
        return results





if __name__ == '__main__':
    QS = QueryMe()
    t1 = time.time()
    r = QS.sequential_search("Sistem SPOT", os.listdir("./data_websites"))#os.listdir("./data_websites"))#)
    for e in r:
        print(e)
    t_seq = time.time() - t1
    t1 = time.time()
    s = QS.ind_search("Sistem SPOT")
    print(s)
    print(t_seq)
    print(time.time()-t1)

    #'evem.gov.si.371.html'