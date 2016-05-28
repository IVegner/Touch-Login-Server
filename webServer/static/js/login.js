$(document).ready(function() {
	$("#touchLoginButton").click(function(){

		var count = 0;
		ellipsisAnimation = setInterval(function(){		//start the ellipsis animation
			count++;
			var dots = new Array(count % 10).join('.');
			$('#authStatusMessage').text("Sending auth request to linked iPhone." + dots);
		}, 1000);

		var username = $("#username").val();

		$.ajax({
			url:"https://touch-login.appspot.com/_ah/api/touchloginAPI/v1/AuthenticateUser",
			type:"POST",
			data: JSON.stringify({ username: username, origin: window.location.hostname }),
			contentType:"application/json; charset=utf-8",
			dataType:"json",
			success: function(data){
				
				clearInterval(ellipsisAnimation);
				//alert(parseInt(data["authStatusCode"])*2);
				var code = parseInt(data["authStatusCode"]);
				// if (code == 4){
				// 	$("#authStatusMessage").text("Request timed out.");
				// }
				switch(code){
					case 0:
						$("#authStatusMessage").text("Authenticated!");
						break;

					case 1:
						$("#authStatusMessage").text("Invalid username, please try again.");
						break;

					case 2:
						$("#authStatusMessage").text("Weird error, please try again.");
						break;

					case 3:
						$("#authStatusMessage").text("Weird error, please try again.");
						break;

					case 4: 
						$("#authStatusMessage").text("Request timed out.");
						break;

					default:
						$("#authStatusMessage").text("Humph.");
						break;
				}
			}
		})
		alert("hi");
		$("#touchLoginStatus").show(300);
		$(".tabbed").hide();
	});
});