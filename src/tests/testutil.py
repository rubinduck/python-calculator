def test(function,arguments_result_list,one_argument_function=False):
	"""
	testing function
	for every (arguments,expected_result) pair in arguments_result_list
	checks if function(arguments) == result
	"""
	for args,expected_result in arguments_result_list:
		if one_argument_function:
			args = [args]
		call_result= function(*args)
		if call_result != expected_result:
			exception_message = f"function {function.__name__} returned {call_result} instaed of {expected_result} for aguments:{args}"
			raise AssertionError(exception_message)