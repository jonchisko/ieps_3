from database import Database
import pickle

db = Database('index.db')

# Sets up database for this project if we need to reset it
db.setup()

data = pickle.load(open('final_take2.pickle', 'br'))
words = set(data['word'])

db.insert('IndexWord', {'word':list(words)})
print("First tabel filled.")
db.insert('Posting', data)
print("Second tabel filled.")
print('Done.')

# This is how you query the db. columns and conditions parameters are optional, default values are
# columns = "*" and conditions = ""
print(db.get('Posting', columns='word, documentName', conditions='WHERE length(word) BETWEEN 1 AND 3'))