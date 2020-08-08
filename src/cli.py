"""
Module allowing calculate expression in cli
to call: python cli.py expression
"""


from argparse import ArgumentParser, RawTextHelpFormatter

import core

INTRO_MESSAGE = \
"""
This is simple calculator program
Supports +,-,*,/,() operations,
positive and negative integers and floats
"""


def main():
    parser = ArgumentParser(description=INTRO_MESSAGE,
                            formatter_class=RawTextHelpFormatter)
    parser.add_argument("expression", type=str,
                        help="expression to be evaluated")
    parser.add_argument("-a", "--accuaracy", type=int,
                        help="accuarcy of answer")
    parser.add_argument("--angle", type=str,
                        help="type of angle: radian or degree, default is radian")

    args = parser.parse_args()
    if args.accuarcy != None:
        core.settings.set_accuracy(args.accuarcy)

    angle = args.angle
    if angle != None:
        if angle == "radian":
            core.settings.set_angle_type(core.AngleType.RADIAN)
        elif angle == "degree":
            core.settings.set_angle_type(core.AngleType.DEGREE)
        else:
            raise ValueError(f"{angle} is incorrect angle type")

    process_expression(args.expression)


def process_expression(expression):
    try:
        result = core.calculate_expression(expression)
        result = core.format_decimal(result)
        print(f"{expression} = {result}")
    except core.IncorrectInputError as ex:
        print("Some of input was incorrect")
        print(ex.agrs[0])
    except Exception as ex:
        print("Something went wrong")
        print(ex)


if __name__ == "__main__":
    main()
