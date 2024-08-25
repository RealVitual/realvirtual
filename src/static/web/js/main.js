// ****************************************** VAR GLOBALS ******************************************
const BODY = document.body,
 	OVERLAY = document.querySelector('.overlay'),
	HEADER = document.querySelector('header'),
 	CONTENTWRAPPER = document.querySelector('.contentWrapper'),
 	WRAPPER = document.querySelector('.wrapper');
	CONTENTWRAPPER.style.paddingTop = `${HEADER.offsetHeight}px`;

// ****************************************** SIDEBAR MOBILE ******************************************
// let elsidebarContentMobile = document.getElementsByClassName('sidebarContentMobile')[0];
// let elopenSidebarMobile = document.getElementsByClassName('openSidebarMobile')[0];
// let elheaderMenuWrap = document.getElementsByClassName('headerMenuWrap')[0].cloneNode(true);
// elsidebarContentMobile.appendChild(elheaderMenuWrap);
// elopenSidebarMobile.style.height = `${HEADER.offsetHeight}px`;
// ****************************************** EVENTS GLOBALS ******************************************
// Event media general
const eventMediaResize = (media,mediaYes,mediaNot) => {
	let windowMedia = window.matchMedia(`(max-width: ${media}px)`);
	let changeDesktopMobile = () => windowMedia.matches ? mediaYes() : mediaNot();
	windowMedia.addListener(changeDesktopMobile);
	changeDesktopMobile();
}
// ****************************************** EVENT CLICK TOGGLE GENERAL ********************************
const eventClickAccordion = (elementClick) => {
	let itemClickAccordion = document.getElementsByClassName(`${elementClick}`);
	for(let eventClickToggle of itemClickAccordion){
		eventClickToggle.nextElementSibling.style.transition = "all 400ms ease";
		eventClickToggle.nextElementSibling.style.overflow = 'hidden';
		if(eventClickToggle.dataset.colorInitial){
			let getColorInitial = eventClickToggle.dataset.colorInitial;
			let elChildrenCircle = eventClickToggle.children[0]
			elChildrenCircle.style.background = getColorInitial
		}
		const stateVisibility = (height,opacity,hidden) => {
			for(let eventClickToggle of itemClickAccordion){
				eventClickToggle.nextElementSibling.style.height = `${height}px`;
				eventClickToggle.nextElementSibling.style.opacity = opacity;
				eventClickToggle.nextElementSibling.style.visibility = `${hidden}`;
			}
			
		}
		stateVisibility(0,0,"hidden")
		eventClickToggle.addEventListener('click',function(e){
			e.preventDefault();
			let getHeightInfo = this.nextElementSibling.children[0].offsetHeight;
			if(!this.parentElement.classList.contains("active")){
				stateVisibility(0,0,"hidden")
				for(let eventClickToggle of itemClickAccordion) eventClickToggle.parentElement.classList.remove('active');
				for(let eventClickToggle of itemClickAccordion) eventClickToggle.classList.remove('active');
				this.parentElement.classList.add('active');
				this.classList.add('active')
				this.nextElementSibling.style.height = `${getHeightInfo}px`;
				this.nextElementSibling.style.opacity = 1;
				this.nextElementSibling.style.visibility = 'visible';
				for(let eventClickToggle of itemClickAccordion){
					if(eventClickToggle.dataset.colorInitial){
						let getColorInitial = eventClickToggle.dataset.colorInitial;
						let elChildrenCircle = eventClickToggle.children[0]
						elChildrenCircle.style.background = getColorInitial
					}
				}
				if(this.dataset.colorActive){
					let getColorActive = this.dataset.colorActive;
					let elChildrenCircle = this.children[0]
					elChildrenCircle.style.background = getColorActive
				}
			}else{
				this.parentElement.classList.remove('active');
				stateVisibility(0,0,"hidden")
				this.classList.remove('active')
				if(this.dataset.colorInitial){
					let getColorInitial = this.dataset.colorInitial;
					console.log(getColorInitial,'COLOR')
					let elChildrenCircle = this.children[0]
					elChildrenCircle.style.background = getColorInitial
				}
			}

			
		})
	}
	// itemClickAccordion[0].click()
}

