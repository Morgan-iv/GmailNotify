import shelve

dbname = "shelvedb"
db = shelve.open(dbname)
db['ids'] = set()
db.close()
