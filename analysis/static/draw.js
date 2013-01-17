// @author Lixing Huang
// @date 1/14/2013

g_paper = null;
g_paper_grids = [];
g_paper_plots = [];

/////////////////////
// data visualization
function createPaper(pid, w, h) {
	var p = Raphael(document.getElementById(pid), w, h);
	g_paper = {"p":p, "w":w, "h":h};
}
function removeLabels() {
	$("#paper span").remove();
}
function removeGrids() {
	for (var i=0; i<g_paper_grids.length; ++i) {
		g_paper_grids[i].remove();
	}
	g_paper_grids.splice(0, g_paper_grids.length);
}
function removePlots() {
	for (var i=0; i<g_paper_plots.length; ++i) {
		g_paper_plots[i].remove();
	}
	g_paper_plots.splice(0, g_paper_plots.length);
}
function drawTimeGrid(hn, vn) {
	// draw horizontal
	var interval = g_paper["h"] / (hn+1);
	for (i=1; i<=hn; i++) {
		var str = "M0,"+(interval*i)+"L"+g_paper["w"]+","+(interval*i);
		var line = g_paper["p"].path(str).attr({"stroke-dasharray":"-.","stroke":"#DDD"});
		g_paper_grids.push(line);
	}
	// draw vertical
	interval = g_paper["w"] / (vn+1);
	for (i=1; i<=vn; i++) {
		var str = "M"+(interval*i)+",0L"+(interval*i)+","+g_paper["h"];
		var line = g_paper["p"].path(str).attr({"stroke-dasharray":"-.","stroke":"#DDD"});
		g_paper_grids.push(line);
	}
}
function drawXLabel(xs) {
	// input is an array
	var startx = $("#canvas").position().left;
	var starty = $("#canvas").position().top + $("#canvas").height();
	var interval = g_paper["w"] / (xs.length+1);
	
	var left_gap = 0;
	for (i=1; i<=xs.length; i++) {
		if (xs[i-1] < 10)
			left_gap = 0;
		else
			left_gap = 2;
		var lt = $("<span>").text(xs[i-1]).css({
			"position":"absolute", "left":startx+(i*interval)-left_gap, "top":starty+10, "font-size":"12px", "font-style":"italic",
		});
		$("#paper").append(lt);
	}
}
function drawYLabel(ys) {
	// input is an array
	var startx = $("#canvas").position().left + $("#canvas").width();
	var starty = $("#canvas").position().top;
	var interval = g_paper["h"] / (ys.length+1);

	for (i=1; i<=ys.length; i++) {
		var lt = $("<span>").text(ys[ys.length-i]).css({
			"position":"absolute", "left":startx+16, "top":starty+(i*interval), "font-size":"12px", "font-style":"italic",
		});
		$("#paper").append(lt);
	}
}

function _drawline(source, x, y, xlabels, ylabels) {
	var max_x = (xlabels.length+1) * 24;  // in hours
	var min_x = 0;
	var max_y = (ylabels[1]-ylabels[0]) + ylabels[ylabels.length-1];
	var min_y = 0;
	var w = $("#canvas").width();
	var h = $("#canvas").height();

	var first_point = true;
	var str = "M";
	for (i=0; i<x.length; ++i) {
		var xx = (x[i]-min_x)/(max_x-min_x) * w;
		var yy = h - (y[i]-min_y)/(max_y-min_y) * h;
		var cc = g_paper["p"].circle(xx, yy, 3).attr({"stroke":g_palette[source]});
		if (first_point) {
			str = str + xx + "," + yy;
			first_point = false;
		} else {
			str = str + "L" + xx + "," + yy;
		}
		g_paper_plots.push(cc);
	}
	var l = g_paper["p"].path(str).attr({"stroke":g_palette[source],"stroke-width":"3"});
	g_paper_plots.push(l);
}


