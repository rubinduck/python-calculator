"""
Core calculator module, providing logic for parsing, converting, evaluating and
formating expression

Some expression structure in BNF form:
operations ::= + | - | * | / | () | ^
functions ::= sin | cos | tan | asin | acos | atan| sqrt
constants ::= pi | e

<number> ::= <cofficeint>[<exponent>]
<cofficeint> ::= [<sign>]<int>[<fraction>] | [<sign>]<fraction>
<sign> ::= + | -
<int> ::= <digit>[<int>]
<digit> ::= 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
<fraction> ::= .<int>
<exponent> ::= E[<sign>]<int>

operations precedence:
1: +, -
2: *, /, ^
3: ()
4:functions
"""


import string
import decimal

from enum import Enum
from typing import Tuple

from decimal import Decimal
from math import sin, cos, tan, asin, acos, atan, sqrt
from math import pi, e

DIGITS = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}

OPERATIONS = {'+', '-', '*', '/', '^'}
FUNCTIONS = ["sin", "cos", "tan", "asin", "acos", "atan", "sqrt"]

CONSTANTS = {"pi": Decimal(str(pi)),
             "e":  Decimal(str(e))}

# simple operations is operations what can be parsed regardless of context
# used in get_tokens. Don't include '+' and '-' becouse number can have them
SIMPLE_OPERATIONS = (OPERATIONS | {'(', ')'}) - {'+', '-'}
NUMBER_START_CHARS = {'+', '-', '.'} | DIGITS
IGNORED_CHARS = [' ']


PRECEDENCE = {'+': 1, '-': 1,
              '*': 2, '/': 2, '^': 2,
              "(": 3, ")": 3,
              **dict.fromkeys(FUNCTIONS, 4)}

UNARY_OPERATIONS = FUNCTIONS[:]
BINARY_OPERATIONS = OPERATIONS.copy()

TRIGONOMETRIC_FUNCTIONS = {"sin": lambda x: Decimal(str(sin(x))),
                           "cos": lambda x: Decimal(str(cos(x))),
                           "tan": lambda x: Decimal(str(tan(x))),
                           "asin": lambda x: Decimal(str(asin(x))),
                           "acos": lambda x: Decimal(str(acos(x))),
                           "atan": lambda x: Decimal(str(atan(x))),
                           "sqrt": lambda x: Decimal(str(sqrt(x)))}

OPERATION_REALIZATIONS = {"+": lambda x, y: x + y,
                          "-": lambda x, y: x - y,
                          "*": lambda x, y: x * y,
                          "/": lambda x, y: x / y,
                          '^': lambda x, y: x**y}
OPERATION_REALIZATIONS.update(TRIGONOMETRIC_FUNCTIONS)

ASSOCIATIVITY = {'+': "left", '-': "left",
                 '*': "left", '/': "left",
                 '^': "left",
                 **dict.fromkeys(FUNCTIONS, "right")}


class AngleType(Enum):
    DEGREE = 1
    RADIAN = 2


class Settings():
    """
    Class providing interface to change settings of core behaviour
    """
    def __init__(self):
        self.accuarcy = 16

    def set_accuracy(self, n: int):
        if not isinstance(n, int) or n < 1:
            raise ValueError(f"{n} is not valid accuarcy")
        if n > 27:
            raise ValueError(
                "sadly accuarcy bigger than 27 don't work in round function (")
        self.accuarcy = n

    def set_angle_type(self, type: AngleType):
        for f_name in TRIGONOMETRIC_FUNCTIONS:
            OPERATION_REALIZATIONS[f_name] = trig_f_wrapper(f_name, type)


def trig_f_wrapper(f_name, angle_type: AngleType):
    """
    function providing realization of trigonometric function depending on use
    of degrees or radians
    """
    if angle_type == AngleType.RADIAN:
        return TRIGONOMETRIC_FUNCTIONS[f_name]
    elif angle_type == AngleType.DEGREE:
        return lambda x: TRIGONOMETRIC_FUNCTIONS[f_name](degree_to_radian(x))
    else:
        raise Exception(f"{angle_type} - incorrect value")


