from PyQt6.QtWidgets import *
from view import *
import math
import operator

ops = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '//': operator.floordiv
}


class Controller(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)

        self.current_num = 1
        self.num1 = ''
        self.num2 = ''
        self.operator = None
        self.clear_entry = False

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
        self.button_sign.clicked.connect(lambda: self.sign())
        self.button_plus.clicked.connect(lambda: self.add())
        self.button_minus.clicked.connect(lambda: self.subtract())
        self.button_times.clicked.connect(lambda: self.multiply())
        self.button_divide.clicked.connect(lambda: self.divide())
        self.button_equals.clicked.connect(lambda: self.result())
        self.button_sin.clicked.connect(lambda: self.sine())
        self.button_cos.clicked.connect(lambda: self.cosine())
        self.button_tan.clicked.connect(lambda: self.tangent())

    def number(self, num):
        if self.current_num == 1:
            if len(f'{self.num1}') < 7:
                self.num1 = int(f'{self.num1}' + f'{num}')
                self.entry.setText(f'{self.num1}')

        elif self.current_num == 2:
            if len(f'{self.num2}') < 7:
                self.num2 = int(f'{self.num2}' + f'{num}')
                self.entry.setText(f'{self.num2}')

        if not self.clear_entry:
            self.clear_entry = True
            self.button_clear.setText('CE')

    def clear(self):
        if self.clear_entry:
            if self.current_num == 1:
                self.num1 = ''
                self.entry.setText('')
            elif self.current_num == 2:
                self.num2 = ''
                self.entry.setText('')

            self.clear_entry = False
            self.button_clear.setText('C')

        else:
            self.num1 = ''
            self.num2 = ''
            self.current_num = 1
            self.operator = None
            self.entry.setText('')

    def sign(self):
        if self.current_num == 1 and self.num1 != '':
            self.num1 = -self.num1
            self.entry.setText(f'{self.num1}')
        elif self.current_num == 2 and self.num2 != '':
            self.num2 = -self.num2
            self.entry.setText(f'{self.num2}')

    def add(self):
        if self.current_num == 2 and self.num2 != '':
            self.num1 = ops[self.operator](self.num1, self.num2)
            self.num2 = ''

        self.operator = '+'
        # self.entry.setText('+')
        if self.num1 != '':
            self.current_num = 2

    def subtract(self):
        if self.current_num == 2 and self.num2 != '':
            self.num1 = ops[self.operator](self.num1, self.num2)
            self.num2 = ''

        self.operator = '-'
        # self.entry.setText('-')
        if self.num1 != '':
            self.current_num = 2

    def multiply(self):
        if self.current_num == 2 and self.num2 != '':
            self.num1 = ops[self.operator](self.num1, self.num2)
            self.num2 = ''

        self.operator = '*'
        # self.entry.setText('×')
        if self.num1 != '':
            self.current_num = 2

    def divide(self):
        if self.current_num == 2 and self.num2 != '':
            self.num1 = ops[self.operator](self.num1, self.num2)
            self.num2 = ''

        self.operator = '//'
        # self.entry.setText('÷')
        if self.num1 != '':
            self.current_num = 2

    def result(self):
        if self.num1 != '' and self.num2 != '':
            self.current_num = 1
            self.num1 = ops[self.operator](self.num1, self.num2)
            self.entry.setText(f'{self.num1}')
            self.num2 = ''
            self.operator = None

    def sine(self):
        pass

    def cosine(self):
        pass

    def tangent(self):
        pass
