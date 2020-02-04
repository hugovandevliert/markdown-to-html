#!/usr/bin/env python3

import argparse
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input-file",
                        help="input markdown file",
                        required=True)
    parser.add_argument("-o", "--output-file",
                        help="output html file (defaults to output.html)",
                        default="output.html")
    args = parser.parse_args()

    inputfile = args.input_file
    outputfile = args.output_file

    try:
        with open(inputfile, 'r') as file:
            markdown = file.read()
    except:
        sys.exit("Could not read file: " + inputfile)

    html = MarkdownParser(markdown).parse()

    try:
        with open(outputfile, 'w') as file:
            markdown = file.write(html)
    except:
        sys.exit("Could write to file: " + inputfile)


class MarkdownParser:
    def __init__(self, input):
        self.input = input
        self.html = ''

    def parse(self):
        for line in self.input.split("\n"):
            self.html += self.parse_line(line)
            self.html += "\n"
        return self.html

    def parse_line(self, line):
        def consume_one():
            nonlocal index
            ch = line[index]
            index += 1
            return ch

        def consume_specific(char):
            if peek() != char:
                sys.exit(
                    "Error while parsing. Expected '{}' but got '{}'".format(char, peek()))
            return consume_one()

        def next_is(next):
            for i, c in enumerate(next):
                if peek(i) != c:
                    return False
            return True

        def peek(offset=0):
            if index + offset < len(line):
                return line[index + offset]
            return 0

        html = ''
        index = 0

        heading = 0
        if peek() == '#':
            while peek() == '#':
                consume_specific('#')
                heading += 1
            consume_specific(' ')
            html += '<h{}>'.format(heading)

        while index < len(line):
            if next_is('  '):
                consume_specific(' ')
                consume_specific(' ')
                html += '<br>'
                continue

            html += consume_one()

        if heading > 0:
            html += '</h{}>'.format(heading)

        return html


if __name__ == "__main__":
    main()
