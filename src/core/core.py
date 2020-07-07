"""
supported operations : +, - , *, /, (),
integers and floating-point numbers with '.' is supported
operations precedence:
1: +, -
2: *, /
3: ()      
"""

DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
ONE_CHARACTER_TOKENS = ['+','-','*','/','(',')']
OPERATIONS = ['+','-','*','/']
IGNORED_CHARS = [' ']

PRECEDENCE = {'+':1,'-':1,
              '*':2,'/':2,
              "(":3,")":3}

UNARY_OPERATIONS = []
BINARY_OPERATIONS = ['+','-','*','/']
OPERATION_REALISATIONS = {"+":lambda x,y:x+y,
                          "-":lambda x,y:x-y,
                          "*":lambda x,y:x*y,
                          "/":lambda x,y:x/y}

ASSOCIATIVITY = {'+':"left",'-':"left",
                 '*':"left",'/':"left"}
 

def get_tokens(expression:str) -> list:
    """
    function converting expression to the list of tokens
    for futher work with them
    """
    function converting 
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
            raise ValueError(f"{ch} is not a valid character")
    convert_string_numbers_to_actual_one(tokens)
    return tokens


def convert_string_numbers_to_actual_one(tokens_list):
    """
    function replaces string representationg of tokens with
    python int or float one
    """
    for index in range(len(tokens_list)):
        token = tokens_list[index]
        if str_is_number(token):
            if "." in token:
                token = float(token)
            else:
                token = int(token)
        tokens_list[index] = token

           
def str_is_number(token):
    """
    function returns True if token is str, representing number
    int or float in python format
    """
    # function is based on restrictions of get_tokens result
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
            while (len(operator_stack) != 0) and\
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
    return type(token) == int or type(token) == float

def is_function(token):
    # temp mock, while there are no functions
    return False

def is_operation(token):
    return token in OPERATIONS


def evalute(rpn_expression) -> float:
    """
    function evaluating expression in RPN form
    in:list of operations and arguments in RPN
    out: expression evaluation value
    mutates rpn_expression argument
    """
    while len(rpn_expression) != 1:
        index = 0
        while not is_operation(rpn_expression[index]):
            index += 1
        operation = rpn_expression[index]
        operation_realization = OPERATION_REALISATIONS[operation]
        if operation in BINARY_OPERATIONS:
            arguments = (rpn_expression[index-2],rpn_expression[index-1])
            calculation_result = [operation_realization(*arguments)]
            rpn_expression[index - 2: index + 1] = calculation_result
        elif operation in UNARY_OPERATIONS:
            arguments = (rpn_expression[index - 1])
            calculation_result = [operation_realization(*arguments)]
            rpn_expression[index - 1:index + 1] = calculation_result
    
    return rpn_expression[0]