// *********************************** EVENT CLICK ELEMENT OVERLAY ********************************
OVERLAY.addEventListener('click',function(e){
	e.preventDefault();
	// remove popup
	document.getElementsByClassName('videoYoutubePopup')[0]?.remove();
	document.getElementsByClassName('videoMp4Popup')[0]?.remove();
	document.getElementsByClassName('videoVimeoPopup')[0]?.remove();
	document.getElementsByClassName('closeVideoPopup')[0]?.remove();
	document.getElementsByClassName('videoPopupContent')[0]?.classList.remove('active');
	document.getElementsByClassName('formLogin')[0]?.classList.remove('active');
	document.getElementsByClassName('formRegistro')[0]?.classList.remove('active');
	document.getElementsByClassName("b4Popup")[0]?.classList.remove('active');
	document.getElementsByClassName('b16Popup')[0]?.classList.remove('active');
	document.getElementsByClassName('b19Popup')[0]?.classList.remove('active');
	BODY.classList.remove('noScroll');
	this.classList.remove('active');
	this.removeAttribute("style")
})

// *********************************** EVENT CLICK SHOW HIDE SIDEBAR ********************************
// elopenSidebarMobile.addEventListener('click',function(e){
// 	e.preventDefault();
// 	if(this.classList.contains('icon-menu')){
// 		this.classList.add('icon-close');
// 		this.classList.remove('icon-menu');
// 		BODY.classList.add('noScroll')
// 		elsidebarContentMobile.classList.add('active');
// 	}else{
// 		this.classList.remove('icon-close');
// 		this.classList.add('icon-menu');
// 		elsidebarContentMobile.classList.remove('active');
// 		BODY.classList.remove('noScroll')
// 	}
// })
// eventMediaResize(1024,()=>{
// 	elopenSidebarMobile.classList.remove('icon-close');
// 	elopenSidebarMobile.classList.add('icon-menu');
// 	elsidebarContentMobile.classList.remove('active');
// },()=>{});

// ****************************************** EVENT CLICK TOOGLE ******************************************
let elheaderMenuItem = document.getElementsByClassName('headerMenuItem')
// let eleventClickToggle = document.getElementsByClassName("eventClickToggle");
eventMediaResize(1024,()=>{
	// eventClickAccordion("eventClickToggle")
	// for(let eventClickToggle of eleventClickToggle){
	// 	eventClickToggle.classList.add('arrowClick')
	// }
},()=>{
	
	// for(let eventClickToggle of eleventClickToggle){
	// 	eventClickToggle?.nextElementSibling.removeAttribute('style');
	// 	eventClickToggle?.classList.remove('active');
	// 	eventClickToggle?.parentElement.classList.remove("active")
	// 	// eventClickToggle.classList.remove('arrowClick')
	// }
	// evento hover active overlay
	for(let headerMenuItem of elheaderMenuItem){
		if(headerMenuItem.classList.contains('hoverOverlay')){
			headerMenuItem.addEventListener('mouseover',function(){
				BODY.classList.add('noScroll');
				OVERLAY.classList.add('active');
				OVERLAY.style.zIndex = 90;
			});
			headerMenuItem.addEventListener('mouseleave',function(){
				BODY.classList.remove('noScroll');
				OVERLAY.classList.remove('active');
				OVERLAY.removeAttribute('style');
			});
		}
	}
});

