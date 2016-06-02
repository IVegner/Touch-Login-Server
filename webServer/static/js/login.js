$(document).ready(function() {
	$("#touchLoginForm").validate({
		debug:true,
		rules:{
			username:"required"
		},
		highlight: function(element) {
			$(element).closest('.form-group').addClass('has-error');
		},
		unhighlight: function(element) {
			$(element).closest('.form-group').removeClass('has-error');
		},
		errorElement: 'span',
		errorClass: 'help-block',
		errorPlacement: function(error, element) {
			if(element.parent('.input-group').length) {
				error.insertAfter(element.parent());
			} else {
				error.insertAfter(element);
			}
		}
	});

	$("#touchLoginForm").removeData("unobtrusiveValidation");

	$("#touchLoginForm").submit(function(){
		if($("#touchLoginForm").valid()){
			var message = "Pending"
			var count = 0;
			ellipsisAnimation = setInterval(function(){		//start the ellipsis animation
				count++;
				var dots = new Array(count % 10).join('.');
				$('#authStatusMessage').text(message+dots);
			}, 1000);

			var username = $("#username").val();
			var next = $("#next").val();
			var clid = $("#clid").val();

			$("#touchLoginStatus").show(300);
			$(".tabbed").hide();

			console.log("Request sent.")
			$.ajax({
				url:"/login/",
				type:"POST",
				data: JSON.stringify({ username: username, next: next, clid: clid }),
				contentType:"application/json; charset=utf-8",
				dataType:"json",
				success: function(data){
					console.log(data);
					var code = parseInt(data["authStatusCode"]);
					if (code == 0){	//success, redirect.
						window.location.href = data["returnMessage"];
					}
					else { //Some error or timeout
						location.reload();
					}
				}
			})
		}
	});
});

function checkStatus(username, next, clid){

}






// // if (code == 4){
// // 	$("#authStatusMessage").text("Request timed out.");
// // }
// switch(code){
// 	case 0:
// 		$("#authStatusMessage").text("Authenticated!");
// 		break;

// 	case 1:
// 		$("#authStatusMessage").text("Invalid username, please try again.");
// 		break;

// 	case 2:
// 		$("#authStatusMessage").text("Weird error, please try again.");
// 		break;

// 	case 3:
// 		$("#authStatusMessage").text("Weird error, please try again.");
// 		break;

// 	case 4: 
// 		$("#authStatusMessage").text("Request timed out.");
// 		break;

// 	default:
// 		$("#authStatusMessage").text("Humph.");
// 		break;