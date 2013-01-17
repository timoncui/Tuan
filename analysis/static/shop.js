// @author Lixing Huang
// @date 1/14/2013

// global variables
g_selected_city = null;
g_selected_shop = null;
g_max_days = 30;
g_cache_dat = null;

// google table api
g_shop_table = null;
function loadShopList(city_name) {
	var ww = $("#shop_box").width();
	if (city_name == null) {
		var shop_data = new google.visualization.DataTable();
		shop_data.addRows(0);
		shop_data.addColumn("string", "商店名");
		g_shop_table.draw(shop_data, {showRowNumber:true, height:"700px", width:ww});
	} else {
		$.post(
			base_url + "shop",
			"type=shoplist&city=" + city_name,
			function(dat) {
				var shop_data = new google.visualization.DataTable();
				shop_data.addColumn("string", "商店名");
				shop_data.addRows(dat.length);
				for (i=0; i<dat.length; ++i) {
					shop_data.setCell(i, 0, dat[i]);
				}
				if (g_shop_table == null) {
					g_shop_table = new google.visualization.Table(document.getElementById('shop_box'));
					google.visualization.events.addListener(g_shop_table, 'select', function(){
						var selection = g_shop_table.getSelection();
						if (selection.length == 0) {
							g_selected_shop = null;
						} else if (selection.length > 1) {
							alert("抱歉，目前只能选择一个商店");
							g_selected_shop = null;
						} else {
							g_selected_shop = shop_data.getFormattedValue(selection[0].row, 0);
						}
					});
				}
				g_shop_table.draw(shop_data, {showRowNumber:true, height:"700px", width:ww});
			},
			"json"
		);
	}
}

function loadCityList() {
	$.post(
		base_url + "dealnum",
		"type=citylist",
		function(dat) {
			var city_data = new google.visualization.DataTable();
			city_data.addColumn("string", "城市名");
			city_data.addRows(dat.length);
			for (i=0; i<dat.length; i++) {
				city_data.setCell(i, 0, dat[i]);
			}
			var city_table = new google.visualization.Table(document.getElementById('city_box'));
			city_table.draw(city_data, {showRowNumber:true, height:"700px", width:$("#city_box").width()});

			google.visualization.events.addListener(city_table, 'select', function(){
				var selection = city_table.getSelection();
				if (selection.length == 0) {
					g_selected_city = null;
				} else if (selection.length > 1) {
					alert("抱歉，目前只能选择一个城市");
					g_selected_city = null;
				} else {
					g_selected_city = city_data.getFormattedValue(selection[0].row, 0);
				}
				loadShopList(g_selected_city);
			});
		},
		"json"
	)
}

google.load('visualization', '1', {packages:['table']});
google.setOnLoadCallback(function(){
	loadCityList()
});

