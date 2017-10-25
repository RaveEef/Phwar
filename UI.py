from Utils import *
from math import cos, sin, pi, sqrt
from PyQt4.QtGui import *


class UI(QFrame):

    clicking_move = pyqtSignal(tuple)
    tile_clicked = pyqtSignal(TileItem)

    def __init__(self, rows, columns, spacing, parent=None):
        super(UI, self).__init__(parent)
        self.resize(600, parent.contentsRect().height())
        self.setFocusPolicy(Qt.StrongFocus)

        self.NR = rows
        self.NR_COORD = (2 * self.NR) - 1
        self.NC = columns
        self.S = spacing

        self.ui_tiles = list()
        self.ctiles = list()
        self.ntiles = dict()
        self.selected = None
        self.player = "B"

        self.init_tiles()

        self.setMouseTracking(True)

    @classmethod
    def currentBoard(cls):
        return cls

    @property
    def r_hex(self):
        tile_h = (self.contentsRect().height() - ((self.NR + 1) * self.S)) / self.NR
        tile_w = (2 * tile_h) / sqrt(3)
        return tile_w / 2

    def init_tiles(self):

        for j in range(self.NC):
            first_row = abs(j - self.NC / 2)
            last_row = (2 * self.NC) - first_row - 1
            for i in range(first_row, last_row, 2):
                name = str(chr(65 + j)) + str((i / 2) + 1)  # chr(65) = A
                d = (self.NC / 2) - j
                # For all columns on the left side, d is positive, so x-value decreases and vice versa
                # Initialize the vertical position to the minimum distance to the upper bound of the frame (spacing + half hexagon height)
                # With every second column, relative to the mid, the first tile is completely positioned below the first tile 2 columns before
                # The row's vertical position below the one above it (and includes spacing)
                # If we are at an odd distance from the column in the middle, the initial offset is increased by half the spacing plus half hexagon height
                real_x = (self.contentsRect().width() / 2) - (d * (self.S + self.r_hex)) - ((d * self.r_hex) / 2)
                real_y = self.S + ((sqrt(3) * self.r_hex) / 2)
                real_y += (abs(d) / 2) * (self.S + (sqrt(3) * self.r_hex))
                real_y += (((i - first_row) / 2) * (self.S + (sqrt(3) * self.r_hex)))
                if d % 2 != 0:
                    real_y += (self.S + (sqrt(3) * self.r_hex)) / 2

                t = TileItem()
                t.set_name(name)
                t.set_coord(QPoint(i, j))
                t.set_pos(QPointF(real_x, real_y))
                t.set_path(self.tile_path(real_x, real_y))
                t.set_color(Qt.white)

                self.ui_tiles.append(t)
                self.ntiles[name] = t

        for i in range(self.NR_COORD):
            self.ctiles.append([None] * self.NC)
            for j in range(self.NC):
                tile = filter(lambda x: x.coord.x() == i and x.coord.y() == j, self.ui_tiles)
                if tile.__len__() > 0:
                    self.ctiles[i][j] = tile[0]

    def set_board_pieces(self, simple_tiles):
        for i in range(simple_tiles.__len___()):
            for j in range(simple_tiles[i].__len__()):
                tile = filter(lambda x: x.coord == QPoint(i, j), self.ui_tiles)[0]
                tile.set_piece(PieceItem(name=simple_tiles[i][j]))

    def tile_at_pos(self, pos):
        for i, tile in enumerate(self.ui_tiles):
            if tile.path.contains(pos):
                return self.ui_tiles[i]
        return None

    def tile_with_name(self, name):
        return filter(lambda x: x.name == name, self.ui_tiles)[0]

    def tile_path(self, cx, cy):
        path = QPainterPath()
        path.moveTo((cx - self.r_hex), cy)
        for i in range(1, 6):
            x = cx + (self.r_hex * cos(((3 - i) * pi) / 3))
            y = cy + (self.r_hex * sin(((3 - i) * pi) / 3))
            path.lineTo(x, y)
        path.closeSubpath()
        return path

    def piece_circle_path(self, tile):
        path = QPainterPath()
        path.moveTo(tile.pos)
        path.addEllipse(tile.pos, 0.75 * self.r_hex, 0.75 * self.r_hex)
        path.closeSubpath()
        return path

    def piece_sign_path(self, tile):
        if tile.piece.sign == "N":
            return QPainterPath()
        else:
            path = QPainterPath()
            path.moveTo(tile.pos.x() - self.r_hex / 2, tile.pos.y())
            path.lineTo(tile.pos.x() + self.r_hex / 2, tile.pos.y())

            if tile.piece.sign == "E":
                return path
            else:
                vertical_line = QPainterPath()
                vertical_line.moveTo(tile.pos.x(), tile.pos.y() - self.r_hex / 2)
                vertical_line.lineTo(tile.pos.x(), tile.pos.y() + self.r_hex / 2)
                path += vertical_line
                return path

    '''def set_tile(self, name, coord, path, pos):
        t = TileItem()
        t.set_name(name)
        t.set_coord(coord)
        t.set_pos(pos)
        t.set_path(path)
        t.set_color(Qt.white)

        self.tiles.append(t)
        # s_Board.TILES.append(t)
        # self.update()'''

    def paint_tiles(self, painter):
        painter.setPen(QPen(Qt.black, 1))
        painter.setBrush(QBrush(Qt.white))

        for tile in self.ui_tiles:
            painter.setBrush(QBrush(tile.color))
            painter.drawPath(tile.path)

    def paint_pieces(self, painter):
        for tile in [t for t in self.ui_tiles if isinstance(t.piece, PieceItem)]:
            if tile.piece.player == 'B':
                painter.setBrush(QBrush(Qt.black))
                painter.setPen(QPen(Qt.black, 0.1 * self.r_hex))
                painter.drawPath(self.piece_circle_path(tile))

                painter.setBrush(QBrush(Qt.white))
                pen = QPen(Qt.white, 0.12 * sqrt(3) * self.r_hex)
                pen.setCapStyle(Qt.RoundCap)
                painter.setPen(pen)
                painter.drawPath(self.piece_sign_path(tile))

            elif tile.piece.player == 'W':
                painter.setBrush(QBrush(Qt.white))
                painter.setPen(QPen(Qt.black, 0.1 * self.r_hex))
                painter.drawPath(self.piece_circle_path(tile))

                painter.setBrush(QBrush(Qt.black))
                pen = QPen(Qt.black, 0.12 * sqrt(3) * self.r_hex)
                pen.setCapStyle(Qt.RoundCap)
                painter.setPen(pen)
                painter.drawPath(self.piece_sign_path(tile))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.fillRect(self.contentsRect(), Qt.lightGray)

        self.paint_tiles(painter)
        self.paint_pieces(painter)
        self.paint_names(painter)

    def paint_names(self, painter):
        painter.setPen(QPen(Qt.red))
        text_font = QFont()
        text_font.setPointSize(12)
        text_font.setBold(True)
        painter.setFont(text_font)

        for tile in self.ui_tiles:

            c = tile.pos
            r = QRectF(c.x() - self.r_hex,
                       c.y() - self.r_hex + text_font.pointSize()/2,
                       self.r_hex * 2,
                       sqrt(3) * self.r_hex)
            tile_text = " {}\n({},{})".format(tile.name, tile.coord.x(), tile.coord.y())
            if tile.piece is not None:
                tile_text += "\n {}".format(tile.piece.name)

            painter.drawText(r, Qt.AlignCenter, tile_text)

    def reset_tile_colors(self):
        for t in self.ui_tiles:
            t.set_color(Qt.white)

    def mousePressEvent(self, event):

        mouse_pos = event.pos()
        move_made = None
        tile_clicked = self.tile_at_pos(mouse_pos)

        if tile_clicked is not None:
            if tile_clicked.piece is not None and self.selected is None:
                #TODO: REMOVE != !!!
                if tile_clicked.piece.player == self.player or tile_clicked.piece.player != self.player:
                    tile_clicked.set_color(Qt.magenta)
                    self.tile_clicked.emit(tile_clicked)
                    self.selected = tile_clicked

            elif isinstance(self.selected, TileItem):
                if self.selected.piece is not None:
                    if tile_clicked.piece is None:
                        self.clicking_move.emit((self.selected, tile_clicked))
                        if self.player == "B":
                            self.player = "W"
                        else:
                            self.player = "B"
                    self.reset_tile_colors()

                self.selected = None
            self.update()


    '''@pyqtSlot(tuple, list)
    def execute_move(self, move, captures):
        if captures is None:'''


    '''
    colors = [QColor(Qt.blue), QColor(Qt.green), QColor(Qt.yellow)]
    for index, direction in enumerate(sight):
        for d in direction:
            Board.TILES[d].set_color(colors[index])
    self.update()
    '''


'''def make_connection(self, board):
    board.tile_clicked.connect(self.get_tile_clicked)

@pyqtSlot(TileItem)
def get_tile_clicked(self, tile):
    if tile.piece is not None:
        if self.from_tile is None:
            print "from tile: ", tile.name
            self.from_tile = tile
            for x in self.get_line_of_sight(tile):
                for i in x[1]:
                    print Board.TILES[i].name
            #for in_sight in self.get_line_of_sight(self.from_tile):
                #print in_sight[1].name
        elif self.to_tile is None:
            print "to tile: ", tile.name
            self.to_tile = tile'''
