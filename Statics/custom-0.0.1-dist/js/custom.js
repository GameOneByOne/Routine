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
        alert("邮箱和密码不能为空");
    } else {
        $.ajax({
            url : "/user/",
            type : "get",
            async : false,
            data : {"email":$("#email").val(), "password":$("#passWord").val()},
            dataType : "json",
            success : function(data) {
                if (data.errorCode == 0){
                    $.cookie('slug', data.slug, {expires: 7});
                    window.location.href = "http://" + window.location.host;
                } else {
                    $("#login_error").removeClass("d-none");
                }
            }
        });
    }

});

// 注册按钮的功能
$("#sign-up").click(function(){
    if ($("#email").val() == "" || $("#passWord").val() == ""){
        alert("邮箱和密码不能为空");
    } else if ($("#RandomCodeInput").hasClass("d-none")){
        $.ajax({
            url : "/user/randomcode",
            type : "get",
            async : false,
            data : {"email":$("#email").val()},
            dataType : "json",
            success : function(data) {
                if (data.errorCode == 0){
                    $("#RandomCodeInput").removeClass("d-none")
                    $("#UserErrorInfo").html(data.desc);
                    $("#UserErrorInfo").removeClass("d-none");
                    $.cookie('email', $("#email").val());
                    $.cookie('password', $("#passWord").val());
                    $("#sign-up").html("验证");
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
            data : {"code":$("#RandomCode").val(), "email":$.cookie('email')},
            dataType : "json",
            success : function(data) {
                if (data.errorCode == 0){
                    $.ajax({
                        url : "/user/",
                        type : "post",
                        async : false,
                        data : {"email":$.cookie('email'), "password":$.cookie('password')},
                        dataType : "json",
                        success : function(data) {
                            if (data.errorCode == 0){
                                $.cookie('slug', data.slug, {expires: 7});
                                $.cookie('email', 'null');
                                $.cookie('password', 'null');
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

// 登出按钮的功能
$("#login-out").click(function(){
    $.cookie('slug', null);
    window.location.href = "http://" + window.location.host;
});

// 上传按钮的悬浮事件
$("#upload-button").hover(function () {
    $("#upload-button").removeClass("bi-arrow-up-square");
    $("#upload-button").addClass("bi-arrow-up-square-fill");
}, function () {
    $("#upload-button").removeClass("bi-arrow-up-square-fill");
    $("#upload-button").addClass("bi-arrow-up-square");
});

// 收藏按钮的悬浮事件
$("#book-mark").hover(function () {
    $("#book-mark").removeClass("bi-bookmark-heart");
    $("#book-mark").addClass("bi-bookmark-heart-fill");
}, function () {
    $("#book-mark").removeClass("bi-bookmark-heart-fill");
    $("#book-mark").addClass("bi-bookmark-heart");
});


/*
-------------------------------
后台接口
-------------------------------
*/

// 获取书籍的接口
function getBooks(callback){
    $.ajax({
      url : '/book/',
      type : "get",
      data : "",
      async : true,
      success : function(data) {
        result = data;
        callback(result);
      }
    });
}

// PDF文件上传事件
$('#md5File').fileinput({
    language: 'zh',
    uploadUrl: 'http://' + window.location.host +'/book/',
    enctype: 'multipart/form-data',
    uploadAsync:true,
    allowedFileExtensions: ['pdf'],
    browseClass: 'btn btn-primary',
    maxFileCount: 1,
    minFileCount : 1,
  }).on('fileuploaded',function (event, data, previewId, index) {
    if (data.errorCode == 1){
        $.toast({
            title: 'Notice!',
            subtitle: 'Just Now',
            content: '文件上传失败，请重试',
            type: 'info',
            delay: 3000,
            img: {
              src: '',
              class: 'rounded-pill',
              title: 'Thumbnail Title',
              alt: 'Alternative'
            },
            pause_on_hover: false
          });
    }
    else{
        $.toast({
            title: 'Notice!',
            subtitle: 'Just Now',
            content: '文件上传成功，感谢你的分享',
            type: 'info',
            delay: 3000,
            img: {
              src: '',
              class: 'rounded-pill',
              title: 'Thumbnail Title',
              alt: 'Alternative'
            },
            pause_on_hover: false
          });
    }
});


/*
-------------------------------
界面事件
-------------------------------
*/

// 页面加载完成时运行
$(document).ready(function(){
    if ( $("#book-window").length > 0 ) {
        getBooks(function(result){
            var book_card = '';
            var index = 0;
            var row_id = "row-0";
            for (obj of result) {
                if (index % 6 == 0) {
                    if (index != 0) {
                        $("#book-window").append('</div>');
                    }
                    row_id = 'row-' + index.toString(10)
                    $("#book-window").append('<div id="' + row_id + '" class="row">');
                }
                book_card = 
                    '<div class="col-2 book-cover" onclick="previewFile(this)" book_id="' + obj.slug + '">' + 
                    '<img class="img-fluid bg-white shadow-lg rounded" src="' + obj.cover + '"></div>';
                $("#" + row_id).append(book_card);
                index++;
            }
        });
    }
})

// 页面被改变大小时执行
$(window).resize(function() {
    if ($(window).width() < 600){
        if (!$("#user-avatar").hasClass("d-none")){
            $("#user-avatar").addClass("d-none");
        }
    }
    else{
        if ($("#user-avatar").hasClass("d-none")){
            $("#user-avatar").removeClass("d-none");
        }  
    }
});

// 打开PDF Book 时，如果未登陆则提醒一下，非强制注册
previewFile = function (obj) {
    if ($.cookie('slug') == "null"){
        alert("你还没有注册哦！希望能注册一下");
    }
    var page = 0
    $.ajax({
        url : '/book/?slug=' + $(obj).attr("book_id"),
        type : "get",
        data : "",
        async : true,
        success : function(data) {
            $('#bookPieces').html("");
            for (page=0; page<data.pieces.length; ++page){
                $('#bookPieces').append('<button book_id="'+ data.slug +'" page_id="' + data.pieces[page] + '" class="row-2 btn btn-info btn-sm" onclick="watchPdf(this)" type="button">'+ page * 100 + '~' + (page+1) * 100 + '页</button>');
            }
            $('#ModelBookName').html(data.name);
            $('#ModelBookAuthor').html(data.author);
            $('#ModelBookUploadPeople').html(data.upload_people);
            $('#ModelBookUploadDate').html(data.upload_date);
            $('#pdfInfoCover').attr("src","/static/image/pdf_cover/" + $(obj).attr("book_id") + ".jpeg");
            $('#BookInfoModal').modal('show')
        }
      });
    
};

watchPdf = function(obj){
    window.open(src="http://" + window.location.host + "/viewer?bookSlug=" + $(obj).attr("book_id") + "&pageSlug=" + $(obj).attr("page_id"));
};