// ****************************************** EVENT VIDEO CLICK ******************************************
let elclickVideo = document.getElementsByClassName('clickVideo');
let elvideoPopupContent = document.getElementsByClassName('videoPopupContent')[0];
for(const clickVideo of elclickVideo){
	clickVideo.addEventListener('click', function(e) {
		e.preventDefault();
		if(this.classList.contains("box")){
			let elCloseVideoBox = document.createElement("a");
			elCloseVideoBox.setAttribute("href","#")
			elCloseVideoBox.classList.add('closeVideoBox')
			elCloseVideoBox.classList.add('icon-close')
			elCloseVideoBox.addEventListener('click',function(e){
				e.preventDefault();
				this.nextElementSibling.remove();
				this.parentElement.classList.remove('active');
				this.remove();
			})
			this.parentElement.classList.add('active')
			this.parentElement.appendChild(elCloseVideoBox)
			let getUrlVideo = this.dataset.urlvideo;
			if(getUrlVideo.includes("youtube.")){
				let getIdVideo = this.dataset.urlvideo.split("=")[1];
				let elYoutube = document.createElement('iframe');
				elYoutube.classList.add('videoYoutube');
				this.parentElement.appendChild(elYoutube);
				elYoutube.src = `https://www.youtube.com/embed/${getIdVideo}?rel=0&amp;autoplay=1&mute=1`;
			}else{
				if(getUrlVideo.includes("vimeo.")){
					let getIdVideo = this.dataset.urlvideo.split("/")[3];
					let elVimeo = document.createElement('iframe');
					elVimeo.classList.add('videoVimeo');
					this.parentElement.appendChild(elVimeo);
					elVimeo.src = `https://player.vimeo.com/video/${getIdVideo}?autoplay=1&muted=1`;
				}else{
					let getUrlMp4 = this.dataset.urlvideo
					let elMp4 = document.createElement('video')
					elMp4.classList.add('videoVimeo');
					this.parentElement.appendChild(elMp4);
					elMp4.setAttribute('playsinline',"")
					elMp4.setAttribute('loop',"")
					elMp4.setAttribute('autoplay',"")
					elMp4.preload = "metadata";
					elMp4.setAttribute('src',getUrlMp4)
				}
			}
		}else{
			let getUrlVideoPopup = this.dataset.urlvideo;
			elvideoPopupContent.classList.add('active');
			OVERLAY.classList.add('active');
			OVERLAY.style.zIndex = 220;
			BODY.classList.add('noScroll');
			let elCloseVideoPopup = document.createElement("a");
			elCloseVideoPopup.setAttribute("href","#")
			elCloseVideoPopup.classList.add('closeVideoPopup')
			elCloseVideoPopup.classList.add('icon-close')
			elvideoPopupContent.appendChild(elCloseVideoPopup)
			elCloseVideoPopup.addEventListener('click',function(e){
				e.preventDefault();
				this.nextElementSibling.remove();
				this.parentElement.classList.remove('active');
				this.remove();
				OVERLAY.classList.remove('active');
				BODY.classList.remove('noScroll');
			})
			if(getUrlVideoPopup.includes('youtube.')){
				let getIdVideo = this.dataset.urlvideo.split("=")[1];
				let elYoutube = document.createElement('iframe');
				elYoutube.classList.add('videoYoutubePopup');
				elvideoPopupContent.appendChild(elYoutube);
				elYoutube.src = `https://www.youtube.com/embed/${getIdVideo}?rel=0&amp;autoplay=1&mute=1`;
			}else{
				if(getUrlVideoPopup.includes("vimeo.")){
					let getIdVideo = this.dataset.urlvideo.split("/")[3];
					let elVimeo = document.createElement('iframe');
					elVimeo.classList.add('videoVimeoPopup');
					elvideoPopupContent.appendChild(elVimeo);
					elVimeo.src = `https://player.vimeo.com/video/${getIdVideo}?autoplay=1&muted=1`;
				}else{
					let getUrlMp4 = this.dataset.urlvideo
					let elMp4 = document.createElement('video')
					elMp4.classList.add('videoMp4Popup')

					elvideoPopupContent.appendChild(elMp4);
					elMp4.setAttribute('playsinline',"")
					elMp4.setAttribute('loop',"")
					elMp4.setAttribute('autoplay',"")
					elMp4.preload = "metadata";
					elMp4.setAttribute('src',getUrlMp4)
					document.addEventListener('touchstart', function() {
						elMp4.play();
					});
				}
			}
		}
	})
}

// ****************************************** EVENT END VIDEO CLICK ************************************
// Event remover todas las clases de un grupo de items hermanos
const removeAllClassList = (element) => {
	for(const elementItem of element){
		elementItem.classList.remove('active')
	}
}

// **********************************************  EVENTO COPY TEXT  ***********************************
if(document.getElementsByClassName('copyText')[0]){
	let elcopyText = document.getElementsByClassName('copyText')
	for(const copyText of elcopyText){
		let eltextAlert = copyText.children[0]
		function myFunction() {
		    navigator.clipboard.writeText(copyText.dataset.textcopy);
		}
		copyText.addEventListener('click',function(e){
		    e.preventDefault();
		    myFunction()
		    eltextAlert.classList.add('active')
		    setTimeout(function(){
		        eltextAlert.classList.remove('active')
		    },1000)
		})
	}
	
}



// ****************************************** EVENT SCROLL WINDOW ********************************
// parametro1 => Bloque que se desea detectar
// parametro2 => porcentaje en referencial al alto de pantalla
// parametro3 => f1 es la funcion que entra al "if"
// parametro4 => f2 es la funcion que entra al "else"

