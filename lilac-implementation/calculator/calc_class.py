from . import *

class Calculator:
    def __init__(self):
        self.env = EnvMonad()
        self.show_stack = False

    def evaluate(self, source):
        cleaned = "".join(source.split())
        print(cleaned)
        # rpn = list(Parser.convert_to_rpn(cleaned))
        action_list = []

        # # for t in rpn:
        #     print(t)
        #     if t in '0123456789':
        #         action_list.append(LiteralAction(int(t)))
        #     elif t.isalpha():
        #         action_list.append(LiteralAction(t))
        #     elif t == '+':
        #         action_list.append(AdditionAction())
        #     elif t == '-':
        #         action_list.append(SubtractionAction())
        #     elif t == '*':
        #         action_list.append(MultiplicationAction())
        #     elif t == '/':
        #         action_list.append(DivisionAction())
        #     elif t == ':':
        #         action_list.append(AssignAction())
        #     else:
        #         pass

        for a in action_list:  
            self.env >> a
            if self.show_stack:
                print(self.env.env.stackmonad.stack)

        print(self.env.env.stackmonad.stack.top.value)

    def print_table(self):
        print(self.env.env.table)
