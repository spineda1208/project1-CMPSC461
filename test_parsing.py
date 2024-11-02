from lexer import Lexer
from Parser import Parser

source_code = """
my_name = 100
x = 12
if x > 10:
    foo(100, 200)
if x != 10:
    bar(200)
else:
    baz(300)
"""

print("Tokenizing inititated:")
print("-" * 30)
lexer = Lexer(source_code)
tokens = lexer.tokenize()

print("Tokenized:")
print("-" * 10)
for i in tokens:
    print(i)
print("\n")

print("Parsing inititated:")
print("-" * 19)
parser = Parser(tokens)
ast = parser.parse()
print("\nParsed:")
print("-" * 7)

result = ""
for node in ast:
    result += node.to_string()

print(result)
