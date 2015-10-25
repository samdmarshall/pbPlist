import os
import pbPlist

tests_path = os.path.join(TEST_DIRECTORY, 'test.plist')
output_path = os.path.join(TEST_DIRECTORY, 'output.plist')

try:
    test_input = pbPlist.PBPlist(tests_path)
    test_input.write(output_path)
    test_output = pbPlist.PBPlist(output_path)
    
    input_items = test_input.root
    if not input_items[0] == 'hello world!':
        raise Exception
    if not input_items[1] == 'this is a test':
        raise Exception
    if not input_items[2] == 'Of quoted strings':
        raise Exception
        
    output_items = test_output.root
    if not output_items[0] == 'hello world!':
        raise Exception
    if not output_items[1] == 'this is a test':
        raise Exception
    if not output_items[2] == 'Of quoted strings':
        raise Exception
    
    if not input_items[0] == output_items[0]:
        raise Exception
    if not input_items[1] == output_items[1]:
        raise Exception
    if not input_items[2] == output_items[2]:
        raise Exception
    
    if not (input_items == output_items):
        raise Exception
    
except:
    print('Test failure!')
    raise