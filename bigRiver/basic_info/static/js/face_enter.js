var counter=0;

//002.1上传图片到服务器 img为转化为base64的图片，name为照片的名称 需要带后缀名 如.jpg .png 默认为temp.jpg
function uploadPhotos(image) {
    if(!image)
    {
        alert("上传照片为空");
        return;
    }
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
        type:'POST',
        url:'/face/faceenter/',
        data:{
            'user_id': getCookie('user_id'),
            'image': image,
        },
        dataType:'json',
        success:function (data) {
            if(!data.success){
                alert("发送图片失败");
            }
            else{
                counter++;
            }
        },
        error:function (err) {
            alert("未知错误");
        }
    });
}

function  initial() {
    while (counter<=200){
        uploadPhotos($(document).getElementById('#canvas2').toDataURL("image/jpeg", 1);
    }
    $.ajax({
        type:'GET',
        url:'/face/faceenter/',
        data:{
            'user_id': getCookie('user_id'),
            'stop':1,
        },
        dataType:'json',
        success:function (data) {
            alert('录制结束的状况已经传给服务器！');
        },
        error:function (err) {
            alert("录制结束错误");
        }
    });
}