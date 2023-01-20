from chemate.board import Board
from chemate.core import Movement
from chemate.positions import EmptyPosition, InitialPosition, PredefinedFENPosition
from chemate.figures import *
from chemate.utils import PlainExporter


class TestBoard(object):
    def test_board_init(self):
        board = Board()
        board.init(InitialPosition())

        assert len(list(board.figures)) == 32, "Need exact 32 figures"

        assert len(list(board.figure_by_class(Figure, Player.WHITE))) == 16, "Need exact 16 white figures"
        assert len(list(board.figure_by_class(Figure, Player.BLACK))) == 16, "Need exact 16 black figures"

        assert len(list(board.figure_by_class(Pawn))) == 16, "Need exact 16 paws"
        assert len(list(board.figure_by_class(Rook))) == 4, "Need exact 4 rooks"
        assert len(list(board.figure_by_class(Knight))) == 4, "Need exact 4 knights"
        assert len(list(board.figure_by_class(Bishop))) == 4, "Need exact 4 bishops"
        assert len(list(board.figure_by_class(Queen))) == 2, "Need exact 2 queens"
        assert len(list(board.figure_by_class(King))) == 2, "Need exact 2 kings"

        assert len(list(board.figure_by_class(Pawn, Player.WHITE))) == 8, "Need exact 8 white paws"
        assert len(list(board.figure_by_class(Rook, Player.WHITE))) == 2, "Need exact 2 white rooks"
        assert len(list(board.figure_by_class(Knight, Player.WHITE))) == 2, "Need exact 2 white knights"
        assert len(list(board.figure_by_class(Bishop, Player.WHITE))) == 2, "Need exact 2 white bishops"
        assert len(list(board.figure_by_class(Queen, Player.WHITE))) == 1, "Need exact 1 white queens"
        assert len(list(board.figure_by_class(King, Player.WHITE))) == 1, "Need exact 1 white kings"
        
        assert len(list(board.figure_by_class(Pawn, Player.BLACK))) == 8, "Need exact 8 black paws"
        assert len(list(board.figure_by_class(Rook, Player.BLACK))) == 2, "Need exact 2 black rooks"
        assert len(list(board.figure_by_class(Knight, Player.BLACK))) == 2, "Need exact 2 black knights"
        assert len(list(board.figure_by_class(Bishop, Player.BLACK))) == 2, "Need exact 2 black bishops"
        assert len(list(board.figure_by_class(Queen, Player.BLACK))) == 1, "Need exact 1 black queens"
        assert len(list(board.figure_by_class(King, Player.BLACK))) == 1, "Need exact 1 black kings"
        pass

    def test_board_valid_moves(self):
        board = Board()
        board.init(PredefinedFENPosition('8/8/r4PK1/8/1k6/8/8/8'))
        print(f'\n{board.export(PlainExporter)}\n')
        moves = list(map(str, board.valid_moves(Player.WHITE)))
        print(moves)
        assert len(moves) == 7
        pass

    def test_board_move(self):
        board = Board()
        board.init(InitialPosition())
        p = board.figure_at(Position.from_char('e2'))
        assert p is not None and isinstance(p, Pawn) and p.color == Player.WHITE
        board.move(next(board.figure_moves(p)))
        assert len(list(board.figures)) == 32, "After move all figures same"

        assert len(board.moves) == 1
        board.rollback()
        assert len(board.moves) == 0

    def test_checkmate(self):
        # No check, no mate
        board = Board()
        board.init(PredefinedFENPosition('7k/p7/8/8/3b4/8/6PP/7K'))
        print(f'\n{board.export(PlainExporter)}\n')
        moves = list(map(str, board.valid_moves(Player.WHITE)))
        print(moves)
        assert len(moves) == 4

        # Check, no mate
        board.init(PredefinedFENPosition('7k/8/p7/8/3b4/8/6PP/6K1'))
        print(f'\n{board.export(PlainExporter)}\n')
        moves = list(map(str, board.valid_moves(Player.WHITE)))
        print(moves)
        assert len(moves) == 2

        board.init(PredefinedFENPosition('7k/8/8/p7/3b4/7P/6P1/2r3K1'))
        print(f'\n{board.export(PlainExporter)}\n')
        moves = list(map(str, board.valid_moves(Player.WHITE)))
        print(moves)
        assert len(moves) == 1

        board.init(PredefinedFENPosition('7k/8/8/p1Q5/3b4/7P/6P1/2r3K1'))
        print(f'\n{board.export(PlainExporter)}\n')
        moves = list(map(str, board.valid_moves(Player.WHITE)))
        print(moves)
        assert len(moves) == 1

        board.init(PredefinedFENPosition('7k/8/8/p1Q5/8/7P/6P1/2r3K1'))
        print(f'\n{board.export(PlainExporter)}\n')
        moves = list(map(str, board.valid_moves(Player.WHITE)))
        print(moves)
        assert len(moves) == 3

        # Check and mate
        board.init(PredefinedFENPosition('7k/8/p7/8/3b4/8/6PP/2r3K1'))
        print(f'\n{board.export(PlainExporter)}\n')
        moves = list(map(str, board.valid_moves(Player.WHITE)))
        print(moves)
        assert len(moves) == 0
        assert board.test_for_mate(Player.WHITE)

    def test_chemate_1(self):
        board = Board()
        board.init(PredefinedFENPosition('7k/8/8/p7/8/7P/5QP1/2r3K1'))
        print(f'\n{board.export(PlainExporter)}\n')
        assert board.test_for_check(Player.WHITE)
        moves = list(map(str, board.valid_moves(Player.WHITE)))
        print(moves)
        assert len(moves) == 3

    def test_has_moved(self):
        board = Board()
        board.init(EmptyPosition())

        p1 = Pawn(Player.WHITE, Position.from_char('a2'))
        p2 = Pawn(Player.BLACK, Position.from_char('a7'))
        board.put_figures([
            p1, p2,
            King(Player.WHITE, Position.from_char('h2')), King(Player.BLACK, Position.from_char('h7'))])

        m = next(board.figure_moves(p1))
        board.move(m)

        assert p1.has_moved
        assert not p2.has_moved

    def test_check_position(self):
        board = Board()
        board.init(PredefinedFENPosition('3k4/r7/8/8/8/8/8/4K3'))
        assert not board.test_for_check(Player.WHITE)
        assert not board.test_for_check(Player.BLACK)

        print(f'\n{board.export(PlainExporter)}\n')
        p = board.figure_at(Position.from_char('a7'))
        move = next(filter(lambda m: m.to_pos == Position.from_char('a1'),
                           board.figure_moves(p)
                           ), None)
        assert move is not None

        board.move(move)
        assert board.test_for_check(Player.WHITE)
        assert not board.test_for_check(Player.BLACK)
        pass

    def test_rollback_move(self):
        board = Board()
        board.init(PredefinedFENPosition('1r6/7K/2N5/8/8/k7/8/8'))
        c6 = board.figure_at(Position.from_char('c6'))
        moves = board.figure_moves(c6)
        move = next(filter(lambda x: x.to_pos == Position.from_char('b8'), moves))
        assert move is not None
        board.move(move)
        assert board.figure_at(Position.from_char('b8')) is not None
        assert board.figure_at(Position.from_char('c6')) is None

        board.rollback()
        assert board.figure_at(Position.from_char('b8')) is not None
        assert board.figure_at(Position.from_char('c6')) is not None
