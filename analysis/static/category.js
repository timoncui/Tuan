// @author Lixing Huang
// @date 1/16/2013

g_category_table = null;
g_bar_chart = null;

function clear() {
	// clear the table
	if (g_category_table) {
		var w = $("#cat_box").width();
		var cat_data = new google.visualization.DataTable();
		cat_data.addColumn('string', '团购种类');
		cat_data.addColumn('number', '数量');
		cat_data.addRows(0);
		g_category_table.draw(cat_data, {showRowNumber:true, height:"700px", width:w});
	}

	// clear the chart
	if (g_bar_chart)
		g_bar_chart.clearChart();
}

function drawChart(dat) {
	var arrayData = [];
	for (var key in dat) {
		arrayData.push([key, dat[key]]);
	}
	arrayData.sort(function(a,b) {return b[1]-a[1]});
	var chartData = [["种类", "数量"]];
	for (var i=0; i<30; ++i) {
		if (i>=arrayData.length)
			break;
		chartData.push(arrayData[i]);
	}
	var options = {
		title: "团购种类分布",
		vAxis: {title: "种类", titleTextStyle: {color:'black'}},
	};
	if (g_bar_chart == null)
		g_bar_chart = new google.visualization.BarChart(document.getElementById('canvas'));
	g_bar_chart.draw(google.visualization.arrayToDataTable(chartData), options);
}

function constructCategoryTable(dat) {
	var w = $("#cat_box").width();
	var sz = objSize(dat);
	var cat_data = new google.visualization.DataTable();
	cat_data.addColumn('string', '团购种类');
	cat_data.addColumn('number', '数量');
	cat_data.addRows(sz);
	var row_index = 0;
	for (var key in dat) {
		cat_data.setCell(row_index, 0, key);
		cat_data.setCell(row_index, 1, dat[key]);
		row_index++;
	}

	if (g_category_table == null) {
		g_category_table = new google.visualization.Table(document.getElementById('cat_box'));
	}
	g_category_table.draw(cat_data, {showRowNumber:true, height:"700px", width:w});
}

function loadCategory(source) {
	$.post(
		base_url + "category",
		"source=" + source,
		function(dat) {
			if (isObjEmpty(dat)) {
				clear();
				return;
			}
			constructCategoryTable(dat);
			drawChart(dat);
		},
		"json"
	);
}

function loadSources() {
	var w = $("#source_box").width();
	var sources = ["嘀嗒", "大众点评", "F团", "拉手", "满座", "美团", "糯米", "窝窝", "58"];
	var source_ids = ["dida", "dianping", "ftuan", "lashou", "manzuo", "meituan", "nuomi", "wowo", "wuba"];
	var source_data = new google.visualization.DataTable();
	source_data.addColumn('string', '团购网站');
	source_data.addRows(sources.length);
	for (var i=0; i<sources.length; ++i) {
		source_data.setCell(i, 0, sources[i]);
	}
	var source_table = new google.visualization.Table(document.getElementById('source_box'));
	source_table.draw(source_data, {showRowNumber:true, height:"700px", width:w});
	google.visualization.events.addListener(source_table, 'select', function(){
		var selection = source_table.getSelection();
		if (selection.length == 0) {
			clear();
		} else if (selection.length > 1) {
			clear();
			alert("抱歉，目前只能选择一个团购网站");
		} else {
			var selected_source = source_data.getFormattedValue(selection[0].row, 0);
			var selected_index = 0;
			for (; selected_index<sources.length; selected_index++) {
				if (sources[selected_index] == selected_source)
					break;
			}
			loadCategory(source_ids[selected_index]);
		}
	});
}

google.load('visualization', '1', {packages:['table', 'corechart']});
google.setOnLoadCallback(function(){
	loadSources();
});

// entry point
$(document).ready(function(){

});