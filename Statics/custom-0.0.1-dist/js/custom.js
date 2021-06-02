/*
* There Are Some JQ Function By Self 
*/

/*
-------------------------------
按钮的功能
-------------------------------
*/

// 登陆按钮的功能
$("#login-in").click(function(){
    if ($("#email").val() == "" || $("#passWord").val() == ""){
        WindowsRemanderError("在<font color=\"green\">登录</font>的时候，输入的邮箱和密码不能为空哦！");
    } else {
        $.ajax({
            url : "/user/",
            type : "get",
            async : false,
            data : {"email":$("#email").val(), "password":$("#passWord").val()},
            headers:{"X-CSRFToken":$.cookie("csrftoken")},
            dataType : "json",
            success : function(data) {
                if (data.errorCode == 0){
                    $.cookie('slug', data.slug, {expires: 7});
                    window.location.href = "http://" + window.location.host;
                } else {
                    $("#UserErrorInfo").html(data.desc);
                    $("#UserErrorInfo").removeClass("d-none");
                }
            }
        });
    }

});

// 注册按钮的功能
$("#sign-up").click(function(){
    if ($("#email").val() == "" || $("#passWord").val() == ""){
        WindowsRemanderError("在<font color=\"orange\">注册</font>的时候，输入的邮箱和密码不能为空哦！");
    } else if ($("#RandomCodeInput").hasClass("d-none")){
        $.ajax({
            url : "/user/randomcode",
            type : "get",
            async : false,
            data : {"email":$("#email").val()},
            headers:{"X-CSRFToken":$.cookie("csrftoken")},
            dataType : "json",
            success : function(data) {
                if (data.errorCode == 0){
                    $("#RandomCodeInput").removeClass("d-none")
                    $("#UserErrorInfo").html(data.desc);
                    $("#UserErrorInfo").removeClass("d-none");
                    $("#sign-up").html("验证");
                    $("#sign-up").removeClass("btn-success");
                    $("#sign-up").addClass("btn-warning");
                    $("#UserName").removeClass("d-none");
                    $("#login-in").addClass("d-none");
                    $("#resend-email").removeClass("d-none");
                    $("#email").attr("disabled","disabled");
                    $("#passWord").attr("disabled","disabled");
                } else {
                    $("#UserErrorInfo").html(data.desc);
                    $("#UserErrorInfo").removeClass("d-none");
                }
            }
        });
    } else {
        $.ajax({
            url : "/user/randomcode",
            type : "post",
            async : false,
            data : {"code":$("#RandomCode").val(), "email":$("#email").val()},
            headers:{"X-CSRFToken":$.cookie("csrftoken")},
            dataType : "json",
            success : function(data) {
                if (data.errorCode == 0){
                    $.ajax({
                        url : "/user/",
                        type : "post",
                        async : false,
                        data : {"email":$("#email").val(), "password":$("#passWord").val(), "user_name":$("#userName").val()},
                        headers:{"X-CSRFToken":$.cookie("csrftoken")},
                        dataType : "json",
                        success : function(data) {
                            if (data.errorCode == 0){
                                $.cookie('slug', data.slug, {expires: 7});
                                window.location.href = "http://" + window.location.host;
                            } else {
                                $("#UserErrorInfo").html(data.desc);
                                $("#UserErrorInfo").removeClass("d-none");
                            }
                        }
                    });
                } else {
                    $("#UserErrorInfo").html(data.desc);
                    $("#UserErrorInfo").removeClass("d-none");
                }
            }
        });
    }
});

// 重发按钮的功能
$("#resend-email").click(function(){
    $.ajax({
        url : "/user/randomcode",
        type : "get",
        async : false,
        data : {"email":$("#email").val()},
        headers:{"X-CSRFToken":$.cookie("csrftoken")},
        dataType : "json",
        success : function(data) {
            $("#UserErrorInfo").html(data.desc);
        }
    });
});

// 登出按钮的功能
$("#login-out").click(function(){
    $.removeCookie('slug');
    $.removeCookie('csrftoken');
    $.removeCookie('sessionid');
    window.location.href = "http://" + window.location.host;
});

// 更换头像按钮事件
$("#ChangeAvatar").click(function(){  
    var new_avatar = md5(Math.random()).substr(0,18);
    var svgCode = multiavatar(new_avatar);
    $("#user-avatar").attr("avatar_id", new_avatar);
    $("#user-avatar").html(svgCode); // 填充右上角的头像
    $("#info-avatar").html(svgCode); // 填充用户信息页的头像

    if ($("#SaveChange").hasClass("d-none")){
        $("#SaveChange").removeClass("d-none")
    }

    if ($("#CancelChange").hasClass("d-none")){
        $("#CancelChange").removeClass("d-none")
    }
    getMsg();
});

// 用户信息保存按钮事件
$("#SaveChange").click(function(){
    var new_avatar = $("#user-avatar").attr("avatar_id");
    $("#SaveChange").addClass("d-none");
    $("#CancelChange").addClass("d-none");
    
    $.ajax({
        url : '/user/',
        type : "patch",
        data : {"avatar_id": new_avatar, "slug": $.cookie("slug")},
        headers:{"X-CSRFToken":$.cookie("csrftoken")},
        async : true,
        success : function(data){
            if (data.errorCode == 0){
                $.cookie("avatar_id", new_avatar);
                WindowsRemanderInfo(data.desc);

            } else {
                WindowsRemanderError(data.desc);
                var old_avatar = $.cookie('avatar_id');
                var svgCode = multiavatar(old_avatar);
                $("#user-avatar").html(svgCode); // 填充右上角的头像
                $("#info-avatar").html(svgCode); // 填充用户信息页的头像
            }
            
        }
      });
});

