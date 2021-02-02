function UserToLogin(account, password) {
    var pageTotal = 0;
    $.ajax({
        url : "/user/",
        type : "get",
        async : false,//此处需要注意的是要想获取ajax返回的值这个async属性必须设置成同步的，否则获取不到返回值
        data : {"account":account, "password":password},
        dataType : "json",
        success : function(data) {
            pageTotal = data.pageTotal;
        }
        
    });
    return pageTotal;
}


$("#login").click(UserToLogin());