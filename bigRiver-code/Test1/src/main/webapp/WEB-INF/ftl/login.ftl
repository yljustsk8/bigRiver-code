<!doctype html>
<html>
<head>
    <h1>欢迎来到云计算大赛的获奖查询界面</h1>
    <h2>请先登录</h2>
</head>
<body>
<div>
    <table>
        <tr>
            <td>登录名</td>
            <td><input name="username" id="username" type="text"></td>
        </tr>
        <tr>
            <td>密码</td>
            <td><input name="password" id="password" type="text"></td>
        </tr>
        <tr>
            <td><input type="button" id="login" class="br">登录</td>
        </tr>
    </table>
</div>
</body>
<script type="text/javascript" src="assets/js/jquery.js"></script>
<script type="text/javascript">
    $("#login ").click(function() {
        var username = $('#username').val();
        var password = $('#password').val();

        $.post("login", { username: username, password: password},
                function (data) {
                    if(data== 0) {
                        alert("登录名不存在。");
                        location.href ="login";
                    }else if(data ==2){
                        alert("密码错误！请重试。");
                        location.href ="login";
                    }else
                        location.href ="awdUpload";
                });
    });
</script>
</html>