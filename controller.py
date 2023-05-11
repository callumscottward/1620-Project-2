from PyQt6.QtWidgets import *
from view import *
import math
import operator

ops = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv
}


class Controller(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)

        self.current_num = 1
        self.num1 = 0
        self.num2 = None
        self.operator = None
        self.clear_entry = False
        self.add_decimal = False
        self.ans_displayed = False

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

    def number(self, num):
        self.reset_operations()

        if self.ans_displayed:
            self.clear()
            self.ans_displayed = False

        if self.add_decimal:
            if self.current_num == 1:
                self.num1 = float(f'{self.num1}.{num}')
                self.entry.setText(f'{self.num1}')
                self.add_decimal = False

            elif self.current_num == 2:
                self.num2 = float(f'{self.num2}.{num}')
                self.entry.setText(f'{self.num2}')
                self.add_decimal = False

        else:
            if self.current_num == 1 and len(f'{self.num1}') < 7 and self.operator is None:
                self.num1 = float(f'{self.num1}' + f'{num}')

                if self.num1 % 1 == 0:
                    self.num1 = int(self.num1)

                self.entry.setText(f'{self.num1}')

            elif self.current_num == 1 and self.operator is not None:
                self.current_num = 2
                self.num2 = num
                self.entry.setText(f'{self.num2}')

            elif self.current_num == 2 and len(f'{self.num2}') < 7:
                if self.num2 is None:
                    self.num2 = 0

                self.num2 = float(f'{self.num2}' + f'{num}')

                if self.num2 % 1 == 0:
                    self.num2 = int(self.num2)

                self.entry.setText(f'{self.num2}')

        if not self.clear_entry:
            self.clear_entry = True
            self.button_clear.setText('CE')

    def clear(self):
        if self.clear_entry:
            if self.current_num == 1:
                self.num1 = 0
                self.entry.setText('0')
            elif self.current_num == 2:
                self.num2 = 0
                self.entry.setText('0')

            self.clear_entry = False
            self.button_clear.setText('C')

        else:
            self.reset_operations()
            self.num1 = 0
            self.num2 = None
            self.current_num = 1
            self.operator = None
            self.entry.setText('0')
            self.add_decimal = False
            self.ans_displayed = False

    def decimal(self):
        if self.current_num == 1 and self.operator is not None:
            self.add_decimal = True
            self.reset_operations()
            self.current_num = 2
            self.num2 = 0
            self.entry.setText('0.')

        elif self.current_num == 1 and '.' not in self.entry.text():
            self.add_decimal = True
            self.entry.setText(f'{self.num1}.')

        elif self.current_num == 2 and '.' not in self.entry.text():
            self.add_decimal = True
            self.entry.setText(f'{self.num2}.')

    def add(self):
        self.reset_operations()
        self.button_plus.setChecked(True)

        if self.current_num == 2 and self.num2 is not None:
            try:
                self.num1 = ops[self.operator](self.num1, self.num2)
                self.current_num = 1
            except ZeroDivisionError:
                self.entry.setText('Error')
                self.ans_displayed = True
                self.num1 = 0

        self.operator = '+'

    def subtract(self):
        self.reset_operations()
        self.button_minus.setChecked(True)

        if self.current_num == 2 and self.num2 is not None:
            try:
                self.num1 = ops[self.operator](self.num1, self.num2)
                self.current_num = 1
            except ZeroDivisionError:
                self.entry.setText('Error')
                self.ans_displayed = True
                self.num1 = 0

        self.operator = '-'

    def multiply(self):
        self.reset_operations()
        self.button_times.setChecked(True)

        if self.current_num == 2 and self.num2 is not None:
            try:
                self.num1 = ops[self.operator](self.num1, self.num2)
                self.current_num = 1
            except ZeroDivisionError:
                self.entry.setText('Error')
                self.ans_displayed = True
                self.num1 = 0

        self.operator = '*'

    def divide(self):
        self.reset_operations()
        self.button_divide.setChecked(True)

        if self.current_num == 2 and self.num2 is not None:
            try:
                self.num1 = ops[self.operator](self.num1, self.num2)
                self.current_num = 1
            except ZeroDivisionError:
                self.entry.setText('Error')
                self.ans_displayed = True
                self.num1 = 0

        self.operator = '/'

    def result(self):
        self.reset_operations()
        self.current_num = 1

        if self.num2 is not None:
            try:
                self.num1 = ops[self.operator](self.num1, self.num2)
            except ZeroDivisionError:
                self.entry.setText('Error')
                self.num1 = 0
            else:
                if self.num1 % 1 == 0:
                    self.num1 = int(self.num1)

                if len(f'{self.num1}') < 8:
                    self.entry.setText(f'{self.num1}')
                else:
                    self.entry.setText(f'{self.num1}'[0:5] + '...')

        self.num2 = None
        self.operator = None
        self.ans_displayed = True

    def sine(self):
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

    def cosine(self):
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

    def tangent(self):
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

    def reset_operations(self):
        if self.button_plus.isChecked():
            self.button_plus.setChecked(False)
        if self.button_minus.isChecked():
            self.button_minus.setChecked(False)
        if self.button_times.isChecked():
            self.button_times.setChecked(False)
        if self.button_divide.isChecked():
            self.button_divide.setChecked(False)
