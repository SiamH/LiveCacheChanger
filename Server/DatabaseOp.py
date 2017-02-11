##########################SIAMH 02/06/2017##################################################
# A Sqllite database holding key and values
# It performs the operations on the cahce
# In the end, when the server stops, then it commits cache to the database
# Depending on the requirement, the server can handle request from multiple clients


import sqlite3

class cDatabase(object):
    sqlite_file = ''    # name of the sqlite database file
    table_name = ''  # name of the table to be created
    field_key = '' # name of the column
    field_value = '' # name of the column
    dicts = {}

    def __init__(self):
        self.sqlite_file = 'keyVal.sqlite'
        self.table_name = 'keyval'
        self.field_key = 'key'
        self.field_value = 'value'

    def RetrieveQuery(self):
        query = "SELECT * FROM " + self.table_name
        return query

    def UpdateQuery(self, key, value):
        query = "UPDATE " + self.table_name + " SET " + self.field_value + "='" \
                 + value + "' WHERE " +\
                 self.field_key + "='" + key + "'"
        return query

    def DeleteQuery(self, key):
        query = "DELETE FROM " + self.table_name +\
                " WHERE " + self.field_key + "='" + key + "'"
        return query

    def PopulateData(self):
        conn = sqlite3.connect(self.sqlite_file)
        c = conn.cursor()
        c.execute(self.RetrieveQuery())

        all_rows = c.fetchall()
        # two dictionaries are populated. One will act as in-memory cahce
        # other one will be kept for later comaprison.

        return_dicts = {}
        for i in all_rows:
            k = str(i[0])
            v = str(i[1])
            self.dicts.update({k:v})
            return_dicts.update({k:v})

        conn.close()
        return return_dicts

    def CommitData(self, Updateddicts):
        conn = sqlite3.connect(self.sqlite_file)
        c = conn.cursor()

        for k in self.dicts:
            #if Key not found, that means it has been deleted by DEL operation
            # So we need to delete the key.
            # Otherwise, if key is found but value is mismatched, then we need to
            # update that record.
            # Otherwise that record is not changed at all.
            # Since no operation perfroms insertion of a new key, we do not need to
            # perform any insert query
            # One option here would be delete all the changed record and insert only the current keys, values
            # It should have same runtime as underneath (update = delete-->create)
            if Updateddicts.has_key(k) == True:
                if self.dicts[k] != Updateddicts[k]:
                    c.execute(self.UpdateQuery(k, Updateddicts[k]))
            else:
                c.execute(self.DeleteQuery(k))

        conn.commit()
        conn.close()


database = cDatabase()

#interfaces to caches

def PopulateData():
    return database.PopulateData()

def CommitData(dicts):
    database.CommitData(dicts)
