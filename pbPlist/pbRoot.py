import collections
import string

import pbKey

class pbRoot(collections.MutableMapping):

    def __init__(self, *args, **kwargs):
        self.store = dict()
        self.key_storage = set()
        self.update(dict(*args, **kwargs))  # use the free update to set keys

    def __getitem__(self, key):
        if type(key) == type(string):
            key = pbKey.pbKey(key, key)
        fetched_item = None
        if key in self.key_storage:
            key_value = self.__keytransform__(key)
            fetched_item = self.store[key_value]
        return fetched_item

    def __setitem__(self, key, value):
        if type(key) == type(string):
            key = pbKey.pbKey(key, key)
        key_value = self.__keytransform__(key)
        if key not in self.key_storage:
            self.key_storage.add(key)
        self.store[key_value] = value

    def __delitem__(self, key):
        if type(key) == type(string):
            key = pbKey.pbKey(key, key)
        key_value = self.__keytransform__(key)
        if key in self.key_storage:
            self.key_storage.remove(key)
        del self.store[key_value]

    def __iter__(self):
        return iter(self.key_storage)

    def __len__(self):
        return len(self.key_storage)

    def __keytransform__(self, key):
        if isinstance(key, pbKey.pbKey):
            return key.name
        else:
            message = 'The class "'+self.__class__.__name__+'" only supports "pbKey" as keys.'
            raise TypeError(message)