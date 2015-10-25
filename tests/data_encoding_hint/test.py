import os
import pbPlist

tests_path = os.path.join(TEST_DIRECTORY, 'test.plist')
output_path = os.path.join(TEST_DIRECTORY, 'output.plist')

try:
    test_input = pbPlist.PBPlist(tests_path)
    test_input.write(output_path)
    test_output = pbPlist.PBPlist(output_path)
    
    input_items = test_input.root
    output_items = test_output.root
    
    if not (input_items == output_items):
        raise Exception
    
except:
    print('Test failure!')
    raise