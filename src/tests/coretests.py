if __name__ == "__main__":
    import sys, os
    dirname = os.path.dirname
    path = dirname(dirname(__file__))
    sys.path.append(path)
    import testutil


import core
from . import testutil
from decimal import Decimal


def test_tokenizer():

    expecations = [
                   (("   1 +2",),         [1,"+",2]),
                   (("   1 + 2   ",),     [1,"+",2]),
                   (("   1.0 + 2   ",),   [1.0,"+",2]),
                   (("1.0 + 2.0",),       [1.0,"+",2.0]),
                   (("1.48 + 2.69843",),  [1.48,"+",2.69843]),

                   (("   1 -2",),         [1,"-",2]),
                   (("   1 - 2   ",),     [1,"-",2]),
                   (("   1.0 - 2   ",),   [1.0,"-",2]),
                   (("1.0 - 2.0",),       [1.0,"-",2.0]),
                   (("1.48 - 2.69843",),  [1.48,"-",2.69843]),

                   (("   1 *2",),         [1,"*",2]),
                   (("   1 * 2   ",),     [1,"*",2]),
                   (("   1.0 * 2   ",),   [1.0,"*",2]),
                   (("1.0 * 2.0",),       [1.0,"*",2.0]),
                   (("1.48 * 2.69843",),  [1.48,"*",2.69843]),

                   (("   1 /2",),         [1,"/",2]),
                   (("   1 / 2   ",),     [1,"/",2]),
                   (("   1.0 / 2   ",),   [1.0,"/",2]),
                   (("1.0 / 2.0",),       [1.0,"/",2.0]),
                   (("1.48 / 2.69843",),  [1.48,"/",2.69843]),

                   (("5*(4 -12.3)",),     [5,"*","(",4,"-",12.3,")"]),
                   (("(4*4)+4.5",),       ['(',4,'*',4,')','+',4.5]),

                   (("   sin(1)/2",),     ["sin","(",1,")","/",2]),
                   (("5*atan7 + 3",),     [5,"*","atan",7,"+",3])
    ]
    expecations = [(i, _to_decimal(j)) for i, j in expecations]

    get_tokens = core.get_tokens
    testutil.test(get_tokens, expecations)

    print("tokenizer test succeeded")


def test_rpn_convertor():

    expecations = [
                   (([1,"+",2],),                  [1,2,"+"]),
                   (([15.37,"+",2.8],),            [15.37,2.8,"+"]),
                   (([2,"*",3,"+",4],),            [2,3,"*",4,"+"]),
                   (([2,"*","(",3,"+",4,")"],),    [2,3,4,"+","*"]),
                   (([5,"/","(",35,"*",8.7,")"],), [5,35,8.7,"*","/"]),
                   ((["sin","(",1,")","/",2],),    [1,"sin",2,"/"]),
                   (([5,"*","atan",7,"+",3],),     [5,7,"atan","*",3,"+"])
    ]
    expecations = [((_to_decimal(i[0]),), _to_decimal(j)) for i, j in expecations]

    convert = core.convert_to_rpn
    testutil.test(convert, expecations)

    print("rpn-convertor test succeeded")


def test_evaluator():
    # wrapper is used becouse python support only float with 16 digits after .
    # at least is seams so
    def evaluate_wrapper(*args, **kargs):
        return round(core.evaluate(*args, **kargs), 17)
    evaluate = evaluate_wrapper

    expecations = [(([2,2,"+"],),4),
                   (([5,3,"-"],),2),
                   (([2,2,2,"*","+"],),6),
                   (([2,2,2,"+","*"],),8),
                   (([5,10,2,"/","/"],),1),
                   (([45.8,75.3,8,6,"/","*","-"],),(-54.6)),
                   (([-1,-1,"*"],),1,),
                   (([5,"sin"],),-0.95892427466313846889),
                   ((([5,7,"*","atan"],),1.54223266895613662476)),
                   (([3.3,"cos",7,5,"+","/"],),-0.0822899808257387403280492542)
                   ]
    expecations = [((_to_decimal(i[0]),),Decimal(str(j))) for i,j in expecations]

    testutil.test(evaluate,expecations)
    print("evaluator test succeded")


def test_calculation():
    # wrapper is used becouse python support only float with 16 digits after .
    # at least is seams so
    def calculate_wrapper(*args, **kargs):
        return round(core.calculate_expression(*args, **kargs), 17)
    calculate = calculate_wrapper

    expecations = [("1+2",3),
                   ("-8.5 + -5.18",-13.68),
                   ("8.7 + -5",3.7),
                   ("-2 - -3",1),
                   ("58 - 23",35),
                   ("58 - - 23",81),
                   ("-5.7 - 3",-8.7),
                   ("54*128",6912),
                   ("-3*-4",12),
                   ("-6.2 * 3",-18.6),
                   ("1/2",0.5),
                   ("-5/-8",0.625),
                   ("-78/0.2",-390),
                   ("78/-0.2",-390),
                   ("0/58",0),
                   ("2+2*2",6),
                   ("(2+2)*2",8),
                   ("2 + 8 / 5 * 8",14.8),
                   ("5*cos(44)+7.34",12.33921654323845610034504508318928015915829569759546),
                   ("8/5+acos(1)",1.6),
                   ]

    expecations = [(i, Decimal(str(j))) for i, j in expecations]

    testutil.test(calculate, expecations, one_argument_function=True)
    print("expression calculation test succeded")


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
    test_calculation()


if __name__ == "__main__":
    run_core_tests()
