from shapes import *
from board import *

class Rules():

    BOARD = None
    TILES = None

    def __init__(self, board):
        Rules.BOARD = board
        Rules.TILES = board.TILES
        self.from_tile = None
        self.to_tile = None
        self.sight = None

    def make_connection_to_board(self, board):
        board.tile_clicked.connect(self.moving_piece)

    @pyqtSlot(TileItem)
    def moving_piece(self, tile):
        if tile.piece is None:
            if self.from_tile is None:
                print "Move not valid (from_tile contains no piece)"
                tile.set_color(QColor(Qt.white))
            elif self.to_tile is None: #So, the from tile has a piece and the to tile doesnt
                self.to_tile = tile
                if self.valid_move():
                    moving_piece = self.from_tile.piece     #Pick up the piece and store it in 'moving_piece'
                    self.from_tile.set_piece(None)          #Remove it from the current tile
                    self.stop_at_center(self.to_tile, self.tiles_in_sight(self.from_tile))
                    moving_piece.set_tile(self.to_tile)     #Put down the piece on the new tile
                    self.to_tile.set_piece(moving_piece)    #Add the piece to the new tile

                else:
                    print "not in the tile's sight"
                tile.set_color(QColor(Qt.white))
                self.from_tile = None
                self.to_tile = None

        else:
            if self.from_tile is None and self.to_tile is None:
                self.from_tile = tile
            elif self.to_tile is None:
                print "Move not valid (to_tile contains piece)"
                tile.set_color(QColor(Qt.white))
                self.from_tile = None

    def valid_move(self):
        if self.from_tile is not None and self.to_tile is not None:
            self.tiles_in_sight(self.from_tile)
            for s in self.sight:
                if s.__contains__(self.to_tile):
                    return True
            return False

    def tiles_in_sight(self, tile_clicked):

        v = list()  #Column of clicked tile
        end_v = False   #If True, stop looking for possible tiles in downward vertical direction
        d1 = list() #Diagonal from upper left corner to lower right corner
        end_d1 = False  #If True, stop looking in the direction of the lower right corner
        d2 = list() #Diagonal from lower left corner to upper right corner
        end_d2 = False  #If True, stop looking in the direction of the upper right corner

        for i, t in enumerate(Rules.TILES):
            if t.coord.x() != tile_clicked.coord.x() and t.coord.y() == tile_clicked.coord.y():
                if t.piece is not None and not end_v:
                    if t.coord.x() < tile_clicked.coord.x():
                        v = list()  #If piece is found above the clicked tile, clear the list so far
                    elif t.coord.x() > tile_clicked.coord.x():
                        end_v = True
                if not end_v and t.piece is None:
                    v.append(t)

            if t != tile_clicked:
                x_diff = tile_clicked.coord.x() - t.coord.x()
                y_diff = tile_clicked.coord.y() - t.coord.y()
                if x_diff == y_diff:
                    if t.piece is not None:
                        if t.coord.y() < tile_clicked.coord.y():
                            d1 = list() #If piece is found on the direction of the upper left corner, clear the list so far
                        elif t.coord.y() > tile_clicked.coord.y():
                            end_d1 = True
                    if not end_d1 and t.piece is None:
                        d1.append(t)
                elif x_diff == -y_diff:
                    if t.piece is not None:
                        if t.coord.y() < tile_clicked.coord.y():
                            d2 = list() #If piece is found on the direction of the lower left corner, clear the list so far
                        elif t.coord.y() > tile_clicked.coord.y():
                            end_d2 = True
                    if not end_d2 and t.piece is None:
                        d2.append(t)

        self.sight = [v, d1, d2]

    def stop_at_center(self, _to, sight):
        direction = [s for s in self.sight if s.__contains__(_to)][0]
        center_tile = [t for t in Rules.TILES if t.coord == QPoint(Rules.BOARD.NR - 1, Rules.BOARD.NC / 2)][0]
        if direction.__contains__(center_tile):
            self.to_tile = center_tile


