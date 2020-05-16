import os

nbr_test = 0
nbr_success = 0
nbr_error = 0
logs = ''

def test(filename, expecting):
	global nbr_test
	global nbr_success
	global nbr_error
	global logs
	os.system('python ../../test/main.py ' + filename + ' test > output')
	f = open('output', 'r')
	content = f.read().strip()
	f.close()
	if (content != expecting):
		nbr_error += 1
		logs += filename + '\n'
		logs += 'got: ' + content + '\n'
		logs += 'expected: ' + expecting + '\n\n'
	else:
		nbr_success += 1
	nbr_test += 1

if __name__ == "__main__":
	test('test1.txt', '1111')
	test('test2.txt', '1101')

	test('test3.txt', '0')
	test('test4.txt', '1')
	test('test5.txt', '1')
	test('test6.txt', '1')

	test('test7.txt', '0')
	test('test8.txt', '1')
	test('test9.txt', '1')
	test('test10.txt', '0')

	test('test11.txt', '0')
	test('test12.txt', '1')
	test('test13.txt', '0')
	test('test14.txt', '0')

	test('test15.txt', '0')
	test('test16.txt', '1')
	test('test17.txt', '1')
	test('test18.txt', '1')

	test('test19.txt', '0')
	test('test20.txt', '1')
	test('test21.txt', '0')
	test('test22.txt', '0')
	test('test23.txt', '1')
	test('test24.txt', '1')
	test('test25.txt', '0')
	test('test26.txt', '0')
	test('test27.txt', '0')
	test('test28.txt', '1')
	test('test29.txt', '1')

	test('test30.txt', '12222')
	test('test31.txt', '000')
	test('test32.txt', '100')
	test('test33.txt', '110')
	test('test34.txt', '12222')

	test('test35.txt', '1')
	test('test36.txt', '0')
	test('test37.txt', '0')
	test('test38.txt', '0')
	test('test39.txt', '1')

	f = open('logs', 'w')
	f.close()
	f = open('logs', 'w')
	f.write(logs)
	f.close()
	os.remove('output')
	print(str(nbr_success) + '/' + str(nbr_test))
