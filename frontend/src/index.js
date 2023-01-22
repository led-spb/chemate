import 'chess-merida-font/css/chessmerida-webfont.css'
import App from './app.js'

// FONT LOADING DETECTION CODE:
var canvas = document.createElement('canvas');
var ctx = canvas.getContext('2d');
ctx.font = 'normal 20px ChessMerida';

var isFontLoaded = false;
var TEXT_TEXT = 'Some test text;';
var initialMeasure = ctx.measureText(TEXT_TEXT);
var initialWidth = initialMeasure.width;

function whenFontIsLoaded(callback, attemptCount) {
  if (attemptCount === undefined) {
    attemptCount = 0;
  }
  if (attemptCount >= 20) {
    callback();
    return;
  }
  if (isFontLoaded) {
    callback();
    return;
  }
  const metrics = ctx.measureText(TEXT_TEXT);
  const width = metrics.width;
  if (width !== initialWidth) {
    isFontLoaded = true;
    callback();
  } else {
    setTimeout(function () {
      whenFontIsLoaded(callback, attemptCount + 1);
    }, 1000);
  }
}

whenFontIsLoaded(function () {
  App.run()
});
