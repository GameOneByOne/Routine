/*
* There Are Some JQ Function By Self 
*/

/*
-------------------------------
界面事件
-------------------------------
*/


// 页面加载完成时运行
$(document).ready(function(){
    // 按列表Slug，开始加载Piece
    for (obj of $("#left-nav").children("ul").children("li").children("div")){
        getPieceTitlesAndAppendHtml(obj);
    }
});


/*
-------------------------------
后台接口
-------------------------------
*/
function getPieceTitlesAndAppendHtml(obj){
    $.ajax({
        url : "/piece/?piece_slug=" + obj.id + "&content=true",
        type : "get",
        async : false,
        data : "",
        headers:"",
        dataType : "json",
        success : function(data) {
            console.log(data);
            if (data.errorCode == 0){
                // 获取到数据并填充HTML
                var min_level = data.data.content.min_title_level;
                for (row of data.data.content.rows){
                    $(obj).children("div").append('<a class="nav-link ms-' + (row[2] - min_level) * 2 + '" href="#' + row[1] + '">' + row[0] + '</a>')
                }
                
            } else {
                
            }
        }
    });
}

