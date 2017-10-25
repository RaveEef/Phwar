from Move import *
from UI import *
from Utils import Searching

NOT_VALID = 0
VALID = 1
STOP_AT_CENTER = 2

INIT_PIECES = [("BN", "E1"),
               ("BP1", "C1")]
'''("BP2", "F2"), ("BP3", "B4"), ("BP4", "E2"),
               ("BE1", "B2"), ("BE2", "D2"), ("BE3", "G2"), ("BE4", "D3"),
               ("WN", "D7"),
               ("WP1", "C6"), ("WP2", "E6"), ("WP3", "C5"), ("WP4", "F4"),
               ("WE1", "B6"), ("WE2", "D6"), ("WE3", "G5"), ("WE4", "E5")]'''

class Board(QObject):

    searcher = Searching()

    def __init__(self, NR, NC, R=None):
        super(Board, self).__init__()
        self.R = R

        self.NR = NR
        self.NR_COORD = 2*self.NR - 1
        self.NC = NC
        self.tiles = list()
        self.axial_tiles = dict()
        self.names = list()
        for i in range(self.NR):
            self.tiles.append(list())
            self.names.append(list())
            for j in range(self.NC):
                self.names[i].append("*")
                self.tiles[i].append("")

        # [ ** ** ** D1 ** ** ** | ** ** C1 ** E1 ** ** ]
        # [ ** B2 ** D2 **
        # [          d3
        # D4
        # D5
        # F6
        # D7

        self.init_names()
        self.init_pieces()
        print self.names
        self.output_board()
        self.axials(0, 0)

    def axials(self, x, y):

        q = x * 2/3 / 6
        r = (-x / 3 + sqrt(3)/3 - y) / 6
        print q, r, (-q-r)

    def init_names(self):
        center_column = self.NC/2

        vertical_positioning = [(0, self.NR)]*7
        for i in range(self.NC):
            if i < center_column:
                start = (center_column - i)/2
                end = (center_column - (i - 1))/2
                vertical_positioning[i] = (start, self.NR - end - start + 1)
            if i > center_column:
                start = (i-center_column)/2
                end = (i - (center_column - 1))/2
                vertical_positioning[i] = (start, self.NR - end - start + 1)

        for j in range(self.NC):
            for i in range(vertical_positioning[j][0], vertical_positioning[j][1]):
                if j < center_column:
                    name = chr(j + 65) + str(i + 1) #abs(d)/2 + 1 + i - 2)
                else:
                    name = chr(j + 65) + str(i + 1) #d/2 + 1 + i)

                '''print "{:<10}".format(name), "{:<25}".format("axial_center_i: {}".format(axial_midcol_startrow)), \
                    "{:<25}".format("axial_center_z: {}".format(axial_midcol_z))
                print "{:<10}".format(''),\
                    "{:<25}".format("axial_i: {}".format(axial_i)), \
                    "{:<25}".format("axial_z: {}".format(axial_z))'''
                self.names[i][j] = name

    def init_pieces(self):
        for piece, tile in INIT_PIECES:
            row = int(tile[1:]) - 1
            col = ord(tile[0]) - 65
            self.tiles[row][col] = piece

        self.axials(1,2)
        #board = UI.currentBoard()
        #print board.S
        #board.set_board_pieces(self.tiles)

    #TODO: Terminal_state checker function

    def move_piece(self, _from, _to):
        if self.tiles[_from.x][_from.y] == "":
            return
        if self.tiles[_to.x][_to.y] != "":
            self.tiles[_to.x][_to.y] = ""
        self.tiles[_to.x][_to.y] = self.tiles[_from.x][_from.y]
        self.tiles[_from.x][_from.y] = ""

    # TODO V: valid(_from, _to, tiles, capture)
    # TODO V.1: --> if capture = False, include first if statement
    # TODO V.2: --> replace self.tiles by tiles
    # TODO V.3: --> nr = tiles.__len__(), nc = tiles[0].__len__()
    # TODO V.4: --> replace self.NR by nr and self.NC by nc
    def valid_move(self, _from, _to):
        if self.tiles[_to.x()][_to.y()] != "":
            return NOT_VALID

        alpha_from = self.names[_from.x()][_from.y()]
        alpha_to = self.names[_to.x()][_to.y()]

        if _from.y() == _to.y():
            if _from.x()() == _to.x()():
                return NOT_VALID
            if _from.x()() > _to.x()():
                for i in range(_from.x()() - _to.x()()):
                    if self.tiles[_from.x()() - i - 1][_from.y()] != "":
                        return NOT_VALID
                    if (_from.x()() - i - 1) == self.NR/2 and _from.y() == self.NC/2:
                        return STOP_AT_CENTER
            if _from.x()() < _to.x():
                for i in range(_from.x() - _to.x()):
                    if self.tiles[_from.x() + i + 1][_from.y()] != "":
                        return NOT_VALID
                    if (_from.x() + i - 1) == self.NR/2 and _from.y() == self.NC/2:
                        return STOP_AT_CENTER
        elif ((2 * _from.x()) - _from.y()) == ((2 * _to.x()) - _to.y()):
            if _from.y() > _to.y():
                for i in range(1, _from.y() - _to.y()):
                    if _from.y() % 2 == 0:
                        x = _from.x() - (i / 2)
                    else:
                        x = _from.x() - ((i / 2) + (i % 2))
                    if self.tiles[x][_from.y() - i] != "":
                        return NOT_VALID
                    if x == self.NR / 2 and (_from.y() - i) == self.NC / 2:
                        return STOP_AT_CENTER
            if _from.y() < _to.y():
                for i in range(1, _to.y() - _from.y()):
                    if _from.y() % 2 == 0:
                        x = _from.x() + ((i / 2) + (i % 2))
                    else:
                        x = _from.x() + (i / 2)
                    if self.tiles[x][_from.y() + i] != "":
                        return NOT_VALID
                    if x == self.NR / 2 and (_from + i) == self.NC/2:
                        return STOP_AT_CENTER
        elif ((2 * _from.x()) + _from.y()) == ((2 * _to.x()) + _to.y()):
            if _from.y() > _to.y():
                for i in range(1, _from.y() - _to.y()):
                    if _from.y() % 2 == 0:
                        x = _from.x() + ((i / 2) + (i % 2))
                    else:
                        x  = _from.x() + (i / 2)
                    if self.tiles[x][_from.y() - i] != "":
                        return NOT_VALID
                    if x == self.NR / 2 and (_from.y() - i) == self.NC / 2:
                        return STOP_AT_CENTER
            if _from.y() < _to.y():
                for i in range(1, _to.y() - _from.y()):
                    if _from.y() % 2 == 0:
                        x = _from.x() - ((i / 2) + (i % 2))
                    else:
                        x = _from.x() - (i / 2)
                    if self.tiles[x][_from.y() - i] != "":
                        return NOT_VALID
                    if x == self.NR / 2 and (_from + i) == self.NC/2:
                        return STOP_AT_CENTER
        return VALID

    def valid_move_s(self, _from, _to):
        return Board.searcher.valid_move(_from, _to, self.tiles, self.names)

    def hex_lines(self, name, coord):
        if self.tiles[coord.x()][coord.y()] != "":
            name += "," + self.tiles[coord.x()][coord.y()]

        # axcoord = Board.searcher.axial_coord(coord)
        hexlines = ["{:^12}".format('______'),
                        "  /{:^6}\\  ".format(''),
                        " /{:^8}\\ ".format(name[2:4]),
                        "/{:^10}\\".format(name[5:]),
                        "\\{:^10}/".format("{:>3}{:^4}{:<3}".format((coord.x() - self.NC / 2),
                                                                       (coord.y() - self.NC / 2),
                                                                       (-coord.x() - coord.y() + self.NC))),
                        " \\{:^8}/ ".format("{:>2} {:<2}".format(name[0], name[1])),
                        "  \\{:_^6}/  ".format(''),
                        " " * 12]
        #if name.__len__() > 4:
        return hexlines

    def print_hex(self):
        total_line = [""]*42 #35

        for line in range(total_line.__len__()):
            total_line[line] = " " * (12 * self.NC)

        for j in range(self.NC):
            d_center = abs(j - (self.NC / 2))
            if j != self.NC/2:
                vertical_offset = 4 * (j - self.NC/2)
            else:
                vertical_offset = 0

            for i in range(self.NR):
                if self.names[i][j] == "*":
                    continue

                start_index = vertical_offset + (i * 8)
                left = 12 * j
                right = left + 12
                hexlines = self.hex_lines(self.names[i][j], QPoint(i, j))

                for index, h in enumerate(hexlines):
                    total_line[start_index + index] = total_line[start_index + index][:left] + h\
                                                  + total_line[start_index + index][right:]

        for i, line in enumerate(total_line):
            total_line[i] = "|  " + line + "  |"
        total_line.insert(0, " " + "_" * ((12 * self.NC) + 4) + " ")
        total_line[total_line.__len__() - 1] = "|" + ("_" * ((12 * self.NC) + 4)) + "|"
        for line in total_line:
            print line


    # def color_print(color, style):

        #COLORS = {'black': 30, 'red': 31, 'green': 32, 'yellow': 33,'blue': 34, 'magenta': 35, 'cyan': 36, 'white': 37}
        #COLUMN_SPACE = ' | '
        #ESC = '\033[%sm'
        #CELL_FORMAT = ESC + '%-3s' + (ESC % 0)  # 0
        #print CELL_FORMAT % (COLORS['yellow'], '{:^12}'.format('________'))

    def output_board(self):

        outputter = list()
        center_modulo = self.NC % 2
        for i in range(self.names.__len__()):
            split1 = list(self.names[i])
            split2 = list(self.names[i])
            for j in range(split1.__len__()):
                if (j % 2) == center_modulo:
                    split2.__setitem__(j, "*")
                else:
                    split1.__setitem__(j, "*")
            outputter.append(split1)
            outputter.append(split2)

        outputter = outputter[:-1]

        for i in range(self.names.__len__()):
            for k in [2 * i, (2 * i) + 1]:
                if k == outputter.__len__():
                    continue
                printer1 = str()
                printer2 = str()
                printer3 = str()
                for j in range(self.names[0].__len__()):
                    if outputter[k][j] != "*":
                        printer1 += "{:^7}".format(outputter[k][j])
                        printer2 += "{:^7}".format("{},{},{}".format(i - self.NC/2, j - self.NC/2, 2 * (self.NC / 2) - i - j))
                        # printer3 += "{:^7}".format("{},{},{}".format(i - self.NC/2, j - self.NC/2, self.NC - i - j - 1))
                    else:
                        printer1 += "{:^7}".format('')
                        printer2 += "{:^7}".format('')
                        # printer3 += "{:^7}".format('')
                print printer1, "\n", printer2 # , "\n", printer3
        print "---------------------------------------------------------------------"
'''if __name__ == "__main__":
    b = Board(5, 5)
    b.init_names()
    b.init_pieces()
    b.print_hex()

    # print b.valid_move(QPoint(0,2), QPoint(2,5))
    # print b.valid_move_s(QPoint(3, 4), QPoint(1, 1))'''