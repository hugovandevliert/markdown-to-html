#!/usr/bin/env python3

import argparse
import sys


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
        sys.exit('Could write to file: ' + inputfile)


class MarkdownParser:
    def parse(self, input):
        def consume_one():
            nonlocal index
            ch = input[index]
            index += 1
            return ch

        def consume_specific(char):
            if peek() != char:
                sys.exit(
                    "Error while parsing. Expected '{}' but got '{}'".format(char, peek()))
            return consume_one()

        def peek(offset=0):
            if index + offset < len(input):
                return input[index + offset]
            return None

        html = ''
        in_para = False
        in_bold = False
        in_italic = False
        index = 0
        while index < len(input):
            if peek() == '\n':
                html += consume_specific('\n')
            if peek() == '\n':
                html += consume_specific('\n')
                continue

            heading = 0
            if peek() == '#':
                while peek() == '#':
                    consume_specific('#')
                    heading += 1
                consume_specific(' ')
                html += '<h{}>'.format(heading)
            elif not in_para:
                html += '<p>'
                in_para = True

            while peek() != '\n':
                if peek() == ' ' and peek(1) == ' ':
                    consume_specific(' ')
                    consume_specific(' ')
                    html += '<br>'
                    continue

                if peek() == '*':
                    if peek(1) == '*':
                        consume_specific('*')
                        consume_specific('*')
                        in_bold = not in_bold
                        html += '<strong>' if in_bold else '</strong>'
                    else:
                        consume_specific('*')
                        in_italic = not in_italic
                        html += '<em>' if in_italic else '</em>'
                    continue

                html += consume_one()

            if heading > 0:
                html += '</h{}>'.format(heading)
            elif peek(1) == '\n':
                html += '</p>'
                in_para = False

            html += consume_specific('\n')

        return html


if __name__ == '__main__':
    main()