const eventSCrollWindow = (block,porcent,f1,f2) => {
    if(document.getElementById(`${block}`)){
        let elBlock = document.getElementById(`${block}`).offsetTop;
        const eventDetected = () =>{
            let windowTop = window.scrollY + (window.innerHeight)/(100/porcent);
            windowTop > elBlock ? f1() : f2();
        }
        window.addEventListener('scroll',function(e) {
            eventDetected();
        })
        eventDetected();
    }
}

// ****************************************** EVENT CONTADOR ANIMATE GENERAL ********************************
// Paramatro 1 => Bloque que contiene a 1 o mas elementos contadores
// Paramatro 2 => Elemento qeu se animarà
// Parametro 3 => Tiempo de animacion , entero en segundos.

const eventCountAnimate = (block,el,time,sumNumber) => {
    if(document.getElementsByClassName(`${el}`)[0]){
        let elnumberCount = document.getElementsByClassName(`${el}`);
        let elBlock = document.getElementById(`${block}`);
        const countElements = () => {
            for(const elnumber of elnumberCount){
                let getNumber = parseInt(elnumber.dataset.num);
                let initial = sumNumber;
                let getTimeInterval = (time*1000)/getNumber
                setInterval(()=>{
                    if(initial <= getNumber){
                        elnumber.innerText = initial;
                        initial = initial + sumNumber;
                    }else{
                        let newSum = parseInt(elnumber.textContent) + 1;
                        newSum <= getNumber && (elnumber.innerText = newSum)
                    }
                },getTimeInterval)
            }
        }
        eventSCrollWindow(block,80,()=>{
            !elBlock.classList.contains('active') && countElements()
            elBlock.classList.add('active')
        },()=>{
    
        })
    }
}

// *******************************  PARA SWIPER JS  *******************************************
// document.addEventListener("visibilitychange", () => {
//     if (document.visibilityState === "visible") {
//         // restart animate progress
//     } else {
//        // stop animate progress
//     }
// })

//evento remover todas las clases de un listado
const eventRemoveClassAllList = (element,nameClass) => {
	for(const elementItem of element){
		elementItem.classList.remove(`${nameClass}`)
	}
}

// ****************************************** EVENT TAB GENERAL ********************************
// parametro1 => element clikeable
// parametro2 => elemento que se actualiza al click
// parametro3 => evento que se usara para la accion sobre el tab
const eventTab = (elTab,elInfo,nameEvent) => {
    let el1 = document.getElementsByClassName(`${elTab}`);
    let el2 = document.getElementsByClassName(`${elInfo}`);
    for(let i=0; i<el1.length; i++){
        el1[i].setAttribute('data-id',`data-${i}`);
        el1[i].addEventListener(`${nameEvent}`,function(e){
            e.preventDefault();
            eventRemoveClassAllList(el1,"active")
            this.classList.add('active')
            let getId = this.dataset.id;
            for(let j=0; j<el2.length; j++){
                let getTab = el2[j].dataset.tab
                if(getId === getTab){
                    eventRemoveClassAllList(el2,"active")
                    el2[j].classList.add('active')
                }
            }
        })
    }
    for(let j=0; j<el2.length; j++){
        el2[j].setAttribute('data-tab',`data-${j}`);
    }
    // si el evento es "click" que se ejecute el click automatico al primero elemento
    nameEvent == "click" && el1[0].click()
}


window.addEventListener("scroll", function(){
	if(window.scrollY > HEADER.offsetHeight){
		BODY.classList.add('scrolling')
	}else{
		BODY.classList.remove('scrolling')
	}
})

// ******************************* EVENTO GRILLA *****************************+**
const eventGrilla = (el,pos) => {
	const detectedPos = () => {
		let elheaderLogo = document.getElementsByClassName("headerLeft")[0].offsetLeft;
		let elBlock = document.getElementsByClassName(`${el}`)[0]
		if(pos === "left"){
			elBlock.style.paddingLeft = `${elheaderLogo}px`;
		}else{
			elBlock.style.paddingRight = `${elheaderLogo}px`;
		}
	}
	detectedPos()
	window.addEventListener("resize",function(){
		detectedPos();
	})
}

