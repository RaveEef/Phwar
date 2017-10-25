from PyQt4.QtCore import *
from PyQt4.QtGui import *


class TileItem(object):

    def __init__(self, tileitem=None):
        object.__init__(self)
        if tileitem is not None:
            self.name = tileitem.name
            self.coord = tileitem.coord
            self.path = tileitem.path
            self.pos = tileitem.pos
            self.color = tileitem.color
            self.piece = tileitem.piece
        else:
            self.name = str()
            self.coord = QPoint()
            self.path = QPainterPath()
            self.pos = QPointF()
            self.color = QColor()
            self.piece = None

    def set_name(self, name):
        self.name = name

    def set_coord(self, coord):
        self.coord = coord

    def set_pos(self, pos):
        self.pos = pos

    def set_path(self, path):
        self.path = path

    def set_color(self, color):
        self.color = color

    def set_piece(self, piece):
        self.piece = piece

    def name(self):
        return self.name

    def coord(self):
        return self.coord

    def pos(self):
        return self.pos

    def path(self):
        return self.path

    def color(self):
        return self.color

    def piece(self):
        return self.piece


class PieceItem:

    def __init__(self, player=None, sign=None, number=None, name=None, pieceitem=None):
        if pieceitem is not None:
            self.player = pieceitem.player
            self.sign = pieceitem.sight
            self.number = pieceitem.number
            self.tile = pieceitem.tile
            self.name = pieceitem.name

        elif name is not None:
            self.player = name[0]
            self.sign = name[1]
            self.name = name
            if name.__len__() > 2:
                print name[1]
                self.number = int(name[2])
            else:
                self.number = int()

        else:
            if player is not None:
                self.player = player
            else:
                self.player = str()

            if sign is not None:
                self.sign = sign
            else:
                self.sign = str()

            if number is not None:
                self.number = number
            else:
                self.number = int()

            if player is not None and sign is not None:
                if number is not None:
                    self.name = self.player + self.sign + str(self.number)
                else:
                    self.name = self.player + self.sign

    '''def set_player(self, player):
        self.player = player
        
    def set_sign(self, sign):
        self.sign = sign
        
    def set_number(self, number):
        self.number = number
        
    def set_name(self):'''

    def player(self):
        return str(self.player)

    def sign(self):
        return str(self.sign)

    def number(self):
        return int(self.number)

    def name(self):
        return str(self.name)

class Axials:

    def __init__(self, x=None, y=None, name=None):
        if x is not None and y is not None:
            self.q = x
            self.r = y
            self.s = 0
            '''(coord.x() - self.NC / 2),
                                                                       (coord.y() - self.NC / 2),
                                                                       (-coord.x() - coord.y() + self.NC))'''

