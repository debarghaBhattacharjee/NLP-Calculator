#Keywords List

add = ['add', 'sum', 'addition', 'plus', 'added', '+']
sub1 = ['difference', 'minus', '-']
sub2 = ['subtract', 'subtraction', 'subtracted']
mult = ['multiply', 'into', 'multiplication', 'times', 'product', 'multiplied', '*']
div = ['divide', 'division', 'divided', '/']

bracket = ['(', ')']
symbols = ['+', '-', '*', '/']
numbers = "0123456789"

markedVerbs = {}
markedVerbs['add'] = 'addition'
markedVerbs['subtract'] = 'subtraction'
markedVerbs['multiply'] = 'multiplication'
markedVerbs['divide'] = 'division'

markedConjunctions = ['by', 'to']
markedSymbols = ['/','*']

swapConjunction = ['by', 'to', 'from']

stopWordsTags = ['NN', 'VB', 'VBN', 'VBG', 'JJ', 'NNS', 'VBP', 'DT', 'WP', 'VBZ'] 
stopWordsSymbols = ['&', '?', '#', '$', '@', '%', '^', '_', '=', ' ']

precedence = {}
precedence['*'] = 3
precedence['/'] = 3
precedence['+'] = 2
precedence['-'] = 2
precedence['--'] = 2
precedence['('] = 1