const eventScrollAnimate = (porcentHeight) => {
	if(document.getElementsByClassName('scrollWrap')[0]){
		let elScrollWrap = document.getElementsByClassName('scrollWrap')
		const detectedScrollActive = () => {
			let windowTop = window.scrollY + window.innerHeight/porcentHeight;
			for(const scrollWrap of elScrollWrap){
				let elScrollWrapTop = scrollWrap.offsetTop;
				if(windowTop > elScrollWrapTop){
					scrollWrap.classList.add('activeScroll')
					let elScrollItem = scrollWrap.getElementsByClassName('scrollItem')
					let countItems = elScrollItem.length
					for(var i = 0; i < elScrollItem.length; i++){
						let elScrollItemTop = window.scrollY + elScrollItem[i].getBoundingClientRect().top;
						if(windowTop > elScrollItemTop){
							elScrollItem[i].classList.add('activeScroll');
							if(!elScrollItem[i].classList.contains('noDelay')){
								elScrollItem[i].style.transitionDelay = `${0.05*(i+1)}s`;
							}
						}
					}
				}
			}
		}
		window.onload = function() {
			detectedScrollActive()
		};
		
		window.addEventListener('scroll',function(){
			detectedScrollActive()
		})
	}
}
eventScrollAnimate(1.1)

$(document).ready(function(){
	if($('.g7WrapBx').length > 0){
		for(let i = 0; i < $('.g7WrapBx').length; i++){
			$('.g7WrapBx').eq(i).addClass(`bxSlider-${i}`)
			let cantItemsVisible = parseInt($('.g7WrapBx').eq(i).attr('data-items-visible'))
			let countItemsBxWrap = $('.g7WrapBx').eq(i).children().length
			if(countItemsBxWrap > cantItemsVisible){
				$('.g7WrapBx').eq(i).addClass('bxSliderActive')
				$('.g7WrapBx').eq(i).removeClass('noBxSlider')
				$(`.bxSlider-${i}`).bxSlider({
					infiniteLoop: true,
					slideWidth: 'auto',
					responsive:true,
					ticker: true,
					speed: countItemsBxWrap*800,
					slideMargin: 'auto',
				});
			}else{
				if($(window).width() < 1025){
					$('.g7WrapBx').eq(i).addClass('bxSliderActive')
					$('.g7WrapBx').eq(i).removeClass('noBxSlider')
					$(`.bxSlider-${i}`).bxSlider({
						infiniteLoop: true,
						slideWidth: 'auto',
						responsive:true,
						ticker: true,
						speed: countItemsBxWrap*800,
						slideMargin: 'auto',
					}); 
				}else{
					$('.g7WrapBx').eq(i).addClass('noBxSlider')
					$('.g7WrapBx').eq(i).removeClass('bxSliderActive')
				}
			}

		}
	}
})

// Eventos POPUP - login - registro

if(document.getElementsByClassName('headerButtonLogin')[0] || document.getElementsByClassName('headerButtonRegistrate')[0]){
	let elformLogin = document.getElementsByClassName('formLogin')[0];
	let elformRegistro = document.getElementsByClassName('formRegistro')[0];
	let elHeaderButtonLogin = document.getElementsByClassName('headerButtonLogin')[0];
	let elHeaderButtonRegistrate = document.getElementsByClassName('headerButtonRegistrate')[0];
	// let elg8ClosePopup = document.getElementsByClassName('g8ClosePopup')

	elHeaderButtonLogin.addEventListener('click', function(e){
		e.preventDefault();
		elformLogin.classList.add('active')
		OVERLAY.classList.add('active')
		OVERLAY.style.zIndex = "500"
	});

	// for(const g8ClosePopup of elg8ClosePopup){
	// 	g8ClosePopup.addEventListener('click', function(e){
	// 		e.preventDefault();
	// 		this.parentNode.classList.remove('active')
	// 		OVERLAY.classList.remove('active')
	// 	});
	// }
	elHeaderButtonRegistrate.addEventListener('click', function(e){
		e.preventDefault();
		elformRegistro.classList.add('active')
		OVERLAY.classList.add('active')
		OVERLAY.style.zIndex = "500"
	});

	if(document.getElementById("openRegistrarme")){
		let elopenRegistrarme = document.getElementById("openRegistrarme");
		elopenRegistrarme.addEventListener('click',function(e){
			e.preventDefault();
			document.getElementsByClassName("closeIniciaSesion")[0].click();
			elHeaderButtonRegistrate.click()
		});
	}
	if(document.getElementById("openIniciaSesion")){
		let elopenIniciaSesion = document.getElementById("openIniciaSesion");
		elopenIniciaSesion.addEventListener('click',function(e){
			e.preventDefault();
			document.getElementsByClassName("closeRegistro")[0].click();
			elHeaderButtonLogin.click()
		});
	}
}