// data visualization
function constructXLabels(y, m, d, vn) {
	var x_labels = [];
	var days_of_month = [];
	if (isLeapYear(y)) {
		days_of_month = [0,31,29,31,30,31,30,31,31,30,31,30,31];
	} else {
		days_of_month = [0,31,28,31,30,31,30,31,31,30,31,30,31];
	}
	for (var i=0; i<vn; ++i) {
		if (d > days_of_month[m]) {
			d=1;
			m++;
		}
		x_labels.push(d);
		d++;
	}
	return x_labels;
}
function constructYLabels(dat, accumulate_y) {
	var y_labels= [];
	var min_num = 100000000;
	var max_num = 0;

	for (key in dat) {
		var total = 0;
		var n = dat[key][2];  // sales number
		for (i=0; i<n.length; ++i) {
			var nn = parseInt(n[i]);
			if (nn < min_num)
				min_num = nn;
			if (nn > max_num)
				max_num = nn;
			total = total + nn;
		}
		if (accumulate_y) {
			if (total > max_num)
				max_num = total;
		}
	}

	var hn_max = 10;
	var interval_set = [1,2,5,10,20,50,100,200,500,1000,2000,5000,10000,20000,50000,100000,200000,500000,1000000];
	var selected_interval = 0;
	// the max value can be (hn+1)*interval. hn is the number of horizontal lines.
	// find the best interval.
	for (i=0; i<interval_set.length; ++i) {
		if (max_num/interval_set[i]-1 <= hn_max) {
			selected_interval = interval_set[i];
			break;
		}
	}
	var hn = 1;
	while (true) {
		y_labels.push(hn*selected_interval);
		hn++;
		if (hn*selected_interval > max_num)
			break;
	}
	return y_labels;
}
function draw(dat, accumulate_y) {
	var beg = $("#starttime").val();
	beg = parse_date(beg, "-");

	removeLabels();
	removePlots();
	removeGrids();

	var xlabels = constructXLabels(beg[0], beg[1], beg[2], g_max_days);
	var ylabels = constructYLabels(dat, accumulate_y);
	drawTimeGrid(ylabels.length, xlabels.length);
	drawXLabel(xlabels);
	drawYLabel(ylabels);

	var prev = decr_date(beg[0], beg[1], beg[2]);
	prev.push(0); // add hour
	for (key in dat) {
		var x = [];
		var y = [];
		var t = dat[key][0];
		var n = dat[key][2];
		for (i=0; i<t.length; ++i) {
			var curr = parse_date_hour(t[i], "_");
			if (curr == null)
				continue;
			var hours = hours_between(curr, prev);
			x.push(hours);

			var num = parseInt(n[i]);
			if (isNaN(num)) {
				x.splice(x.length-1, 1);  // get rid of the just inserted x
				continue;
			}
			if (accumulate_y) {
				y.push( (y.length==0) ? num : (y[y.length-1]+num) );
			} else {
				y.push(num);
			}
		}
		_drawline(key, x, y, xlabels, ylabels);
	}
}

// data interaction
function validate_dates(starttime, endtime) {
	var beg = parse_date(starttime, "-");
	var end = parse_date(endtime, "-");
	if (beg == null || end == null)
		return false;
	if (compare_date(beg, end) > 0)
		return false;

	var num_of_days = 1;
	while (num_of_days <= g_max_days) {
		beg = incr_date(beg[0], beg[1], beg[2]);
		if (compare_date(beg, end) > 0) {
			break;
		}
		++num_of_days;
	}
	if (num_of_days <= g_max_days)
		return true;
	else
		return false;
}
function query() {
	if (g_selected_city == null || g_selected_shop == null) {
		return;
	}

	var starttime = $("#starttime").val();
	var endtime = $("#endtime").val()
	if (!validate_dates(starttime, endtime)) {
		alert("合法的日期格式:2012-1-5, 我们目前最多只能显示一个月的数据.");
		return;
	}

	$.post(
		base_url + "shop",
		"type=num&city=" + g_selected_city + "&shop=" + g_selected_shop + "&beg=" + starttime + "&end=" + endtime,
		function(dat) {
			if (isObjEmpty(dat)) {
				return;
			}
			g_cache_dat = dat;
			draw(dat, true);
			// check the source selector
			$("input:checkbox").attr("disabled", "disabled").removeAttr("checked");
			for (var key in dat) {
				$("#" + key).attr("checked", "checked").removeAttr("disabled");
			}
		},
		"json"
	);
}

// entry point
$(document).ready(function(){
	// get current date
	var date = new Date();
	var y = date.getFullYear();
	var m = date.getMonth() + 1;
	var d = date.getDate();
	$("#starttime").val("2012-12-30");
	$("#endtime").val(y+"-"+m+"-"+d);

	// prepare the canvas
	var w = $("#canvas").width();
	var h = $("#canvas").height();
	createPaper("canvas", w, h);

	// register events
	$("#search").click(function(){
		query();
	});

	// disable check box
	$("input:checkbox").change(function(evt){
		var tmp = {};
		var checked = $("#source_box input:checked");
		for (i=0; i<checked.length; ++i) {
			var src = $(checked[i]).attr("id");
			if (g_cache_dat[src]) {
				tmp[src] = g_cache_dat[src];
			}
		}
		draw(tmp, true);
	});
});








