from chemate.board import Board
from chemate.positions import EmptyPosition, InitialPosition, PredefinedFENPosition
from chemate.figure import *


class TestBoard(object):
    def test_board_init(self):
        board = Board(InitialPosition())

        assert len(list(board.figures())) == 32, "Need exact 32 figures"

        assert len(list(board.find_figures(Figure, Player.WHITE))) == 16, "Need exact 16 white figures"
        assert len(list(board.find_figures(Figure, Player.BLACK))) == 16, "Need exact 16 black figures"

        assert len(list(board.find_figures(Pawn))) == 16, "Need exact 16 paws"
        assert len(list(board.find_figures(Rook))) == 4, "Need exact 4 rooks"
        assert len(list(board.find_figures(Knight))) == 4, "Need exact 4 knights"
        assert len(list(board.find_figures(Bishop))) == 4, "Need exact 4 bishops"
        assert len(list(board.find_figures(Queen))) == 2, "Need exact 2 queens"
        assert len(list(board.find_figures(King))) == 2, "Need exact 2 kings"

        assert len(list(board.find_figures(Pawn, Player.WHITE))) == 8, "Need exact 8 white paws"
        assert len(list(board.find_figures(Rook, Player.WHITE))) == 2, "Need exact 2 white rooks"
        assert len(list(board.find_figures(Knight, Player.WHITE))) == 2, "Need exact 2 white knights"
        assert len(list(board.find_figures(Bishop, Player.WHITE))) == 2, "Need exact 2 white bishops"
        assert len(list(board.find_figures(Queen, Player.WHITE))) == 1, "Need exact 1 white queens"
        assert len(list(board.find_figures(King, Player.WHITE))) == 1, "Need exact 1 white kings"
        
        assert len(list(board.find_figures(Pawn, Player.BLACK))) == 8, "Need exact 8 black paws"
        assert len(list(board.find_figures(Rook, Player.BLACK))) == 2, "Need exact 2 black rooks"
        assert len(list(board.find_figures(Knight, Player.BLACK))) == 2, "Need exact 2 black knights"
        assert len(list(board.find_figures(Bishop, Player.BLACK))) == 2, "Need exact 2 black bishops"
        assert len(list(board.find_figures(Queen, Player.BLACK))) == 1, "Need exact 1 black queens"
        assert len(list(board.find_figures(King, Player.BLACK))) == 1, "Need exact 1 black kings"
        pass

    def test_board_legal_moves(self):
        board = Board(PredefinedFENPosition('8/8/r4PK1/8/1k6/8/8/8'))
        assert len(board.legal_moves(Player.WHITE)) == 7
        pass

    def test_board_move(self):
        board = Board(InitialPosition())
        board.make_move(Movement.from_char('e2-e4'))
        assert len(list(board.figures())) == 32, "After move all figures same"

        assert len(board.moves) == 1
        board.rollback_move()
        assert len(board.moves) == 0

    def test_checkmate(self):
        # No check, no mate
        board = Board(PredefinedFENPosition('7k/p7/8/8/3b4/8/6PP/7K'))
        moves = board.legal_moves(Player.WHITE)
        assert len(moves) == 4

        # Check, no mate
        board = Board(PredefinedFENPosition('7k/8/p7/8/3b4/8/6PP/6K1'))
        moves = board.legal_moves(Player.WHITE)
        assert len(moves) == 2

        board = Board(PredefinedFENPosition('7k/8/8/p7/3b4/7P/6P1/2r3K1'))
        moves = board.legal_moves(Player.WHITE)
        assert len(moves) == 1

        board = Board(PredefinedFENPosition('7k/8/8/p1Q5/3b4/7P/6P1/2r3K1'))
        moves = board.legal_moves(Player.WHITE)
        assert len(moves) == 1

        board = Board(PredefinedFENPosition('7k/8/8/p1Q5/8/7P/6P1/2r3K1'))
        moves = board.legal_moves(Player.WHITE)
        assert len(moves) == 3

        board = Board(PredefinedFENPosition('7k/8/8/p7/8/7P/5QP1/2r3K1'))
        moves = board.legal_moves(Player.WHITE)
        assert len(moves) == 3

        # Check and mate
        board = Board(PredefinedFENPosition('7k/8/p7/8/3b4/8/6PP/2r3K1'))
        moves = board.legal_moves(Player.WHITE)
        assert len(moves) == 0
        assert board.has_mate(Player.WHITE)

    def test_has_moved(self):
        board = Board(EmptyPosition())

        p1 = Pawn(Player.WHITE, Position.from_char('a2'))
        p2 = Pawn(Player.BLACK, Position.from_char('a7'))
        board.put_figures([p1, p2])

        m = board.legal_moves(Player.WHITE)[0]
        board.make_move(m)

        assert board.has_moved(p1)
        assert not board.has_moved(p2)

    def test_check_position(self):
        board = Board(PredefinedFENPosition('3k4/r7/8/8/8/8/8/4K3'))
        assert not board.test_for_check(Player.WHITE)
        assert not board.test_for_check(Player.BLACK)

        board.make_move(Movement.from_char('a7-a1'))
        assert board.test_for_check(Player.WHITE)
        assert not board.test_for_check(Player.BLACK)
        pass

    def test_rollback_move(self):
        board = Board(PredefinedFENPosition('1r6/7K/2N5/8/8/k7/8/8'))
        c6 = board.get_figure(Position.from_char('c6'))
        moves = c6.available_moves(hash(board))
        move = next(filter(lambda x: x.to_pos == Position.from_char('b8'), moves))
        assert move is not None
        board.make_move(move)
        assert board.get_figure(Position.from_char('b8')) is not None
        assert board.get_figure(Position.from_char('c6')) is None

        board.rollback_move()
        assert board.get_figure(Position.from_char('b8')) is not None
        assert board.get_figure(Position.from_char('c6')) is not None
