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
                window.location.href = "http://" + window.location.host + "/home/";
            } else {
                alert("Account Or Password Is Worry")
            }
        }
        
    });
});