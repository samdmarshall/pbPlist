class pbItem(object):
    
    def __init__(self, value=None, annotation=None):
        if value != None:
            self.value = value
            self.annotation = annotation
        else:
            message = 'The class "'+self.__class__.__name__+'" must be initialized with a non-None value'
            raise ValueError(message)
    
    def __eq__(self, other):
        is_equal = False
        if isinstance(other, pbItem):
            is_equal = (other.value == self.value)
        return is_equal
    
    def __hash__(self):
        return hash(self.value)
        
    def __repr__(self):
        return self.value