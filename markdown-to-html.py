#!/usr/bin/env python3

import argparse
import sys
from parser import MarkdownParser


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input-file',
                        help='input markdown file',
                        required=True)
    parser.add_argument('-o', '--output-file',
                        help='output html file (defaults to output.html)',
                        default='output.html')
    args = parser.parse_args()

    inputfile = args.input_file
    outputfile = args.output_file

    try:
        with open(inputfile, 'r') as file:
            markdown = file.read()
    except:
        sys.exit('Could not read file: ' + inputfile)

    html = MarkdownParser().parse(markdown)

    try:
        with open(outputfile, 'w') as file:
            markdown = file.write(html)
    except:
        sys.exit('Could not write to file: ' + outputfile)


if __name__ == '__main__':
    main()
