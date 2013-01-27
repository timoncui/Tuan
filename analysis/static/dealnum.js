// @author Lixing Huang
// @date 1/3/2013

// global variables
g_selected_city = null;
g_max_days = 30;

// google table api
function loadCityList() {
	$.post(
		base_url + "dealnum",
		"type=citylist",
		function(dat) {
			var ww = $("#city_box").width();
			var city_data = new google.visualization.DataTable();
			city_data.addColumn("string", "城市名");
			city_data.addRows(dat.length + 1);
			city_data.setCell(0, 0, "全部");
			for (i=0; i<dat.length; i++) {
				city_data.setCell(i+1, 0, dat[i]);
			}
			var city_table = new google.visualization.Table(document.getElementById('city_box'));
			city_table.draw(city_data, {showRowNumber:true, height:"700px", width:ww});
			// preselect city
			city_table.setSelection([{row:3, column:null}]);
			g_selected_city = city_data.getFormattedValue(city_table.getSelection()[0].row, 0);
			google.visualization.events.addListener(city_table, 'select', function(){
				var selection = city_table.getSelection();
				if (selection.length == 0) {
					g_selected_city = null;
				} else if (selection.length > 1) {
					alert("抱歉，目前只能选择一个城市");
					g_selected_city = null;
				} else {
					if (selection[0].row == 0) {
						g_selected_city = "total";
					} else {
						g_selected_city = city_data.getFormattedValue(selection[0].row, 0);
					}
				}
			});
		},
		"json"
	)
}

google.load('visualization', '1', {packages:['table']});
google.setOnLoadCallback(function(){
	loadCityList()
});

/////////////////////////////
// data visualization
// x is fixed. display one month day.
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
// y is dynamic. adjust based on the max value.
function constructYLabels(dat, accumulate_y) {
	var y_labels= [];
	var min_num = 100000000;
	var max_num = 0;
	for (key in dat) {
		var total = 0;
		var n = dat[key][1];
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
	var interval_set = [50,100,200,500,1000,2000,5000,10000,20000,50000,100000,500000,1000000,5000000,10000000,20000000,50000000,100000000];
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
		var n = dat[key][1];
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

///////////////////
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
	// selected city
	if (g_selected_city == null)
		return;
	// selected deal source
	$sources = "";
	$checked = $("#source_box input:checked");
	for (i=0; i<$checked.length; i++) {
		$sources = $sources + $($checked[i]).attr("id") + ",";
	}
	if ($sources == "")
		return;
	// selected date
	var starttime = $("#starttime").val();
	var endtime = $("#endtime").val()
	if (!validate_dates(starttime, endtime)) {
		alert("合法的日期格式:2012-1-5, 我们目前最多只能显示一个月的数据.");
		return;
	}

	page = $("#search").attr("page");
	$.post(
		base_url + page,
		"type=num&city=" + g_selected_city + "&src=" + $sources + "&beg=" + starttime + "&end=" + endtime,
		function(dat) {
			if (isObjEmpty(dat)) {
				return;
			}
			// for current design:
			// dat is a hash table, key is source, value is an array with two arrays as elements; the first array is
			// date description, and the second array is deal number
			if (page == 'dealnum')
				draw(dat, false);
			else if (page == 'sales')
				draw(dat, true);
		},
		"json"
	);
}

///////////////////
// entry point
$(document).ready(function(){
	// get current date
	var date = new Date();
	var y = date.getFullYear();
	var m = date.getMonth() + 1;
	var d = date.getDate();
	$("#starttime").val("2012-12-30");
	$("#endtime").val(y+"-"+m+"-"+d);

	// check meituan
	$("#meituan").attr("checked", "checked");

	// prepare the canvas
	var w = $("#canvas").width();
	var h = $("#canvas").height();
	createPaper("canvas", w, h);

	// register events
	$("#search").click(function(){
		query();
	});
});