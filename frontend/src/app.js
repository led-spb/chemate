import Konva from 'konva'
import utils from './utils'
const axios = require('axios')


export default {
    cellSize: 64,
    container: 'container',
    board: null,
    current: 'w',
    player: 'w',
    history: [],

    run(){
        console.log('Chemate is started')

        this.stage = new Konva.Stage({
             container: this.container,
             width: this.cellSize*8, height: this.cellSize*8,
        })

        this.figuresLayer = new Konva.Layer()
        this.boardLayer = new Konva.Layer()
        this.initBoard()

        this.stage.add(this.boardLayer)
        this.stage.add(this.figuresLayer)

        document.getElementById('rollback').onclick=() => { this.rollback() }
        document.getElementById('new').onclick=() => { this.new_game() }
        this.new_game()
    },

    makeFigures(){
        this.figuresLayer.destroyChildren()
        for(const fig of utils.fenFigures(this.board)){
            const figure = this.makeFigure(fig.position.x, fig.position.y, fig.figure)
            this.figuresLayer.add(figure)
        }
        this.clearAllSelection()
    },

    getCellById(id){
        return this.boardLayer.findOne('#'+id)
    },

    clearAllSelection(){
        for(const cell of this.boardLayer.getChildren()){
            this.clearSelection(cell)
        }
    },

    clearSelection(cell){
        cell.cache()
        cell.filters([])
    },

    setSelection(cell){
        cell.cache()
        cell.filters([Konva.Filters.RGBA])
        cell.green(200)
    },

    makeFigure(x, y, type){
        const char = "kqrbnplwtvmo".charAt("KQRBNPkqrbnp".indexOf(type))
        const offset = 0
        const figure = new Konva.Text({
            x: x*this.cellSize, y: (7-y)*this.cellSize+offset,
            fontSize: this.cellSize,
            text:char, fill: 'black', fontFamily: 'ChessMerida',
            verticalAlign: 'top',
            id: utils.positionStr(x, y)
        })

        figure.on('click', (event)=> {
            this.onCellClick(event.target)
        })
        return figure
    },

    parseResponse(data){
        this.board = data.board
        this.makeFigures()
        this.current = this.board.split(' ')[1]
        if( this.current == this.player){
            this.valid_moves = data.valid_moves
        }else{
            this.valid_moves = []
        }

        this.history.push({board: this.board, valid_moves: this.valid_moves})
    },

    makeMove(move){
        console.log('Make move', move[2])
        axios.post('api/game/move', {board: this.board, move: move}).then( (response) => {
            this.parseResponse(response.data)
            if(this.current != this.player){
                axios.post('/api/game/calc', {board: this.board}).then( (response) => {
                    this.parseResponse(response.data)
                })
            }
        })
    },

    rollback(){
        if( this.history.length < 3)
           return
        this.history.pop()
        this.history.pop()
        const state = this.history.pop()
        console.log('Rollback move', this.history, state)
        this.parseResponse(state)
    },

    new_game(){
        this.history = []
        axios.get('api/game/new')
            .then((response) => { this.parseResponse(response.data) })
    },

    onCellClick(cell){
        const pos = cell.id()
        this.clearAllSelection()

        for(const move of this.valid_moves){
            if( move[0] == pos ){
                this.from_pos = pos
                this.setSelection(this.getCellById(move[0]))
                this.setSelection(this.getCellById(move[1]))
            }
            if( this.from_pos==move[0] && move[1] == pos){
                this.makeMove(move)
                return
            }
        }
    },

    initBoard(){
        for(let y=0; y<8; y++){
            for(let x=0; x<8; x++){
                let cell = new Konva.Rect({
                    x: x*this.cellSize, y: y*this.cellSize, width: this.cellSize, height: this.cellSize,
                    fill: (x+y%2) %2 ? 'gray' : 'white', stroke: 'black', strokeWidth: 1,
                    id: utils.positionStr(x, (7-y))
                })
                cell.on('click', (event) => {
                    this.onCellClick(event.target)
                })
                this.boardLayer.add(cell)
            }
        }
    }
}