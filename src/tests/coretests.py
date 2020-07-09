if __name__ == "__main__":
	import sys, os
	dirname=os.path.dirname
	path = dirname(dirname(__file__))
	sys.path.append(path)
	import testutil


import core
from . import testutil
from decimal import Decimal

def test_tokenizer():

	expecations = [
				   (("   1 +2",),		 [1,"+",2]),
				   (("   1 + 2   ",),	 [1,"+",2]),
				   (("   1.0 + 2   ",),  [1.0,"+",2]),
				   (("1.0 + 2.0",),		 [1.0,"+",2.0]),
				   (("1.48 + 2.69843",), [1.48,"+",2.69843]),

				   (("   1 -2",),		 [1,"-",2]),
				   (("   1 - 2   ",),	 [1,"-",2]),
				   (("   1.0 - 2   ",),  [1.0,"-",2]),
				   (("1.0 - 2.0",),		 [1.0,"-",2.0]),
				   (("1.48 - 2.69843",), [1.48,"-",2.69843]),

				   (("   1 *2",),		 [1,"*",2]),
				   (("   1 * 2   ",),	 [1,"*",2]),
				   (("   1.0 * 2   ",),  [1.0,"*",2]),
				   (("1.0 * 2.0",),		 [1.0,"*",2.0]),
				   (("1.48 * 2.69843",), [1.48,"*",2.69843]),

				   (("   1 /2",),		 [1,"/",2]),
				   (("   1 / 2   ",),	 [1,"/",2]),
				   (("   1.0 / 2   ",),  [1.0,"/",2]),
				   (("1.0 / 2.0",),		 [1.0,"/",2.0]),
				   (("1.48 / 2.69843",), [1.48,"/",2.69843]),

				   (("5*(4 -12.3)",),	 [5,"*","(",4,"-",12.3,")"]),
				   (("(4*4)+4.5",),		 ['(',4,'*',4,')','+',4.5])				   				   				   

	]
	expecations = [(i,_to_decimal(j)) for i,j in expecations]

	get_tokens = core.get_tokens
	testutil.test(get_tokens,expecations)

	print("tokenizer test succeeded")

def test_rpn_convertor():

	expecations = [
				   (([1,"+",2],),				   [1,2,"+"]),
				   (([15.37,"+",2.8],),			   [15.37,2.8,"+"]),
				   (([2,"*",3,"+",4],),			   [2,3,"*",4,"+"]),
				   (([2,"*","(",3,"+",4,")"],),	   [2,3,4,"+","*"]),
				   (([5,"/","(",35,"*",8.7,")"],), [5,35,8.7,"*","/"]),
	]
	expecations = [((_to_decimal(i[0]),),_to_decimal(j)) for i,j in expecations]

	convert = core.convert_to_rpn
	testutil.test(convert,expecations)

	print("rpn-convertor test succeeded")


def test_evaluator():
	evaluate = core.evaluate

	expecations = [(([2,2,"+"],),4),
				   (([5,3,"-"],),2),
				   (([2,2,2,"*","+"],),6),
				   (([2,2,2,"+","*"],),8),
				   (([5,10,2,"/","/"],),1),
				   (([45.8,75.3,8,6,"/","*","-"],),(-54.6)),
				   (([-1,-1,"*"],),1,)]
	expecations = [((_to_decimal(i[0]),),Decimal(str(j))) for i,j in expecations]

	testutil.test(evaluate,expecations)
	print("evaluator test succeded")

def _to_decimal(input_list) -> list:
	input_list = input_list[:]
	for i in range(len(input_list)):
		if type(input_list[i]) == int or type(input_list[i]) == float:
			input_list[i] = Decimal(str(input_list[i]))
	return input_list




def run_core_tests():
	test_tokenizer()
	test_rpn_convertor()
	test_evaluator()

if __name__ == "__main__":
	run_core_tests()