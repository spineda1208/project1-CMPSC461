from lexer import Lexer
# from Parser import Parser

source_code = """
x = 12
if x > 10: foo(100)
if x == 10: bar(200)
else: baz(200)
"""

lexer = Lexer(source_code)
tokens = lexer.tokenize()

print(tokens)

# parser = Parser(tokens)
# ast = parser.parse()
