"""
supported operations : +, - , *, /, (),
integers and floating-point numbers with '.' is supported
operations precedence:
1: - +, -
2: *, /
3: ()      
"""

DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
ONE_CHARACTER_TOKENS = ['+','-','*','/','(',')']
IGNORED_CHARS = [' ']


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
            
        
def convert_to_rpn(tokens_list):pass

def evalute(rpn_expression):pass


if __name__ == "__main__":
    print(tokenize("583048+(5)"))
    print(tokenize("3.0 + 5.87.fdsl"))
