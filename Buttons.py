from Board import *

class Buttons(QFrame):

    def __init__(self, parent=None):
        super(Buttons, self).__init__(parent)
        self.setFixedSize(200, 600)


        button = QPushButton()
        button.setText("BUTTON")

        button2 = QPushButton()
        button2.setText("BUTTON2")

        layout = QVBoxLayout()
        layout.addWidget(button)
        layout.addWidget(button2)

        self.setLayout(layout)
