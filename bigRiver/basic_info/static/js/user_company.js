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
            dataType:'json',
            async:false,
            data: {'user_id':getCookie('user_id')},
            success:function(data) {
                if(data.success) {
                    company=data;
                    add_company_to_page();
                }
                else
                {
                    console.log("no company");
                }
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
        $('#search-container').hide();
        var p = document.createElement('p');
        var h2 = document.createElement('h2');
        var p1 = document.createElement('p');
        if(getCookie('user_id')==company['bossID'])
            var companytext = document.createTextNode('您已创建 '+company['name']);
        else
            var companytext = document.createTextNode('您已加入 '+company['name']);
        var jointext2 = document.createTextNode('  公司税号: '+company['taxNumber']);
        var jointext1 = document.createTextNode('公司ID: '+company['companyID']);
        p.appendChild(jointext1);
        p.appendChild(jointext2);
        h2.appendChild(companytext);
        $('#joined-company').append(p);
        $('#joined-company').append(p1);
        $('#joined-company').append(h2);
}

$(document).on('click','#submit-company',function () {
       $.ajax({
            type: 'POST',
            url: "/usercompany/search/",
            async:false,
            dataType:'json',
            data: {'user_id':getCookie('user_id'),
                    'company_id':$('#input-company').val()
            },
            success:function(data) {
                if(data.success) {
                    var ok = confirm("你将要要加入" + data.name);
                    if(ok) {
                        $.ajax({
                            type: 'POST',
                            url: "/usercompany/confirm/",
                            dataType: 'json',
                            async: false,
                            data: {
                                'company_id': $('#input-company').val(),
                                'user_id': getCookie('user_id')
                            },
                            success: function (data) {
                                if (data.success) {
                                    alert("发送申请成功");
                                }
                                else {
                                    alert("发送申请失败");
                                }
                            },
                            error: function () {
                                alert("发送申请异常");
                            }
                        });
                    }
                }
                else{
                    alert("搜索公司不存在");
                }
            },
            error : function() {
                alert("数据库异常，搜索公司时get不到公司信息");
                //window.location.href="../login/";
            }
        });
    });

/**创建公司*/
/**点击弹窗输入想要创建公司的信息*/
$(document).on('click','#new_company',function () {
       window.open("/createcompany", 'create_company', 'height=300, width=600, top=200, left=150, toolbar=no, scrollbars=no, resizable=no,location=no, status=no');
})

function initial(){
    get_company_id();
}

window.addEventListener("load",initial,false);
