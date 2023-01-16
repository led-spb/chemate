from chemate.board import Board
from chemate.core import Player, Position
from chemate.figures import Pawn, Queen
from chemate.positions import EmptyPosition, PredefinedFENPosition


class TestPawn(object):
    def test_first_move(self):
        board = Board()
        board.init(EmptyPosition())

        # 1. White pawn can move 2 on up at first
        p1 = Pawn(Player.WHITE, Position.from_char('d2'))
        board.put_figure(p1)
        moves = list(board.figure_moves(p1))
        assert len(moves) == 2 \
               and 'd2-d3' in map(str, moves) and 'd2-d4' in map(str, moves), "White pawn can move 2 on up at first"

        # 2. After this only one
        board.move(next(filter(lambda m: m.to_pos == Position.from_char('d3'), moves)))
        moves = list(board.figure_moves(p1))
        assert len(moves) == 1 \
               and 'd3-d4' in map(str, moves), "After move, pawn can only one"

        # 3. Black pawn can move 2 on down
        p2 = Pawn(Player.BLACK, Position.from_char('b7'))
        moves = list(board.figure_moves(p2))
        assert len(moves) == 2 \
               and 'b7-b6' in map(str, moves) and 'b7-b5' in map(str, moves)

        board.move(next(filter(lambda m: m.to_pos == Position.from_char('b5'), moves)))
        moves = list(board.figure_moves(p2))
        assert len(moves) == 1 \
               and 'b5-b4' in map(str, moves)

    def test_blocked(self):
        board = Board()
        board.init(EmptyPosition())

        # Blocked by end of board
        a8 = Pawn(Player.WHITE, Position.from_char('a8'))
        board.put_figure(a8)
        moves = list(board.figure_moves(a8))
        assert len(moves) == 0

        # Blocked by own figure
        e4 = Pawn(Player.WHITE, Position.from_char('a7'))
        board.put_figure(e4)
        moves = list(board.figure_moves(e4))
        assert len(moves) == 0

        # Blocked by opposite figure and fight
        d4 = Pawn(Player.WHITE, Position.from_char('d4'))
        e4 = Pawn(Player.WHITE, Position.from_char('e4'))
        d5 = Pawn(Player.BLACK, Position.from_char('d5'))
        e5 = Pawn(Player.BLACK, Position.from_char('e5'))
        board.put_figures([d4, e4, d5, e5])

        moves = list(board.figure_moves(d4))
        assert len(moves) == 1
        assert 'd4xe5' in list(map(str, moves))

        moves = list(board.figure_moves(e4))
        assert len(moves) == 1
        assert 'e4xd5' in list(map(str, moves))

        moves = list(board.figure_moves(d5))
        assert len(moves) == 1
        assert 'd5xe4' in map(str, moves)

        moves = list(board.figure_moves(e5))
        assert len(moves) == 1
        assert 'e5xd4' in map(str, moves)
        pass

    def test_transform(self):
        board = Board()
        board.init(PredefinedFENPosition('7n/P5P1/8/8/8/8/p5p1/7N'))

        # White
        a7 = board.figure_at(Position.from_char('a7'))
        moves = list(board.figure_moves(a7))
        assert len(moves) == 4, "White pawn can transform to 4 figures"

        move = next(filter(lambda x: isinstance(x.transform_to, Queen), moves))
        board.move(move)

        a8 = board.figure_at(Position.from_char('a8'))
        assert isinstance(a8, Queen) and a8.color == Player.WHITE
        assert board.figure_at(Position.from_char('a7')) is None

        g7 = board.figure_at(Position.from_char('g7'))
        moves = list(board.figure_moves(g7))
        assert len(moves) == 8
        move = next(filter(lambda x: isinstance(x.transform_to, Queen) and x.to_pos == Position.from_char('h8'), moves))
        board.move(move)
        h8 = board.figure_at(Position.from_char('h8'))
        assert isinstance(h8, Queen) and h8.color == Player.WHITE
        assert board.figure_at(Position.from_char('g7')) is None

        # Black
        a2 = board.figure_at(Position.from_char('a2'))
        moves = list(board.figure_moves(a2))
        assert len(moves) == 4, "White pawn can transform to 4 figures"

        move = next(filter(lambda x: isinstance(x.transform_to, Queen), moves))
        board.move(move)

        a1 = board.figure_at(Position.from_char('a1'))
        assert isinstance(a1, Queen) and a1.color == Player.BLACK
        assert board.figure_at(Position.from_char('a2')) is None

        g2 = board.figure_at(Position.from_char('g2'))
        moves = list(board.figure_moves(g2))
        assert len(moves) == 8
        move = next(filter(lambda x: isinstance(x.transform_to, Queen) and x.to_pos == Position.from_char('h1'), moves))
        board.move(move)
        h1 = board.figure_at(Position.from_char('h1'))
        assert isinstance(h1, Queen) and h1.color == Player.BLACK
        assert board.figure_at(Position.from_char('g2')) is None

    def test_passthrough_black(self):
        board = Board()
        board.init(EmptyPosition())

        p1 = Pawn(Player.WHITE, Position.from_char('e2'))
        p2 = Pawn(Player.BLACK, Position.from_char('f4'))

        board.put_figures([p1, p2])
        board.move(
            next(filter(
                lambda m: m.to_pos == Position.from_char('e4'),
                board.figure_moves(p1)
            ))
        )
        moves = list(board.figure_moves(p2))
        assert 'f4xe3' in list(map(str, moves)), "Take on passthrough must be available"

        move = next(filter(lambda m: str(m) == 'f4xe3', moves))
        board.move(move)
        assert len(list(board.figures)) == 1 and next(board.figures) == p2 \
               and str(p2.position) == 'e3', "Incorrect take on passthrough position"

        board.rollback()
        assert len(list(board.figures)) == 2 \
               and str(p2.position) == 'f4' and str(p1.position) == 'e4', "Incorrect take on passthrough rollback " \
                                                                          "position "
