import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QGridLayout, QPushButton
from PyQt5.QtCore import Qt

class Calculator:
    def __init__(self):
        self.win = QWidget()
        self.win.setWindowTitle('计算器')
        self.win.resize(200, 250)

        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignRight) 
        self.display.setFixedHeight(35)          
        self.display.setReadOnly(True)           

        layout = QGridLayout()
        self.win.setLayout(layout)
        layout.addWidget(self.display, 0, 0, 1, 4)

        button_groups = [
            ['C', '(', ')', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '=', '='] 
        ]

        for row, buttons in enumerate(button_groups):
            for col, button_text in enumerate(buttons):
                if button_text == '=' and row == 4 and col == 3:
                    continue 
                
                btn = QPushButton(button_text)
                btn.setFixedSize(35, 35)
                layout.addWidget(btn, row + 1, col)

                if button_text == 'C':
                    btn.clicked.connect(self.clear_display)
                elif button_text == '=':
                    btn.clicked.connect(self.calculate_result)
                else:
                    btn.clicked.connect(self.append_text)

    def clear_display(self):
        self.display.setText('')

    def calculate_result(self):
        try:
            result = str(eval(self.display.text()))
            self.display.setText(result)
        except Exception:
            self.display.setText("Error")

    def append_text(self):
        btn = self.win.sender() 
        self.display.setText(self.display.text() + btn.text())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.win.show()
    sys.exit(app.exec_())
