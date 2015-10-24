import os

import pbPlist

tests_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tests')

for subdir, dirs, files in os.walk(tests_path):
    for test_case in dirs:
        test_case_directory = os.path.join(tests_path, test_case)
        test_case_plist_path = os.path.join(test_case_directory, 'test.plist')
        print('Running test "'+test_case+'"...')
        try:
            plist = pbPlist.PBPlist(test_case_plist_path)
            print(plist.root)
        except:
            print('Test failure on test "'+test_case+'"!')
            raise