$(function(){
/* BASE */

	/* FECHA FOOTER */
	var fecha = new Date();
	var ano =fecha.getFullYear();
	$('#id_year').text(ano)

	/* MENU RESPONSIVE */
	//se clona 'menu-list' para poder tener mas flexibilidad y control
	$('.h1-logo-2').clone().appendTo('.menu-sidebar-cnt').addClass('resp-logo').removeClass('h1-logo-2').removeClass('h1-logo');
	$('.menu-list').clone().appendTo('.menu-sidebar-cnt').addClass('menu-responsive').removeClass('menu-list-1');
	$('.footer-menu ul li').clone().appendTo('.menu-responsive');
	$('.clone-contacto ul li:last-child').clone().appendTo('.menu-responsive');
	$('.clone-menu').clone().appendTo('.menu-sidebar-cnt').addClass('menu-toggle-resp').removeClass('footer-item').removeClass('clone-contacto').removeClass('clone-menu');
	$('.h2-btn').clone().appendTo('.menu-sidebar-cnt');
	$('.h1-languaje').clone().appendTo('.menu-sidebar-cnt');
	$('.h2-iconos').clone().appendTo('.menu-sidebar-cnt');


	$('.menu-mobile-open').click(function(){
		$(this).addClass('active');
		$('.menu-mobile-close').addClass('active');
		$('.menu-sidebar').addClass('active');
		$('.menu-overlay').addClass('active');
		$('.cnt-wrapper').addClass('active');
		$('.footer').addClass('active');
		$('body').addClass('active');
	});

	// funcion  para cerrar menu responsive
	function cerrar_nav() {
		$('.menu-sidebar').removeClass('active');
		$('.menu-overlay').removeClass('active');
		$('.menu-mobile-close').removeClass('active');
		$('.menu-mobile-open').removeClass('active');
		$('.cnt-wrapper').removeClass('active');
		$('.footer').removeClass('active');
		$('body').removeClass('active');
	};

	//click en boton cerrar y overlay
	$('.menu-mobile-close').click(function() {
		cerrar_nav();
	});

	$('.menu-overlay').click(function() {
		cerrar_nav();
	});


	//para cerrar el menu responsive en caso hagan resize, o giren la tablet o celular con el menu responsive abierto
		//detectando moviendo de ipad y tablet
	function readDeviceOrientation() {
	    switch (window.orientation) {
	    case 0:
	        break;
	    case 180:
	        break;
	    case -90:
	        break;
	    case 90:
	        break;
	    }
	}
	//detectando tablet, celular o ipad
	dispositivo_movil = $.browser.device = (/android|webos|iphone|ipad|ipod|blackberry|iemobile|opera mini/i.test(navigator.userAgent.toLowerCase()))

	if ( dispositivo_movil ) {
			function readDeviceOrientation() {
			    if (Math.abs(window.orientation) === 90) {
			        // Landscape
			      	cerrar_nav();
			    } else {
			    	// Portrait
			    	cerrar_nav();
			    }
			}
			window.onorientationchange = readDeviceOrientation;
	}else{
		$(window).resize(function(event) {
			var estadomenu = $('.menu-responsive').width();
			if(estadomenu != 0){
				cerrar_nav();
			}
		});
	};
	//Detectando navegador
		$.browser.chrome = /chrome/.test(navigator.userAgent.toLowerCase());

		/* Detect Chrome */
		if($.browser.chrome){
			/* Do something for Chrome at this point */
			// alert("You are using Chrome!");

			/* Finally, if it is Chrome then jQuery thinks it's
			   Safari so we have to tell it isn't */
			$.browser.safari = false;
		}

		/* Detect Safari */
		if($.browser.safari){
			/* Do something for Safari */
			// alert("You are using Safari!");
		}






	// Ancla scroll - AGREGAR CLASE DEL ENLACE
	$('.miclase[href*=#]').click(function() {
	if(location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'')&& location.hostname == this.hostname) {
			var $target = $(this.hash);
			$target = $target.length && $target || $('[name=' + this.hash.slice(1) +']');
			if ($target.length) {
			var targetOffset = $target.offset().top;
			$('html,body').animate({scrollTop: targetOffset}, 1000);
			return false;
			}
		}
	});

	// Reseteando cajas de texto administrables
	$('.no-style *').removeAttr('style');


	// Menu responsive traslucido con scrolling
	var altoScroll = 0
	$(window).scroll(function() {
		altoScroll = $(window).scrollTop();
		if (altoScroll > 0) {
			$('.header-home .header').addClass('active');
		}else{
			$('.header-home .header').removeClass('active');
		};
	});


	// controlar los placeholde
	$('input, textarea').placeholder();

/* --- FIN BASE --- */
});

