from ShapeItems import *
from Board import *

class TakeTurn:

    ORIGINAL_TILES = None
    PIECES = None
    moving_piece = None

    def __init__(self, player, tiles, pieces):

        self.player = player

        self.TILES = tiles              # Copy of the TILES object on the board
        self.tiles = list(tiles)        # Copy of the TILES values on the board --> Changes won't affect the board

        self.PIECES = pieces            # Copy of PIECES object on board
        self.pieces = list(pieces)      # Copy of the PIECES values on the board --> Changes wont't affect the board

        #self.print_tiles(self.TILES)

        self._sight_lines = list()
        self._valid_tiles = list()

        self._pieces = filter(lambda x: x[0].player == self.player, self.PIECES)
        self._moves = self.moves()

        #for m in self._moves:
        #    s_TakeTurn.print_move(m)

        TakeTurn.print_move(self._moves[0])
        self._local_boards = self.local_boards(1)
        #self.print_tiles(self.tiles, 9)

        for index, l_b in enumerate(self._local_boards):
            self.tiles = l_b
            self.check_captures(l_b)


    def moves(self):
        _moves = list()
        for piece, tile in self._pieces:
            self._sight_lines = self.sight_lines(tile)
            self._valid_tiles = self.valid_tiles(tile)
            for direction in self._valid_tiles:
                for to_tile in direction:
                    _moves.append((tile, to_tile))
        return _moves

    def sight_lines(self, tile):
        _sight = [[], [], []]

        for t in self.tiles:
            if t.coord.y() == tile.coord.y():
                _sight[0].append(t)

            x_diff = tile.coord.x() - t.coord.x()
            y_diff = tile.coord.y() - t.coord.y()

            if x_diff == y_diff:
                _sight[1].append(t)

            if x_diff == -y_diff:
                _sight[2].insert(0, t)

        return _sight

    def valid_tiles(self, tile):
        _valid = [[], [], []]

        for d in range(_valid.__len__()):
            passed_tile = False
            for t in self._sight_lines[d]:
                #print t.name
                if not isinstance(t.piece, PieceItem):
                    _valid[d].append(t)
                elif t == tile:
                    passed_tile = True
                elif passed_tile:
                    break

        '''print "valid tiles for ", tile.name
        for d in _valid:
            s = str()
            for t in d:
                s += t.name + "  "
            print s
        print "---------------------------------------------------"'''
        return _valid

  #  def local_boards(self, move):

    def sight_pieces(self, tile):

        _sight_pieces = [None, None, None, None, None, None] #, None], [None, None], [None, None]]
        self._sight_lines = self.sight_lines(tile)
        #self._valid_tiles = self.valid_tiles(self._moves[0][1])

        for index, sight in enumerate(self._sight_lines):
            i = filter(lambda i: sight[i].name == tile.name, range(sight.__len__()))[0] - 1
            while i > -1:
                if isinstance(sight[i].piece, PieceItem):
                    _sight_pieces[(index*2)/2] = sight[i]
                    break
                i -= 1

            i = filter(lambda i: sight[i].name == tile.name, range(sight.__len__()))[0] + 1
            while i < sight.__len__():
                if isinstance(sight[i].piece, PieceItem):
                    _sight_pieces[(index*2)/2] = sight[i]
                    break
                i += 1

        return _sight_pieces

    def local_boards(self, n=None):
        if n is None:
            n = self._moves.__len__()
        local_boards = list()
        for _from, _to in self._moves[:n]:
            tiles = list(self.TILES)
            i_from = filter(lambda i: tiles[i].name == _from.name, range(tiles.__len__()))[0]
            i_to = filter(lambda i: tiles[i].name == _to.name, range(tiles.__len__()))[0]
            self.piece_movement(tiles, i_from, i_to)
            local_boards.append(tiles)
        return local_boards

    def check_captures(self, local_board):

        tiles_opponent = filter(lambda t: t.piece.player != self.player, [t_p for t_p in local_board if isinstance(t_p.piece, PieceItem)])
        for t_opp in tiles_opponent:
            s = self.sight_pieces(t_opp)

            my_pieces_linesight = 0
            total_sum = 0
            print "Checking if we could capture ", t_opp.name
            p_str = str()
            for i in s:
                if i is None:
                    p_str += "None  "
                else:
                    if i.piece.player == self.player:
                        my_pieces_linesight += 1
                    if i.piece.sign == "E":
                        total_sum -= 1
                    elif i.piece.sign == "P":
                        total_sum += 1

                    p_str += i.name + "  "

            valid_capture = False
            if my_pieces_linesight > 1 and total_sum == 0:
                valid_capture = True
            print p_str
            print "Sum of {} and {} of my tiles in sight, so {}".format(total_sum, my_pieces_linesight, valid_capture)



            #self._sight_lines = self.sight_lines(t_opp)
            #self._valid_tiles = self.valid_tiles(t_opp)



        #for op in tiles_opponent:
        #    print "Piece {} in Tile {}".format(op.piece.name, op.name)

    @staticmethod
    def piece_movement(tiles, i_from, i_to):
        piece = tiles[i_from].piece

        from_tile = TileItem()
        from_tile.set_name(tiles[i_from].name)
        from_tile.set_coord(tiles[i_from].coord)
        from_tile.set_color(tiles[i_from].color)
        from_tile.set_path(tiles[i_from].path)
        from_tile.set_pos(tiles[i_from].pos)
        from_tile.set_piece(tiles[i_to].piece)
        tiles[i_from] = from_tile

        to_tile = TileItem()
        to_tile.set_name(tiles[i_to].name)
        to_tile.set_coord(tiles[i_to].coord)
        to_tile.set_color(tiles[i_to].color)
        to_tile.set_path(tiles[i_to].path)
        to_tile.set_pos(tiles[i_to].pos)
        to_tile.set_piece(piece)
        tiles[i_to] = to_tile

    @staticmethod
    def print_tiles(x, n=None, y=None, m=None):
        if n is None:
            n = x.__len__()
        print "-------------------------------------------------------------"
        if m is not None:
            print "Move from {} to {}\n  TILES    -    tiles".format(m[0].name, m[1].name)
        for i in range(n):
            sp = "(" + x[i].name + ", "
            if not isinstance(x[i].piece, PieceItem):
                sp += "None)"
            else:
                sp += x[i].piece.name + ")"

            if y is not None:
                sp += "  -  (" + y[i].name + ", "
                if not isinstance(y[i].piece, PieceItem):
                    sp += "None)"
                else:
                    sp += y[i].piece.name + ")"
            print sp

    @staticmethod
    def print_move(move):
        print "Moving piece in {} to {}".format(move[0].name, move[1].name)

    @staticmethod
    def print_sight_pieces(sight_p):
        to_print = str()
        for s in sight_p:
            if s is None:
                to_print += "None  "
            else:
                to_print += s.name + "  "
        print to_print

