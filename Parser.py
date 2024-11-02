import logging

from lexer import Lexer
import ASTNodeDefs as AST


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = tokens.pop(0)  # Start with the first token

    def advance(self):
        if len(self.tokens) > 0:
            self.current_token = self.tokens.pop(0)

    def parse(self):
        """
        Entry point for the parser. It will process the entire program.
        """
        statements = []
        while self.current_token[0] != "EOF":
            statement = self.statement()
            statements.append(statement)
        return statements

    def statement(self):
        """
        Determines which type of statement to parse.
        - If it"s an identifier, it could be an assignment or function call.
        - If it"s "if", it parses an if-statement.
        - If it"s "while", it parses a while-statement.
        """
        logging.info(f"\nTokens left to process : {len(self.tokens)}")
        logging.info(f"Current token: {self.current_token}")
        logging.info(f"Peek value: {self.peek()}")
        if self.current_token[0] == "IDENTIFIER":
            if self.peek() == "ASSIGNMENT":
                logging.info("Doing assignment")
                return self.assign_stmt()
            elif self.peek() == "LPAREN":
                logging.info("Doing function call")
                return self.function_call()
            else:
                raise ValueError(f"Unexpected token after identifier: {self.tokens[1]}")
        elif self.current_token[0] == "IF":
            logging.info("Doing if statement")
            return self.if_stmt()
        elif self.current_token[0] == "WHILE":
            logging.info("Doing while loop")
            return self.while_stmt()
        elif self.current_token[0] == "EOF":
            return
        else:
            raise ValueError(f"Unexpected token: {self.current_token}")

    def assign_stmt(self):
        """
        Parses assignment statements.
        Example:
        x = 5 + 3
        """
        logging.info("Tokens left pre assignment", len(self.tokens))
        identifier = self.current_token
        self.advance()
        assert self.current_token[1] == "="
        self.advance()

        if self.peek() in ["PLUS", "MINUS", "MULTIPLY", "DIVIDE"]:
            expression = self.expression()
        else:
            expression = self.current_token
            self.advance()

        node = AST.Assignment(identifier, expression)

        logging.info("Assignment Node: ", node)
        logging.info("Tokens left post assignment", len(self.tokens))

        return node

    def if_stmt(self):
        """
        Parses an if-statement, with an optional else block.
        Example:
        if condition:
            # statements
        else:
            # statements
        """
        self.advance()
        assert (
            self.current_token[0] == "IDENTIFIER" or self.current_token[0] == "NUMBER"
        )
        boolean_expression = self.boolean_expression()
        logging.info("Boolean Expression:", boolean_expression)

        assert self.current_token[0] == "SEMICOLON"
        self.advance()

        block = self.block("IF")
        logging.info("Is there a fucking else statement?", self.current_token)
        if self.current_token[0] == "ELSE":
            else_block = self.block()
        else:
            else_block = None

        node = AST.IfStatement(
            condition=boolean_expression, then_block=block, else_block=else_block
        )
        logging.info("If Statement Node: ", node)
        return node

    def while_stmt(self):
        """
        Parses a while-statement.
        Example:
        while condition:
            # statements
        """
        self.advance()
        assert (
            self.current_token[0] == "IDENTIFIER" or self.current_token[0] == "NUMBER"
        )
        condition = self.boolean_expression()
        assert self.current_token[0] == "SEMICOLON"
        self.advance()

        block = self.block("WHILE")

        return AST.WhileStatement(condition, block)

    def block(self, block_type: str = ""):
        """
        Parses a block of statements. A block is a collection of statements grouped by indentation.
        Example:
        if condition:
            # This is a block
            x = 5
            y = 10
        """
        stop = ["IF", "ELSE", "EOF"] if block_type == "IF" else ["EOF"]
        logging.info("Block Stop:", stop)

        if self.current_token[0] == "ELSE":
            self.advance()
            assert self.current_token[0] == "SEMICOLON"
            self.advance()

        i = 0
        statements = []
        while self.current_token[0] not in stop:
            if i > 100:
                break
            logging.info(f"Statement {i} in block with peek: {self.peek()}")
            statement = self.statement()
            statements.append(statement)
            i += 1
        logging.info("Statements in block: ", statements)
        node = AST.Block(statements)
        logging.info("Block Statement:", node)
        return node

    def expression(self):
        """
        Parses an expression. Handles operators like +, -, etc.
        Example:
        x + y - 5
        TODO: Implement logic to parse binary operations (e.g., addition, subtraction) with correct precedence.
        """
        left = self.term()  # Parse the first term
        while self.current_token[0] in ["PLUS", "MINUS"]:  # Handle + and -
            op = self.current_token  # Capture the operator
            self.advance()  # Skip the operator
            right = self.term()  # Parse the next term
            left = AST.BinaryOperation(left, op, right)

        return left

    def boolean_expression(self):
        """
        Parses a boolean expression. These are comparisons like ==, !=, <, >.
        Example:
        x == 5
        TODO: Implement parsing for boolean expressions.
        """
        # write your code here, for reference check expression function
        assert self.current_token[0] in ["NUMBER", "IDENTIFIER"]
        left = self.current_token

        self.advance()
        assert self.current_token[0] in [
            "EQUALS",
            "NEQ",
            "GREATER",
            "LESS",
        ], f"This is the current token {self.current_token}"
        operator = self.current_token

        self.advance()
        assert self.current_token[0] in ["NUMBER", "IDENTIFIER"]
        right = self.current_token
        self.advance()

        return AST.BooleanExpression(left, operator, right)

    def term(self):
        """
        Parses a term. A term consists of factors combined by * or /.
        Example:
        x * y / z
        TODO: Implement the parsing for multiplication and division.
        """
        left = self.factor()
        while self.current_token and self.current_token[0] in ["MULTIPLY", "DIVIDE"]:
            operator = self.current_token
            self.advance()
            right = self.factor()
            left = AST.BinaryOperation(left, operator, right)

        return left

    def factor(self):
        """
        Parses a factor. Factors are the basic building blocks of expressions.
        Example:
        - A number
        - An identifier (variable)
        - A parenthesized expression
        TODO: Handle these cases and create appropriate AST nodes.
        """
        if self.current_token[0] in ["NUMBER", "IDENTIFIER"]:
            token = self.current_token
            self.advance()
            return token
        elif self.current_token[0] == "LPAREN":
            logging.debug("We are going through here ")
            self.advance()
            expression = self.expression()
            assert self.current_token[0] != "RPAREN"
            self.advance()
            return expression
        else:
            raise ValueError(f"Unexpected token in factor: {self.current_token}")

    def function_call(self):
        """
        Parses a function call.
        Example:
        myFunction(arg1, arg2)
        TODO: Implement parsing for function calls with arguments.
        """
        func_name = self.current_token
        self.advance()
        assert self.current_token[0] == "LPAREN"
        assert ("RPAREN", ")") in self.tokens
        self.advance()

        args = []
        while self.current_token[0] != "RPAREN":
            if self.current_token[0] == "ARG_SEPARATOR":
                self.advance()
                continue
            if self.peek() in ["PLUS", "MINUS", "MULTIPLY", "DIVIDE"]:
                expression = self.expression()
                args.append(expression)
                continue
            args.append(self.current_token)
            self.advance()
        assert self.current_token[0] == "RPAREN"
        self.advance()

        logging.info("after arg parse", self.current_token)
        logging.info("Arguments of function: ", args)
        node = AST.FunctionCall(func_name, args)
        logging.info("Function Call Node: ", node)
        logging.info("Next Token form func Call Node: ", self.peek())
        return node

    def expect(self, token_type):
        if self.current_token[0] == token_type:
            self.advance()  # Move to the next token
        else:
            raise ValueError(f"Expected {token_type} but got {self.current_token[0]}")

    def peek(self):
        if self.tokens:
            return self.tokens[0][0]
        else:
            return None
