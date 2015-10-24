class pbItem(object):
    
    def __init__(self, value=None, annotation=None):
        if value != None:
            self.name = value
            self.annotation = annotation
        else:
            raise ValueError('The class "'+self.__class__.__name__+'" must be initialized with a non-None value')
    
    def __eq__(self, other):
        is_equal = False
        if isinstance(other, pbItem):
            is_equal = (other.name == self.name)
        return is_equal
    
    def __hash__(self):
        return hash(self.name)
        
    def __repr__(self):
        return self.name