import flask
from flask.views import MethodView
from flask_smorest import Blueprint

from chemate.board import Board
from chemate.decision import DecisionTree
from chemate.positions import InitialPosition, PredefinedFENPosition
from chemate.utils import FENExporter

blueprint = Blueprint('items', __name__)


@blueprint.route('/api/game/new')
class GameNewApi(MethodView):
    @blueprint.response(200)
    def get(self):
        board = Board()
        board.init(InitialPosition())
        return {'board': board.export(FENExporter),
                'balance': board.balance,
                'valid_moves': list(map(str, board.valid_moves(board.current)))
                }


@blueprint.route('/api/game/moves')
class GameMoveApi(MethodView):
    @blueprint.response(200)
    def post(self):
        board = Board()
        board.init(PredefinedFENPosition(flask.request.json.get("board")))
        return {'board': board.export(FENExporter),
                'balance': board.balance,
                'valid_moves': list(map(str, board.valid_moves(board.current)))
                }


@blueprint.route('/api/game/calc')
class BoardCalcApi(MethodView):
    @blueprint.response(200)
    def post(self):
        board = Board()
        board.init(PredefinedFENPosition(flask.request.json.get("board")))

        decision = DecisionTree(4)
        move, score, variants = decision.best_move(board)
        board.move(move)

        return {'move': str(move),
                'board': board.export(FENExporter),
                'balance': board.balance,
                'score': score,
                'variants': variants,
                'valid_modes':  list(map(str, board.valid_moves(board.current)))
                }
