import os

tests_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tests')

test_count = 0
test_failures = 0
test_success = 0

for subdir, dirs, files in os.walk(tests_path):
    for test_case in dirs:
        test_case_directory = os.path.join(tests_path, test_case)
        test_case_path = os.path.join(test_case_directory, 'test.py')
        if os.path.exists(test_case_path):
            test_count += 1
            print('Running test "'+test_case+'"...')
            try:
                execfile(test_case_path, {"TEST_DIRECTORY": test_case_directory})
                test_success += 1
                print(u'\u2705 Test Passed!')
            except:
                test_failures +=1
                print(u'\U0001F6AB Test Failed!')
                pass

test_percent = (float(test_success) / float(test_count)) * 100
results_string = str(test_success)+'/'+str(test_count)+' Tests Passed, '+str(test_percent)+'%'
print('='*len(results_string))
print(results_string)