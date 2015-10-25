import os

tests_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tests')

for subdir, dirs, files in os.walk(tests_path):
    for test_case in dirs:
        test_case_directory = os.path.join(tests_path, test_case)
        test_case_path = os.path.join(test_case_directory, 'test.py')
        if os.path.exists(test_case_path):
            print('Running test "'+test_case+'"...')
            execfile(test_case_path, {"TEST_DIRECTORY": test_case_directory}) 