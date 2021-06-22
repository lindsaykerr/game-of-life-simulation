from math import ceil, floor
import tkinter as tk

from .gui_variables import TkAppVariables


def is_integer(value) -> bool:
    """
    checks if value is an integer
    """
    try:
        return int(value) % 1 == 0
    except:
        return False

class ValidationMethods:
    '''
    Provides a number of validation methods which can be used with
    inputs widgets.
    ''' 
    @staticmethod
    def is_valid_range(value, var1: tk.Variable, start=0, end=100):
        if is_integer(value) and int(value) in range(start, end+1):
            return True
        else: 
            if len(str(var1.get())) > 1:
                var1.set(str(var1.get())[:-1])
            else:
                var1.set("0")
            return False


    @staticmethod
    def  is_valid_x(
        value, 
        var1: tk.Variable, 
        **kargs
        ):
        if is_integer(value) and int(value) in range(kargs['start'], kargs['end']+1):
            TkAppVariables.grid_y.set(floor(int(var1.get()) / kargs['factor']))
        
            kargs['y_widget'].configure(
                textvariable=TkAppVariables.grid_y
            )
            kargs['y_widget'].update()
            
            return True
        else: 
            if len(str(var1.get())) > 1:
                var1.set(str(var1.get())[:-1])
            else:
                var1.set(kargs['default'])
          
            kargs['y'].set(floor(int(var1.get()) / kargs['factor']))
            kargs['y_widget'].configure(
                textvariable=kargs['y']
            )
            kargs['y_widget'].update()
            
            return False

    @staticmethod
    def  is_valid_y(
        value, 
        var1: tk.Variable, 
        **kargs
        ):
        if is_integer(value) and int(value) in range(kargs['start'], kargs['end']+1):
           
            kargs['x'].set(ceil(int(var1.get()) * kargs['factor']))
            kargs['x_widget'].configure(
                textvariable=kargs['x']
            )
            kargs['x_widget'].update()
            
            return True
        else: 
            if len(str(var1.get())) > 1:
                var1.set(str(var1.get())[:-1])

            else:
                var1.set(kargs['default'])
            
       
            kargs['x'].set(ceil(int(var1.get()) * kargs['factor']))
            kargs['x_widget'].configure(
                textvariable=kargs['x']
            )
            kargs['x_widget'].update()
            
            return False

    @staticmethod
    def is_positive_int(value, in_func: tk.Variable):
        try:
            return is_integer(value) and int(value) > 0
        except:
            if len(str(in_func.get())) > 1:
                in_func.set(str(in_func.get())[:-1])
            else:
                in_func.set("0")
            return False

    @staticmethod
    def is_Y_position(value, var, **kargs):
        return is_integer(value) and int(value) >=0 and int(value) < int(TkAppVariables.grid_y.get())

    @staticmethod
    def is_X_position(value, var, **kargs):
        return is_integer(value) and int(value) >=0 and int(value) < int(TkAppVariables.grid_x.get())


class ValidationAssignment:
    """
    Used to assign a validation method to a general method which in turn 
    can be used by kinter for input validation.
    
    Implements a strategy pattern allowing validation methods to be swappable,

    Methods:

    method(value) -- function
        accepts a tkinter variable for validation testing, this variable can also
        be modified by a validation function

    back_to_default() : none
        set the tkinter input variable to its initial value 

    set_method(func, **kargs)
        allows validation functions to swapped and set.

    """
    _input_var = None

    def __init__(self, input_var:tk.Variable, func, **kargs) -> None:
        """
        Parameters:
     
        input_var -- tk.Variable
            a tkinter variable, contains data for validation
        func -- ValidationMethod.staticmethod
            a validation method which checks the contraints placed on the input_var
            holds true.
        **kargs
            any keyword argurments that are required by the validation method/function 
        
        """

        self._default = input_var.get()    # holds initial value
        self._input_var = input_var
        self._func = func 
        self._key_args = kargs


    # uses the strategy pattern to change validation methods    
    def set_method(self, func, **kargs):
        """
        Allows validation functions to swapped and set. 
        
        Parameters:

        func -- ValidationMethod.staticmethod 
            A validation method 
        **kargs
            any keyword argurments that are required by the validation method/function 
        """
        
        self._key_args = kargs
        self._func = func

    def method(self, value):
        """
        A validation method in a form which can be accepted by tkinter

        Parameters:
        value -- tk.Variable 
            a tkinter variable, contains data for validation

        """
        return self._func(value, self._input_var, **self._key_args) 
        
    def back_to_default(self):
        """
        Sets the tkinter validation variable back to its initial value 
        """
        self._input_var.set(self._default)