from . import *

class StackMonad:
    """Monadic wrapper around a Stack, used for the pop and push operations"""
    def __init__(self, stack=None, out=[]) -> None:
        if stack is None:
            self.stack = Stack()
        else:
            self.stack = stack
        self.out = out

    def bind(self, f) -> 'StackMonad':
        result, out = f(self.stack)
        if result is None:
            return StackMonad(self.stack)
        elif out is None:
            return StackMonad(result)
        else:
            self.out.append(out)
            return StackMonad(result)

    def __rshift__(self, f) -> 'StackMonad':
        return self.bind(f) 


class Node:
    def __init__(self, val=None, n=None):
        self.value = val
        self.next = n


class Stack:
    def __init__(self):
        self.top = Node()

    def __str__(self):
        cur = self.top
        msg = f'top: '
        while cur is not None:
            msg += f'{cur.value}\n     '
            cur = cur.next
        return msg

    @staticmethod
    def push(value):
        def inner_push(stack):
            if stack.top is None:
                stack.top = Node(value)
            else:
                stack.top = Node(value, stack.top)
            return stack, None
        return inner_push

    @staticmethod
    def pop():
        def inner_pop(stack):
            val = stack.top.value
            stack.top = stack.top.next
            return stack, val
        return inner_pop
