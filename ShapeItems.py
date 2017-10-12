from PyQt4.QtCore import *
from PyQt4.QtGui import *


class TileItem(object):

    def __init__(self):
        object.__init__(self)
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

    def __init__(self):
        self.player = str()
        self.sign = str()
        self.number = None
        self.tile = None
        self.name = ""

    def set_player(self, player):
        self.player = player
    def set_sign(self, sign):
        self.sign = sign
    def set_number(self, number):
        self.number = number
    def set_tile(self, tile):
        self.tile = tile
    def set_name(self):
        self.name = self.player + self.sign + self.number

    def player(self):
        return self.player
    def sign(self):
        return self.sign
    def number(self):
        return self.number
    def tile(self):
        return self.tile
    def name(self):
        return self.name


class BoardTiles:

    def __init__(self, tiles=None):
        if tiles is None:
            self.tiles = list()
        else:
            self.tiles = list(tiles)

    def set_tiles(self, tiles):
        self.tiles = list(tiles)
        self.len = tiles.__len__()
    def __setitem__(self, key, value):
        self.tiles[key] = value

    def tiles(self):
        return self.tiles
    def __len__(self):
        return self.tiles.__len__()
    def __getitem__(self, item):
        return self.tiles[item]
