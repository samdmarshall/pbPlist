class pbItem(object):
    
    def __init__(self, value=None, type_name=None, annotation=None):
        if value != None and type_name != None:
            self.value = value
            if type_name not in KnownTypes.keys():
                message = 'Unknown type "'+type_name+'" passed to '+self.__class__.__name__+' initializer!'
                raise TypeError(message)
            self.type_name = type_name
            self.annotation = annotation
        else:
            message = 'The class "'+self.__class__.__name__+'" must be initialized with a non-None value'
            raise ValueError(message)
    
    def __eq__(self, other):
        is_equal = False
        if isinstance(other, pbItem) and other.type_name == self.type_name:
            is_equal = (other.value == self.value)
        return is_equal
    
    def __hash__(self):
        return hash(self.value)
        
    def __repr__(self):
        return self.value
    
    def writeString(self):
        message = 'This is a base class, it cannot write!'
        raise Exception(message)
    
    def writeAnnotation(self):
        output_string = ''
        if self.annotation != None:
            output_string += ' '
            output_string += '/* '
            output_string += self.annotation
            output_string += ' */'
        return output_string

class pbString(pbItem):
    def writeString(self):
        string_string = ''
        string_string += self.value
        string_string += self.writeAnnotation()
        return string_string
    
class pbQString(pbItem):
    def writeString(self):
        qstring_string = ''
        qstring_string += '"'
        qstring_string += self.value
        qstring_string += '"'
        qstring_string += self.writeAnnotation()
        return qstring_string
        
class pbData(pbItem):
    def writeString(self):
        data_string = ''
        data_string += '<'
        for hex_byte in map(ord, self.value.decode()):
            data_string += format(hex_byte, 'x')
        data_string += '>'
        data_string += self.writeAnnotation()
        return data_string

class pbDictionary(pbItem):
    def writeString(self):
        dictionary_string = ''
        dictionary_string += '{\n'
        for key in self.value:
            dictionary_string += '\t'
            dictionary_string += key.name.writeString()
            dictionary_string += ' = '
            dictionary_string += self.value[key].writeString()
            dictionary_string += ';\n'
        dictionary_string += '}\n'
        return dictionary_string

class pbArray(pbItem):
    def writeString(self):
        array_string = ''
        array_string += '(\n'
        for value in self.value:
            array_string += '\t'
            array_string += value.writeString()
            array_string += ',\n'
        array_string += ')\n'
        return array_string

KnownTypes = {
    'string': pbString,
    'qstring': pbQString,
    'data': pbData,
    'dictionary': pbDictionary,
    'array': pbArray,
}

def pbItemResolver(obj, type_name):
    initializer = KnownTypes[type_name]
    if initializer != None:
        return initializer(obj, type_name)
    else:
        message = 'Unknown type "'+type_name+'" passed to pbItemResolver!'
        raise TypeError(message)