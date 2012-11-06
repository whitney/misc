function getParam(key) {
	// taken from http://stackoverflow.com/a/901144
	key = key.replace(/[\[]/, "\\\[").replace(/[\]]/, "\\\]");
	var regexS = "[\\?&]" + key + "=([^&#]*)";
	var regex = new RegExp(regexS);
	var results = regex.exec(window.location.search);
	if(results == null)
		return "";
	else
		return decodeURIComponent(results[1].replace(/\+/g, " "));
}

function getGridDim(deflt) {
	var dimStr = getParam('dimension');
	return dimStr == "" ? deflt : parseInt(dimStr);
}

function scrambleImg() {
	var imgToTile = new Image();
	imgToTile.src = 'images/Skyline.png';
	imgToTile.onload = tileImg;
}

function tileImg(event) {
	var imgToTile = event.target;
	var scale = getGridDim(10);
	var tiledImage = new ImageHelper().sliceImageIntoTiles(imgToTile, new Coords(scale, scale));
	var scrambleDiv = document.getElementById('output');
	scrambleDiv.appendChild(tiledImage);    
}

function Coords(x, y) {
	this.x = x;
	this.y = y;    

	this.clone = function() {
		return new Coords(this.x, this.y);
	}

	this.divide = function(other) {
		this.x /= other.x;
		this.y /= other.y;

		return this;
	}

	this.multiply = function(other) {
		this.x *= other.x;
		this.y *= other.y;

		return this;
	}

	this.overwriteWith = function(other) {
		this.x = other.x;
		this.y = other.y;

		return this;
	}

	this.toString = function() {
		return "(" + this.x + "," + this.y + ")";
	}
}

function canvasPosnByTileIdx(randIdx, edgeTileCount, tileSize) {
	var x = (randIdx % edgeTileCount) * tileSize;
	var y = Math.floor(randIdx / edgeTileCount) * tileSize;
	return new Coords(x,y);
}

// returns a random int inclusive of both min and max
function getRandInt(min, max) {
	return Math.floor(Math.random() * (max - min + 1)) + min;
}

function ImageHelper() {
	this.sliceImageIntoTiles = function(imageToSlice, sizeInTiles) {
		var imageToSliceSize = new Coords(imageToSlice.width, imageToSlice.height);
		var tileSize = imageToSliceSize.clone().divide(sizeInTiles);

		var tilePos = new Coords(0, 0);
		var sourcePos = new Coords(0, 0);

		var canvas = document.createElement("canvas");
		canvas.id = "scambled";
		canvas.width = imageToSlice.width;
		canvas.height = imageToSlice.height;

		var ctx = canvas.getContext("2d");

		var numTiles = sizeInTiles.x*sizeInTiles.x;
		var tileIdxArray = [];
		for (var i = 0; i < numTiles; i++) {
			tileIdxArray[i] = i;
		}

		for (var y = 0; y < sizeInTiles.y; y++) {
			tilePos.y = y;

			for (var x = 0; x < sizeInTiles.x; x++) {                            
				tilePos.x = x;

				sourcePos.overwriteWith(tilePos).multiply(tileSize);

				var randIdx = getRandInt(0, tileIdxArray.length-1);
				var randTileIdx = tileIdxArray[randIdx];
				var destPos = canvasPosnByTileIdx(randTileIdx, sizeInTiles.x, tileSize.x);
				tileIdxArray.splice(randIdx,1);

				ctx.drawImage
					(
					 imageToSlice,
					 sourcePos.x, sourcePos.y, // source pos
					 tileSize.x, tileSize.y, // source size
					 destPos.x, destPos.y, // destination pos
					 tileSize.x, tileSize.y // destination size
					);
			}
		}

		// browser dependent?
		var imageFromCanvasURL = canvas.toDataURL("image/png");
		var imageFromCanvas = document.createElement("img");
		imageFromCanvas.width = canvas.width;
		imageFromCanvas.height = canvas.height;
		imageFromCanvas.src = imageFromCanvasURL;

		return imageFromCanvas;
	}
}

scrambleImg();
