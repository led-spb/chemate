export default {
    fenFigures: function* (data){
        let y = 7
        for(const row of data.split(' ').shift().split('/')){
            let x = 0
            for(const c of row){
                if( isNaN(Number.parseInt(c)) ){
                    yield { position: {x: x, y: y}, figure: c}
                    x++
                }else{
                    x += Number.parseInt(c)
                }
            }
            y--
        }
    }
}
