     var localDate = {
                     date: [],
                     time_in:[],
                     status_in:[],
                     time_out:[],
                     status_out:[]
                 }

     var curr_month_Date = {
                     date: [],
                     date_num: [],
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

    function getCookie(name) {
         var arr,reg=new RegExp("(^| )"+name+"=([^;]*)(;|$)");

         if(arr=document.cookie.match(reg))
             return unescape(arr[2]);
         else
             return null;
     }

    //初始化日期数据
     var date_obj = new Date();

     var curr_month_num = date_obj.getMonth() + 1;
     var x = date_obj.getMonth() + 1;
     var n = date_obj.getMonth();
     var monthCheck = (date_obj.getMonth() + 1);

     var month_first_day = new Date(date_obj.getFullYear(), parseInt(n), 1).getDay(); //获取当月的1日等于星期几
     var curr_month_obj = new Date(date_obj.getFullYear(), parseInt(curr_month_num), 0); //获取月
     var curr_month_day_num = curr_month_obj.getDate(); //获取当前月的天数

     var curr_month_str = "0" + curr_month_num + "月";
     var year_str = date_obj.getFullYear() +"年";

     var user_id = getCookie('user_id');
     var y = date_obj.getDate();

    function initall() {
         $.ajaxSetup({
             headers: { "X-CSRFToken": getCookie("csrftoken") }
         });
         $.ajax({
             type: 'POST',
             url: "/calendar/",
             data: {'user_id':getCookie('user_id')},
             success:function(data) {
                 for(var i = 1;i<12;i++){
                     value =data[i.toString()];
                     value.forEach(function (item,j) {
                         if(item != ""&&item.length!=5 &&j!=0){
                             var paras = item.split('@');
                             localDate.date.push(paras[0]);
                             localDate.time_in.push(paras[1].split('&')[0]);
                             localDate.status_in.push(paras[1].split('&')[1]);
                             localDate.time_out.push(paras[2].split('&')[0]);
                             localDate.status_out.push(paras[2].split('&')[1]);
                         }
                     });
                 };
                 dateHandler(month_first_day, curr_month_obj, curr_month_day_num, curr_month_str);
                 checkDate(monthCheck);
             },
             error : function() {
                 alert("连接数据库异常，请刷新重试");
             }
         })
    }

    /**调整表格行数，并把每个用到的td加上内容&赋予id*/
    function dateHandler(month_first_day, curr_month_obj, curr_month_day_num, curr_month_str) {

         var blank = true;
         var $tbody = $('#tbody'), //日历网格
             $month = $("#month"),  //“09月”
             _nullnei = '';
         var p = document.createElement("p");
         var monthText = document.createTextNode(curr_month_str);
         var yearText = document.createTextNode(year_str);
         p.appendChild(yearText);
         p.appendChild(monthText);
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
         for (var i = 0; i < curr_month_day_num; i++) {
             //eq(index)将匹配元素集缩减指定index上的一个
             $slitd.eq(i + month_first_day).html("<p>" + parseInt(i + 1) + "</p>")
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
        for (var i = 0; i < 32; i++) {
            var item_id = "#td" + i;
            $(document).off('click', item_id);
        }
        for (var i = 0; i < localDate.date.length; i++) {
            var month_num = parseInt(localDate.date[i].substr(0,2));
             if (month_num == prep) {
                 var date_num = parseInt(localDate.date[i].substr(2,2));
                 var item_id = "#td" + date_num;
                 curr_month_Date.date_num.push(date_num);
                 curr_month_Date.date.push(localDate.date[i]);
                 curr_month_Date.time_in.push(localDate.time_in[i]);
                 curr_month_Date.time_out.push(localDate.time_out[i]);
                 if (localDate.status_in[i]==1 && localDate.status_out[i]==1) {
                     $(item_id).addClass("qiandao");
                 } else if (localDate.status_in[i]==1 && localDate.status_out[i]==0) {
                     $(item_id).addClass("in_time");
                 } else if (!localDate.status_in[i]==0 && localDate.status_out[i]==1) {
                     $(item_id).addClass("out_time");
                 }
                 $(document).on('click',item_id,function () {
                     var item_id_str = $(this).attr("id").substr(2);
                     var item_id = parseInt(item_id_str) - 1;
                     var month = curr_month_Date.date[item_id].substr(0,2);
                     var date = curr_month_Date.date[item_id].substr(2,2);
                     var content = document.getElementById('content_info').value;
                     var type = (month >= date_obj.getMonth() + 1) && (date >= y)
                     alert('y='+y);
                     var type_str = ["补卡","请假"];
                     var confirm_code = window.confirm('您确定要申请' + month + '月' + date + '日' + type_str[type] + '吗？');
                     if (confirm_code == true){
                        $.ajax({
                            type: 'POST',
                            url: "/send_requests/",
                            data: {'user_id': getCookie('user_id'),
                                    'request_type':type,
                                    'request_content':content,
                                    'date':date,
                                    'month':month},
                            success: function (data) {
                                alert(data);
                            },
                            error: function () {
                                alert("连接申请数据库异常，请刷新重试");
                            }
                        })
                     } else{
                         alert('申请失败，请重试！');
                     }
                 })
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
        dateHandler(month_first_day, curr_month_obj, curr_month_day_num, curr_month_str);
        //给此月签到的加BUFF*/
        checkDate(monthCheck);
        var thisDay = "#td" + y;
        var checkPic = false;
        /**thisBlock="0909"*/
        if (curr_month_num > 10 && y < 10) {
            var thisBlock = curr_month_num.toString() + y.toString();
        } else if (curr_month_num < 10 && y> 10) {
            var thisBlock = "0" + curr_month_num.toString() + y.toString();
        } else if (curr_month_num > 10 && y < 10) {
            var thisBlock = curr_month_num.toString() + "0" + y.toString();
        } else if (curr_month_num < 10 && y < 10) {
            var thisBlock = "0" + curr_month_num.toString() + "0" + y.toString();
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
        if (curr_month_num > 0 && n > 0) {
             curr_month_num--;n--;
         }
        var monthFirst = new Date(date_obj.getFullYear(), parseInt(n), 1).getDay(); //获取当月的1日等于星期几
        var d = new Date(date_obj.getFullYear(), parseInt(curr_month_num), 0); //获取月
        var conter = d.getDate(); //获取当前月的天数
        var monthNum = "0" + (curr_month_num) + "月";
        var monthCheck = curr_month_num;
        dateHandler(monthFirst, d, conter, monthNum);
        checkDate(monthCheck);
    });

    //返回上月记录
    $(document).on('click','#back',function () {
        $("tr").remove();
        $("p").remove();
        if (curr_month_num < x) {
             curr_month_num++;n++;
        }
        var monthFirst = new Date(date_obj.getFullYear(), parseInt(n), 1).getDay(); //获取当月的1日等于星期几
        var d = new Date(date_obj.getFullYear(), parseInt(curr_month_num), 0); //获取月
        var conter = d.getDate(); //获取当前月的天数
        var monthNum = "0" + (curr_month_num) + "月";
        var monthCheck = curr_month_num;
        dateHandler(monthFirst, d, conter, monthNum);
        checkDate(monthCheck);
    })
     //返回
    $(document).on('click','#return_calendar',function () {
        window.location.href='/calendar/';
    });

 window.addEventListener("load", initall, false);