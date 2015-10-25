import collections

import pbItem

class pbRoot(collections.MutableMapping):

    def __init__(self, *args, **kwargs):
        self.store = dict()
        self.key_storage = set()
        self.update(dict(*args, **kwargs))  # use the free update to set keys

    def __internalKeyCheck(self, key):
        safe_key = key
        if type(safe_key) == str:
            safe_key = pbItem.pbItemResolver(safe_key, 'qstring')
        return safe_key

    def __getitem__(self, key):
        key = self.__internalKeyCheck(key)
        fetched_item = None
        if key in self.key_storage:
            key_value = self.__keytransform__(key)
            fetched_item = self.store[key_value]
        return fetched_item

    def __setitem__(self, key, value):
        key = self.__internalKeyCheck(key)
        key_value = self.__keytransform__(key)
        if key not in self.key_storage:
            self.key_storage.add(key)
        self.store[key_value] = value

    def __delitem__(self, key):
        key = self.__internalKeyCheck(key)
        key_value = self.__keytransform__(key)
        if key in self.key_storage:
            self.key_storage.remove(key)
        del self.store[key_value]

    def __iter__(self):
        return self.key_storage.__iter__()

    def __len__(self):
        return self.key_storage.__len__()
    
    def __str__(self):
        return str(self.store)
    
    def __contains__(self, item):
        item = self.__internalKeyCheck(item)
        return item in self.key_storage

    def __keytransform__(self, key):
        if isinstance(key, pbItem.pbItem):
            return key.value
        else:
            message = 'The class "'+self.__class__.__name__+'" only supports "pbItem" as keys.'
            raise TypeError(message)