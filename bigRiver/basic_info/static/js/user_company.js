var company = null;

function getCookie(name) {
    var arr,reg=new RegExp("(^| )"+name+"=([^;]*)(;|$)");

     if(arr=document.cookie.match(reg))
         return unescape(arr[2]);
     else
         return null;
}

/**根据用户id初始化MyCompany界面*/
function get_company_id(){
    $.ajaxSetup({
            headers: { "X-CSRFToken": getCookie("csrftoken") }
        });
    $.ajax({
            type: 'POST',
            url: "/usercompany/",
            data: {'user_id':getCookie('user_id')},
            success:function(data) {
                company=data.toString();
                add_company_to_page();
            },
            error : function() {
                alert("数据库异常，加载用户对应公司名称时get不到公司信息");
                //window.location.href="../login/";
            }
    })
}

/**如果有公司后调用的函数
 * 隐藏搜索栏并将公司信息印在屏幕*/
function add_company_to_page(){
    if (company != 'False'&& company !='' &&company!=null){
        //hide
        $('#search-container').hide();
        var p = document.createElement('p');var h2 = document.createElement('h2');
        var companytext = document.createTextNode(company);
        var jointext = document.createTextNode('您已加入'+company+'公司');
        p.appendChild(jointext);
        h2.appendChild(companytext);
        $('#joined-company').append(p);
        $('#joined-company').append(h2);
    }
}

$(document).on('click','#submit-company',function () {
       $.ajax({
            type: 'POST',
            url: "/usercompany/search/",
            data: {'user_id':getCookie('user_id'),
                    'company_id':$('#input-company').getValue},
            success:function(data) {
                var ok = confirm("你将要要加入" + data.toString());
                    $.ajax({
                        type:'POST',
                        url:"/usercompany/confirm/",
                        data:{'status': ok,
                            'company_id':$('#input-company').getValue,
                            'user_id':getCookie('user_id')},
                        success:function (data) {
                            if (data)
                                alert("success.")
                            else
                                alert("fail.")
                        }
                    })
            },
            error : function() {
                alert("数据库异常，搜索公司时get不到公司信息");
                //window.location.href="../login/";
            }
        })
    })

/**创建公司*/
/**点击弹窗输入想要创建公司的信息*/
$(document).on('click','#new_company',function () {
       window.open("/createcompany", 'create_company', 'height=300, width=400, top=200, left=50, toolbar=no, scrollbars=no, resizable=no,location=no, status=no');
})
/**一些和css联动的效果*/
var inp = document.getElementsByClassName("create_input");
var main = document.getElementsByClassName("create_bar");
inp.onfocus = function(){
  if(inp.value == ""){
      main.className += "focus";
  }
}
inp.onblur = function(){
  if(inp.value == ""){
      main.className = "";
  }
}
/**提交更改*/
$(document).on('click','#create-submit',function (){
    var new_company = $('#name_create').getValue;
    var taxNumber =$('#taxNumber_create').getValue;
    $.ajax({
            type: 'POST',
            url: "/createcompany",
            data: {'user_id':getCookie('user_id'),
                    'company_name':new_company,
                    'taxNumber':taxNumber},
            success:function(data) {
                if(data==True){
                    alert("创建成功！请重新登录！");
                    window.location.href = "../login";
                }
                else
                    alert(data.toString());

            },
            error : function() {
                alert("数据库/cookie异常，创建公司时传不出去数据！");
                //window.location.href="../login/";
            }
        })
})

function initial(){
    get_company_id();
}

window.addEventListener("load",initial,false);
