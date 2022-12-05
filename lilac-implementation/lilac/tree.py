from . import StatusHandler

class Tree:
    def __init__(self, data, action, left=None, right=None) -> None:
        self.data = data
        self.left = left
        self.right = right
        
        self.action = action
        self.action.left = self.left
        self.action.right = self.right

    def __str__(self) -> str:
        if self.is_leaf():
            return f'{self.data}'
        return f"({self.data}, left:{self.left}, right:{self.right})"

    def post_order(self) -> str:
        string = ''
        if not self.is_leaf():
            string += self.left.post_order()
            string += self.right.post_order()
            string += self.data
        else:
            string = self.data
        return string

    def post_order_list(self):
        out_list = []
        if not self.is_leaf():
            out_list += self.left.post_order_list()
            out_list += self.right.post_order_list()
            out_list += self.data
        else:
            out_list = [self.data]
        return out_list

    def in_order(self):
        string = f''
        if not self.is_leaf():
            string += f'({self.left.in_order()}'
            string += self.data.lexeme
            string += f'{self.right.in_order()})'
        else:
            string = self.data.lexeme
        return string

    def is_leaf(self):
        return (self.left is None and self.right is None)


