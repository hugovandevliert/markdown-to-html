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

        def next_is(next):
            for i, c in enumerate(next):
                if peek(i) != c:
                    return False
            return True

        def peek(offset=0):
            if index + offset < len(input):
                return input[index + offset]
            return None

        html = ''
        in_para = False
        in_bold = False
        in_italic = False
        in_code = False
        in_strike = False
        in_olist = False
        in_ulist = False
        in_list = False
        index = 0
        while index < len(input):
            if peek() == '\n':
                html += consume_specific('\n')
            if peek() == '\n':
                html += consume_specific('\n')
                continue
            if not peek():
                break

            heading = 0
            if peek() == '#':
                while peek() == '#':
                    consume_specific('#')
                    heading += 1
                consume_specific(' ')
                id = ''
                id_index = 0
                while peek(id_index) != '\n':
                    if peek(id_index) == ' ':
                        id += '-'
                    else:
                        id += peek(id_index).lower()
                    id_index += 1
                html += '<h{} id="{}">'.format(heading, id)
            elif peek() == '-' and peek(1) == '-' and peek(2) == '-':
                consume_specific('-')
                consume_specific('-')
                consume_specific('-')
                html += '<hr />'
                continue
            elif peek().isdigit() and peek(1) == '.' and peek(2) == ' ':
                consume_one()
                consume_specific('.')
                consume_specific(' ')
                if not in_olist:
                    html += '<ol>'
                    in_olist = True
                    html += '\n'
                in_list = True
                html += '\t'
                html += '<li>'
            elif peek() == '-':
                consume_specific('-')
                consume_specific(' ')
                if not in_ulist:
                    html += '<ul>'
                    in_ulist = True
                    html += '\n'
                in_list = True
                html += '\t'
                html += '<li>'
            elif not in_para:
                in_para = True
                html += '<p>'

            while peek() != '\n':
                if peek() == ' ' and peek(1) == ' ':
                    consume_specific(' ')
                    consume_specific(' ')
                    html += '<br />'
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

                if peek() == '`':
                    consume_specific('`')
                    in_code = not in_code
                    html += '<code>' if in_code else '</code>'
                    continue

                if peek() == '~':
                    consume_specific('~')
                    in_strike = not in_strike
                    html += '<s>' if in_strike else '</s>'
                    continue

                html += consume_one()

            if heading > 0:
                html += '</h{}>'.format(heading)
                html += consume_specific('\n')
            elif in_list:
                html += '</li>'
                html += consume_specific('\n')
                in_list = False
                if in_olist:
                    if not (peek() and peek().isdigit() and peek(1) == '.' and peek(2) == ' ') and not (peek() == '\n' and peek(1) and peek(1).isdigit() and peek(2) == '.' and peek(3) == ' '):
                        html += '</ol>'
                        html += '\n'
                        in_olist = False
                if in_ulist:
                    if not (peek() == '-' and peek(1) == ' '):
                        html += '</ul>'
                        html += '\n'
                        in_ulist = False
            elif peek(1) == '\n':
                html += '</p>'
                in_para = False
                html += consume_specific('\n')
            else:
                html += consume_specific('\n')
                html += '\t'

        return html


if __name__ == '__main__':
    main()
