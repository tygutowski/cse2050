from functools import partial
from PyQt5.QtWidgets import (
    QWidget,
    QPushButton,
    QGridLayout,
    QLineEdit,
    QVBoxLayout
)

# i only used one class because i feel like intentionally
# abstracting it further would only overcomplicate it.
class Calculator(QWidget):
    # initializes all of the neccesary items for
    # the calculator to work, such as the widget window, the
    # output textbox, and the button grid
    def __init__(self):
        super().__init__()
        self.setup_widget()
        self.setup_textbox()
        self.setup_buttons()

    # sets up the widget, which sets the layout,
    # moves the window to the appropriate position,
    # changes the window's size, and changes its name.
    def setup_widget(self):
        self.vertical_layout = QVBoxLayout()
        self.central_widget = QWidget(self)
        self.central_widget.setLayout(self.vertical_layout)
        self.move(300, 150)
        self.setWindowTitle("Calculator")
        self.setFixedSize(440, 230)

    # puts all of the buttons onto a QGridLayout, then
    # connects them all to the input_item method
    def setup_buttons(self):
        grid_layout = QGridLayout()
        # button list (to make buttons with!)
        button_labels = [
            "Cls",
            "(",
            ")",
            "Close",
            "7",
            "8",
            "9",
            "/",
            "4",
            "5",
            "6",
            "*",
            "1",
            "2",
            "3",
            "-",
            "0",
            ".",
            "=",
            "+",
        ]
        # automatically determines the button's positions using their indexes
        button_positions = [(i, j) for i in range(5) for j in range(4)]
        buttons = {}
        for position, button_label in zip(button_positions, button_labels):
            if button_label == "":
                continue
            # instances new buttons for each in the list
            button = QPushButton(button_label, self)
            buttons[button_label] = button
            # if the button is the last column, make it longer.
            if position[1] == 3:
                grid_layout.addWidget(button, *position, *(position[1] - 2, 2))
            else:
                grid_layout.addWidget(button, *position)
        # for every button, connect it to its appropriate method.
        for button_label in buttons:
            if button_label not in {"=", "Close", "Cls"}:
                buttons[button_label].clicked.connect(
                    partial(self.input_item, button_label)
                )
        # connects these three buttons to the function that
        # closes, clears, and evaluates, respectively
        buttons["Close"].clicked.connect(self.close)
        buttons["Cls"].clicked.connect(self.clear_text)
        buttons["="].clicked.connect(self.evaluate)
        self.vertical_layout.addLayout(grid_layout)

    # sets up the textbox output line with the appropriate
    # size, sets it to read only, and adds it to the
    # vertical layout
    def setup_textbox(self):
        self.text = QLineEdit()
        self.text.setFixedHeight(35)
        self.text.setFixedWidth(420)
        self.text.setReadOnly(True)
        self.vertical_layout.addWidget(self.text)

    # sets the textbox given a string
    def set_text(self, text):
        self.text.setText(text)
        self.text.setFocus()

    # returns the text in the textbox output
    def get_text(self):
        return self.text.text()

    # clears the text in the textbox output
    def clear_text(self):
        self.set_text("")

    # gets item inputted, then adds it to the textbox
    # output using set_text()
    def input_item(self, button):
        expression = self.get_text() + button
        self.set_text(expression)

    # attemps to evaluate the expression. if its valid, it
    # sets the textbox output to the evaluation. if there is
    # an error, then it excepts the error and outputs "ERROR."
    # i didnt use djiktra's shunting algorithm because id
    # waited until the last minute!
    def evaluate(self):
        try:
            self.set_text(str(eval(self.get_text())))
        except:
            self.set_text("ERROR")
