from chemate.board import Board
from chemate.core import Player, Position
from chemate.figures import King, Rook, Pawn, Bishop
from chemate.positions import EmptyPosition
from chemate.utils import PlainExporter


class TestKing(object):
    def test_move(self):
        board = Board()
        board.init(EmptyPosition())
        king = King(Player.WHITE, Position.from_char('b2'))
        board.put_figures([king, King(Player.BLACK, Position.from_char('g8'))])

        moves = list(board.figure_moves(king))
        assert len(moves) == 8

        board.move(next(filter(lambda m: str(m) == 'Kb2-a1', moves)))
        moves = list(board.figure_moves(king))
        assert len(moves) == 3

    def test_short_rook(self):
        board = Board()
        board.init(EmptyPosition())

        king = King(Player.WHITE, Position.from_char('e1'))
        rook = Rook(Player.WHITE, Position.from_char('h1'))
        board.put_figures([king, rook, King(Player.BLACK, Position.from_char('g8'))])

        moves = [move for move in board.figure_moves(king) if move.rook is not None]
        assert len(moves) == 1, "Rook must be available"

        # make and rollback move
        board.move(next(iter(moves)))
        assert board.figure_at(Position.from_char('f1')) == rook, 'After rooking is invalid rook position'
        assert board.figure_at(Position.from_char('g1')) == king, 'After rooking is invalid king position'

        board.rollback()
        assert board.figure_at(Position.from_char('e1')) == king, 'Rollback after rooking is invalid king position'
        assert board.figure_at(Position.from_char('h1')) == rook, 'Rollback after rooking is invalid rook position'

    def test_short_rook_1(self):
        board = Board()
        board.init(EmptyPosition())

        king = King(Player.WHITE, Position.from_char('e1'))
        rook = Rook(Player.WHITE, Position.from_char('h1'))
        pawn = Pawn(Player.WHITE, Position.from_char('g1'))
        board.put_figures([king, rook, pawn, King(Player.BLACK, Position.from_char('g8'))])

        moves = list(map(str, board.figure_moves(king)))
        assert '0-0' not in moves, "Rook must be unavailable when figures between"

    def test_short_rook_2(self):
        board = Board()
        board.init(EmptyPosition())
        king = King(Player.WHITE, Position.from_char('e1'))
        rook = Rook(Player.WHITE, Position.from_char('h1'))
        board.put_figures([king, rook])

        board.move(next(filter(lambda m: str(m) == 'Ke1-e2', board.figure_moves(king))))
        board.move(next(filter(lambda m: str(m) == 'Ke2-e1', board.figure_moves(king))))

        moves = list(map(str, board.figure_moves(king)))
        assert '0-0' not in moves, "Rook must be unavailable when king has moved"

    def test_short_rook_3(self):
        board = Board()
        board.init(EmptyPosition())

        king = King(Player.WHITE, Position.from_char('e1'))
        rook = Rook(Player.WHITE, Position.from_char('h1'))
        board.put_figures([king, rook])

        board.move(next(filter(lambda m: str(m) == 'Rh1-h2', board.figure_moves(rook))))
        board.move(next(filter(lambda m: str(m) == 'Rh2-h1', board.figure_moves(rook))))
        moves = list(map(str, board.figure_moves(king)))
        assert '0-0' not in moves, "Rook must be unavailable when rook is moved"

    def test_short_rook_4(self):
        board = Board()
        board.init(EmptyPosition())
        king = King(Player.WHITE, Position.from_char('e1'))
        rook = Rook(Player.WHITE, Position.from_char('h1'))
        bishop = Bishop(Player.BLACK, Position.from_char('a5'))
        board.put_figures([king, rook, bishop])
        print(f'\n{board.export(PlainExporter)}\n')
        moves = list(map(str, board.figure_moves(king)))
        assert '0-0' not in moves, "Rook must be unavailable when e1 is under pressure"

        board.remove_figure(bishop)
        bishop.position = Position.from_char('b5')
        board.put_figure(bishop)
        moves = list(map(str, board.figure_moves(king)))
        assert '0-0' not in moves, "Rook must be unavailable when f1 is under pressure"

        board.remove_figure(bishop)
        bishop.position = Position.from_char('c5')
        board.put_figure(bishop)
        moves = [move for move in board.figure_moves(king) if move.rook is not None]
        assert '0-0' not in moves, "Rook must be unavailable when g1 is under pressure"

    def test_short_rook_5(self):
        board = Board()
        board.init(EmptyPosition())
        king = King(Player.WHITE, Position.from_char('e1'))
        rook = Rook(Player.WHITE, Position.from_char('h1'))
        pawn = Pawn(Player.BLACK, Position.from_char('e2'))
        board.put_figures([king, rook, pawn])

        moves = list(map(str, board.figure_moves(king)))
        assert '0-0' not in moves, "Rook must be unavailable when e2 is under pressure"

    def test_long_rook(self):
        board = Board()
        board.init(EmptyPosition())

        king = King(Player.BLACK, Position.from_char('e8'))
        rook = Rook(Player.BLACK, Position.from_char('a8'))
        board.put_figures([king, rook])

        moves = [move for move in board.figure_moves(king) if move.rook is not None]
        assert '0-0-0' in list(map(str, moves)), "Rook must be available"

        # make and rollback move
        board.move(next(iter(moves)))
        assert board.figure_at(Position.from_char('d8')) == rook, 'After rooking is invalid rook position'
        assert board.figure_at(Position.from_char('c8')) == king, 'After rooking is invalid king position'

        board.rollback()
        assert board.figure_at(Position.from_char('e8')) == king, 'Rollback after rooking is invalid king position'
        assert board.figure_at(Position.from_char('a8')) == rook, 'Rollback after rooking is invalid rook position'

    def test_long_rook_1(self):
        board = Board()
        board.init(EmptyPosition())
        king = King(Player.BLACK, Position.from_char('e8'))
        rook = Rook(Player.BLACK, Position.from_char('f8'))
        pawn = Pawn(Player.BLACK, Position.from_char('a8'))
        board.put_figures([king, rook, pawn])

        moves = [move for move in board.figure_moves(king) if move.rook is not None]
        assert len(moves) == 0, "Rook must be unavailable when figures between"

    def test_long_rook_2(self):
        board = Board()
        board.init(EmptyPosition())
        king = King(Player.BLACK, Position.from_char('e8'))
        rook = Rook(Player.BLACK, Position.from_char('a8'))
        board.put_figures([king, rook])

        board.move(next(filter(lambda m: str(m) == 'ke8-e7', board.figure_moves(king))))
        board.move(next(filter(lambda m: str(m) == 'ke7-e8', board.figure_moves(king))))

        moves = [move for move in board.figure_moves(king) if move.rook is not None]
        assert len(moves) == 0, "Rooking must be unavailable when king has moved"

    def test_long_rook_3(self):
        board = Board()
        board.init(EmptyPosition())

        king = King(Player.BLACK, Position.from_char('e7'))
        rook = Rook(Player.BLACK, Position.from_char('a8'))
        board.put_figures([king, rook])

        board.move(next(filter(lambda m: str(m) == 'ra8-a7', board.figure_moves(rook))))
        board.move(next(filter(lambda m: str(m) == 'ra7-a8', board.figure_moves(rook))))

        moves = [move for move in board.figure_moves(king) if move.rook is not None]
        assert len(moves) == 0, "Rooking must be unavailable when rook is moved"

    def test_long_rook_4(self):
        board = Board()
        board.init(EmptyPosition())

        king = King(Player.BLACK, Position.from_char('e8'))
        rook = Rook(Player.BLACK, Position.from_char('a8'))
        bishop = Bishop(Player.WHITE, Position.from_char('h5'))
        board.put_figures([king, rook, bishop])

        moves = [move for move in board.figure_moves(king) if move.rook is not None]
        assert len(moves) == 0, "Rooking must be unavailable when e1 is under pressure"

        board.remove_figure(bishop)
        bishop.position = Position.from_char('g5')
        board.put_figure(bishop)
        moves = [move for move in board.figure_moves(king) if move.rook is not None]
        assert len(moves) == 0, "Rooking must be unavailable when f1 is under pressure"

        board.remove_figure(bishop)
        bishop.position = Position.from_char('f5')
        board.put_figure(bishop)
        moves = [move for move in board.figure_moves(king) if move.rook is not None]
        assert len(moves) == 0, "Rooking must be unavailable when g1 is under pressure"
