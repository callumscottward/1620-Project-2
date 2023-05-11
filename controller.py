from PyQt6.QtWidgets import *
from view import *
import math
import operator

# ops dict along with operator module allows for operations between numbers to be more
# succinctly completed by converting self.operator (str) to an operation
ops = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv
}


class Controller(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs) -> None:
        """
        Initializes GUI controller, adding backend-frontend integration for calculator
        based on view.py file.
        :param args: Essential for functionality of PyQt, based on Test 10 code
        :param kwargs: See above
        """
        # PyQt vars from Test 10
        super().__init__(*args, **kwargs)
        self.setupUi(self)

        # Basic variables for calculator functionality, with current_num determining
        # which number of a two-number calculation the user is on, num1 and num2 holding
        # number values, operator determining which math operator is active, clear_entry
        # determining whether clear button clears all or just the current number,
        # add_decimal preparing to add a decimal, and ans_displayed allowing text from an
        # answer to be overwritten by the next number press
        self.current_num = 1
        self.num1 = 0
        self.num2 = None
        self.operator = None
        self.clear_entry = False
        self.add_decimal = False
        self.ans_displayed = False

        # Number button connections to number method with different parameters
        self.button_0.clicked.connect(lambda: self.number(0))
        self.button_1.clicked.connect(lambda: self.number(1))
        self.button_2.clicked.connect(lambda: self.number(2))
        self.button_3.clicked.connect(lambda: self.number(3))
        self.button_4.clicked.connect(lambda: self.number(4))
        self.button_5.clicked.connect(lambda: self.number(5))
        self.button_6.clicked.connect(lambda: self.number(6))
        self.button_7.clicked.connect(lambda: self.number(7))
        self.button_8.clicked.connect(lambda: self.number(8))
        self.button_9.clicked.connect(lambda: self.number(9))

        # Other buttons connecting to respective parameters
        self.button_clear.clicked.connect(lambda: self.clear())
        self.button_point.clicked.connect(lambda: self.decimal())
        self.button_plus.clicked.connect(lambda: self.add())
        self.button_minus.clicked.connect(lambda: self.subtract())
        self.button_times.clicked.connect(lambda: self.multiply())
        self.button_divide.clicked.connect(lambda: self.divide())
        self.button_equals.clicked.connect(lambda: self.result())
        self.button_sin.clicked.connect(lambda: self.sine())
        self.button_cos.clicked.connect(lambda: self.cosine())
        self.button_tan.clicked.connect(lambda: self.tangent())

    def number(self, num: int) -> None:
        """
        Very extensive method called when any number is pressed. Appends an integer to
        whichever number is active, appends a decimal if add_decimal is true, and makes
        sure clear button acts as clear entry when numbers are displayed.
        :param num: Number button pressed on which calculations are performed
        """
        self.reset_operations()

        if self.ans_displayed:
            self.clear()
            self.ans_displayed = False

        if self.add_decimal:
            # Block to append number after decimal spot if decimal button has been pressed
            if self.current_num == 1:
                self.num1 = float(f'{self.num1}.{num}')
                self.entry.setText(f'{self.num1}')
                self.add_decimal = False

            elif self.current_num == 2:
                self.num2 = float(f'{self.num2}.{num}')
                self.entry.setText(f'{self.num2}')
                self.add_decimal = False

        else:
            # Normal number appending
            if self.current_num == 1 and len(f'{self.num1}') < 7 and self.operator is None:
                # Append number to num1 if length is short enough to fit and no operator yet
                self.num1 = float(f'{self.num1}' + f'{num}')

                if self.num1 % 1 == 0:
                    self.num1 = int(self.num1)

                self.entry.setText(f'{self.num1}')

            elif self.current_num == 1 and self.operator is not None:
                # Change current_num to 2 since an operator is selected and set num2's value
                self.current_num = 2
                self.num2 = num
                self.entry.setText(f'{self.num2}')

            elif self.current_num == 2 and len(f'{self.num2}') < 7:
                # Append to num2 if short enough
                if self.num2 is None:
                    self.num2 = 0

                self.num2 = float(f'{self.num2}' + f'{num}')

                if self.num2 % 1 == 0:
                    # Cut off decimal if ends in .0
                    self.num2 = int(self.num2)

                self.entry.setText(f'{self.num2}')

        if not self.clear_entry:
            self.clear_entry = True
            self.button_clear.setText('CE')

    def clear(self) -> None:
        """
        Either clears current number if clear_entry is true or everything if not.
        """
        if self.clear_entry:
            # Only clears current number
            if self.current_num == 1:
                self.num1 = 0
                self.entry.setText('0')
            elif self.current_num == 2:
                self.num2 = 0
                self.entry.setText('0')

            self.clear_entry = False
            self.button_clear.setText('C')

        else:
            # Resets almost everything back to defaults
            self.reset_operations()
            self.num1 = 0
            self.num2 = None
            self.current_num = 1
            self.operator = None
            self.entry.setText('0')
            self.add_decimal = False
            self.ans_displayed = False

    def decimal(self) -> None:
        """
        Prepares for number method to add a decimal in, and adds an implied 0 if number
        does not have a value (i.e., 0.8 instead of just .8).
        """
        if self.current_num == 1 and self.operator is not None:
            # Starts num2 with 0. if no number was pressed prior
            self.add_decimal = True
            self.reset_operations()
            self.current_num = 2
            self.num2 = 0
            self.entry.setText('0.')

        elif self.current_num == 1 and '.' not in self.entry.text():
            # Prep num1 for decimal
            self.add_decimal = True
            self.entry.setText(f'{self.num1}.')

        elif self.current_num == 2 and '.' not in self.entry.text():
            # Prep num2 for decimal
            self.add_decimal = True
            self.entry.setText(f'{self.num2}.')

    def add(self) -> None:
        """
        Sets operator to addition and performs retroactive calculations if pending.
        """
        self.reset_operations()
        self.button_plus.setChecked(True)

        if self.current_num == 2 and self.num2 is not None:
            # Retroactive calculations, accounting for zero division
            try:
                self.num1 = ops[self.operator](self.num1, self.num2)
                self.current_num = 1
            except ZeroDivisionError:
                self.entry.setText('Error')
                self.ans_displayed = True
                self.num1 = 0

        self.operator = '+'

    def subtract(self) -> None:
        """
        Sets operator to addition and performs retroactive calculations if pending.
        """
        self.reset_operations()
        self.button_minus.setChecked(True)

        if self.current_num == 2 and self.num2 is not None:
            # Retroactive calculations, accounting for zero division
            try:
                self.num1 = ops[self.operator](self.num1, self.num2)
                self.current_num = 1
            except ZeroDivisionError:
                self.entry.setText('Error')
                self.ans_displayed = True
                self.num1 = 0

        self.operator = '-'

    def multiply(self) -> None:
        """
        Sets operator to multiplication and performs retroactive calculations if pending.
        """
        self.reset_operations()
        self.button_times.setChecked(True)

        if self.current_num == 2 and self.num2 is not None:
            # Retroactive calculations, accounting for zero division
            try:
                self.num1 = ops[self.operator](self.num1, self.num2)
                self.current_num = 1
            except ZeroDivisionError:
                self.entry.setText('Error')
                self.ans_displayed = True
                self.num1 = 0

        self.operator = '*'

    def divide(self) -> None:
        """
        Sets operator to division and performs retroactive calculations if pending.
        """
        self.reset_operations()
        self.button_divide.setChecked(True)

        if self.current_num == 2 and self.num2 is not None:
            # Retroactive calculations, accounting for zero division
            try:
                self.num1 = ops[self.operator](self.num1, self.num2)
                self.current_num = 1
            except ZeroDivisionError:
                self.entry.setText('Error')
                self.ans_displayed = True
                self.num1 = 0

        self.operator = '/'

    def result(self) -> None:
        """
        Returns result of calculations to entry label, making that number the new num1
        for future calculations and ensuring it can be easily overwritten with number's
        block for if ans_displayed
        """
        self.reset_operations()
        self.current_num = 1

        if self.num2 is not None:
            # Performs calculations if num2 exists, accounting for zero division
            try:
                self.num1 = ops[self.operator](self.num1, self.num2)
            except ZeroDivisionError:
                self.entry.setText('Error')
                self.num1 = 0
            else:
                if self.num1 % 1 == 0:
                    self.num1 = int(self.num1)

                if len(f'{self.num1}') < 8:
                    # Exact answer if short enough
                    self.entry.setText(f'{self.num1}')
                else:
                    # Cut off with ellipses if too long
                    self.entry.setText(f'{self.num1}'[0:5] + '...')

        self.num2 = None
        self.operator = None
        self.ans_displayed = True

    def sine(self) -> None:
        """
        Calculates and immediately displays the sine of the current number, with
        display logic very similar to that of return method.
        """
        self.reset_operations()

        if self.current_num == 1:
            self.num1 = math.sin(self.num1)

            if self.num1 % 1 == 0:
                self.num1 = int(self.num1)

            if len(f'{self.num1}') < 8:
                self.entry.setText(f'{self.num1}')
            else:
                self.entry.setText(f'{self.num1}'[0:5] + '...')

        elif self.current_num == 2:
            self.num2 = math.sin(self.num2)

            if self.num2 % 1 == 0:
                self.num2 = int(self.num2)

            if len(f'{self.num2}') < 8:
                self.entry.setText(f'{self.num2}')
            else:
                self.entry.setText(f'{self.num2}'[0:5] + '...')

    def cosine(self) -> None:
        """
        Calculates and immediately displays the cosine of the current number, with
        display logic very similar to that of return method.
        """
        self.reset_operations()

        if self.current_num == 1:
            self.num1 = math.cos(self.num1)

            if self.num1 % 1 == 0:
                self.num1 = int(self.num1)

            if len(f'{self.num1}') < 8:
                self.entry.setText(f'{self.num1}')
            else:
                self.entry.setText(f'{self.num1}'[0:5] + '...')

        elif self.current_num == 2:
            self.num2 = math.cos(self.num2)

            if self.num2 % 1 == 0:
                self.num2 = int(self.num2)

            if len(f'{self.num2}') < 8:
                self.entry.setText(f'{self.num2}')
            else:
                self.entry.setText(f'{self.num2}'[0:5] + '...')

    def tangent(self) -> None:
        """
        Calculates and immediately displays the tangent of the current number, with
        display logic very similar to that of return method.
        """
        self.reset_operations()

        if self.current_num == 1:
            self.num1 = math.tan(self.num1)

            if self.num1 % 1 == 0:
                self.num1 = int(self.num1)

            if len(f'{self.num1}') < 8:
                self.entry.setText(f'{self.num1}')
            else:
                self.entry.setText(f'{self.num1}'[0:5] + '...')

        elif self.current_num == 2:
            self.num2 = math.tan(self.num2)

            if self.num2 % 1 == 0:
                self.num2 = int(self.num2)

            if len(f'{self.num2}') < 8:
                self.entry.setText(f'{self.num2}')
            else:
                self.entry.setText(f'{self.num2}'[0:5] + '...')

    def reset_operations(self) -> None:
        """
        Deselects any currently selected operator button to prevent multiple being checked
        simultaneously. It takes several lines and occurs frequently enough in the code
        that I felt a standalone method would be handy.
        """
        if self.button_plus.isChecked():
            self.button_plus.setChecked(False)
        if self.button_minus.isChecked():
            self.button_minus.setChecked(False)
        if self.button_times.isChecked():
            self.button_times.setChecked(False)
        if self.button_divide.isChecked():
            self.button_divide.setChecked(False)
