import sys
from Board import *
from Rules import *
from Game import *
from Buttons import *


class Phwar(QMainWindow):
    def __init__(self):
        super(Phwar, self).__init__()

        self.init_ui()

    def init_ui(self):

        self.resize(800, 600)
        self.center()

        window = QWidget()
        window.setFixedSize(800, self.size().height())

        layout = QBoxLayout(QBoxLayout.LeftToRight)
        layout.setContentsMargins(0, 0, 0, 0)

        self.pboard = Board(7, 7, 5, window)
        self.prules = Rules(self.pboard)
        self.pgame = Game(self.pboard, self.prules)
        self.buttons = Buttons(window)
        '''self.prules.make_connection_to_board(self.pboard)
        self.pgame.make_connection_to_board(self.pboard)'''

        layout.addWidget(self.pboard)
        layout.addWidget(self.buttons)
        window.setLayout(layout)

        self.setCentralWidget(window)
        self.setWindowTitle('Phwar')
        self.show()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.resize(0.7*screen.height(), 0.8*screen.height())
        self.move(screen.width() - (1.05*size.width()), 0.05*size.height())

if __name__ == "__main__":
    app = QApplication([])
    phwar = Phwar()
    sys.exit(app.exec_())
