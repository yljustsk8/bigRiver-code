
    var localDate = {
                    date: [],
                    time_in:[],
                    status_in:[],
                    time_out:[],
                    status_out:[]
                }
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
    // var user_id = $.cookie('user_id');
    var y = slidate.getDate();




    function initall() {
        function getCookie(name)
        {
            var arr,reg=new RegExp("(^| )"+name+"=([^;]*)(;|$)");

            if(arr=document.cookie.match(reg))
                return unescape(arr[2]);
            else
                return null;
        }

        $.ajaxSetup({
            headers: { "X-CSRFToken": getCookie("csrftoken") }
        });
        $.ajax({
            type: 'POST',
            url: "/calendar/",
            data: {'user_id':'123'},
            success:function(data) {
                for(var i = 1;i<12;i++){
                    value =data[i.toString()];
                    value.forEach(function (item,j) {
                        if(item != ""&&item.length!=5 &&j!=0){
                            paras = item.split('@');
                            localDate.date.push(paras[0]);
                            localDate.time_in.push(paras[1].split('&')[0]);
                            localDate.status_in.push(paras[1].split('&')[1]);
                            localDate.time_out.push(paras[2].split('&')[0]);
                            localDate.status_out.push(paras[2].split('&')[1]);
                        }
                    });
                };
                dateHandler(monthFirst, d, conter, monthNum);
                checkDate(monthCheck);
            },
            error : function() {
                alert("连接数据库异常，请刷新重试");
            }
        })
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
        var dateArray = [];var time_inArray = [];var time_outArray = [];
        var newArray = [];var newinArray = []; var newoutArray = [];
         //删除不是本月的签到日期
        //把签到本地日期copy至datearray
        for (var i = 0; i < localDate.date.length; i++) {
            dateArray.push(localDate.date[i]);
            time_inArray.push(localDate.time_in[i]);time_outArray.push(localDate.time_out[i]);
        }
        for (var i = 0; i < dateArray.length; i++) {
            if (dateArray[i].charAt(1) != prep) {
                dateArray[i] = undefined;
                time_inArray[i] = undefined;
                time_outArray[i] = undefined;
            }
        }
        for (var i = 0; i < dateArray.length; i++) {
            if (dateArray[i] != undefined) {
                newArray.push(dateArray[i]);
                newinArray.push(time_inArray[i]);
                newoutArray.push(time_outArray[i]);
            }
        }
        //遍历数组为已签到日期添加class
        for (var i = 0; i < newArray.length; i++) {
            if (newArray[i].charAt(2) == 0) {
                for (var j = 0; j < 10; j++) {
                    if (newArray[i].charAt(3) == j) {
                        var checked = "#td" + j;
                        $(checked).addClass("qiandao");
                        $(document).on('click',checked,function () {
                            alert("上班时间："+ newinArray[j]+"\n下班时间："+ newoutArray[j]);
                        })
                    }
                }
            } else if (newArray[i].charAt(2) == 1) {
                for (var j = 0; j < 10; j++) {
                    if (newArray[i].charAt(3) == j) {
                        var checked = "#td1" + j;
                        $(checked).addClass('qiandao');
                        $(document).on('click',checked,function () {
                            alert("上班时间："+ newinArray[j+10]+"\n下班时间："+ newoutArray[j+10]);
                        })
                    }
                }
            } else {
                for (var j = 0; j < 10; j++) {
                    if (newArray[i].charAt(3) == j) {
                        var checked = "#td2" + j;
                        $(checked).addClass("qiandao");
                        $(document).on('click',checked,function () {
                            var check="2"+j;
                            alert("上班时间："+ newinArray[j+20]+"\n下班时间："+ newoutArray[j+20]);
                        })
                    }
                }
            }
        }
    }

    $(document).on('mouseover','#sign_btn',function () {
        $("#sign_btn").addClass("animated tada");
    })
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


    window.addEventListener("load",initall,false);