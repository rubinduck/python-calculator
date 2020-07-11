def test(function,arguments_result_list,one_argument_function=False):
	"""
	testing function
	for every (arguments,result) pair in arguments_result_list
	checks if function(arguments) == result
	"""
	for args,result in arguments_result_list:
		if one_argument_function:
			args = [args]
		if function(*args) != result:
			actual_result = function(*args)
			exception_message = f"function {function.__name__} returned {actual_result} instaed of {result} for aguments:{args}"
			raise AssertionError(exception_message)