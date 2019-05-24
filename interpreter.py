from node import Node
from token import Token, TokenTypes, TokenTypeError


class OperatorExprError(Exception):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


class ExecuteProgramError(Exception):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


def token_type_check_fabric(token_types):
    def token_type_check(function):
        def wrapper(self: Interpreter, node: Node, *args, **kwargs):
            if node not in token_types:
                raise TokenTypeError("", f"{function.__name__} wait "
                                         f"{node.token.name} in"
                                         f"{token_types} types.")
            return function(self, node, *args, **kwargs)
        return wrapper
    return token_type_check


class Interpreter:
    # Class for interpret a semantic tree from code. Working only with int
    # variables, read in the start point and print them at the end. Working only
    # with simple arithmetic and binary operations. Conditional variable is
    # integer, 0 or 1.
    operations_one = {
        '-': lambda x: -x,
        '~': lambda x: ~x,
    }

    operations_two = {
        '+': lambda x, y: x + y,
        '-': lambda x, y: x - y,
        '*': lambda x, y: x * y,
        '/': lambda x, y: x // y,
        '%': lambda x, y: x % y,
        '**': lambda x, y: x ** y,
        '&': lambda x, y: x & y,
        '|': lambda x, y: x | y,
        '^': lambda x, y: x ^ y,
        '=': lambda x, y: 1 if x == y else 0,
        '~': lambda x, y: 1 if x != y else 0,
        '>': lambda x, y: 1 if x > y else 0,
        '<': lambda x, y: 1 if x < y else 0,
    }

    @token_type_check_fabric((TokenTypes.Program,))
    def __iter__(self, root):
        self.root = root
        self.variables = {}

    def run(self) -> None:
        # Run loaded semantic tree
        self.initial()
        # Use queue of basic block to execute program line by line
        queue = [i for i in self.root.get_children((TokenTypes.BasicBlock,))]

        while len(queue) > 0:
            current = queue.pop(0)
            if current.token.type is TokenTypes.Return:
                break

            for assignment in current.get_children((TokenTypes.Assignment,)):

                variable = assignment.get_child(TokenTypes.Var)
                expr = assignment.get_child(TokenTypes.Expr)
                self.variables[variable] = self.execute_expr(expr)

            jump = current.get_child(TokenTypes.Jump)
            queue.insert(0, self.execute_jump(jump))

        self.exit()

    def initial(self):
        # Initialize variables and read them from user
        for child in self.root.get_children((TokenTypes.Var,)):
            tmp = input(f'{child.token.value} :=')
            self.variables[child.token.value] = int(tmp)

    def exit(self):
        # Clear all variables
        self.variables.clear()

    @token_type_check_fabric((TokenTypes.Constant, TokenTypes.Expr,
                              TokenTypes.Var))
    def execute_expr(self, node) -> int:
        # Execute expresion. Node has two or three children: operation and
        # variable or constant.
        if node.token.type is TokenTypes.Constant:
            return node.token.value
        if node.token.type is TokenTypes.Var:
            return self.variables[node.token.name]

        children = [i for i in node.get_children((TokenTypes.Constant,
                                                  TokenTypes.Expr,
                                                  TokenTypes.Var))]
        operator = node.get_child(TokenTypes.Op).token
        if len(children) == 1:
            arg = self.execute_expr(children[0])
            if operator.value in Interpreter.operations_one:
                return Interpreter.operations_one[operator.value](arg)
            else:
                raise OperatorExprError("", "Not suitable operator.")
        elif len(children) == 2:
            arg1 = self.execute_expr(children[0])
            arg2 = self.execute_expr(children[1])
            if operator.value in Interpreter.operations_two:
                return Interpreter.operations_two[operator.value](arg1, arg2)
            else:
                raise OperatorExprError("", f"There are not {operator.value}"
                                            f" operator.")
        else:
            raise OperatorExprError("", "There are not three argument "
                                        "function.")

    @token_type_check_fabric((TokenTypes.Jump,))
    def execute_jump(self, node) -> Node:
        # Execute jump token. In value it has type of jump, it can be goto, if
        # condition or return. Every type return node, basic block node to
        # insert in queue.
        if node.token.value == 'goto':
            return self.execute_goto(node)
        elif node.token.value == 'if':
            return self.execute_if(node)
        elif node.token.value == 'return':
            return self.execute_return(node)
        else:
            raise ExecuteProgramError("", f"There is no jump with "
                                          f"{node.token.value}.")

    @token_type_check_fabric((TokenTypes.Jump,))
    def execute_goto(self, node) -> Node:
        label = node.get_child(TokenTypes.Label).token.value
        for basic_block in self.root.get_children((TokenTypes.BasicBlock,)):
            if basic_block.get_child(TokenTypes.Label).token.value == label:
                return basic_block

        raise ExecuteProgramError("", f"There is no block with {label} label.")

    @token_type_check_fabric((TokenTypes.Jump,))
    def execute_if(self, node) -> Node:
        condition, true_label, false_label = \
            node.get_children((TokenTypes.Expr, TokenTypes.Label))
        result_condition = self.execute_expr(condition)
        if result_condition == 1:
            return self.execute_goto(true_label)
        return self.execute_goto(false_label)

    @token_type_check_fabric((TokenTypes.Jump,))
    def execute_return(self, node) -> Node:
        expr = node.get_child(TokenTypes.Expr)
        result_expr = self.execute_expr(expr)
        print(result_expr)
        return Node(Token(TokenTypes.Return))
