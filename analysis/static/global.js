var base_url = "http://localhost:8483/"

var g_palette = {
	'dida':'#0066cc', 'dianping':'#ff6600', 'ftuan':'#83b34d',
	'lashou':'#eb4800', 'manzuo':'#dff1fe', 'meituan':'#0a9e9d',
	'nuomi':'#ec3a6a', 'wowo':'#ff8000', 'wuba':'#d95f00',
};

function isObjEmpty(obj) {
	for (var key in obj) {
		if (hasOwnProperty.call(obj, key))
			return false;
	}
	return true;
}


function isLeapYear(y) {
	if (y%400 == 0)
		return true;
	else if (y%100 == 0)
		return false;
	else if (y%4 == 0)
		return true;
	else
		return false;
}
function decr_date(y, m, d) {
	var days_of_month = [];
	if (isLeapYear(y)) {
		days_of_month = [0,31,29,31,30,31,30,31,31,30,31,30,31];
	} else {
		days_of_month = [0,31,28,31,30,31,30,31,31,30,31,30,31];
	}
	if (d-1 > 0) {
		return [y, m, d-1];
	} else if (m-1 > 0) {
		return [y, m-1, days_of_month[m-1]];
	} else {
		return [y-1, 12, 31];
	}
}
function incr_date(y, m, d) {
	var days_of_month = [];
	if (isLeapYear(y)) {
		days_of_month = [0,31,29,31,30,31,30,31,31,30,31,30,31];
	} else {
		days_of_month = [0,31,28,31,30,31,30,31,31,30,31,30,31];
	}
	if (d+1 <= days_of_month[m]) {
		return [y, m, d+1];
	} else if (m <= 11) {
		return [y, m+1, 1];
	} else {
		return [y+1, 1, 1];
	}
}
function parse_date(date, sep) {
	var tokens = $.trim(date).split(sep);
	if (tokens.length != 3)
		return null;
	var y = parseInt(tokens[0]);
	var m = parseInt(tokens[1]);
	var d = parseInt(tokens[2]);
	if (isNaN(y) || isNaN(m) || isNaN(d))
		return null;
	if (y>=2010 && (m>=1&&m<=12) && (d>=1&&d<=31)) {
		days_of_month = [];
		if (isLeapYear(y)) {
			days_of_month = [0,31,29,31,30,31,30,31,31,30,31,30,31];
		} else {
			days_of_month = [0,31,28,31,30,31,30,31,31,30,31,30,31];
		}
		if (d<=days_of_month[m]) {
			return [y,m,d]
		}
	}
	return null;
}
// parse 2012-12-31-7
// date + hour
function parse_date_hour(date, sep) {
	var tokens = $.trim(date).split(sep);
	if (tokens.length != 4)
		return null;
	var y = parseInt(tokens[0]);
	var m = parseInt(tokens[1]);
	var d = parseInt(tokens[2]);
	var h = parseInt(tokens[3]);
	if (isNaN(y) || isNaN(m) || isNaN(d) || isNaN(h))
		return null;
	if (y>=2010 && (m>=1&&m<=12) && (d>=1&&d<=31) && (h>=0&&h<=23)) {
		days_of_month = [];
		if (isLeapYear(y)) {
			days_of_month = [0,31,29,31,30,31,30,31,31,30,31,30,31];
		} else {
			days_of_month = [0,31,28,31,30,31,30,31,31,30,31,30,31];
		}
		if (d<=days_of_month[m]) {
			return [y,m,d,h]
		}
	}
	return null;
}
// time1 and time2 are two arrays, [y,m,d,h]
function hours_between(time1, time2) {
	var date1 = new Date(time1[0], time1[1], time1[2], time1[3], 0, 0, 0);
	var date2 = new Date(time2[0], time2[1], time2[2], time2[3], 0, 0, 0);
	var one_hour = 1000*60*60;
	var hours = (date1.getTime() - date2.getTime()) / one_hour;
	return hours;
}
// compare two dates, [y,m,d]
function compare_date(date1, date2) {
	if (date1[0]<date2[0] || (date1[0]==date2[0] && date1[1]<date2[1]) || (date1[0]==date2[0] && date1[1]==date2[1] && date1[2]<date2[2]))
		return -1;
	else if (date1[0]==date2[0] && date1[1]==date2[1] && date1[2]==date2[2])
		return 0;
	else
		return 1;
}
