//B2-Animacion
var b3_animation = $('#b2-animacion');
b3_animation.waypoint(function(direction) {
	if (direction === 'down') {
		$('.b2').addClass('active');
	}
}, {
	offset:'85%'
});

//b15 animacion
var b15_anima = $('#b15-anima');
b15_anima.waypoint(function(direction) {
	if (direction === 'down') {
		$('.b15').addClass('active');
	}
}, {
	offset:'30%'
});

// b6
	var b6_anima = $('#b6-anima');
	b6_anima.waypoint(function(direction) {
		if (direction === 'down') {
			$('.b6').addClass('active');
		}
	}, {
		offset:'70%'
	});
	// end b6

	//bloque #b11 animacion
	var b11_anima = $('#b11-anima');
	b11_anima.waypoint(function(direction) {
		if (direction === 'down') {
			$('.b11').addClass('active');
		}
	}, {
		offset:'30%'
	});
	// end b11
