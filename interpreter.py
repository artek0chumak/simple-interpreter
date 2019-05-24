from typing import List

from node import Node
from token import Token, TokenTypes


class Interpreter:
    class OperatorExprError(Exception):
        def __init__(self, expression, message):
            self.expression = expression
            self.message = message

    class ExecuteProgramError(Exception):
        def __init__(self, expression, message):
            self.expression = expression
            self.message = message

    def __iter__(self, root: Node):
        self.root = root
        self.variables = {}

    def run(self) -> None:
        for child in self.root.get_children():
            if child.token is TokenTypes.Var:
                token = child.token
                tmp = input(f'{token.name} :=')
                self.variables[token.name] = int(tmp)

        queue = [i for i in self.root.get_children()
                 if i.token.type is TokenTypes.BasicBlock]

        while len(queue) > 0:
            current = queue.pop(0)
            assignments = [i for i in current.get_children()
                           if i.token.type is TokenTypes.Assignment]
            for assignment in assignments:
                variable = next(i for i in assignment.get_children()
                                if i.token.type is TokenTypes.Var)
                expr = next(i for i in assignment.get_children()
                            if i.token.type is TokenTypes.Expr)
                self.variables[variable] = self.execute_expr(expr)

            jump = next(i for i in current.get_children()
                        if i.token.type is TokenTypes.Jump)
            if jump.token.value == 'goto':
                queue = self.execute_goto(jump, queue)
            elif jump.token.value == 'if':
                queue = self.execute_if(jump, queue)
            elif jump.token.value == 'return':
                self.execute_return(jump)
            else:
                raise Interpreter.ExecuteProgramError("",
                                                      f"There is no jump with "
                                                      f"{jump.token.value}.")

    def execute_expr(self, node) -> int:
        if node.token.type is TokenTypes.Constant:
            return node.token.value
        if node.token.type is TokenTypes.Var:
            return self.variables[node.token.name]

        children = [i for i in node.get_children()]
        if len(children) == 1:
            arg = self.execute_expr(children[0])
            if node.token.value == '-':
                return - arg
            elif node.token.value == '~':
                return ~ arg
            else:
                raise Interpreter.OperatorExprError("", "Not suitable operator")
        elif len(children) == 2:
            arg1 = self.execute_expr(children[0])
            arg2 = self.execute_expr(children[1])
            if node.token.value == '+':
                return arg1 + arg2
            elif node.token.value == '-':
                return arg1 - arg2
            elif node.token.value == '*':
                return arg1 * arg2
            elif node.token.value == '/':
                return arg1 // arg2
            elif node.token.value == '%':
                return arg1 % arg2
            elif node.token.value == '**':
                return arg1 ** arg2
            elif node.token.value == '&':
                return arg1 & arg2
            elif node.token.value == '|':
                return arg1 | arg2
            elif node.token.value == '^':
                return arg1 ^ arg2
            elif node.token.value == '=':
                return 1 if arg1 == arg2 else 0
            elif node.token.value == '~':
                return 1 if arg1 != arg2 else 0
            elif node.token.value == '<':
                return 1 if arg1 < arg2 else 0
            elif node.token.value == '>':
                return 1 if arg1 > arg2 else 0
            else:
                raise Interpreter.OperatorExprError("", "Not suitable operator")
        else:
            raise Interpreter.OperatorExprError("", "There are not three "
                                                    "argument function.")

    def execute_goto(self, node, queue) -> List[Node]:
        label = node.token.value
        basic_blocks = filter(lambda x:
                              len([i for i in x.get_children()
                                   if i.token.type == TokenTypes.Label and
                                   i.token.value == label]) > 0,
                              [i for i in self.root.get_children()
                               if i.token.type is TokenTypes.BasicBlock])
        queue.insert(0, next(basic_blocks))
        return queue

    def execute_if(self, node, queue) -> List[Node]:
        condition, true_label, false_label = node.get_children()
        result_condition = self.execute_expr(condition)
        if result_condition == 1:
            queue = self.execute_goto(true_label, queue)
        else:
            queue = self.execute_goto(false_label, queue)
        return queue

    def execute_return(self, node) -> None:
        expr = node.get_children()[0]
        result_expr = self.execute_expr(expr)
        print(result_expr)
        self.clear_variables()

    def clear_variables(self) -> None:
        self.variables.clear()
