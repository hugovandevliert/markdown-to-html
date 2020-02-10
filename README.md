# Markdown to HTML converter

A Markdown to HTML converter written in Python.

## Support

Currently, the following Markdown syntax is supported:

- [x] Heading `#`, `##`, `###`
- [x] Bold text `**`
- [x] Italic text `*`
- [x] Strikethrough `~`
- [ ] Blockquote `>`
- [x] Ordered list
- [x] Unordered list
- [x] Code inline ``` ` ```
- [ ] Code block ` ``` `
- [x] Horizontal rule `---`
- [ ] Link `[title](https://www.example.com)`
- [ ] Image `![alt text](image.jpg)`
- [ ] Task list

## Installation

```bash
# clone the repo
git clone https://github.com/hugovandevliert/markdown-to-html

# change the working directory to markdown-to-html
cd markdown-to-html

# install python3 if not yet installed

# check if the installation succeeded
./markdown-to-html.py -h
```

## Usage

General usage:

```bash
./markdown-to-html.py -i input.md -o output.html
```

For more options:

```bash
./markdown-to-html.py -h
```

## Authors

Made by [@hugovandevliert](https://github.com/hugovandevliert).

## License

[![MIT](https://img.shields.io/cocoapods/l/AFNetworking.svg?style=style&label=License&maxAge=2592000)](LICENSE)

This software is distributed under the MIT license.
