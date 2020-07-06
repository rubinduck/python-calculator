import core

def test_tokenizer():
	get_tokens = core.get_tokens
	assert get_tokens("1+2") == ["1","+","2"]
	assert get_tokens("   1 +2") == ["1","+","2"]
	assert get_tokens("   1 + 2   ") == ["1","+","2"]
	assert get_tokens("   1.0 + 2   ") == ["1.0","+","2"]
	assert get_tokens("1.0 + 2.0") == ["1.0","+","2.0"]
	assert get_tokens("1.48 + 2.69843") == ["1.48","+","2.69843"]


	assert get_tokens("1-2") == ["1","-","2"]
	assert get_tokens("   1 -2") == ["1","-","2"]
	assert get_tokens("   1 - 2   ") == ["1","-","2"]
	assert get_tokens("   1.0 - 2   ") == ["1.0","-","2"]
	assert get_tokens("1.0 - 2.0") == ["1.0","-","2.0"]
	assert get_tokens("1.48 - 2.69843") == ["1.48","-","2.69843"]

	assert get_tokens("1/2") == ["1","/","2"]
	assert get_tokens("   1 /2") == ["1","/","2"]
	assert get_tokens("   1 / 2   ") == ["1","/","2"]
	assert get_tokens("   1.0 / 2   ") == ["1.0","/","2"]
	assert get_tokens("1.0 / 2.0") == ["1.0","/","2.0"]
	assert get_tokens("1.48 / 2.69843") == ["1.48","/","2.69843"]

	assert get_tokens("1*2") == ["1","*","2"]
	assert get_tokens("   1 *2") == ["1","*","2"]
	assert get_tokens("   1 * 2   ") == ["1","*","2"]
	assert get_tokens("   1.0 * 2   ") == ["1.0","*","2"]
	assert get_tokens("1.0 * 2.0") == ["1.0","*","2.0"]
	assert get_tokens("1.48 * 2.69843") == ["1.48","*","2.69843"]

	assert get_tokens("5*(4 -12.3)") == ["5","*","(","4","-","12.3",")"]
	assert get_tokens("(4*4)+4.5") == ['(','4','*','4',')','+','4.5']

	print("tokenizer test succeeded")

def test_rpn_convertor():
	convert = core.convert_to_rpn

	assert convert(["1","+","2"]) == [1,2,"+"]
	assert convert(["15.37","+","2.8"]) == [15.37,2.8,"+"]
	assert convert(["2","*","3","+","4"]) == [2,3,"*",4,"+"]
	assert convert(["2","*","(","3","+","4",")"]) == [2,3,4,"+","*"]
	assert convert(["5","/","(","35","*","8.7",")"]) == [5,35,8.7,"*","/"]

	print("rpn-convertor test succeeded")




def run_core_tests():
	test_tokenizer()
	test_rpn_convertor()

if __name__ == "__main__":
	import sys, os
	os.chdir(os.path.abspath(os.path.dirname(__file__)))
	run_tests()