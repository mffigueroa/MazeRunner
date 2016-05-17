// Function to set gaps
var setGaps = function() {
	var gaps = new Array();
	var template = [0, Math.PI * (10/180), Math.PI * (20/180), Math.PI * (25/180), Math.PI * (30/180), Math.PI * (15/180), Math.PI * (25/180)];

	for(var i = 0; i < template.length; i++) {
		var gapRow = new Array();
		var count = 4;

		for(var j = 0; j < count; j++) {
			switch(j) {
				case 0:
					gapRow.push(template[i]);
					break;
				case 1:
					gapRow.push((Math.PI/2) + template[i]);
					break;
				case 2:
					gapRow.push(Math.PI + template[i]);
					break;
				case 3:
					gapRow.push(((3 * Math.PI)/2) + template[i]);
					break;
			}
		}

		gaps.push(gapRow);
	}

	return gaps;
}

// Get window width and height, their smallest dimension, and their center point
var windowWidth = window.innerWidth;
var windowHeight = window.innerHeight;
var smallestDimension = Math.min(windowWidth, windowHeight);
var screenCenter = [windowWidth/2, windowHeight/2];

console.log("Dimensions: (" + windowWidth + ", " + windowHeight + ")");

// Set gaps
var openingGap = 12 * Math.PI/180;
var gaps = setGaps();