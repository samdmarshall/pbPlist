import os
import pbPlist

tests_path = os.path.join(TEST_DIRECTORY, 'test.plist')
output_path = os.path.join(TEST_DIRECTORY, 'output.plist')

try:
    test_input = pbPlist.PBPlist(tests_path)
    test_input.write(output_path)
    test_output = pbPlist.PBPlist(output_path)
    
    if not test_input.string_encoding == 'UTF8':
        raise Exception
    
    if not test_output.string_encoding == 'UTF8':
        raise Exception
    
    if not test_input.string_encoding == test_output.string_encoding:
        raise Exception
    
    if not len(test_input.root) == 0:
        raise Exception
        
    if not len(test_output.root) == 0:
        raise Exception
    
    if not (len(test_input.root) == len(test_output.root)):
        raise Exception
except:
    raise