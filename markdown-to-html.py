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
        sys.exit('Could not write to file: ' + outputfile)


class HtmlElement:
    tags = {
        'root': None,
        'text': '',
        'h1': '<h1{}>{}</h1>',
        'h2': '<h2{}>{}</h2>',
        'h3': '<h3{}>{}</h3>',
        'h4': '<h4{}>{}</h4>',
        'h5': '<h5{}>{}</h5>',
        'h6': '<h6{}>{}</h6>',
        'p': '<p{}>{}</p>',
        'strong': '<strong{}>{}</strong>',
        'code': '<code{}>{}</code>',
        'strikethrough': '<s{}>{}</s>',
        'em': '<em{}>{}</em>',
        'br': '<br{} />',
        'hr': '<hr{} />',
        'ul': '<ul{}>\n{}\n</ul>',
        'ol': '<ol{}>\n{}\n</ol>',
        'li': '<li{}>{}</li>',
        'blockquote': '<blockquote{}>{}</blockquote>'
    }

    def __init__(self, tag):
        self.tag = HtmlElement.tags[tag]
        self.attributes = []
        self.children = []
        self.parent = None
        self.text = ''

    def add_child(self, tag):
        child = HtmlElement(tag)
        child.parent = self
        self.children.append(child)
        return child

    def is_tag(self, tag):
        return self.tag == self.tags[tag]

    def in_tag(self, tag):
        element = self.parent
        while element:
            if element.tag == self.tags[tag]:
                return True
            element = element.parent
        return False

    def find_tag_in_parents(self, tag):
        element = self.parent
        while element:
            if element.tag == self.tags[tag]:
                return element
            element = element.parent
        return None

    def __str__(self):
        if self.tag == self.tags['root']:
            content = ''
            for child in self.children:
                content += str(child)
            return content
        if self.tag == self.tags['text']:
            return self.text
        attributes = ''
        for attribute in self.attributes:
            attributes += ' '
            attributes += str(attribute)
        children = ''
        for child in self.children:
            children += str(child)
        return self.tag.format(attributes, children)


class HtmlAttribute:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __str__(self):
        return '{}="{}"'.format(self.name, self.value)


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

        def open_or_close_tag(tag):
            nonlocal child_element
            if not child_element.in_tag(tag):
                strong_element = child_element.parent.add_child(tag)
                child_element = strong_element.add_child('text')
            else:
                child_element = child_element.find_tag_in_parents(
                    tag).parent.add_child('text')

        root_element = HtmlElement('root')
        index = 0
        while index < len(input):
            newpara = False
            if peek() == '\n':
                consume_specific('\n')
                newpara = True
                element = root_element.add_child('text')
                element.text = '\n'
                if peek() == '\n':
                    consume_specific('\n')

            heading = 0
            if peek() == '#':
                while peek() == '#' and heading <= 6:
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
                element = root_element.add_child('h{}'.format(heading))
                element.attributes.append(HtmlAttribute('id', id))
            elif peek() == '-' and peek(1) == '-' and peek(2) == '-':
                consume_specific('-')
                consume_specific('-')
                consume_specific('-')
                element = root_element.add_child('hr')
                continue
            elif peek().isdigit() and peek(1) == '.' and peek(2) == ' ':
                consume_one()
                consume_specific('.')
                consume_specific(' ')
                if not element.in_tag('ol'):
                    element = root_element.add_child('ol')
                    tab_element = element.add_child('text')
                    tab_element.text += '\t'
                    element = element.add_child('li')
                else:
                    tab_element = element.parent.add_child('text')
                    tab_element.text += '\n\t'
                    element = element.parent.add_child('li')
            elif peek() == '-':
                consume_specific('-')
                consume_specific(' ')
                if not element.in_tag('ul'):
                    element = root_element.add_child('ul')
                    tab_element = element.add_child('text')
                    tab_element.text += '\t'
                    element = element.add_child('li')
                else:
                    tab_element = element.parent.add_child('text')
                    tab_element.text += '\n\t'
                    element = element.parent.add_child('li')
            elif peek() == '>':
                consume_specific('>')
                if peek() == ' ':
                    consume_specific(' ')
                tab_element = element.parent.add_child('text')
                tab_element.text += '\n\t'
                element = element.parent.add_child('blockquote')
            elif not element.is_tag('p') or newpara:
                element = root_element.add_child('p')
            else:
                tab_element = element.add_child('text')
                tab_element.text += '\n\t'

            child_element = element.add_child('text')

            while peek() != '\n':
                if peek() == ' ' and peek(1) == ' ':
                    consume_specific(' ')
                    consume_specific(' ')
                    element.add_child('br')
                    child_element = child_element.parent.add_child('text')
                    continue

                if peek() == '*':
                    if peek(1) == '*':
                        consume_specific('*')
                        consume_specific('*')
                        open_or_close_tag('strong')
                    else:
                        consume_specific('*')
                        open_or_close_tag('em')
                    continue

                if peek() == '`':
                    consume_specific('`')
                    open_or_close_tag('code')
                    continue

                if peek() == '~':
                    consume_specific('~')
                    open_or_close_tag('strikethrough')
                    continue

                child_element.text += consume_one()

            consume_specific('\n')

        return str(root_element)


if __name__ == '__main__':
    main()
