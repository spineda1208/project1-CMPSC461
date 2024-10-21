from typing import List, Tuple


class Lexer:
    def __init__(self, code: str):
        self.source_code: str = code
        self.position: int = 0
        self.tokens: List[Tuple[str, str]] = []

    def _get_token(self, string: str):
        match string:
            case "if":
                return ("IF", string)
            case "else":
                return ("ELSE", string)
            case "while":
                return ("WHILE", string)
            case "+":
                return ("PLUS", string)
            case "-":
                return ("MINUS", string)
            case "*":
                return ("MULTIPLY", string)
            case "/":
                return ("DIVIDE", string)
            case "<":
                return ("LESS", string)
            case ">":
                return ("GREATER", string)
            case "==":
                return ("EQUALS", string)
            case "!=":
                return ("NEQ", string)
            case "(":
                return ("LPAREN", string)
            case ")":
                return ("RPAREN", string)
            case ":":
                return ("SEMICOLON", string)
            case "=":
                return ("ASSIGNMENT", string)
            case _:
                return ("IDENTIFIER", string)

    def _get_number(self, position: int) -> int:
        number = ""
        while position < len(self.source_code) and self.source_code[position].isdigit():
            number += self.source_code[position]
            position += 1
        self.tokens.append(("NUMBER", number))
        return position

    def _get_identifier(self, position: int) -> int:
        buffer = ""
        while position < len(self.source_code) and self.source_code[position].isalpha():
            buffer += self.source_code[position]
            position += 1
        token = self._get_token(buffer)
        self.tokens.append(token)
        return position

    def tokenize(self) -> List[Tuple[str, str]]:
        position = 0
        while position < len(self.source_code):
            character = self.source_code[position]

            if character.isspace():
                position += 1
                continue

            if character.isdigit():
                position = self._get_number(position)
                continue

            if character.isalpha():
                position = self._get_identifier(position)
                continue

            token = self._get_token(character)
            self.tokens.append(token)
            position += 1

        return self.tokens
