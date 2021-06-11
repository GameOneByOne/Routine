/*
-------------------------------
界面事件
-------------------------------
*/

// 用户保存编辑中的文档事件
$("#piece-save").click(function(){
    var content = $("#editor").children("textarea").first().html();
    var name = $("#piece-name").val();
    var slug = $("#piece-save").attr("piece-slug");

    $.ajax({
        url : "/piece/",
        type : "patch",
        async : false,
        data : {"content": content, "name":name, "slug":slug},
        headers:"",
        dataType : "json",
        success : function(data) {
            if (data.errorCode == 0){
                alert("更新成功");
            }
        }
    });
});

/*
-------------------------------
快捷键监听
-------------------------------
*/
document.addEventListener('keydown', function(e){
    if (e.keyCode == 83 && (navigator.platform.match("Mac") ? e.metaKey : e.ctrlKey)){
        e.preventDefault();
     }
});