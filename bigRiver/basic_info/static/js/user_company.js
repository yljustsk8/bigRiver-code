var company = null;

function get_company_id(){
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
            url: "/joincompany/",
            data: {'user_id':'123'},
            //data: {'user_id':getCookie('user_id')},
            success:function(data) {
                company=data.toString();
                add_company_to_page();
            },
            error : function() {
                alert("数据库异常，get不到公司信息");
                //window.location.href="../login/";
            }
        })
}

function add_company_to_page(){
    if (company != 'False'&& company != null){
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

    })

function initial(){
    get_company_id();
}

window.addEventListener("load",initial,false);
