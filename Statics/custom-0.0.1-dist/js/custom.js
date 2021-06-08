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

// 用户新建知识库的预览事件
$("#stock-browse").click(function(){
    var reader = new FileReader();
    
    if ($("#knowledge-cover")[0].files.length > 0){
        reader.readAsDataURL($("#knowledge-cover")[0].files[0]);
        reader.onload = function () {
            $("#example-stock-cover").css("background-image", "url('" + reader.result + "')");
            $("#example-stock-cover").css("background-size", "cover");
            $("#example-stock-title").html($("#knowledge-name").val());
            $("#example-stock-desc").html($("#knowledge-desc").val());
        }
    } else {
        $("#example-stock-cover").css("background-image", "url()");
        $("#example-stock-cover").css("background-size", "cover");
        $("#example-stock-title").html($("#knowledge-name").val()); 
        $("#example-stock-desc").html($("#knowledge-desc").val()); 
    }
    $("#show-stock-browse").removeClass("d-none");

});

// 用户新建知识库的保存事件
$("#stock-create").click(function(){
    if (($("#knowledge-name").val().length > 12) || ($("#knowledge-name").val().length < 1)){
        alert("名称长度不符...");
        return ;
    } else {
        var formdata = new FormData(); 
        formdata.append('name', $("#knowledge-name").val());
        formdata.append('tag', $("#knowledge-tag").val());
        formdata.append('describe', $("#knowledge-desc").val());
        formdata.append('cover',$("#knowledge-cover")[0].files[0]);
    
        $.ajax({
            url : '/stock/',
            type : "post",
            processData:false,
            contentType:false,
            data : formdata,
            headers:{"X-CSRFToken":$.cookie("csrftoken")},
            async : true,
            success : function(data){
                if (data.errorCode == 0){
                    WindowsRemanderInfo(data.desc);
                } else {
                    WindowsRemanderError(data.desc);
                }
            }
        });
        $("#show-picture").addClass("d-none");
        $("#knowledge-name").val("");
        $("#knowledge-cover").val("");
    }
});

// 用户取消新建知识库的事件
$("#stock-cancel-create").click(function(){
    $("#show-stock-browse").addClass("d-none");
    $("#knowledge-name").val("");
    $("#knowledge-cover").val("");
});

// 用户编辑知识库的事件
$("#stock-edit").click(function(){
    $("#knowledge-name-edit").attr("disabled", false);
    $("#knowledge-desc-edit").attr("disabled", false);
    $("#knowledge-tag-edit").attr("disabled", false);
    $("#knowledge-cover-edit").attr("disabled", false);
});

// 用户更新知识库的事件
$("#stock-update").click(function(){
    if (($("#knowledge-name-edit").val().length > 12) || ($("#knowledge-name-edit").val().length < 1)){
        alert("名称长度不符...");
        return ;
    } else {
        var formdata = new FormData(); 
        formdata.append('name', $("#knowledge-name-edit").val());
        formdata.append('tag', $("#knowledge-tag-edit").val());
        formdata.append('describe', $("#knowledge-desc-edit").val());
        formdata.append('slug', $("#StockInfoModal").attr("stockSlug"));

        if ($("#knowledge-cover-edit")[0].files.length != 0){
            formdata.append('cover',$("#knowledge-cover-edit")[0].files[0]);
        }
        
        $.ajax({
            url : '/stock/',
            type : "patch",
            processData:false,
            contentType:false,
            data : formdata,
            headers:{"X-CSRFToken":$.cookie("csrftoken")},
            async : true,
            success : function(data){
                if (data.errorCode == 0){
                    WindowsRemanderInfo(data.desc);
                    cleanStockInHtml("#down-stock-window-my");
                    getStocksByUserSlug(generateStocksInSelfPage);
                } else {
                    WindowsRemanderError(data.desc);
                }
            }
        });

    }
});

