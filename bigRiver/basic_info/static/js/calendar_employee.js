     var localDate = {
                     date: [],
                     time_in:[],
                     status_in:[],
                     time_out:[],
                     status_out:[]
                 }

     var curr_month_Date = {
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
             data: {'user_id':getCookie('employee_id')},
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
        curr_month_Date = {
                     date: [],
                     time_in:[],
                     status_in:[],
                     time_out:[],
                     status_out:[]
                 };
        for (var i = 0; i < localDate.date.length; i++) {
            var month_num = parseInt(localDate.date[i].substr(0,2));
             if (month_num == prep) {
                 var date_num = parseInt(localDate.date[i].substr(2,2));
                 var item_id = "#td" + date_num;
                 curr_month_Date.date.push(date_num);
                 curr_month_Date.time_in.push(localDate.time_in[i]);
                 curr_month_Date.time_out.push(localDate.time_out[i]);
                 curr_month_Date.status_in.push(localDate.status_in[i]);
                 curr_month_Date.status_out.push(localDate.status_out[i]);
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
                     var content = '正常';
                     if(curr_month_Date.status_in[item_id]=='0'&&curr_month_Date.status_out[item_id]=='1')
                         content = '迟到';
                     else if(curr_month_Date.status_in[item_id]=='1'&&curr_month_Date.status_out[item_id]=='0')
                         content = '早退';
                     else if(curr_month_Date.status_in[item_id]=='0'&&curr_month_Date.status_out[item_id]=='0')
                         content = '迟到早退';
                     else if(curr_month_Date.status_in[item_id]=='2'&&curr_month_Date.status_out[item_id]=='2')
                         content = '请假';
                     else if(curr_month_Date.status_in[item_id]=='3'&&curr_month_Date.status_out[item_id]=='3')
                         content = '没上班';

                     alert("第" + curr_month_Date.date[item_id] + "日状态：" + content + "\n上班时间："+ curr_month_Date.time_in[item_id] + "\n下班时间：" + curr_month_Date.time_out[item_id]);
                 })
             }
         }
     }

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
    $(document).on('click','#back',function nextMonth() {
        $("tr").remove();
        $("p").remove();
        if (curr_month_num <13 && n < 13) {
            curr_month_num++;
            n++;
        }
        var monthFirst = new Date(date_obj.getFullYear(), parseInt(n), 1).getDay(); //获取当月的1日等于星期几
        var d = new Date(date_obj.getFullYear(), parseInt(curr_month_num), 0); //获取月
        var conter = d.getDate(); //获取当前月的天数
        if(parseInt(curr_month_num)<10)
            var monthNum = "0" + (curr_month_num) + "月";
        else
            var monthNum = (curr_month_num) + "月";
        var monthCheck = curr_month_num;
        dateHandler(monthFirst, d, conter, monthNum);
        checkDate(monthCheck);
    })

  function nextMonth() {
        $("tr").remove();
        $("p").remove();
        if (curr_month_num <13 && n < 13) {
            curr_month_num++;
            n++;
        }
        var monthFirst = new Date(date_obj.getFullYear(), parseInt(n), 1).getDay(); //获取当月的1日等于星期几
        var d = new Date(date_obj.getFullYear(), parseInt(curr_month_num), 0); //获取月
        var conter = d.getDate(); //获取当前月的天数
        if(parseInt(curr_month_num)<10)
            var monthNum = "0" + (curr_month_num) + "月";
        else
            var monthNum = (curr_month_num) + "月";
        var monthCheck = curr_month_num;
        dateHandler(monthFirst, d, conter, monthNum);
        checkDate(monthCheck);
    }

 window.addEventListener("load", initall, false);