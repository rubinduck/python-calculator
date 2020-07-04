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

ASSOCIATIVITY = {'+':"left",'-':"left",
                 '*':"left",'/':"left"}
 

def get_tokens(expression):
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
    return tokens
            
        
def convert_to_rpn(tokens_list):
    """
    function converting list of tokens to expression in Reverse Polish Nonation
    using Shunting-yard algorithm
    """
    output_list = []
    operator_stack = []
    while len(tokens_list) != 0:
        token = tokens_list.pop(0)
        if is_number(token):
            if "." in token:
                token = float(token)
            else:
                token = int(token)
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
    # function is based on restrictions of get_tokens result
    for ch in token:
        if ch not in DIGITS and ch != ".":
            return False
    return True

def is_function(token):
    # temp mock, while there are no functions
    return False

def is_operation(token):
    return token in OPERATIONS


def evalute(rpn_expression):pass