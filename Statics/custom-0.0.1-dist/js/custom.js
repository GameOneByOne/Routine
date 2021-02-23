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

$("#user_avatar").hover(function(){
    $("#user_info_panel").toggleClass("invisible");
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
                '<div class="card mb-3 m-lg-2" style="max-width: 560px;">'+
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
        if($("#user-info").hasClass("d-none")){
            $("#user-info").removeClass("d-none");
        }
        if (!$("#user-avatar").hasClass("d-none")){
            $("#user-avatar").addClass("d-none");
        }
    }
    else{
        if(!$("#user-info").hasClass("d-none")){
            $("#user-info").addClass("d-none");
        }
        if ($("#user-avatar").hasClass("d-none")){
            $("#user-avatar").removeClass("d-none");
        }  
    }
  });