// +++ inicio languaje hover +++
function languaje_hover(){
	$('.h1-languaje li:nth-child(1)').hover(function() {
		$('.h1-languaje').addClass('borde-1');
	}, function() {
		$('.h1-languaje').removeClass('borde-1');
	});
	$('.h1-languaje li:nth-child(2)').hover(function() {
		$('.h1-languaje').addClass('bordes');
	}, function() {
		$('.h1-languaje').removeClass('bordes');
	});
	$('.h1-languaje li:nth-child(3)').hover(function() {
		$('.h1-languaje').addClass('borde-2');
	}, function() {
		$('.h1-languaje').removeClass('borde-2');
	});
}
// +++ final languaje hover +++

// +++ inicio - languaje active +++
function languaje_active(){
	var languaje_li_1 = $('.h1-languaje li:nth-child(1).active');
	if (languaje_li_1.hasClass('active')) {
		$('.h1-languaje li:nth-child(1)').addClass('delet-borde1');
		// console.log("tiene active");
	}
	var languaje_li_2 = $('.h1-languaje li:nth-child(2).active');
	if (languaje_li_2.hasClass('active')) {
		$('.h1-languaje li:nth-child(1)').addClass('delet-borde1');
		$('.h1-languaje li:nth-child(2)').addClass('delet-borde1');
		// console.log("tiene active");
	}
	var languaje_li_3 = $('.h1-languaje li:nth-child(3).active');
	if (languaje_li_3.hasClass('active')) {
		$('.h1-languaje li:nth-child(2)').addClass('delet-borde1');
		// console.log("tiene active");
	}
}


// +++ inicio - efecto menu desplegable +++
function h_open_menu(){
	$('.header').addClass('header-color');
	$('.header-home .header').removeClass('header-color').addClass('home-color-desplegable');
	$('.header-desplegable').addClass('active');
	$('.header-overlay').addClass('active');
	$('.h1-openDesplegable').addClass('active');
	$('.h1-closeDesplegable').addClass('active');
}
function h_close_menu(){
	$('.header').removeClass('header-color') ;
	$('.header-home .header').removeClass('home-color-desplegable');
	$('.header-desplegable').removeClass('active');
	$('.header-overlay').removeClass('active');
	$('.h1-closeDesplegable').removeClass('active');
	$('.h1-openDesplegable').removeClass('active');
}
// +++ final - efecto menu desplegable +++

// +++ inicio - acordión menu responsive +++
var menu_resp_toggle = $('.openToggleResp.active');
if (menu_resp_toggle.hasClass('active')) {
	$('.desplegableResp').hide();
	menu_resp_toggle.closest('.openToggleResp').find('.desplegableResp').show();
};
// +++ final - acordión menu responsive +++

$(function(){
	// +++ inicio - acordión menu responsive +++
	$('.openToggleResp').click(function(event){
		if ($(this).hasClass('active')) {
			$(this).removeClass('active').parent().find('.desplegableResp').stop().slideUp();
		}else{
			$('.openToggleResp').removeClass('active');
			$('.desplegableResp').stop().slideUp();
			$(this).addClass('active').parent().find('.desplegableResp').stop().slideToggle();
		};
	});
	// +++ final - acordión menu responsive +++


	// +++ inicio languaje hover +++
	var h_calc_ancho = $(window).width()
	if (h_calc_ancho > 1007) {
		languaje_hover();
		// console.log(h_calc_ancho, "cumple condicional");
	}
	// +++ final languaje hover +++


	// inicio - condicional si tiene active - languaje
	languaje_active();
	// inicio - condicional si tiene active - languaje


	// +++ inicio - efecto menu desplegable +++
	$('.h1-openDesplegable').click(function(event) {
		h_open_menu();
	});

	$('.h1-closeDesplegable, .header-overlay').click(function(event) {
		h_close_menu();
	});
	// +++ final - efecto menu desplegable +++


	$(window).resize(function(event) {
	// +++ inicio languaje hover +++
		languaje_hover();
	// +++ final languaje hover +++
	});
});
