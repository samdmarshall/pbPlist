import os
import pbPlist

tests_path = os.path.join(TEST_DIRECTORY, 'test.plist')
output_path = os.path.join(TEST_DIRECTORY, 'output.plist')

try:
    test_input = pbPlist.PBPlist(tests_path)
    test_input.write(output_path)
    test_output = pbPlist.PBPlist(output_path)
    
    input_encoding_hint = 'UTF8'
    if not test_input.string_encoding == input_encoding_hint:
        print(u'\U0001F4A5 [INPUT] Expected encoding hint "%s", found "%s"' % (input_encoding_hint, test_input.string_encoding))
        raise Exception
    
    output_encoding_hint = 'UTF8'
    if not test_output.string_encoding == output_encoding_hint:
        print(u'\U0001F4A5 [OUTPUT] Expected encoding hint "%s", found "%s"' % (output_encoding_hint, test_output.string_encoding))
        raise Exception
    
    if not test_input.string_encoding == test_output.string_encoding:
        print(u'\U0001F4A5 [CMP] Mismatch encoding hints from INPUT "%s" and OUTPUT "%s"' % (test_input.string_encoding, test_output.string_encoding))
        raise Exception
    
    input_expected_length = 0
    if not len(test_input.root) == input_expected_length:
        print(u'\U0001F4A5 [INPUT] Expected length to be "%i", found "%i"' % (input_expected_length, len(test_input.root)))
        raise Exception
        
    output_expected_length = 0
    if not len(test_output.root) == output_expected_length:
        print(u'\U0001F4A5 [OUTPUT] Expected length to be "%i", found "%i"' % (output_expected_length, len(test_output.root)))
        raise Exception
    
    if not (len(test_input.root) == len(test_output.root)):
        print(u'\U0001F4A5 [CMP] Mismatch expected length from INPUT "%i" and OUTPUT "%i"' % (len(test_input.root), len(test_output.root)))
        raise Exception
except:
    raise