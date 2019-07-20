import stringtree

class User:
    def __init__(self,alias,table,rating):
        self.alias = alias
        self.table = int(table)
        self.online = True
        self.rating = rating
