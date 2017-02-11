##########################SIAMH 02/06/2017##################################################
# Populates the in-memory cache
# Performs four operations (Set key, Get Key, Del Key, List keys)
# Before destructing, commits changes to the main database
# It should be singleton object, so that the cache is only populated once in this class's constructor

import string
from DatabaseOp import PopulateData, CommitData

class CacheMemory(object):
    dicts = {}
    bChanged = False

    def __init__(self):
        self.dicts = PopulateData()

    def __del__(self):
        try:
            if self.bChanged == True:
                CommitData(self.dicts)
        except NameError:
            return

    def SetKey(self, key, value):
        if self.dicts.has_key(key) == True:
            self.dicts[key] = value
            self.bChanged = True
            return "Successfully updated value of '" + key + "' in cache memory."
        else:
            return  key + ": is not present in cache memory."

    def UpdateTokens(self, key, token):
        if self.dicts.has_key(key):
            value = self.dicts[key]
        else:
            return key + ": is not present in cache memory."

        toreplace = "${" + key + "}"
        token = token.replace(toreplace, value)
        token = token.replace('EXPAND ', '')
        return token


    def DeleteKey(self, key):
        if self.dicts.has_key(key):
            del self.dicts[key]
            self.bChanged = True
            return "Successfully deleted " + key + "."
        else:
            return key + ": is not present in cache memory."

    def ListAllKeys(self):
        return str(self.dicts.values())

    def GetMessageOfQuery(self, ids, key, values, token):
        if ids == 1:
            return self.SetKey(key, values)
        elif ids == 2:
            return self.UpdateTokens(key, token)
        elif ids == 3:
            return self.DeleteKey(key)
        elif ids == 4:
            return self.ListAllKeys()
        else:
            return "Invalid command line options: " + token


g_cCache = CacheMemory();

# interface function to Server.
# id : 1 --> set key
# id : 2 --> Expand key (Update token)
# id : 3 --> Del key
# id : 4 --> List key
# else --> invalid
def ProcessQuery(ids, key, value, token):
    return g_cCache.GetMessageOfQuery(ids, key, value, token)
