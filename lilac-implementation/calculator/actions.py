from . import *

class LiteralAction:
    def __init__(self, val):
        self.val = val

    def run(self, glob):
        glob.stackmonad >> Stack.push(self.val)
        return glob


class AssignAction():
    def __init__(self):
        pass

    def run(self, glob):
        
        glob.stackmonad >> Stack.pop() >> Stack.pop()
        val1 = glob.stackmonad.out[-1]
        val2 = glob.stackmonad.out[-2]
        
        glob.table[val1] = val2 
        return glob


class ArithmeticAction:
    def __init__(self):
        pass

    def check(self, glob, op1, op2):
        # if try
        if isinstance(op1, str):
            try:
                val1 = glob.table[op1]
            except:
                print(f'Identifier {op1} does not exist in the data table')
        else:
            val1 = op1

        if isinstance(op2, str):
            val2 = glob.table[op2]
        else:
            val2 = op2

        return val1, val2



class AdditionAction(ArithmeticAction):
    def __init__(self):
        pass
    
    def run(self, glob):
        glob.stackmonad >> Stack.pop() >> Stack.pop()
        op1 = glob.stackmonad.out[-1]
        op2 = glob.stackmonad.out[-2]
        
        # check the results
        val1, val2 = self.check(glob, op1, op2) 

        # do the operation
        ans = val1 + val2
        glob.stackmonad >> Stack.push(ans)
        return glob

class SubtractionAction(ArithmeticAction):
    def __init__(self):
        pass
    
    def run(self, glob):
        
        glob.stackmonad >> Stack.pop() >> Stack.pop()
        op1 = glob.stackmonad.out[-1]
        op2 = glob.stackmonad.out[-2]
        
        # Check the results
        val1, val2 = self.check(glob, op1, op2)

        # Do the operation
        ans = val1 - val2
        glob.stackmonad >> Stack.push(ans)
        return glob

class MultiplicationAction(ArithmeticAction):
    def __init__(self):
        pass
    
    def run(self, glob):
        
        glob.stackmonad >> Stack.pop() >> Stack.pop()
        op1 = glob.stackmonad.out[-1]
        op2 = glob.stackmonad.out[-2]
        
        # check the results
        val1, val2 = self.check(glob, op1, op2) 

        # do the operation
        ans = val1 * val2
        glob.stackmonad >> Stack.push(ans)
        return glob

class DivisionAction(ArithmeticAction):
    def __init__(self):
        pass
    
    def run(self, glob):
        
        glob.stackmonad >> Stack.pop() >> Stack.pop()
        op1 = glob.stackmonad.out[-1]
        op2 = glob.stackmonad.out[-2]
        
        # check the results
        val1, val2 = self.check(glob, op1, op2) 

        # do the operation
        ans = val1 / val2
        glob.stackmonad >> Stack.push(ans)
        return glob