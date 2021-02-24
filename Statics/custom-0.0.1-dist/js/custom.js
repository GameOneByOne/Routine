/*
* There Are Some JQ Function By Self 
*/

$("#login").click(function(){
    $.ajax({
        url : "/user/",
        type : "get",
        async : false,
        data : {"account":$("#account").val(), "password":$("#password").val()},
        dataType : "json",
        success : function(data) {
            if (data.errorCode == 0){
                window.location.href = "http://" + window.location.host + "/home?account=" + 
                                        $("#account").val()+ "&password=" + $("#password").val();
            } else {
                alert("Account Or Password Is Worry")
            }
        }
        
    });
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
                    '<div class="book-cover">' +
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

function loadFile(file){
    $("#file-name").html(file.name);
};

$('#md5File').fileinput({
    language: 'zh',
    uploadUrl: 'http://127.0.0.1:8081/book/',
    enctype: 'multipart/form-data',
    uploadAsync:true,
    allowedFileExtensions: ['pdf'],
    browseClass: 'btn btn-primary',
    maxFileCount: 1,
    minFileCount : 1,
  }).on('filebatchuploadsuccess',function(res) {
    alert(res);
});


function showPDF(urlSrc){
var urlPre ="pdfjs/web/viewer.html?file="+ urlSrc;
    $("#pdfContainer").attr('src',urlPre); 
    $("#pdf_Modal").modal("show");
}