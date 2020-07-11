"""
Core calculator module, providing logic for parsing, converting and evaluating
expressions

operations ::= + | - | * | / | ()
float ::= [<interger part>].<floating part> 
numbers ::= [-]<int> | <float>

operations precedence:
1: +, -
2: *, /
3: ()      
"""

from decimal import Decimal

DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
ONE_CHARACTER_TOKENS = ['+','-','*','/','(',')']
OPERATIONS = ['+','-','*','/']
IGNORED_CHARS = [' ']

PRECEDENCE = {'+':1,'-':1,
              '*':2,'/':2,
              "(":3,")":3}

UNARY_OPERATIONS = []
BINARY_OPERATIONS = ['+','-','*','/']

OPERATION_REALIZATIONS = {"+":lambda x,y:x+y,
                          "-":lambda x,y:x-y,
                          "*":lambda x,y:x*y,
                          "/":lambda x,y:x/y}

ASSOCIATIVITY = {'+':"left",'-':"left",
                 '*':"left",'/':"left"}
 

def get_tokens(expression:str) -> list:
    """
    function converting expression to the list of tokens for 
    futher work with them
    """
    tokens = []

    for ch in expression:
        if ch in IGNORED_CHARS:
            continue
        elif ch in ONE_CHARACTER_TOKENS:
            tokens.append(ch)
        elif ch in DIGITS:
            if len(tokens) == 0:
                tokens.append(ch)
            elif tokens[-1][-1] in DIGITS or tokens[-1][-1] == '.':
                tokens[-1] += ch
            else:
                tokens.append(ch)
        elif ch == '.':
            if len(tokens) == 0:
                tokens.append(ch)
            elif tokens[-1][-1] in DIGITS:
                if '.' not in tokens[-1]:
                    tokens[-1] += '.'
                else:
                    raise ValueError("two . is not allowed in number")
            else:
                tokens.append(ch)
        else:
            raise ValueError(f"{ch} is not a valid character")

    tokens = convert_string_numbers_to_decimal(tokens)
    return tokens


def convert_string_numbers_to_decimal(tokens_list):
    """
    function replacing string representationg of tokens with Decimal
    and appling unary "-" operator (joining "-" to numbers) 
    """
    tokens_list = tokens_list[:]
    for index in range(len(tokens_list)):
        token = tokens_list[index]
        if str_is_number(token):
            token = Decimal(token)
            tokens_list[index] = token

    index = 0
    while index < len(tokens_list):
        token = tokens_list[index]
        if (token == "-") and\
           (index == 0 or tokens_list[index - 1] in OPERATIONS) and\
           (type(tokens_list[index + 1]) == Decimal):
           tokens_list[index:index+2] = [-tokens_list[index+1]]
        index += 1

    return tokens_list

           
def str_is_number(token):
    """
    function returns True if token is str, representing number
    int or float in python format
    """
    for ch in token:
        if ch not in DIGITS and ch != ".":
            return False
    return True


def convert_to_rpn(tokens_list) -> list:
    """
    function converting list of tokens to expression in Reverse Polish Nonation
    using Shunting-yard algorithm
    """
    output_list = []
    operator_stack = []
    while len(tokens_list) != 0:
        token = tokens_list.pop(0)
        if is_number(token):
            output_list.append(token)
        elif is_function(token):
            pass
        elif is_operation(token):
            while len(operator_stack) != 0 and\
                  (((PRECEDENCE[operator_stack[-1]] > PRECEDENCE[token]) or\
                   (PRECEDENCE[operator_stack[-1]] == PRECEDENCE[token] and ASSOCIATIVITY[token] == "left")) and\
                  (operator_stack[-1] != "(")):
                output_list.append(operator_stack.pop())
            operator_stack.append(token)
        elif token == "(":
            operator_stack.append(token)
        elif token == ")":
            try:
                while operator_stack[-1] != "(":
                    output_list.append(operator_stack.pop())
            except IndexError:
                raise ValueError("there is not closed parenthesis")
            operator_stack.pop()
        else:
            raise ValueError(f"{token} is not a valid token")

    while len(operator_stack) != 0:
        output_list.append(operator_stack.pop())
    return output_list    



def is_number(token):
    return type(token) == Decimal

def is_function(token):
    # temp mock, while there are no functions
    return False

def is_operation(token):
    return token in OPERATIONS


def evaluate(rpn_expression:list) -> Decimal:
    """
    function evaluating expression in RPN form
    in:list of operations and arguments in RPN
    out: expression evaluation value
    """
    rpn_expression = rpn_expression[:]
    while len(rpn_expression) != 1:
        index = 0
        while not is_operation(rpn_expression[index]):
            index += 1

        # after exracting arguments for some operation, algorithm replaces
        # place where were operation and arguments with operation(*arguments)
        operation = rpn_expression[index]
        operation_realization = OPERATION_REALIZATIONS[operation]
        if operation in BINARY_OPERATIONS:
            # without this check index - 2 can give -2 or -1 for index = 0,1
            # but in python -2 and -1 is valid index, so we need catch it here
            if index < 2:
                raise ValueError(f"Binary operation {operation} wihtout enough arguments")
            arguments = (rpn_expression[index-2],rpn_expression[index-1])
            calculation_place = slice(index - 2,index +1)
        elif operation in UNARY_OPERATIONS:
            arguments = (rpn_expression[index - 1])
            calculation_place = slice(index - 1,index +1)

        calculation_value = [operation_realization(*arguments)]
        rpn_expression[calculation_place] = calculation_value

    return rpn_expression[0]


def calculate_expression(expression:str) -> Decimal:
    return evaluate(convert_to_rpn(get_tokens(expression)))