if(document.getElementsByClassName("headerAnclaBlock")[0]){
	document.querySelectorAll('.headerAnclaBlock').forEach(function(element) {
		element.addEventListener('click', function(event) {
			var pathname = location.pathname.replace(/^\//,'');
			var hash = this.hash.slice(1);
			if (pathname == this.pathname.replace(/^\//,'') && location.hostname == this.hostname) {
				var target = document.getElementById(hash);
				var headerAnclaBlocks = document.querySelectorAll('.headerAnclaBlock');
				headerAnclaBlocks.forEach(function(block) {
					block.classList.remove('active');
				});
				this.classList.add('active');
				var target = target || document.querySelector('[name=' + hash + ']');
				if (target) {
					var marginTop = parseInt(window.getComputedStyle(target).marginTop, 10);
					var targetOffset = target.getBoundingClientRect().top + window.pageYOffset - (marginTop || 0) - HEADER.offsetHeight;
					
					window.scrollTo({
						top: targetOffset,
						behavior: 'smooth'
					});
					event.preventDefault();
				}
			}
		});
	});
	
	window.addEventListener('scroll', function() {
		const topWindow = window.scrollY + window.innerHeight / 2;
		document.querySelectorAll('.anclaBlock').forEach(anclaBlock => {
			const targetOffset = anclaBlock.offsetTop;
			const headerAnclaBlock = document.querySelector(`.headerAnclaBlock[href="#${anclaBlock.id}"]`);
			if (topWindow > targetOffset) {
				document.querySelectorAll('.headerAnclaBlock').forEach(header => header.classList.remove('active'));
				headerAnclaBlock && headerAnclaBlock.classList.add('active');
			}
		});
	});
}



// if (localStorage.getItem('selectedItems') && document.getElementsByClassName("headerEventos")[0]) {
// 	const storedItems = JSON.parse(localStorage.getItem('selectedItems'));
// 	document.getElementById('total-count').innerText = storedItems.length;
// }



// if(document.getElementsByClassName("agregarCalendario")[0]){
// 	const items = document.querySelectorAll('.agregarCalendario');
// 	const totalCountDisplay = document.getElementById('total-count');
// 	let totalCount = 0;
// 	const selectedItems = new Set();

// 	// Cargar el estado inicial desde localStorage
// 	if (localStorage.getItem('selectedItems')) {
// 		const storedItems = JSON.parse(localStorage.getItem('selectedItems'));
// 		storedItems.forEach(itemId => {
// 			const item = document.querySelector(`.agregarCalendario[data-item-id="${itemId}"]`);
// 			if (item) {
// 				item.classList.add('selected');
// 				selectedItems.add(itemId);
// 				item.children[0].textContent = "Agendado";
// 			}
// 		});
// 		totalCount = selectedItems.size;
// 		updateTotalCountDisplay();
// 	}

// 	items.forEach(item => {
// 		item.addEventListener('click', function(e) {
// 			e.preventDefault()
// 			const itemId = this.getAttribute('data-item-id');
// 			if (selectedItems.has(itemId)) {
// 				selectedItems.delete(itemId);
// 				this.classList.remove('selected');
// 				this.children[0].textContent = "Agendar";
// 				totalCount--;
// 			} else {
// 				selectedItems.add(itemId);
// 				this.classList.add('selected');
// 				this.children[0].textContent = "Agendado";
// 				totalCount++;
// 			}
// 			updateTotalCountDisplay();
// 			saveToLocalStorage();
// 		});
// 	});

// 	function updateTotalCountDisplay() {
// 		totalCountDisplay.textContent = totalCount;
// 	}

// 	function saveToLocalStorage() {
// 		localStorage.setItem('selectedItems', JSON.stringify(Array.from(selectedItems)));
// 	}
// }


if(document.getElementsByClassName("show-hide-pass")[0]){
	let elShowHiddePass = document.getElementsByClassName("show-hide-pass")
	for(const ShowHiddePass of elShowHiddePass){
		ShowHiddePass.addEventListener('click',function(e){
			e.preventDefault();
			if(!this.classList.contains('active')){
				this.classList.add('active')
				this.previousElementSibling.setAttribute('type','text')
			}else{
				this.classList.remove('active')
				this.previousElementSibling.setAttribute('type','password')
			}
			
		})
	}
}