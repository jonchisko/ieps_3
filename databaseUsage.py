from database import Database

db = Database('index.db')

# Sets up database for this project if we need to reset it
#db.setup()

# This is how you query the db. columns and conditions parameters are optional, default values are
# columns = "*" and conditions = ""
print(db.get('Posting', columns='word, documentName', conditions='WHERE length(word) BETWEEN 1 AND 3'))