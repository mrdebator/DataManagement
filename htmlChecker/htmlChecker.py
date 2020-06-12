# Python Code for html Checker
# Author: Ansh Chandnani

class Stack:

    def __init__(self):
        self.html_string = []

    def push(self, item):
        self.html_string.append(item)

    def pop(self):
        return self.html_string.pop()

    def peek(self):
        return self.html_string[-1]

    def is_empty(self):
        return self.html_string == []

    def size(self):
        return len(self.html_string)


def check_html(html_string):
    htmlStack = Stack()       # declare object of class Stack()
    balanced = True
    text_lines = html_string.split("\n")
    # print(text_lines)
    for line in text_lines:
        wordList = line.split(" ")
        for word in wordList:
            if '<' in word:
                word = word.replace('<', '')
                word = word.replace('>', '')
                if '/' in word:                 # code case for closing tags
                    word = word.replace('/', '')
                    if (not htmlStack.is_empty()) and (word == htmlStack.peek()):
                        # print('Popped', word)
                        htmlStack.pop()
                    else:
                        balanced = False
                else:                          # code case for opening tags
                    # print('Pushed', word)
                    htmlStack.push(word)
    if not htmlStack.is_empty():
        balanced = False
    return balanced


def htmlInput():
    print('You are now in input mode. Type \'esc\' in a new line to exit.')
    htmlCode = ''
    line = ''
    while line != 'esc':
        line = input()
    print(htmlCode)
    return htmlCode


def printResult(bool):
    if bool:
        print('Your file contains balanced HTML code!')
    else:
        print('Uh Oh, looks like your HTML code is unbalanced!')


ch = 'y'
while ch == 'y' or ch == 'Y':

    # Menu display
    print('''MENU
    1. Check file
    2. Enter code manually
    ''')
    option = int(input('Enter corresponding number to select menu item: '))

    if option == 1:
        fileName = input('Enter filename with extension: ')
        file = open(fileName, 'r')
        content = file.read()
        printResult(check_html(content))
    elif option == 2:
        code = htmlInput()
        printResult(check_html(code))
    else:
        print('Invalid option!')

    ch = input('Do you wish to continue? (y/n): ')
