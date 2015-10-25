import string_helper as StrParse

def PushIndent(indent_level):
    return indent_level + 1

def PopIndent(indent_level):
    return indent_level - 1

def WriteNewline(level=0):
    output = '\n'
    for index in range(level):
        output += '\t'
    return output

class pbItem(object):
    indentLevel = 0
    
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
        if other != None:
            can_compare_types = False
            if type(other) == str:
                other = pbItemResolver(other, 'qstring')
            if self.type_name == 'string' or self.type_name == 'qstring':
                can_compare_types = (other.type_name == 'string' or other.type_name == 'qstring')
            else:
                can_compare_types = (other.type_name == self.type_name)
            if can_compare_types == True:
                is_equal = (other.value == self.value)
        return is_equal
    
    def __hash__(self):
        return hash(self.value)
        
    def __repr__(self):
        return self.value
    
    def __iter__(self):
        return iter(self.value)
    
    def __getattr__(self, attrib):
        return getattr(self.value, attrib)
   
    def __str__(self):
        return self.writeString(0, False)[0]

    def __getitem__(self, key):
        return self.value.__getitem__(key)

    def __setitem__(self, key, value):
        self.value.__setitem__(key, value)
    
    def __len__(self):
        return len(self.value)
    
    def __contains__(self, item):
        return self.value.__contains__(item)
    
    def writeString(self, indent_level=0, pretty=True):
        message = 'This is a base class, it cannot write!'
        raise Exception(message)
    
    def writeAnnotation(self):
        output_string = ''
        if self.annotation != None and len(self.annotation) > 0:
            output_string += ' '
            output_string += '/*'
            output_string += self.annotation
            output_string += '*/'
        return output_string

class pbString(pbItem):
    def writeString(self, indent_level=0, pretty=True):
        string_string = ''
        string_string += self.value
        if pretty == True:
            string_string += self.writeAnnotation()
        return (string_string, indent_level)
    
class pbQString(pbItem):
    def writeString(self, indent_level=0, pretty=True):
        qstring_string = ''
        qstring_string += '"'
        for character in self.value:
            qstring_string += StrParse.SanitizeCharacter(character)
        qstring_string += '"'
        if pretty == True:
            qstring_string += self.writeAnnotation()
        return (qstring_string, indent_level)
        
class pbData(pbItem):
    def writeString(self, indent_level=0, pretty=True):
        data_string = ''
        indent_level = PushIndent(indent_level)
        data_string += '<'
        grouping_byte_counter = 0
        grouping_line_counter = 0
        for hex_byte in map(ord, self.value.decode()):
            data_string += format(hex_byte, 'x')
            grouping_byte_counter += 1
            # write a space every 4th byte
            if grouping_byte_counter == 4:
                data_string += ' '
                grouping_byte_counter = 0
                grouping_line_counter += 1
            # write a newline every 4th grouping of bytes
            if grouping_line_counter == 4:
                data_string += WriteNewline(indent_level)
                data_string += ' ' # indent an additional space to make the byte groupings line up
                grouping_line_counter = 0
        data_string += '>'
        if pretty == True:
            data_string += self.writeAnnotation()
        indent_level = PopIndent(indent_level)
        return (data_string, indent_level)

class pbDictionary(pbItem):
    def writeString(self, indent_level=0, pretty=True):
        dictionary_string = ''
        dictionary_string += '{'
        dictionary_string += WriteNewline(indent_level)
        indent_level = PushIndent(indent_level)
        keys_array = list(self.value.keys())
        if len(keys_array) == 0:
            indent_level = PopIndent(indent_level)
        else:
            dictionary_string += '\t'
            for key in keys_array:
                write_string, indent_level = key.writeString(indent_level, pretty)
                dictionary_string += write_string
                dictionary_string += ' = '
                write_string, indent_level = self.value[key].writeString(indent_level, pretty)
                dictionary_string += write_string
                dictionary_string += ';'
                if key == keys_array[-1]:
                    indent_level = PopIndent(indent_level)
                dictionary_string += WriteNewline(indent_level)
        dictionary_string += '}'
        return (dictionary_string, indent_level)

class pbArray(pbItem):
    def writeString(self, indent_level=0, pretty=True):
        array_string = ''
        array_string += '('
        array_string += WriteNewline(indent_level)
        indent_level = PushIndent(indent_level)
        values_array = list(self.value)
        if len(values_array) == 0:
            indent_level = PopIndent(indent_level)
        else:
            array_string += '\t'
            for value in values_array:
                write_string, indent_level = value.writeString(indent_level, pretty)
                array_string += write_string
                if value != values_array[-1]:
                    array_string += ','
                else:
                    indent_level = PopIndent(indent_level)
                array_string += WriteNewline(indent_level)
        array_string += ')'
        return (array_string, indent_level)

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