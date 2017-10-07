from Board import *

class Rules():

    BOARD = None
    TILES = None

    def __init__(self, board):
        Rules.BOARD = board
        Rules.TILES = board.TILES
        self.from_tile = None
        self.to_tile = None

        self.total_sight = None
        self.valid_sight = None
        self.captures_in_sight = None

    def make_connection_to_board(self, board):
        board.tile_clicked.connect(self.generate_move)

    @pyqtSlot(TileItem)
    def generate_move(self, tile):
        if tile.piece is not None:
            if self.from_tile is None and self.to_tile is None:
                self.from_tile = tile

                self.possible_captures()
            elif self.to_tile is None:
                print "Move not valid (to_tile contains piece)"
                tile.set_color(QColor(Qt.white))
                self.from_tile = None
        else:
            if self.from_tile is None:
                print "Move not valid (from_tile contains no piece)"
            elif self.to_tile is None:
                self.to_tile = tile
                if self.validate():
                    self.move_piece()
                else:
                    print "not in the tile's sight"
                self.from_tile = None
                self.to_tile = None
            tile.set_color(QColor(Qt.white))

    # Function to get all tiles in line of sight
    def line_of_sight(self, tile):
        # [[vertical], [diagonal from upper-left to lower-right], [diagonal from upper-right to lower-left]]
        sight = [[], [], []]

        for t in Rules.TILES:
            if t.coord.y() == tile.coord.y():
                sight[0].append(t)

            x_diff = tile.coord.x() - t.coord.x()
            y_diff = tile.coord.y() - t.coord.y()
            if x_diff == y_diff:
                sight[1].append(t)

            if x_diff == -y_diff:
                sight[2].insert(0, t)

        self.total_sight = sight

    # Function to get all valid tiles to move to
    def valid_moves(self, tile):
        valid_tiles = [[], [], []]  # bool is zero if end of valid tiles in that direction is reached
        self.line_of_sight(tile)

        for i, direction in enumerate(self.total_sight):
            for t in [d for d in direction if i == 0]:  # Vertical direction
                if t.piece is not None:
                    if t.coord.x() < tile.coord.x():
                        valid_tiles[0] = []  # If piece is found above the clicked tile, clear the list so far
                    elif t.coord.x() > tile.coord.x():
                        break
                else:
                    valid_tiles[0].append(t)

            for t in [d for d in direction if i == 1]:  # Diagonal 1 (UL -> LR)
                if t.piece is not None:
                    if t.coord.y() < tile.coord.y():
                        valid_tiles[1] = []  # If piece is found above the clicked tile, clear the list so far
                    elif t.coord.y() > tile.coord.y():
                        break
                else:
                    valid_tiles[1].append(t)

            for t in [d for d in direction if i == 2]:  # Diagonal 1 (UR -> LL)
                if t.piece is not None:
                    if t.coord.y() > tile.coord.y():
                        valid_tiles[2] = []  # If piece is found above the clicked tile, clear the list so far
                    elif t.coord.y() < tile.coord.y():
                        break
                else:
                    valid_tiles[2].append(t)

        self.valid_sight = valid_tiles

    # Function to get the nearest pieces in each direction (if there isn't any, the value is set to None)
    # [ [(Tile, Piece, Index in Vertical Line), (Tile, Piece, Index in Vertical Line)],
    #   [(Tile, Piece, Index in Diagonal_1 Line), (Tile, Piece, Index in Diagonal_1 Line)],
    #   [(Tile, Piece, Index in Diagonal_2 Line), (Tile, Piece, Index in Diagonal_2 Line)] ]
    def pieces_in_sight(self):
        sight_pieces = [[None] * 2, [None] * 2, [None] * 2]

        self.line_of_sight(self.from_tile)

        for index, s_line in enumerate(self.total_sight):
            # 0, [Tile, Tile, Tile, ...]
            i = s_line.index(self.from_tile) - 1
            while i > -1:
                if s_line[i].piece is not None:
                    sight_pieces[index][0] = (s_line[i], s_line[i].piece, i)
                    break
                i -= 1

            i = s_line.index(self.from_tile) + 1
            while i < s_line.__len__():
                if s_line[i].piece is not None:
                    sight_pieces[index][1] = (s_line[i], s_line[i].piece, i)
                    break
                i += 1

        return sight_pieces

    # Function to print all pieces
    def print_pieces_sight(self):
        sight_p = self.pieces_in_sight()
        for pieces in [sight_p[direction] for direction in range(sight_p.__len__())]:
            for piece in pieces:
                if piece is None:
                    print "None"
                else:
                    print " Tile: {}, Piece: {}{}{}, Index: {}".format(piece[0].name,
                                                                       piece[1].player, piece[1].sign, piece[1].number,
                                                                       piece[2])

    # Function to find all possible captures
    # The piece should not be equal to the current player's piece
    # The tile after/before should be empty
    def possible_captures(self):
        opponent_pieces = []
        sight_pieces = self.pieces_in_sight()

        for line_index, line_pieces in enumerate(sight_pieces):
            for poss_capture in [not_none for i, not_none in enumerate(line_pieces) if line_pieces[i] is not None]:
                if poss_capture[1].player != self.from_tile.piece.player:
                    if line_pieces.index(poss_capture) == 0 and poss_capture[2] - 1 > -1:
                        if self.total_sight[line_index][poss_capture[2] - 1].piece is None:
                            opponent_pieces.append(poss_capture)
                    elif line_pieces.index(poss_capture) == 1 and poss_capture[2] + 1 < line_pieces.__len__():
                        if self.total_sight[line_index][poss_capture[2] + 1].piece is None:
                            opponent_pieces.append((poss_capture[0], poss_capture[1], poss_capture[2]))

        if opponent_pieces.__len__() > 0:
            print self.from_tile.name, " could capture:"
            for opp_p in opponent_pieces:
                print "Piece {}{}{} at Tile {} at Index {}".format(opp_p[1].player, opp_p[1].sign, opp_p[1].number, opp_p[0].name, opp_p[2])

    # Function to validate whether a move is valid
    def validate(self):
        if self.from_tile is not None and self.to_tile is not None:
            self.valid_moves(self.from_tile)
            for s in self.valid_sight:
                if s.__contains__(self.to_tile):
                    return True
            return False

    # Function to actually move the piece (in the Board.TILES)
    def move_piece(self):
        piece = self.from_tile.piece
        self.from_tile.set_piece(None)  # Remove it from the current tile
        self.stop_at_center()
        piece.set_tile(self.to_tile)    # Put down the piece on the new tile
        self.to_tile.set_piece(piece)  # Add the piece to the new tile

    # If center hex is passed in planned move, stop at the center hex
    def stop_at_center(self):
        direction = [s for s in self.valid_sight if s.__contains__(self.to_tile)][0]
        center_tile = [t for t in Rules.TILES if t.coord == QPoint(Rules.BOARD.NR - 1, Rules.BOARD.NC / 2)][0]

        if direction.__contains__(center_tile):
            if min(self.to_tile.coord.x(), self.from_tile.coord.x()) < center_tile.coord.x() < max(self.to_tile.coord.x(), self.from_tile.coord.x()):
            #   print "crossing center"
                self.to_tile = center_tile
            #else:
            #    print "moving in a direction containing center, but not crossing it"


