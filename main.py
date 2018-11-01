import sys

from sheet_parser import Parser, SheetParserError
from sheet import Sheet
from maker import Maker

import argparse
parser = argparse.ArgumentParser(description='Huguhugu')
parser.add_argument("-i", "--image", help = "Using image sheet", required =False, default = "")
parser.add_argument("-t", "--text", help = "Using text sheet", required=False, default="")
args = parser.parse_args()

def main():
    print()
    if args.image:
        print('1. Read image sheet')
        print('Path : '+args.image)
    elif args.text:
        print('1. Read text sheet')
        print('Path : '+args.text)
        sheet_parser = Parser(args.text)
    else :
        print('Needs input')
        exit(1)
    print()


    print('2. Parse sheet')
    try:
        sheet = sheet_parser.parse()
    except SheetParserError as err:
        expression, message = err.args
        print()
        print('!! Sheet Parser Error !!')
        print(expression)
        print(message)
        print()
        exit(1)
    else:
        print('parse success')
        print('Print sheet...')
        print(sheet)
    print()

    print('3. Load videos')
    print()

    print('4. Generate music video.')
    music = Maker(sheet)
    music.make()
    print()

if __name__ == "__main__":
    main()