// 用户上传新章节的事件
$("#piece-upload").click(function(){
    if ($("#piece-file")[0].files.length == 0){
        alert("要上传一个文件才行");
        return ;
    } else {
        var formdata = new FormData(); 
        formdata.append('piece_file',$("#piece-file")[0].files[0]);
        formdata.append('belong_stock_slug', $("#StockInfoModal").attr("stock-slug"));
        
        $.ajax({
            url : '/piece/',
            type : "post",
            processData:false,
            contentType:false,
            data : formdata,
            headers:{"X-CSRFToken":$.cookie("csrftoken")},
            async : true,
            success : function(data){
                if (data.errorCode == 0){
                    WindowsRemanderInfo(data.desc);
                } else {
                    WindowsRemanderError(data.desc);
                }
            }
        });
        // $("#show-picture").addClass("d-none");
        // $("#knowledge-name").val("");
        // $("#knowledge-cover").val("");
    }
});

// 导航的点击事件
$("#main-page").click(function(){
    if ($("#main-page").hasClass("active")){ return ; } 
    $("#main-page").addClass("active");
    $("#my-stock").removeClass("active");
    $("#ranking").removeClass("active");
    $("#desc-site").removeClass("active");
    $("#brand-for-main-page").removeClass("d-none");
    $("#brand-for-my-stock").addClass("d-none");
    $("#brand-for-ranking").addClass("d-none");
    $("#brand-for-desc-site").addClass("d-none");
    $("#tag-for-main-page").removeClass("d-none");
    $("#tag-for-my-stock").addClass("d-none");
    $("#tag-for-ranking").addClass("d-none");
    $("#tag-for-desc-site").addClass("d-none");
    $("#down-stock-window-my").children("div.row").addClass("d-none");
    $("#down-stock-window-main").children("div.row").removeClass("d-none");
    cleanStockInHtml("#down-stock-window-main");
    getStocks(generateStocksInMainPage);
    getMsg();
});
$("#my-stock").click(function(){
    if ($("#my-stock").hasClass("active")){ return ; } 
    $("#main-page").removeClass("active");
    $("#my-stock").addClass("active");
    $("#ranking").removeClass("active");
    $("#desc-site").removeClass("active");
    $("#brand-for-main-page").addClass("d-none");
    $("#brand-for-my-stock").removeClass("d-none");
    $("#brand-for-ranking").addClass("d-none");
    $("#brand-for-desc-site").addClass("d-none");
    $("#tag-for-main-page").addClass("d-none");
    $("#tag-for-my-stock").removeClass("d-none");
    $("#tag-for-ranking").addClass("d-none");
    $("#tag-for-desc-site").addClass("d-none");
    $("#down-stock-window-my").children("div.row").removeClass("d-none");
    $("#down-stock-window-main").children("div.row").addClass("d-none");
    cleanStockInHtml("#down-stock-window-my");
    getStocksByUserSlug(generateStocksInSelfPage);
    getMsg();
});
$("#ranking").click(function(){
    if ($("#ranking").hasClass("active")){ return ; } 
    $("#main-page").removeClass("active");
    $("#my-stock").removeClass("active");
    $("#ranking").addClass("active");
    $("#desc-site").removeClass("active");
    $("#brand-for-main-page").addClass("d-none");
    $("#brand-for-my-stock").addClass("d-none");
    $("#brand-for-ranking").removeClass("d-none");
    $("#brand-for-desc-site").addClass("d-none");
    $("#tag-for-main-page").addClass("d-none");
    $("#tag-for-my-stock").addClass("d-none");
    $("#tag-for-ranking").removeClass("d-none");
    $("#tag-for-desc-site").addClass("d-none");
    getMsg();
});
$("#desc-site").click(function(){
    if ($("#desc-site").hasClass("active")){ return ; } 
    $("#main-page").removeClass("active");
    $("#my-stock").removeClass("active");
    $("#ranking").removeClass("active");
    $("#desc-site").addClass("active");
    $("#brand-for-main-page").addClass("d-none");
    $("#brand-for-my-stock").addClass("d-none");
    $("#brand-for-ranking").addClass("d-none");
    $("#brand-for-desc-site").removeClass("d-none");
    $("#tag-for-main-page").addClass("d-none");
    $("#tag-for-my-stock").addClass("d-none");
    $("#tag-for-ranking").addClass("d-none");
    $("#tag-for-desc-site").removeClass("d-none");
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

// 获取全部Stock
function getStocks(callback){
    $.ajax({
        url : '/stock/',
        type : "get",
        data : "",
        async : true,
        success : function(data) {
            if (data.errorCode == 0){
                callback(data.data);
            } else {
                WindowsRemanderError(data.desc);
            }
        }
    });
}

// 获取某些用户创建的Stock
function getStocksByUserSlug(callback){
    $.ajax({
        url : '/stock/?userSlug=' + $.cookie("slug"),
        type : "get",
        data : "",
        async : true,
        success : function(data) {
            if (data.errorCode == 0){
                callback(data.data);
            } else {
                WindowsRemanderError(data.desc);
            }
        }
    });
} 

function getPiecesByStockSlugAndAppend(stockSlug){
    $("#piece-list").html("");
    $.ajax({
        url : '/piece/?stock_slug=' + stockSlug,
        type : "get",
        data : "",
        async : true,
        success : function(data) {
            for (var ind=0; ind<data.data.length; ++ind){
                $("#piece-list").append('<tr><td>' + ind + '</td><td title="' + data.data[ind].name + '">' + data.data[ind].name + '<span class="position-top badge bg-success float-end mx-1" onclick="positionTop(this)">向上</span><span class="position-down badge bg-danger float-end" onclick="positionDown(this)">向下</span></td></tr>')
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

    // 先清空Stock
    cleanStockInHtml();

    // 加载Stock
    getStocks(generateStocksInMainPage);
    getMsg();
});


function generateStocksInMainPage(datas){
    var stock_card = '';
    for (obj of datas) {
        var avatar_svg = multiavatar(obj.author_avatar);
        stock_card = 
            '<div id="' + obj.slug + ' "class="col" onclick=browseStock(this)>' + 
            '<div class="card card-cover h-100 overflow-hidden text-white bg-dark rounded-5 shadow-lg " >' + 
            '<div class="d-flex flex-column h-100 p-5 pb-3 text-white text-shadow-1 div-cover" style="background-image: url(' + obj.cover + '); background-size: cover">' +
            '<figure class="pt-5 mt-5 mb-4 lh-1 fw-bold">' +
            '<blockquote class="blockquote"><h6 class="display-6">' + obj.name + '</h6></blockquote>' +
            '<figcaption class="blockquote-footer">' + obj.describe + '</figcaption>' +
            '</figure>' +
            '<ul class="d-flex list-unstyled mt-auto">' +
            '<li class="me-auto">' +
            '<a class="d-inline-block text-white" data-bs-toggle="tooltip" data-bs-placement="top" title="' + obj.author_name + '"><svg id="user-avatar" class="rounded-circle me-2" width="32" height="32">' + avatar_svg + '<svg></a>' +
            '</li>' +
            '<li class="d-flex align-items-center me-3">' +
            '<a class="d-inline-block text-white" data-bs-toggle="tooltip" data-bs-placement="top" title="阅读数"><svg class="bi me-2" width="1em" height="1em"><use xlink:href="#people-circle"/></svg></a>' +
            '<small>' + obj.read_count + '</small>' +
            '</li>' +
            '<li class="d-flex align-items-center me-3">' +
            '<a class="d-inline-block text-white" data-bs-toggle="tooltip" data-bs-placement="top" title="收藏数"><svg class="bi me-2" width="1em" height="1em"><use xlink:href="#heart"/></svg></a>' +
            '<small>' + obj.marked_count + '</small>' +
            '</li>' +
            '<li class="d-flex align-items-center">' +
            '<a class="d-inline-block text-white" data-bs-toggle="tooltip" data-bs-placement="top" title="最近更新"><svg class="bi me-2" width="1em" height="1em"><use xlink:href="#calendar3"/></svg></a>' +
            '<small>'+ obj.upgrade_date +'</small>' +
            '</li></ul></div></div></div>';

        $("#down-stock-window-main").children("div.row").last().append(stock_card);
    }
}

function generateStocksInSelfPage(datas){
    var stock_card = '';
    for (obj of datas) {
        var avatar_svg = multiavatar(obj.author_avatar);
        stock_card = 
            '<div id="' + obj.slug + '" tag="' + obj.tag + '" class="col" onclick=updateStockModel(this) data-bs-toggle="modal" data-bs-target="#StockInfoModal">' + 
            '<div class="card card-cover h-100 overflow-hidden text-white bg-dark rounded-5 shadow-lg " >' + 
            '<div class="d-flex flex-column h-100 p-5 pb-3 text-white text-shadow-1 div-cover" style="background-image: url(' + obj.cover + '); background-size: cover">' +
            '<figure class="pt-5 mt-5 mb-4 lh-1 fw-bold">' +
            '<blockquote class="blockquote"><h6 class="display-6">' + obj.name + '</h6></blockquote>' + 
            '<figcaption class="blockquote-footer">' + obj.describe + '</figcaption>' +
            '</figure>' +
            '<ul class="d-flex list-unstyled mt-auto">' +
            '<li class="me-auto">' +
            '<a class="d-inline-block text-white" data-bs-toggle="tooltip" data-bs-placement="top" title="' + obj.author_name + '"><svg id="user-avatar" class="rounded-circle me-2" width="32" height="32">' + avatar_svg + '<svg></a>' +
            '</li>' +
            '<li class="d-flex align-items-center me-3">' +
            '<a class="d-inline-block text-white" data-bs-toggle="tooltip" data-bs-placement="top" title="阅读数"><svg class="bi me-2" width="1em" height="1em"><use xlink:href="#people-circle"/></svg></a>' +
            '<small>' + obj.read_count + '</small>' +
            '</li>' +
            '<li class="d-flex align-items-center me-3">' +
            '<a class="d-inline-block text-white" data-bs-toggle="tooltip" data-bs-placement="top" title="收藏数"><svg class="bi me-2" width="1em" height="1em"><use xlink:href="#heart"/></svg></a>' +
            '<small>' + obj.marked_count + '</small>' +
            '</li>' +
            '<li class="d-flex align-items-center">' +
            '<a class="d-inline-block text-white" data-bs-toggle="tooltip" data-bs-placement="top" title="最近更新"><svg class="bi me-2" width="1em" height="1em"><use xlink:href="#calendar3"/></svg></a>' +
            '<small>'+ obj.upgrade_date +'</small>' +
            '</li></ul></div></div></div>';

        $("#down-stock-window-my").children("div.row").last().append(stock_card);
    }
}

function cleanStockInHtml(div){
    $(div).children("div.row").last().html("")
}

function updateStockModel(obj){
    $("#StockInfoModal").attr("stock-slug", obj.id);
    $("#knowledge-name-edit").val($("#" + obj.id).children("div").children("div").children("figure").children("blockquote").children("h6").html());
    $("#knowledge-name-edit").attr("disabled", true);
    $("#knowledge-desc-edit").val($("#" + obj.id).children("div").children("div").children("figure").children("figcaption").html());
    $("#knowledge-desc-edit").attr("disabled", true);
    $("#knowledge-tag-edit").val(obj.tag);
    $("#knowledge-tag-edit").attr("disabled", true);
    $("#knowledge-cover-edit").attr("disabled", true);
    $("#StockInfoModal").attr("stockSlug", obj.id);

    getPiecesByStockSlugAndAppend(obj.id);
}

function browseStock(obj){
    window.open("/stock/" + obj.id);
}

function positionTop(obj){
    if ($(obj).parent().parent().prev().length == 0){
        return ;
    }

    var cur_name = $(obj).parent().html();
    var top_name = $(obj).parent().parent().prev().children().last().html();

    $(obj).parent().parent().prev().children().last().html(cur_name);
    $(obj).parent().html(top_name);
}

function positionDown(obj){
    if ($(obj).parent().parent().next().length == 0){
        return ;
    }

    var cur_name = $(obj).parent().html();
    var top_name = $(obj).parent().parent().next().children().last().html();

    $(obj).parent().parent().next().children().last().html(cur_name);
    $(obj).parent().html(top_name);
}
