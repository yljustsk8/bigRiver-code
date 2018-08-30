function show(personnelId) {
$("#AttendanceDataDetailDiv").show();//显示日历
$("#AttendanceDataDetailDiv").createDialogFun();
var year = $("#YearSelect").val();//年
var month = $("#MonthSelect").val();//月
showDate(year, month);//加载日历
//根据员工的编号查询员工在当期月份的考勤信息放在日历上
ShowAttendanceDateFun(personnelId);
}

var NumDay = "", //一个月有多少天
Week = "", //这个月第一天是星期几
ldate = "", //日期行数
iHtmlNow = ""; //日历结构

//显示日历
function showDate(year, month) {
//获得当前月的第一天是星期一
getlWeek(year, month);

creatHtml();//创建HTML结构


}

//创建日期行 l:行
function creatTr(l) {
$("#CalendarTab tbody").empty();
var lstrTd = ""; //行的DOM结构
for (var i = 0; i < l; i++) {
lstrTd += "<tr style='height:90px;'><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>";
}
$("#CalendarTab tbody").append(lstrTd);

insertdate(Week);
}

//获得当前月的第一天是星期一
function getlWeek(nowYear, nowMonth) {
$("#CalendarMonthDiv span").html("");
var date = nowMonth + "/" + "1/" + nowYear; //此处也可以写成 17/07/2014 一样识别
var day = new Date(Date.parse(date)); //需要正则转换的则 此处为 ： var day = new Date(Date.parse(date.replace(/-/g, '/')));
Week = day.getDay();//获取星期
var monthArray = ["一", "二", "三", "四", "五", "六", "七", "八", "九", "十", "十一", "十二"];
$("#CalendarMonthDiv span").html(monthArray[nowMonth - 1]);
getTdDay(nowMonth, nowYear);//根据大小月份取得天数
}


////根据大小月份取得天数
//function getTdDay(m1, y1) {
// NumDay = new Date(y1, m1, 0).getDate();
//}
//根据大小月份取得天数
function getTdDay(m1, y1) {
if (m1 == 1 || m1 == 3 || m1 == 5 || m1 == 7 || m1 == 8 || m1 == 10 || m1 == 12) {
NumDay = 31;
} else if (m1 == 4 || m1 == 6 || m1 == 9 || m1 == 11) {
NumDay = 30;
} else if (m1 == 2 && isRunYear(y1)) {
NumDay = 29;
} else if (m1 == 2) {
NumDay = 28;
}
}

//根据传入的年份参数，判断是否是润年，即能够被4整除，但不能被100整除，同时满足时；或者能被400整除；
function isRunYear(y) {
if (y % 4 == 0 && y % 100 != 0) {
return true;
} else if (y % 400 == 0) {
return true;
} else {
return false;
}
}

//创建HMTL结构
function creatHtml() {
//根据当前月份的一号是星期几，来生成有几行存放所有日期
if (Week >= 5) {
ldate = 6;
} else {
ldate = 5;
}
creatTr(ldate);

}

//将日期插入到对应的TD当中 d:当前月的第一天是星期几
function insertdate(d) {
//$("#CalendarTab tbody td").add($(".nextDate table tbody td")).css({ "background-color": "", "color": "" }).empty();
//插入到左边
for (var i = 0; i < NumDay; i++) {
$("#CalendarTab tbody td").eq(i + d).html(i + 1);
$("#CalendarTab tbody td").eq(i + d).append($("<div style='background-color:white;'>"));
}
}



//根据员工的编号查询员工在当期月份的考勤信息放在日历上
function ShowAttendanceDateFun(personnelId) {
$.ajax({
    type: "POST",
    contentType: "application/json",
    //返回给后端日期格式：{userID:'xxx',year:'xxxx',month:'xx'}
    data: "{userID:'" + userID + "',year:" + $("#YearSelect").val() + ",month:" + $("#MonthSelect").val() + "}",
    dataType: "json",
    url: "/AttendanceDataManager/GetAttendanceById",
    success: function (r) {
    if (r != null && r.Data != null) {
    for (var i = 0; i < r.Data.length; i++) {
    var date = dayFormatter(r.Data[i].AttendanceDay);
    $("#CalendarTab tbody td").each(function () {
    if ($(this).text() == date) {
        $(this).find("div").css("width", "97px");
        var content = "";
        if (r.Data[i].AttendanceType == "正常") {
        content = r.Data[i].AttendanceType + "<br/>" + "打卡:" + (r.Data[i].OnDutyTime == null ? "" : r.Data[i].OnDutyTime) + "-" + (r.Data[i].OffDutyTime == null ? "" : r.Data[i].OffDutyTime);
        }
        else if (r.Data[i].AttendanceType == "迟到") {
        $(this).css("background-color", "#FFE5E6");
        content = r.Data[i].AttendanceType + ":" + r.Data[i].LaterMinutes + "分<br/>" + "打卡:" + (r.Data[i].OnDutyTime == null ? "" : r.Data[i].OnDutyTime) + "-" + (r.Data[i].OffDutyTime == null ? "" : r.Data[i].OffDutyTime);
        }
        else if (r.Data[i].AttendanceType == "早退") {
        $(this).css("background-color", "#E1EEC2");
        content = r.Data[i].AttendanceType + ":" + r.Data[i].EarlyMinutes + "分<br/>" + "打卡:" + (r.Data[i].OnDutyTime == null ? "" : r.Data[i].OnDutyTime) + "-" + (r.Data[i].OffDutyTime == null ? "" : r.Data[i].OffDutyTime);
        }
        else if (r.Data[i].AttendanceType == "迟到早退") {
        $(this).css("background-color", "red");
        content ="迟到:" + r.Data[i].LaterMinutes +"分<br/>早退:"+ r.Data[i].EarlyMinutes + "分<br/>" + "打卡:" + (r.Data[i].OnDutyTime) + "-" + (r.Data[i].OffDutyTime == null ? "" : r.Data[i].OffDutyTime);
        }
        else if (r.Data[i].AttendanceType == "") {
        //content = r.Data[i].AttendanceType + "<br/>" + "打卡：" + (r.Data[i].OnDutyTime == null ? "" : r.Data[i].OnDutyTime) + "-" + (r.Data[i].OffDutyTime == null ? "" : r.Data[i].OffDutyTime);
        content = "";
        }
    else {
    $(this).css("background-color", "#FBCA4A");
    content = r.Data[i].AttendanceType + "<br/>" + (r.Data[i].AttendanceType=='未打下班卡'?("打卡:"+r.Data[i].OnDutyTime):"");
    }
    $(this).find("div").html(content);
    }
});
}
}
}
});
}