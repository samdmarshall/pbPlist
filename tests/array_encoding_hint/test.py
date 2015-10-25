import os
import pbPlist

tests_path = os.path.join(TEST_DIRECTORY, 'test.plist')
output_path = os.path.join(TEST_DIRECTORY, 'output.plist')

try:
    test_input = pbPlist.PBPlist(tests_path)
    test_input.write(output_path)
    test_output = pbPlist.PBPlist(output_path)
    
    if not len(test_input.root) == 0:
        raise Exception
        
    if not len(test_output.root) == 0:
        raise Exception
    
    if not (len(test_input.root) == len(test_output.root)):
        raise Exception
except:
    print('Test failure!')
    raise