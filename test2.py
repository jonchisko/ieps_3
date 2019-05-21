import pickle

infile = open("final.pickle", "rb")
slovar = pickle.load(infile, encoding="bytes")


print(len(slovar["documentName"]))
print(len(slovar["word"]))
print(len(slovar["frequency"]))
print(len(slovar["indexes"]))