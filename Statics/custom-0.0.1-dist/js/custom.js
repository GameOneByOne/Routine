/*
* There Are Some JQ Function By Self 
*/

$("#login-in").click(function(){
    $.ajax({
        url : "/user/",
        type : "get",
        async : false,
        data : {"account":$("#account").val(), "password":$("#password").val()},
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
});

$("#sign-up").click(function(){
    $.ajax({
        url : "/user/",
        type : "post",
        async : false,
        data : {"account":$("#account").val(), "password":$("#password").val()},
        dataType : "json",
        success : function(data) {
            if (data.errorCode == 0){
                $.cookie('slug', data.slug, {expires: 7});
                window.location.href = "http://" + window.location.host;
            } else {
                $("#sign_error").removeClass("d-none");
            }
        }
    });
});

$("#login-out").click(function(){
    $.cookie('slug', null);
    window.location.href = "http://" + window.location.host;
});



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

$(document).ready(function(){
    if ( $("#book-window").length > 0 ) {
        getBooks(function(result){
            var book_card = '';
            var index = 0;
            for (obj of result) {
                book_card = 
                '<div class="mb-3 m-lg-2 shadow-lg p-1 mb-5 bg-white rounded" style="max-width: 560px;">' +
                    '<div class="book-cover" onclick="previewFile(this)" book_id="' + obj.slug + '">' + 
                    '<img src="' + obj.cover + '" alt="..."></div>' +
                '</div>';
                $("#book-window").append(book_card);
                index++;
            }
        });
    }
})

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

$("#upload-button").hover(function () {
        $("#upload-button").removeClass("bi-arrow-up-square");
        $("#upload-button").addClass("bi-arrow-up-square-fill");
    }, function () {
        $("#upload-button").removeClass("bi-arrow-up-square-fill");
        $("#upload-button").addClass("bi-arrow-up-square");
});

$("#book-mark").hover(function () {
    $("#book-mark").removeClass("bi-bookmark-heart");
    $("#book-mark").addClass("bi-bookmark-heart-fill");
}, function () {
    $("#book-mark").removeClass("bi-bookmark-heart-fill");
    $("#book-mark").addClass("bi-bookmark-heart");
});

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

previewFile = function (obj) {
    if ($.cookie('slug')){
        alert("你还没有注册哦！希望能注册一下");
    }
    window.open(src="http://" + window.location.host + "/viewer?bookSlug=" + $(obj).attr("book_id"));
};
