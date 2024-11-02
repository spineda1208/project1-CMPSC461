from lexer import Lexer
from Parser import Parser

source_code = """
x = 12
if x > 10: foo(100)
if x == 10: bar(200)
else: baz(200)
"""

lexer = Lexer(source_code)
tokens = lexer.tokenize()

print("These are the tokens:")
for i in tokens:
    print(i)
print("\n")

print("Parsing inititated:")
parser = Parser(tokens)
ast = parser.parse()

result = ""
for node in ast:
    result += node.to_string()  # Use to_string() method for each AST node

print(result)

# parser = Parser(tokens)
# ast = parser.parse()
