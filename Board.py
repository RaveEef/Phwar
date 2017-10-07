from ShapeItems import *
from Rules import *
from math import sqrt, cos, sin, pi

class Board(QFrame):

    NR = int()
    NR_COORD = int()
    NC = int()
    S = int()
    TILES = list()
    PIECES = ['BN', 'BP1', 'BP2', 'BE1', 'BE2', 'BE3', 'BP3', 'BP4', 'BE4',
              'WN', 'WP1', 'WP2', 'WE1', 'WE2', 'WE3', 'WP3', 'WP4', 'WE4']

    tile_clicked = pyqtSignal(TileItem)

    def __init__(self, nr, nc, s, parent):
        super(Board, self).__init__(parent)
        self.resize(parent.size())
        self.setFocusPolicy(Qt.StrongFocus)

        Board.NR = nr
        Board.NR_COORD = (2 * Board.NR) - 1
        Board.NC = nc
        Board.S = s

        self.selected = None
        self.tile_h = float()
        self.tile_w = float()
        self.tiles = list()

        self.init_tiles()
        self.init_pieces()

        self.setMouseTracking(True)

    @property
    def rHex(self):
        self.tile_h = (self.contentsRect().height() - ((Board.NR + 1) * Board.S)) / Board.NR
        self.tile_w = (2 * self.tile_h) / sqrt(3)
        return self.tile_w / 2

    def init_tiles(self):
        b = [ ]
        for i in range(Board.NR_COORD):
            b.append([None] * Board.NC)
            self.tiles.append([None] * Board.NC)

        for j in range(Board.NC):
            #for r in range(abs(c - Board.cols/2), 2*Board.cols - 1 - abs(c - Board.cols/2), 2):
            first_row = abs(j - (Board.NC / 2))
            last_row = (2 * Board.NC) - first_row - 1
            for i in range(first_row, last_row, 2):
                #chr(65) = A
                name = str(chr(65+j)) + str((i/2) + 1)
                d = (Board.NC/2) - j

                # For all columns on the left side, d is positive, so x-value decreases and vice versa
                real_x = (self.contentsRect().width() / 2) - (d * (self.S + self.rHex)) - ((d * self.rHex)/2)
                # Initialize the vertical position to the minimum distance to the upper bound of the frame (spacing + half hexagon height)
                # With every second column, relative to the mid, the first tile is completely positioned below the first tile 2 columns before
                # The row's vertical position below the one above it (and includes spacing)
                # If we are at an odd distance from the column in the middle, the initial offset is increased by half the spacing plus half hexagon height
                real_y = Board.S + ((sqrt(3) * self.rHex) / 2)
                real_y += (abs(d)/ 2)*(Board.S + (sqrt(3) * self.rHex))
                real_y += (((i - first_row) / 2) * (Board.S + (sqrt(3) * self.rHex)))
                if d % 2 != 0:
                    real_y += (Board.S + (sqrt(3) * self.rHex)) / 2

                b[i][j] = {'coord': {'i': i, 'j': j}, 'name': name, 'x': real_x, 'y': real_y}
                self.add_tile(name, QPoint(i, j), self.tile_path(real_x, real_y), QPointF(real_x, real_y))

    def init_pieces(self):
        mid_col = Board.NC / 2
        initial_pos = [(0, mid_col),
                       (1, mid_col-1), (1,mid_col+1),
                       (2, mid_col-2), (2, mid_col), (2, mid_col+2),
                       (3, mid_col-1), (3, mid_col+1),
                       (4, mid_col)]
        for index, c in enumerate(initial_pos):
            black_tile = [t for t in Board.TILES if t.coord.x() == c[0] and t.coord.y() == c[1]][0]
            self.add_piece(Board.PIECES[index], black_tile)
            ''' Uncomment to position Black positron on F4
            if black_tile.name == "C2":
                F4 = [t for t in Board.TILES if t.name == "F4"][0]
                self.add_piece(Board.PIECES[index], F4)
            else:
                self.add_piece(Board.PIECES[index], black_tile)'''

            white_tile = [t for t in Board.TILES if t.coord.x() == (Board.NR_COORD - 1 - c[0]) and t.coord.y() == c[1]][0]
            white_index = index + (Board.PIECES.__len__() / 2)
            self.add_piece(Board.PIECES[white_index], white_tile)

    def tile_path(self, cx, cy):
        path = QPainterPath()
        path.moveTo((cx - self.rHex), cy)
        for i in range(1,6):
            x = cx + (self.rHex * cos(((3 - i) * pi) / 3))
            y = cy + (self.rHex * sin(((3 - i) * pi) / 3))
            path.lineTo(x, y)
        path.closeSubpath()
        #path.setFillRule(Qt.WindingFill)
        return path

    def piece_circle_path(self, tile):
        path = QPainterPath()
        path.moveTo(tile.pos)
        path.addEllipse(tile.pos, 0.75*self.rHex, 0.75*self.rHex)
        path.closeSubpath()
        return path

    def piece_sign_path(self, tile):
        if tile.piece.sign == "N":
            return QPainterPath()
        else:
            path = QPainterPath()
            path.moveTo(tile.pos.x() - self.rHex/2, tile.pos.y())
            path.lineTo(tile.pos.x() + self.rHex/2, tile.pos.y())

            if tile.piece.sign == "E":
                return path
            else:
                vertical_line = QPainterPath()
                vertical_line.moveTo(tile.pos.x(), tile.pos.y() - self.rHex/2)
                vertical_line.lineTo(tile.pos.x(), tile.pos.y() + self.rHex/2)
                path += vertical_line
                return path

    def add_tile(self, name, coord, path, pos):
        t = TileItem()
        t.set_name(name)
        t.set_coord(coord)
        t.set_pos(pos)
        t.set_path(path)
        t.set_color(Qt.white)
        t.set_piece(None)

        Board.TILES.append(t)
        #self.update()

    def add_piece(self, piece, tile):
        p = PieceItem()
        p.set_player(piece[0])
        p.set_sign(piece[1])
        if piece.__len__() > 2:
            p.set_number(piece[2])
        else:
            p.set_number("")
        p.set_tile(tile)

        tile.set_piece(p)

    def tile_at(self, mouse_pos):
        for i, tile in enumerate(Board.TILES):
            if tile.path.contains(mouse_pos):
                return i
        return -1

    def paint_tiles(self, painter):
        painter.setPen(QPen(Qt.black, 1))
        painter.setBrush(QBrush(Qt.white))

        for tile in Board.TILES:
            painter.setBrush(QBrush(tile.color))
            painter.drawPath(tile.path)

    def paint_pieces(self, painter):

        for tile in [t for t in Board.TILES if t.piece is not None]:
            if tile.piece.player == 'B':
                painter.setBrush(QBrush(Qt.black))
                painter.setPen(QPen(Qt.black, 0.1*self.rHex))
                painter.drawPath(self.piece_circle_path(tile))

                painter.setBrush(QBrush(Qt.white))
                pen = QPen(Qt.white, 0.12*sqrt(3)*self.rHex)
                pen.setCapStyle(Qt.RoundCap)
                painter.setPen(pen)
                painter.drawPath(self.piece_sign_path(tile))

            elif tile.piece.player == 'W':
                painter.setBrush(QBrush(Qt.white))
                painter.setPen(QPen(Qt.black, 0.1*self.rHex))
                painter.drawPath(self.piece_circle_path(tile))

                painter.setBrush(QBrush(Qt.black))
                pen = QPen(Qt.black, 0.12*sqrt(3)*self.rHex)
                pen.setCapStyle(Qt.RoundCap)
                painter.setPen(pen)
                painter.drawPath(self.piece_sign_path(tile))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.fillRect(self.contentsRect(),Qt.lightGray)

        self.paint_tiles(painter)
        self.paint_pieces(painter)
        self.paint_names(painter)

    def paint_names(self, painter):
        painter.setPen(QPen(Qt.red))
        text_font = QFont()
        text_font.setPointSize(10)
        text_font.setBold(True)
        painter.setFont(text_font)

        for tile in Board.TILES:
            c = tile.pos
            r = QRectF(c.x() - self.rHex, c.y() - self.rHex, self.rHex*2, sqrt(3) * self.rHex)
            coord_text = " {}\n({},{})".format(tile.name, tile.coord.x(), tile.coord.y())
            painter.drawText(r, Qt.AlignCenter, coord_text)

    def mousePressEvent(self, event):
        for tile in Board.TILES:
            tile.set_color(Qt.white)
        self.update()

        mouse_pos = event.pos()
        index = self.tile_at(mouse_pos)
        if index != -1:
            Board.TILES[index].set_color(Qt.magenta)
            self.tile_clicked.emit(Board.TILES[index])
            #self.line_of_sight(index)

        self.update()

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

    def line_of_sight(self, index):
        selected = Board.TILES[index]
        sight = list()
        v = list()
        d1 = list()
        d2 = list()

        for i, t in enumerate(Board.TILES):
            if t.coord.x() != selected.coord.x() and t.coord.y() == selected.coord.y():
                v.append(i)

            if t != selected:
                x_diff = selected.coord.x() - t.coord.x()
                y_diff = selected.coord.y() - t.coord.y()
                if x_diff == y_diff:
                    d1.append(i)
                elif x_diff == -y_diff:
                    d2.append(i)

        sight.append((Qt.blue, v))
        sight.append((Qt.green, d1))
        sight.append((Qt.yellow, d2))

        for color, direction in sight:
            for d in direction:
                Board.TILES[d].set_color(color)
        self.update()
