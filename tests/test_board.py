from chemate.board import Board
from chemate.positions import EmptyPosition, InitialPosition
from chemate.figure import *


class TestBoard(object):
    def test_board_init(self):
        board = Board(InitialPosition())
        print()
        print(board)

        assert len(list(board.figures())) == 32

        assert len(list(filter(lambda x: x.color == Player.WHITE, board.figures()))) == 16
        assert len(list(filter(lambda x: x.color == Player.BLACK, board.figures()))) == 16

        assert len(list(filter(lambda x: isinstance(x, Pawn), board.figures()))) == 16
        assert len(list(filter(lambda x: isinstance(x, Rook), board.figures()))) == 4
        assert len(list(filter(lambda x: isinstance(x, Knight), board.figures()))) == 4
        assert len(list(filter(lambda x: isinstance(x, Bishop), board.figures()))) == 4
        assert len(list(filter(lambda x: isinstance(x, Queen), board.figures()))) == 2
        assert len(list(filter(lambda x: isinstance(x, King), board.figures()))) == 2

        assert len(list(filter(lambda x: isinstance(x, Pawn) and x.color == Player.WHITE, board.figures()))) == 8
        assert len(list(filter(lambda x: isinstance(x, Pawn) and x.color == Player.BLACK, board.figures()))) == 8
        assert len(list(filter(lambda x: isinstance(x, Rook) and x.color == Player.WHITE, board.figures()))) == 2
        assert len(list(filter(lambda x: isinstance(x, Rook) and x.color == Player.BLACK, board.figures()))) == 2
        assert len(list(filter(lambda x: isinstance(x, Knight) and x.color == Player.WHITE, board.figures()))) == 2
        assert len(list(filter(lambda x: isinstance(x, Knight) and x.color == Player.BLACK, board.figures()))) == 2
        assert len(list(filter(lambda x: isinstance(x, Bishop) and x.color == Player.WHITE, board.figures()))) == 2
        assert len(list(filter(lambda x: isinstance(x, Bishop) and x.color == Player.BLACK, board.figures()))) == 2
        assert len(list(filter(lambda x: isinstance(x, Queen) and x.color == Player.WHITE, board.figures()))) == 1
        assert len(list(filter(lambda x: isinstance(x, Queen) and x.color == Player.BLACK, board.figures()))) == 1
        assert len(list(filter(lambda x: isinstance(x, King) and x.color == Player.WHITE, board.figures()))) == 1
        assert len(list(filter(lambda x: isinstance(x, King) and x.color == Player.BLACK, board.figures()))) == 1
        pass

    def test_board_move(self):
        board = Board(InitialPosition())
        board.make_move(Position.char('e2'), Position.char('e4'))
        print(board)
        assert len(board.moves) == 1
        board.rollback_move()
        print(board)
        assert len(board.moves) == 0

    def test_checkmate(self):
        board = Board(EmptyPosition())
        fig = [
            King(Player.WHITE, Position('h1')),
            Pawn(Player.WHITE, Position('g2')),
            Pawn(Player.WHITE, Position('h2')),
            Bishop(Player.BLACK, Position('d4')),
            Pawn(Player.BLACK, Position('a7'))
        ]
        board.put_figures(fig)
        print()
        print(board)

        # No check, no mate
        moves = board.legal_moves(Player.WHITE)
        assert len(moves) == 4

        board.make_move(Position('h1'), Position('g1'))
        board.make_move(Position('a7'), Position('a6'))
        print()
        print(board)
        moves = board.legal_moves(Player.WHITE)
        # Check, no mate
        assert len(moves) == 2

        board.put_figure(Rook(Player.BLACK, Position('c1')))
        moves = board.legal_moves(Player.WHITE)
        assert len(moves) == 0

        board.make_move(Position('h2'), Position('h3'))
        board.make_move(Position('a6'), Position('a5'))
        moves = board.legal_moves(Player.WHITE)
        assert len(moves) == 1

    def test_has_moved(self):
        board = Board(EmptyPosition())

        p1 = Pawn(Player.WHITE, Position('a2'))
        p2 = Pawn(Player.BLACK, Position('a7'))
        board.put_figures([p1, p2])

        m = board.legal_moves(Player.WHITE)[0]
        board.make_move(m.from_pos, m.to_pos)

        print()
        print(board)

        assert board.has_moved(p1)
        assert not board.has_moved(p2)

    def test_check_position(self):
        board = Board(EmptyPosition())

        k = King(Player.WHITE, Position('e1'))
        r = Rook(Player.BLACK, Position('a7'))
        board.put_figures([k, r])

        print()
        print(board)

        assert not board.has_check(Player.WHITE)
        assert not board.has_check(Player.BLACK)

        board.make_move(r.position, Position('a1'))
        print()
        print(board)
        assert board.has_check(Player.WHITE)
        assert not board.has_check(Player.BLACK)
        pass
