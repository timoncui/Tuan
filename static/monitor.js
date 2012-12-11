
var base_url = "http://localhost:8483/"

function populate_list(source, dat) {
	$container = $("#" + source + " div");
	for (i = 0; i < dat.length; ++i) {
		$container.append(
			$("<span>").text(dat[i]).css({
				"width":"30%",
				"margin":"10px",
				"padding":"2 2 2 2",
				"border":"1px solid #CCC",
				"-webkit-border-radius":"3px",
			}).mouseover(function(){
				$(this).css('cursor', 'pointer');
			}).mouseout(function(){
				$(this).css('cursor', 'auto');
			}).click(function(evt){
				$mouse_x = evt.pageX;
				$mouse_y = evt.pageY;
				$date = $(this).text();
				$.post(
					base_url,
					"src=" + source + "&date=" + $date,
					function(dat) {
						if (dat.error) {
							alert(dat.error);
						} else {
							success_array = dat.success;
							failure_array = dat.failure;
							total_evt = dat.total;
							dat_description = "";
							for (i = 0; i < success_array.length; ++i) {
								dat_description = dat_description + "<span>" + success_array[i] + "</span><br/>";
							}
							for (i = 0; i < failure_array.length; ++i) {
								dat_description = dat_description + "<span style='color:red'>" + failure_array[i] + "</span><br/>";
							}
							$('#info').html(
								dat_description
							).show().css({
								"left":$mouse_x + 5,
								"top":$mouse_y + 5,
							});
						}
					},
					"json"
				)
			})
		);
		if (i % 3 == 2) {
			$container.append( $("<div>").css("margin", "10px 0px 10px 0px") );
		}
	}
}

function fetch_log_list(source) {
	$.post(
		base_url,
		"src=" + source,
		function(dat) {
			populate_list(source, dat);
		},
		"json"
	);
}

$(document).ready(function(){
	sources = [
		"dida",
		"dianping",
		"ftuan",
		"lashou",
		"manzuo",
		"meituan",
		"nuomi",
		"wowo",
		"wuba",
	];
	for (i = 0; i < sources.length; ++i) {
		fetch_log_list( sources[i] );
	}

	$("body").click(function(){
		$("#info").hide();
	});
});




