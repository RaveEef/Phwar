from Board import *


class Rules:
    BOARD = None
    TILES = None

    def __init__(self, board):
        Rules.BOARD = board
        Rules.TILES = board.TILES


        self.from_tile = None
        self.to_tile = None
        self.total_sight = None
        self.valid_sight = None
        self.piece_sight = None
        self.captures_in_sight = None

    def new_move(self):
        self.from_tile = None
        self.to_tile = None
        self.total_sight = None
        self.valid_sight = None
        self.piece_sight = None
        self.captures_in_sight = None

    def make_connection_to_board(self, board):
        board.tile_clicked.connect(self.generate_move)

    @pyqtSlot(TileItem)
    def generate_move(self, tile):
        if self.from_tile is not None and self.to_tile is not None:
            self.new_move()

        if tile.piece is not None:
            if self.from_tile is None and self.to_tile is None:
                self.from_tile = tile

                #self.line_of_sight()
                self.valid_moves()

            elif self.to_tile is None:
                print "Move not valid (to_tile contains piece)"
                tile.set_color(QColor(Qt.white))
                self.from_tile = None
        else:
            if self.from_tile is None:
                print "Move not valid (from_tile contains no piece)"
            elif self.to_tile is None:
                self.to_tile = tile
                self.total_sight = self.line_of_sight()
                self.valid_sight = self.valid_moves()
                if self.validate():
                    self.move_piece()
                else:
                    print "not in the tile's sight"
            tile.set_color(QColor(Qt.white))

    # Function to get all tiles in line of sight
    def line_of_sight(self, tile=None):
        if tile is None:
            tile = self.from_tile

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

        return sight

    # Function to get all valid tiles to move to
    def valid_moves(self, tile=None):
        if tile is None:
            tile = self.from_tile
            sight = self.line_of_sight()
        else:
            sight = self.line_of_sight(tile)

        valid_tiles = [[], [], []]  # bool is zero if end of valid tiles in that direction is reached
        center_tile = [t for t in Rules.TILES if t.coord == QPoint(Rules.BOARD.NR - 1, Rules.BOARD.NC / 2)][0]

        for i, direction in enumerate(sight):
            for t in [d for d in direction if i == 0]:  # Vertical direction
                if t.piece is not None:
                    if t.coord.x() < tile.coord.x():
                        valid_tiles[0] = []  # If piece is found above the clicked tile, clear the list so far
                    elif t.coord.x() > tile.coord.x():
                        break
                else:
                    valid_tiles[0].append(t)
                    if t == center_tile:
                        break

            for t in [d for d in direction if i == 1]:  # Diagonal 1 (UL -> LR)
                if t.piece is not None:
                    if t.coord.y() < tile.coord.y():
                        valid_tiles[1] = []  # If piece is found above the clicked tile, clear the list so far
                    elif t.coord.y() > tile.coord.y():
                        break
                else:
                    valid_tiles[1].append(t)
                    if t == center_tile:
                        break

            for t in [d for d in direction if i == 2]:  # Diagonal 1 (UR -> LL)
                if t.piece is not None:
                    if t.coord.y() > tile.coord.y():
                        valid_tiles[2] = []  # If piece is found above the clicked tile, clear the list so far
                    elif t.coord.y() < tile.coord.y():
                        break
                else:
                    valid_tiles[2].append(t)
                    if t == center_tile:
                        break

        self.valid_sight = valid_tiles
        self.possible_captures(tile)

        '''print "valid tiles: "
        for i in self.valid_sight:
            print_str = str()
            for v in i:
                if v.name.__len__() > 0:
                    print_str += v.name + " "
            if print_str.__len__() > 0:
                print print_str'''

        return self.valid_sight

    # Function to get the nearest pieces in each direction (if there isn't any, the value is set to None)
    # [ [(Tile, Piece, Index in Vertical Line), (Tile, Piece, Index in Vertical Line)],
    #   [(Tile, Piece, Index in Diagonal_1 Line), (Tile, Piece, Index in Diagonal_1 Line)],
    #   [(Tile, Piece, Index in Diagonal_2 Line), (Tile, Piece, Index in Diagonal_2 Line)] ]
    def pieces_in_sight(self, tile=None):
        if tile is None:
            tile = self.from_tile
            sight = self.line_of_sight()
        else:
            sight = self.line_of_sight(tile)

        sight_pieces = [[None] * 2, [None] * 2, [None] * 2]

        # self.line_of_sight(tile)

        for index, s_line in enumerate(sight):
            # 0, [Tile, Tile, Tile, ...]
            i = s_line.index(tile) - 1
            while i > -1:
                if s_line[i].piece is not None:
                    sight_pieces[index][0] = (s_line[i], s_line[i].piece, i)
                    break
                i -= 1

            i = s_line.index(tile) + 1
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

    # Function to find all possible captures and return which paths capture which pieces
    # The piece should not be equal to the current player's piece
    # The tile after/before should be empty
    # [(from, catured tile), (..., ...), ...]
    def possible_captures(self, tile=None):
        if tile is None:
            tile = self.from_tile
            sight_pieces = self.pieces_in_sight()
        else:
            sight_pieces = self.pieces_in_sight(tile)

        total_sight = self.line_of_sight()
        capturing_paths = []
        captures = []

        for line_index, line_pieces in enumerate(sight_pieces):

            for capture in [line_pieces[0], line_pieces[1]]:
                if capture is not None and capture[1].player != tile.piece.player:
                    if self.validate_capture(capture[0], tile):
                        self.valid_sight[line_index].append(capture[0])
                        capturing_paths.append((tile, capture[0]))

            '''if above is not None:
                if above[1].player != tile.piece.player and above[2] > 0:
                    if above[2] - 1 >= 0 and total_sight[line_index][above[2] - 1].piece is None:
                        if self.validate_capture(above[0], tile):
                            self.valid_sight[line_index].append(above[0])
                            capturing_paths.append((tile, above[0]))
                            i = 1
                            while above[2] - i >= 0:
                                if isinstance(total_sight[line_index][above[2] - i].piece, PieceItem):
                                    break
                                self.valid_sight[line_index].append(total_sight[line_index][above[2] - i])
                                capturing_paths.append((tile, total_sight[line_index][above[2] - i], above[0]))
                                i += 1

            if below is not None:
                if below[1].player != tile.piece.player and below[2] < total_sight[line_index].__len__() - 1:
                    if below[2] + 1 < total_sight[line_index].__len__() and not isinstance(
                            total_sight[line_index][below[2] + 1].piece, PieceItem):
                        if self.validate_capture(below[0], tile):
                            i = 1
                            while below[2] + i < total_sight[line_index].__len__():
                                if isinstance(total_sight[line_index][below[2] + i].piece, PieceItem):
                                    break

                                self.valid_sight[line_index].append(total_sight[line_index][below[2] + i])
                                capturing_paths.append((self.from_tile, total_sight[line_index][below[2] + i], below[0]))
                                i += 1'''

        for i, v in enumerate(self.valid_sight):
            self.valid_sight[i] = sorted(v, key=lambda tile: tile.coord.x())

        '''if opponent_pieces.__len__() > 0:
            print tile.name, " could capture:"
            for opp_p in opponent_pieces:
                print "Piece {}{}{} at Tile {} at Index {}".format(opp_p[1].player, opp_p[1].sign, opp_p[1].number,
                                                                   opp_p[0].name, opp_p[2])'''

        return capturing_paths

    # Function to validate whether a move is valid
    def validate(self):
        if self.from_tile is not None and self.to_tile is not None:
            for s in self.valid_sight:
                if s.__contains__(self.to_tile):
                    return True
            return False

    # Function to validate whether a capture is valid
    # TODO: A capturing configuration has to be created by yourself. In case the opponent puts itself in such a configuration no capture takes place.
    def validate_capture(self, to_capture, tile=None):
        if tile is None:
            tile = self.from_tile
        #total_sight = self.total_sight
        #self.total_sight = self.line_of_sight(to_capture[0])
        in_sight_captured = self.pieces_in_sight(to_capture)

        '''print_str = str()
        for i in in_sight_captured:
            if i[0] is None:
                print_str += " None "
            else:
                print_str += " " + i[0][0].name + " "
            if i[1] is None:
                print_str += " None "
            else:
                print_str += " " + i[1][0].name + " "
            print_str += "\n"
        print print_str'''

        check_tiles = [None, None]
        counter = 0
        total_sum = 0
        sum_by_pieces = []
        for sight_pieces in in_sight_captured:
            if sight_pieces[0] is not None:
                if sight_pieces[0][1].sign == "E":
                    total_sum -= 1
                    sum_by_pieces.append(sight_pieces[0][0].name)
                    # if sight_pieces[0][1].player == tile.
                elif sight_pieces[0][1].sign == "P":
                    total_sum += 1
                    sum_by_pieces.append(sight_pieces[0][0].name)

                if sight_pieces[0][1].player == tile.piece.player:
                    counter += 1
                    if check_tiles[0] is None:
                        check_tiles[0] = sight_pieces[0][0]
                    else:
                        check_tiles[1] = sight_pieces[0][0]

            if sight_pieces[1] is not None:
                if sight_pieces[1][1].sign == "E":
                    total_sum -= 1
                    sum_by_pieces.append(sight_pieces[1][0].name)
                elif sight_pieces[1][1].sign == "P":
                    total_sum += 1
                    sum_by_pieces.append(sight_pieces[1][0].name)

                if sight_pieces[1][1].player == tile.piece.player:
                    counter += 1
                    if check_tiles[0] is None:
                        check_tiles[0] = sight_pieces[1][0]
                    else:
                        check_tiles[1] = sight_pieces[1][0]

        '''print "Checking for two tiles (there are {} in total)".format(counter)
        if check_tiles[0] is not None:
            print "first: ", check_tiles[0].name
            if check_tiles[1] is not None:
                print "second: ", check_tiles[1].name
            else:
                print "second: None"
        else:
            print "first: None\nsecond: None"'''

        if counter >= 2:
            print "The total sum is {} by pieces {}".format(total_sum, sum_by_pieces)
            self.sum = total_sum

        if counter >= 2 and total_sum == 0:
            print "{} s"
            return True

        return False

    # Function to actually move the piece (in the Board.TILES)
    # If a capture takes places, remove the captured piece from the board
    def move_piece(self):
        self.stop_at_center()

        piece = self.from_tile.piece
        self.from_tile.set_piece(None)  # Remove it from the current tile
        piece.set_tile(self.to_tile)  # Put down the piece on the new tile
        self.to_tile.set_piece(piece)  # Add the piece to the new tile

        '''capturing_p = self.possible_captures(self.to_tile)
        for p in capturing_p:
            if p[0] == self.from_tile and p[1] == self.to_tile:
                if self.validate_capture(p[1]):
                    p[1].piece.set_tile(None)
                    p[1].set_piece(None)
                    piece = self.from_tile.piece
                    self.from_tile.set_piece(None)  # Remove it from the current tile
                    piece.set_tile(self.to_tile)  # Put down the piece on the new tile
                    self.to_tile.set_piece(piece)  # Add the piece to the new tile
                    return
                else:
                    print "Sum of all pieces is ", self.sum
                    return'''

    # If center hex is passed in planned move, stop at the center hex
    def stop_at_center(self):

        direction = [s for s in self.valid_sight if s.__contains__(self.to_tile)][0]
        center_tile = [t for t in Rules.TILES if t.coord == QPoint(Rules.BOARD.NR - 1, Rules.BOARD.NC / 2)][0]

        if direction.__contains__(center_tile):
            if min(self.to_tile.coord.x(), self.from_tile.coord.x()) < center_tile.coord.x() < max(
                    self.to_tile.coord.x(), self.from_tile.coord.x()):
                #   print "crossing center"
                self.to_tile = center_tile
                # else:
                #    print "moving in a direction containing center, but not crossing it"

    # Function to evaluate whether the game has reached its ending
    def terminate(self):
        return False
