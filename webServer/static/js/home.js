$(document).ready(function() {
	console.log("loaded");
	//Email grabber pop-up
	var waypoint = new Waypoint({
	  element: $('#whenIsLaunch'),
	  handler: function() {
	  	var modal = $("#email-modal");
	    modal.modal();
	    waypoint.disable();

	    //And now for fixing some weird and confusing bugs in HTML/CSS'
	    console.log("fired1");
	    modal.css({"padding-right": ""});
	  },
	  offset: "50%"
	})

	// Transparent Navbar when above fold
	window.onscroll = function() {
		console.log("fire2");
		if (document.body.scrollTop < $(window).height()*2/3){		//This is for the transparent navbar
			$("#custom-navbar.navbar-default").addClass("transparent-navbar");
		} else {
			console.log("fired.")
			$("#custom-navbar.navbar-default").removeClass("transparent-navbar");
		}
  		window.scroll(0, window.pageYOffset);	//nasty workaround, try disabling and see white margin on the right
	}

	// Smooth anchor scrolling
	$('a[href^="#"]').on('click',function (e) {
		e.preventDefault();

		var target = this.hash;
		var $target = $(target);

		$('html, body').stop().animate({
			'scrollTop': $target.offset().top - 100
		}, 900, 'swing', function () {
			window.location.hash = target;
		});
	});
});