class Searching:

    player = "B"
    opponent = "W"

    def __init__(self):
        self.tree = list()
        self.current_player = Searching.player

    def add_tree_layer(self, tiles, parent=None):
        if parent is None:
            if self.tree.__len__() == 0:
                self.tree.append(list(tiles))
            else:
                self.tree[0] = list(tiles)
        else:
            if self.tree.__len__() < parent + 1:
                self.tree.append(list())
                self.tree[parent+1].append(list(tiles))
            else:
                self.tree[parent+1].append(list(tiles))


    def tile_tree(self):
        return self.tree

    @staticmethod
    def update_tiles(move, tiles):
        if tiles is None:
            return

        _tiles = list(tiles)

        from_tile = TileItem(move[0])
        to_tile = TileItem(move[1])

        to_tile.set_piece(from_tile.piece)
        from_tile.set_piece(None)

        index = filter(lambda i: _tiles[i].piece == move[0].piece, range(_tiles.__len__()))[0]
        _tiles[index] = from_tile
        #_tiles[_tiles.index(move[0])] = from_tile


        if _tiles.__contains__(move[1]):
            _tiles[_tiles.index(move[1])] = to_tile
        else:
            index = filter(lambda i: _tiles[i].piece == move[1].piece, range(_tiles.__len__()))[0]
            _tiles[index] = to_tile

        return _tiles

    @staticmethod
    def find_lines_of_sight(tiles):

        if tiles is None:
            return

        pieces = filter(lambda x: x.piece is not None, tiles)
        lines_of_sight = list()

        for i_p, p in enumerate(pieces):
            v_sight = filter(lambda t: t.coord.y() == p.coord.y(), tiles)
            lr_sight = filter(lambda t: t.coord.x() - t.coord.y() == p.coord.x() - p.coord.y(), tiles)
            rl_sight = filter(lambda t: t.coord.x() + t.coord.y() == p.coord.y() + p.coord.x(), tiles)
            rl_sight.reverse()

            lines_of_sight.append([v_sight, lr_sight, rl_sight])

        return lines_of_sight

    @staticmethod
    def find_one_line_of_sight(tile, tiles):

        if tiles is None:
            return

        v_sight = filter(lambda t: t.coord.y() == tile.coord.y(), tiles)
        lr_sight = filter(lambda t: t.coord.x() - t.coord.y() == tile.coord.x() - tile.coord.y(), tiles)
        rl_sight = filter(lambda t: t.coord.x() + t.coord.y() == tile.coord.x() + tile.coord.y(), tiles)
        rl_sight.reverse()

        return [v_sight, lr_sight, rl_sight]

    @staticmethod
    def find_pieces_in_sight(piece, line_of_sight):

        pieces_in_sight = list()

        for sight in line_of_sight:
            if not sight.__contains__(piece):
                piece = filter(lambda x: x.name == piece.name, sight)[0]

            i = sight.index(piece) - 1

            while i > -1:
                if isinstance(sight[i].piece, PieceItem):
                    pieces_in_sight.append(sight[i])
                    break
                i -= 1

            i = sight.index(piece) + 1
            while i < sight.__len__():
                if isinstance(sight[i].piece, PieceItem):
                    pieces_in_sight.append(sight[i])
                    break
                i += 1

        return pieces_in_sight

    @staticmethod
    def find_pieces_of_player_in_sight(piece, player, line_of_sight):

        pieces_of_player_in_sight = list()

        for sight in line_of_sight:
            if not sight.__contains__(piece):
                piece = filter(lambda x: x.name == piece.name, sight)[0]

            i = sight.index(piece) - 1
            while i > -1:
                if isinstance(sight[i].piece, PieceItem):
                    if sight[i].piece.player == player:
                        pieces_of_player_in_sight.append(sight[i])
                    break
                i -= 1

            i = sight.index(piece) + 1
            while i < sight.__len__():
                if isinstance(sight[i].piece, PieceItem):
                    if sight[i].piece.player == player:
                        pieces_of_player_in_sight.append(sight[i])
                    break
                i += 1

        return pieces_of_player_in_sight

    @staticmethod
    def axial_coord(coord, center):


        center = QPoint(3,3)
        x_axial = coord.x() - center.x()
        y_axial = coord.y() - center.y()
        return x_axial, y_axial


    @staticmethod
    def valid_move(_from, _to, tiles, names):
        valid = "VALID" #1
        stop_at_center = "STOP AT CENTER" #0
        nr = tiles.__len__()
        nc = tiles[0].__len__()

        diag_tiles = list()
        # even rows
        for i in range(0, (2 * nr), 2):
            print i
            diag_tiles.append([""] * nc)
            for j in range(nc):
                print j
                diag_tiles[i][j] = tiles[(i/2)][j]
                print "({}, {}) -> ({}, {})".format((i/2), j, i, j)


        from_x, from_y = _from.x(), _from.y()
        alpha_from = names[from_x][from_y][0]
        to_x, to_y = _to.x(), _to.y()
        alpha_to = names[to_x][to_y][0]

        if tiles[from_x][from_y] == "":
            print "No piece to move at", names[from_x][from_y]
            return not valid
        if tiles[to_x][to_y] != "":
            print "There's a piece at", names[to_x][to_y]
            return not valid

        if from_y == to_y:
            for i in range(min(from_x, to_x) + 1, max(from_x, to_x)):
                if tiles[i][from_y] != "":
                    return not valid, not stop_at_center
                if i == nr/2 and from_y == nc/2:
                    return valid, stop_at_center

        if (from_x - (nr/2)) % 2 == 0:
            from_x = 2 * from_x
        else:
            from_x = (2 * from_x) + 1






        #print
        '''if _from.y() == _to.y():
            if _from.x()() == _to.x()():
                return not_valid
            if _from.x()() > _to.x()():
                for i in range(_from.x()() - _to.x()()):
                    if self.tiles[_from.x()() - i - 1][_from.y()] != "":
                        return not_valid
                    if (_from.x()() - i - 1) == self.NR / 2 and _from.y() == self.NC / 2:
                        return stop_at_center
            if _from.x()() < _to.x():
                for i in range(_from.x() - _to.x()):
                    if self.tiles[_from.x() + i + 1][_from.y()] != "":
                        return not_valid
                    if (_from.x() + i - 1) == self.NR / 2 and _from.y() == self.NC / 2:
                        return stop_at_center
        elif ((2 * _from.x()) - _from.y()) == ((2 * _to.x()) - _to.y()):
            if _from.y() > _to.y():
                for i in range(1, _from.y() - _to.y()):
                    if _from.y() % 2 == 0:
                        x = _from.x() - (i / 2)
                    else:
                        x = _from.x() - ((i / 2) + (i % 2))
                    if self.tiles[x][_from.y() - i] != "":
                        return not_valid
                    if x == self.NR / 2 and (_from.y() - i) == self.NC / 2:
                        return stop_at_center
            if _from.y() < _to.y():
                for i in range(1, _to.y() - _from.y()):
                    if _from.y() % 2 == 0:
                        x = _from.x() + ((i / 2) + (i % 2))
                    else:
                        x = _from.x() + (i / 2)
                    if self.tiles[x][_from.y() + i] != "":
                        return not_valid
                    if x == self.NR / 2 and (_from + i) == self.NC / 2:
                        return stop_at_center
        elif ((2 * _from.x()) + _from.y()) == ((2 * _to.x()) + _to.y()):
            if _from.y() > _to.y():
                for i in range(1, _from.y() - _to.y()):
                    if _from.y() % 2 == 0:
                        x = _from.x() + ((i / 2) + (i % 2))
                    else:
                        x = _from.x() + (i / 2)
                    if self.tiles[x][_from.y() - i] != "":
                        return not_valid
                    if x == self.NR / 2 and (_from.y() - i) == self.NC / 2:
                        return stop_at_center
            if _from.y() < _to.y():
                for i in range(1, _to.y() - _from.y()):
                    if _from.y() % 2 == 0:
                        x = _from.x() - ((i / 2) + (i % 2))
                    else:
                        x = _from.x() - (i / 2)
                    if self.tiles[x][_from.y() - i] != "":
                        return not_valid
                    if x == self.NR / 2 and (_from + i) == self.NC / 2:
                        return stop_at_center'''
        return diag_tiles

    @classmethod
    def get_player(cls):
        return cls.player

    @classmethod
    def get_opponent(cls):
        return cls.opponent


    @classmethod
    def set_player(cls, player):
        cls.player = player
        if player == "B":
            cls.opponent = "W"
        else:
            cls.opponent = "B"

    def diagonals(self, tile, tiles):
        nc = tiles[0].__len__()
        dir = 0
        while dir < 4:
            x, y = tile.x(), tile.y()
            while x >= 0 and y >= 0:
                if abs(y - (nc/2)) % 2 == 0:
                    neigbors = [(x-1, y-1), (x-1, y), (x-1, y+1),
                                (x, y-1), (x+1, y+1), (x, y+1)]
