from TakeTurn import *
class Game:

    TILES = list()
    PIECES = list()

    def __init__(self, board, rules):
        self.board = board
        Game.TILES = board.TILES
        Game.PIECES = board.PIECES
        self.rules = rules
        self.player = "B"


        turn = TakeTurn(self.player, board.tiles, board.PIECES)

        '''self.pieces = self.own_pieces()
        self.moves = list()

        self.all_moves()'''

    def make_connection_to_board(self, board):
        board.board_changed.connect(self.update_board)

    @pyqtSlot(tuple)
    def update_board(self, board):
        Game.TILES = board[0]
        Game.PIECES = board[1]
        print "-------------------------------------------------------\nboard in game updated!"
        self.pieces = self.own_pieces()
        self.moves = self.all_moves()

    def own_pieces(self):
        pieces = list(filter(lambda p: p[0].player == self.player, Game.PIECES))
        return pieces

    # [(from, to)]
    def all_moves(self):
        moves = list()
        for p in self.pieces:
            for direction in self.rules.valid_moves(p[1]):
                p_str = "From {}: ".format(p[1].name)
                for v in direction:
                    p_str += v.name + " "
                    moves.append((p[1], v))
        return moves