// 用户信息取消按钮事件
$("#CancelChange").click(function(){
    var old_avatar = $.cookie('avatar_id');
    var svgCode = multiavatar(old_avatar);
    $("#user-avatar").html(svgCode); // 填充右上角的头像
    $("#info-avatar").html(svgCode); // 填充用户信息页的头像
    $("#SaveChange").addClass("d-none");
    $("#CancelChange").addClass("d-none");
});

// 用户提交消息事件
$("#send-msg").click(function(){
    if ($("#UserMessage").val() == ""){
        WindowsRemanderWarn("你可能得留下点什么，才可以提交哦！");
    } else {
        sendMsg($("#UserMessage").val());
        $("#UserMessage").val("");
    }
});

// 导航的点击事件
$("#main-page").click(function(){
    $("#main-page").addClass("active");
    $("#my-stock").removeClass("active");
    $("#ranking").removeClass("active");
    $("#desc-site").removeClass("active");
    getMsg();
});
$("#my-stock").click(function(){
    $("#main-page").removeClass("active");
    $("#my-stock").addClass("active");
    $("#ranking").removeClass("active");
    $("#desc-site").removeClass("active");
    getMsg();
});
$("#ranking").click(function(){
    $("#main-page").removeClass("active");
    $("#my-stock").removeClass("active");
    $("#ranking").addClass("active");
    $("#desc-site").removeClass("active");
    getMsg();
});
$("#desc-site").click(function(){
    $("#main-page").removeClass("active");
    $("#my-stock").removeClass("active");
    $("#ranking").removeClass("active");
    $("#desc-site").addClass("active");
    getMsg();
});

// 小窗口弹窗信息事件
function WindowsRemanderInfo(content){
    $.toast({
        title: "一个小提醒",
        subtitle: "刚刚",
        content: content,
        type: 'info',
        delay: 3000,
        img: {
          src: '',
          class: 'rounded-lg',
          title: 'Thumbnail Title',
          alt: ''
        },
        pause_on_hover: true
      });
}

// 小窗口弹窗警告事件
function WindowsRemanderWarn(content){
    $.toast({
        title: "我们想提醒你一下",
        subtitle: "刚刚",
        content: content,
        type: 'warn',
        delay: 3000,
        img: {
          src: '',
          class: 'rounded-lg',
          title: 'Thumbnail Title',
          alt: ''
        },
        pause_on_hover: true
      });
}

// 小窗口弹窗错误事件
function WindowsRemanderError(content){
    $.toast({
        title: "我们遇到了一个问题",
        subtitle: "刚刚",
        content: content,
        type: 'error',
        delay: 5000,
        img: {
          src: '',
          class: 'rounded-lg',
          title: 'Thumbnail Title',
          alt: ''
        },
        pause_on_hover: true
      });
}


/*
-------------------------------
后台接口
-------------------------------
*/

// 实时获取消息接口
function getMsg() {
    $.ajax({
        url : '/message/',
        type : "get",
        data : "",
        async : true,
        success : function(data) {
            if (data.errorCode == 0){
                if (data.msg_type == "[info]") {
                    WindowsRemanderInfo(data.desc);
                }
                else if (data.msg_type == "[warn]") {
                    WindowsRemanderWarn(data.desc);
                }
                else if (data.msg_type == "[error]"){
                    WindowsRemanderError(data.desc);
                } 
            }
        }
    });
}

// 用户提交消息的接口
function sendMsg(message){
    $.ajax({
        url : '/message/',
        type : "post",
        data : {"message":message},
        headers:{"X-CSRFToken":$.cookie("csrftoken")},
        async : true,
        success : function(data) {
          if (data.errorCode == 0){
              WindowsRemanderInfo(data.desc);
          } else {
              WindowsRemanderError(data.desc);
          }
        }
      });
}

/*
-------------------------------
界面事件
-------------------------------
*/

// 页面加载完成时运行
$(document).ready(function(){
    // 加载头像
    var avatarId = $("#user-avatar").attr("avatar_id");
    
    var svgCode = multiavatar(avatarId);
    $("#user-avatar").html(svgCode); // 填充右上角的头像
    $("#info-avatar").html(svgCode); // 填充用户信息页的头像
    $.cookie("avatar_id", avatarId);

    // 加载书籍
    $.cookie("page_num", 0);
    if ( $("#book-window").length > 0 ) {
        var page_num = $.cookie("page_num");
        getBooks(function(result){
            var book_card = '';
            for (obj of result) {
                book_card = 
                    '<div class="col-2 book-cover mt-3 md-3" onclick="previewFile(this)" book_id="' + obj.slug + '">' + 
                    '<img class="img-fluid bg-white shadow-lg rounded-lg" src="' + obj.cover + '" width="150px" height="225px"></div>';
                $("#book-window").children("div.row").last().append(book_card);
            }
            $.cookie("page_num", parseInt(page_num) + result.length);
        });
    }

    getMsg();
})