def degree_to_radian(angle: Decimal):
    return angle * CONSTANTS["pi"] / Decimal(180)


settings = Settings()


class ExpressionIterator():
    """
    Class represinting iterator functionality, used to parse expresssion into
    tokens
    """
    def __init__(self, expression):
        self.expression = expression
        self.index = 0

    def has_next(self):
        return self.index < len(self.expression)

    def next(self):
        value = self.expression[self.index]
        self.index += 1
        return value

    def previous(self):
        self.index -= 1
        return self.expression[self.index]


class Token(Enum):
    """
    Enum representing some tokens types. Is used in get_tokens to have some
    behaviour based on previous parsed token
    """
    NUMBER              = 1
    BI_OPERATION        = 2
    LEFT_PARENTHESIS    = 3
    RIGHT_PARENTHESIS   = 4
    FUNCTION            = 5


def get_tokens(expression: str) -> list:
    """
    Function reterning token list for given expression.
    Operations and functions tokens are represented by str, numbers and const -
    by Decimal.
    Mainly works on finite-state machine similar idea - parses next token
    depengiding on type of previous one
    """
    iterator = ExpressionIterator(expression)
    tokens = []
    previous_token_type = None

    while iterator.has_next():
        ch = iterator.next()
        if ch in IGNORED_CHARS:
            while ch in IGNORED_CHARS and iterator.has_next():
                ch = iterator.next()
            if iterator.has_next() or ch not in IGNORED_CHARS:
                iterator.previous()
        elif ch in SIMPLE_OPERATIONS:
            tokens.append(ch)
            if ch == '(':
                previous_token_type = Token.LEFT_PARENTHESIS
            elif ch == ')':
                previous_token_type = Token.RIGHT_PARENTHESIS
            else:
                previous_token_type = Token.BI_OPERATION
        elif previous_token_type == Token.NUMBER:
            if ch in BINARY_OPERATIONS:
                tokens.append(ch)
                previous_token_type = Token.BI_OPERATION
            else:
                raise ValueError("Not a parenthesis or operation after number")
        elif previous_token_type == Token.BI_OPERATION:
            token = parse_number_or_function(iterator)
            tokens.append(token)
            if isinstance(token, Decimal):
                previous_token_type = Token.NUMBER
            else:
                previous_token_type = Token.FUNCTION
        elif previous_token_type == Token.LEFT_PARENTHESIS:
            if ch in string.ascii_lowercase:
                tokens.append(parse_function(iterator))
                previous_token_type = Token.FUNCTION
            else:
                tokens.append(parse_number(iterator))
                previous_token_type = Token.NUMBER
        elif previous_token_type == Token.RIGHT_PARENTHESIS:
            if ch in OPERATIONS:
                tokens.append(ch)
                previous_token_type = Token.BI_OPERATION
            else:
                raise ValueError("No binary operation after parenthesis")
        elif previous_token_type == Token.FUNCTION:
            raise ValueError("Parametr passed to function must be enclosed in brekets")
        else:
            token = parse_number_or_function(iterator)
            tokens.append(token)
            if isinstance(token, Decimal):
                previous_token_type = Token.NUMBER
            else:
                previous_token_type = Token.FUNCTION

    return tokens


def parse_number_or_function(iterator: ExpressionIterator):
    """
    fucnction deciding should number or function be parsed and parsing it
    """
    iterator.previous()
    ch = iterator.next()
    if ch in NUMBER_START_CHARS:
        return (parse_number(iterator))
    elif ch in string.ascii_lowercase:
        token = parse_charcter_thing(iterator)
        if token in CONSTANTS:
            token = CONSTANTS[token]
        return token
    else:
        raise ValueError(f"{ch} is not a valid token")


