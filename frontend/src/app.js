import Konva from 'konva'
import utils from './utils'


export default {
    cellSize: 64,
    container: 'container',

    run: function() {
        console.log('Chemate is started')

        this.stage = new Konva.Stage({
             container: this.container,
             width: this.cellSize*8, height: this.cellSize*8,
        })

        this.figuresLayer = new Konva.Layer()
        this.boardLayer = new Konva.Layer()
        this.initBoard()

        let data = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
        for(const fig of utils.fenFigures(data)){
            const figure = this.makeFigure(fig.position.x, fig.position.y, fig.figure)
            this.figuresLayer.add(figure)
        }
        this.stage.add(this.boardLayer)
        this.stage.add(this.figuresLayer)
    },

    makeFigure(x, y, type){
        let char = String.fromCharCode("KQRBNPkqrbnp".indexOf(type)+9812)

        let figure = new Konva.Text({
           x: x*this.cellSize, y: (7-y)*this.cellSize+8,
           fontSize: this.cellSize, text:char, fill: 'black', fontFamily: 'ChessMerida'
        })
        return figure
    },

    initBoard: function(){
        for(let y=0; y<8; y++){
            for(let x=0; x<8; x++){
                let cell = new Konva.Rect({
                    x: x*this.cellSize, y: y*this.cellSize, width: this.cellSize, height: this.cellSize,
                    fill: (x+y%2) %2 ? 'gray' : 'white', stroke: 'black', strokeWidth: 1
                })
                this.boardLayer.add(cell)
            }
        }
    }
}