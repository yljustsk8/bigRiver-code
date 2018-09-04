//本地模拟已签到日期天数
    var localDate = {
        date: []
    }
    localDate.date.push("0901");localDate.date.push("0912");localDate.date.push("0908");
    localDate.date.push("0913");localDate.date.push("0905");localDate.date.push("0906");
    /**
    for (var j = 0; j < 30; j++) {
        var a = Math.ceil(Math.random() * 11);
        if (a < 10) {
            a = "0" + a;
        }

        var b = Math.ceil(Math.random() * 30);
        if (b < 10) {
            b = "0" + b;
        }

        var c = a.toString() + b.toString();
        localDate.date.push(c);
    }*/

    //初始化日期数据
    var slidate = new Date();
    var m = slidate.getMonth() + 1;
    var x = slidate.getMonth() + 1;
    var n = slidate.getMonth();
    var monthFirst = new Date(slidate.getFullYear(), parseInt(n), 1).getDay(); //获取当月的1日等于星期几
    var d = new Date(slidate.getFullYear(), parseInt(m), 0); //获取月
    var conter = d.getDate(); //获取当前月的天数
    var monthNum = "0" + (slidate.getMonth() + 1) + "月";
    var yearNum = slidate.getFullYear() +"年";
    var monthCheck = (slidate.getMonth() + 1);
    var y = slidate.getDate();

    function initall() {
        dateHandler(monthFirst, d, conter, monthNum);
        checkDate(monthCheck);
    }

    /**调整表格行数，并把每个用到的td加上内容&赋予id*/
    function dateHandler(monthFirst, d, conter, monthNum) {
        var blank = true;
        var $tbody = $('#tbody'), //日历网格
            $month = $("#month"),  //“09月”
            _nullnei = '';
        var p = document.createElement("p");
        var monthText = document.createTextNode(monthNum);
        var yearText = document.createTextNode(yearNum);
        p.appendChild(yearText);p.appendChild(monthText);
        $month.append(p);
        //遍历日历网格
        for (var i = 1; i <= 6; i++) {
            _nullnei += "<tr>";
            for (var j = 1; j <= 7; j++) {
                _nullnei += '<td></td>';
            }
            _nullnei += "</tr>";
        }
        $tbody.html(_nullnei);

        //遍历网格内容
        var $slitd = $tbody.find("td");
        for (var i = 0; i < conter; i++) {
            //eq(index)将匹配元素集缩减指定index上的一个
            $slitd.eq(i + monthFirst).html("<p>" + parseInt(i + 1) + "</p>")
        }
        //给有日期的td加上id
        var u = 1;
        var dayBlock = document.getElementsByTagName("td");
        for (var i = 0; i < dayBlock.length; i++) {
            if (dayBlock[i].textContent != "") {
                dayBlock[i].setAttribute("id", "td" + u);
                u++;
            }
        }
        //若日期不足排满每一行的tr，则删除最后一个tr
        var blankTr = document.getElementsByTagName("tr");
        var blankTd = blankTr[5].getElementsByTagName("td");
        for (var i = 0; i < blankTd.length; i++) {
            if (blankTd[i].textContent != "") {
                blank = false;
            }
        }
        if (blank == true) {
            blankTr[5].remove();
        }
    }

    //确认本月签到日期，并把他们加上标红buff
    function checkDate(prep) {
        var dateArray = [];
        var newArray = [];
        //删除不是本月的签到日期
        //把签到本地日期copy至datearray
        for (var i = 0; i < localDate.date.length; i++) {
            dateArray.push(localDate.date[i]);
        }
        for (var i = 0; i < dateArray.length; i++) {
            if (dateArray[i].charAt(1) != prep) {
                dateArray[i] = undefined;
            }
        }
        for (var i = 0; i < dateArray.length; i++) {
            if (dateArray[i] != undefined) {
                newArray.push(dateArray[i]);
            }
        }
        //遍历数组为已签到日期添加class
        for (var i = 0; i < newArray.length; i++) {
            if (newArray[i].charAt(2) == 0) {
                for (var j = 0; j < 10; j++) {
                    if (newArray[i].charAt(3) == j) {
                        var checked = "#td" + j;
                        $(checked).addClass("qiandao");
                    }
                }
            } else if (newArray[i].charAt(2) == 1) {
                for (var j = 0; j < 10; j++) {
                    if (newArray[i].charAt(3) == j) {
                        var checked = "#td1" + j;
                        $(checked).addClass('qiandao');
                    }
                }
            } else {
                for (var j = 0; j < 10; j++) {
                    if (newArray[i].charAt(3) == j) {
                        var checked = "#td2" + j;
                        $(checked).addClass("qiandao");
                    }
                }
            }
        }
    }

    //当天签到添加样式
    $(document).on('click','#sign_btn',function () {
        $("tr").remove();
        $("p").remove();
        //initall();
        dateHandler(monthFirst, d, conter, monthNum);
        //给此月签到的加BUFF*/
        checkDate(monthCheck);
        /**y = slidate.getDate();*/
        var thisDay = "#td" + y;
        var checkPic = false;
        /**thisBlock="0909"*/
        if (m > 10 && y < 10) {
            var thisBlock = m.toString() + y.toString();
        } else if (m < 10 && y> 10) {
            var thisBlock = "0" + m.toString() + y.toString();
        } else if (m > 10 && y < 10) {
            var thisBlock = m.toString() + "0" + y.toString();
        } else if (m < 10 && y < 10) {
            var thisBlock = "0" + m.toString() + "0" + y.toString();
        }

        for (var e = 0; e < localDate.date.length; e++) {
            if (localDate.date[e] === thisBlock) {
                checkPic = true;
            }
        }
        if (checkPic == true) {
            alert("您今天已经签到了！");
        } else {
            $(thisDay).addClass("qiandao");
            alert("已签到！");
            localDate.date.push(thisBlock);
        }
    });

    //查询已签到天数
    $(document).on('click','#sign_days',function () {
        alert("您已经签到了" + localDate.date.length + "天！");
    });

    //查询历史记录
    $(document).on('click','#check_lastmonth',function () {
        $("tr").remove();
        $("p").remove();
        if (m > 0 && n > 0) {
            m--;n--;
        }
        var monthFirst = new Date(slidate.getFullYear(), parseInt(n), 1).getDay(); //获取当月的1日等于星期几
        var d = new Date(slidate.getFullYear(), parseInt(m), 0); //获取月
        var conter = d.getDate(); //获取当前月的天数
        var monthNum = "0" + (m) + "月";
        var monthCheck = m;
        dateHandler(monthFirst, d, conter, monthNum);
        checkDate(monthCheck);
    });

    //返回上月记录
    $(document).on('click','#back',function () {
        $("tr").remove();
        $("p").remove();
        if (m < x) {
            m++;n++;
        }
        var monthFirst = new Date(slidate.getFullYear(), parseInt(n), 1).getDay(); //获取当月的1日等于星期几
        var d = new Date(slidate.getFullYear(), parseInt(m), 0); //获取月
        var conter = d.getDate(); //获取当前月的天数
        var monthNum = "0" + (m) + "月";
        var monthCheck = m;
        dateHandler(monthFirst, d, conter, monthNum);
        checkDate(monthCheck);
    })

    //联系
    $(document).on('click','#sign_btn',function () {
        
    })

 window.addEventListener("load", initall, false);