var myInfo={
    password: null ,
    name: null ,
    email: null ,
}

function getCookie(name) {
    var arr,reg=new RegExp("(^| )"+name+"=([^;]*)(;|$)");

     if(arr=document.cookie.match(reg))
         return unescape(arr[2]);
     else
         return null;
}

/**根据用户id初始化MyCompany界面*/
function get_info(){
    $.ajaxSetup({
            headers: { "X-CSRFToken": getCookie("csrftoken") }
        });
    $.ajax({
            type: 'POST',
            url: "/userinfo/",
            data: {'user_id':getCookie('user_id') },
            success:function(data) {
                myInfo.name=data['name'];
                myInfo.email=data['email'];
                myInfo.password =data['password'];
                add_info_to_page();
            },
            error : function() {
                alert("数据库异常，在edit界面初始化时获取不到个人信息");
                //window.location.href="../login/";
            }
    })
}

function add_info_to_page(){
    $('#name_edit').attr('placeholder',myInfo.name);
    $('#password_edit').attr('placeholder',myInfo.password);
    $('#email_edit').attr('placeholder',myInfo.email);
    $.ajax({
            type: 'POST',
            url: "/useredit/",
            data: {'user_id':getCookie('user_id'),
                    'name':myInfo.name,
                    'password':myInfo.password,
                    'email':myInfo.email,},
            success:function(data){
                myInfo.name=data['name'];
                add_info_to_page();
            },
            error : function() {
                alert("数据库异常，add to page时取不到个人信息");
                //window.location.href="../login/";
            }
    })
}


function initial(){
    get_info();
}

/**修改信息*/
$(document).on('click','#submit-edit',function () {
    if ($('#name_edit').getValue!='') myInfo.name = $('#name_edit').getValue;
    if ($('#email_edit').getValue!='') myInfo.email = $('#email_edit').getValue;
    if ($('#password_edit').getValue!='') myInfo.password = $('#password_edit').getValue;

    $.ajax({
        type:'POST',
        url:"/useredit/",
        data:{'name': $('#name_edit').getValue,
            'email': $('#email_edit').getValue,
            'password': $('#password_edit').getValue,},
        success:function (data) {
            if (data)
                alert("修改资料成功！")
            else
                alert("fail.")
        }
    })
})

/**退出登录*/
$(document).on('click','#exit',function (){
    window.location.href = "../login";
})

window.addEventListener("load",initial,false);