def parse_number(iterator: ExpressionIterator) -> Decimal:
    """
    function parsing number according to BNF notation in doc on start of module
    parses number by parts:sign, int, fraction, exponent
    """
    result = ""
    ch = iterator.previous()
    ch = iterator.next()
    if ch in ['+', '-']:
        result += ch
        ch = iterator.next()

    while ch in DIGITS:
        result += ch
        ch = iterator.next() if iterator.has_next() else None

    if ch == '.':
        result += ch
        ch = iterator.next()
        while ch in DIGITS:
            result += ch
            ch = iterator.next() if iterator.has_next() else None

    if ch == 'E':
        result += ch
        ch = iterator.next()
        if ch in ['+', '-']:
            result += ch
            ch = iterator.next()
        while ch in DIGITS:
            result += ch
            ch = iterator.next() if iterator.has_next() else None

    if ch != None:
        iterator.previous()
    return Decimal(result)


def parse_function(iterator: ExpressionIterator) -> str:
    return parse_charcter_thing(iterator)

def parse_constant(iterator: ExpressionIterator) -> Decimal:
    return CONSTANTS[parse_charcter_thing(iterator)]

def parse_charcter_thing(iterator: ExpressionIterator):
    """
    function parsing anything consisting only from string.ascii_lowercase as
    one token
    """
    result = ""
    iterator.previous()
    ch = iterator.next()
    while ch in string.ascii_lowercase:
        result += ch
        ch = iterator.next() if iterator.has_next() else None

    if ch != None:
        iterator.previous()
    return result


def convert_to_rpn(tokens_list) -> list:
    """
    function converting list of tokens to expression in Reverse Polish Nonation
    using Shunting-yard algorithm
    """
    tokens_list = tokens_list[:]
    output_list = []
    operator_stack = []
    while len(tokens_list) != 0:
        token = tokens_list.pop(0)
        if is_number(token):
            output_list.append(token)
        elif is_function(token):
            operator_stack.append(token)
        elif is_operation(token):
            while len(operator_stack) != 0 and\
                (((PRECEDENCE[operator_stack[-1]] > PRECEDENCE[token]) or
                    (PRECEDENCE[operator_stack[-1]] == PRECEDENCE[token] and ASSOCIATIVITY[token] == "left"))
                 and (operator_stack[-1] != "(")):
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
    return token in FUNCTIONS


def is_operation(token):
    return token in OPERATIONS


def evaluate(rpn_expression: list) -> Decimal:
    """
    function evaluating expression in RPN form
    in:list of operations and arguments in RPN
    out: expression evaluation value
    """
    rpn_expression = rpn_expression[:]

    # for the one char and simular cases. For examle '('
    if len(rpn_expression) == 1 and not isinstance(rpn_expression[0], Decimal):
        raise IncorrectInputError("incorrect input")

    while len(rpn_expression) != 1:
        index = 0
        while not (is_operation(rpn_expression[index]) or is_function(rpn_expression[index])):
            index += 1

        # after exracting arguments for some operation, algorithm replaces
        # place where were operation and arguments with operation(*arguments)
        operation = rpn_expression[index]
        operation_realization = OPERATION_REALIZATIONS[operation]
        if operation in BINARY_OPERATIONS:
            # without this check index - 2 can give -2 or -1 for index = 0,1
            # but in python -2 and -1 is valid index, so we need catch it here
            if index < 2:
                raise ValueError(f"Binary operation {operation} without enough arguments")
            arguments = (rpn_expression[index - 2], rpn_expression[index - 1])
            calculation_place = slice(index - 2, index + 1)
        elif operation in UNARY_OPERATIONS:
            arguments = [(rpn_expression[index - 1])]
            calculation_place = slice(index - 1, index + 1)

        calculation_value = [operation_realization(*arguments)]
        rpn_expression[calculation_place] = calculation_value

    return rpn_expression[0]


def calculate_expression(expression: str) -> Decimal:
    """
    evaluate wrapper with exceptioins
    """
    try:
        return evaluate(convert_to_rpn(get_tokens(expression)))
    except ValueError as ex:
        raise IncorrectInputError(*ex.args)
    except decimal.DivisionByZero as ex:
        raise IncorrectInputError("can't divide by zero")


def format_decimal(result: Decimal) -> str:
    """
    function formating calculation result to normal looking string
    """
    result = round(result, settings.accuarcy)
    result = str(result)
    result = result.rstrip('0') if '.' in result else result
    result = result.rstrip('.')
    return result


class IncorrectInputError(Exception):
    pass
