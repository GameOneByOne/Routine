/*
* There Are Some JQ Function By Self 
*/

/*
-------------------------------
界面事件
-------------------------------
*/

var ALL_PIECE = new Array();


// 页面加载完成时运行
$(document).ready(function(){
    // 按列表Slug，开始加载Piece
    ind = 0
    for (obj of $("#left-nav").children("ul").children("li").children("div")){
        getPieceTitlesAndAppendHtml(obj, ind++);
    }
});

/*
-------------------------------
后台接口
-------------------------------
*/
function getPieceTitlesAndAppendHtml(obj, index){
    $.ajax({
        url : "/piece/?piece_slug=" + obj.id + "&content=true",
        type : "get",
        async : false,
        data : "",
        headers:"",
        dataType : "json",
        success : function(data) {
            if (data.errorCode == 0){
                // 获取到数据并填充HTML
                
                var min_level = data.data.content.min_title_level;
                for (row of data.data.content.rows){
                    $(obj).children("div").append('<a content-id=content' + ind +' class="once-show nav-link ms-' + (row[2] - min_level) * 3 + '" href="#' + row[1] + '" onclick=onceCanShow(this)>' + row[0] + '</a>')
                }
                
                // 填充文本区
                var content_div = "";
                if (ind == 1){
                    var content_div = '<div id="content' + ind + '" class="markdown-body editormd-html-preview">';
                } else {
                    var content_div = '<div id="content' + ind + '" class="markdown-body editormd-html-preview d-none">';
                }
                
                content_div += '<textarea id="text' + ind + '" style="display:none;"></textarea></div>';

                $("#markdown-content").append(content_div);
                
                // 生成markdown文档
                $("#text" + ind).html(data.data.content.content);

                // 取消spin的图标
                $(obj).prev().prev().addClass("d-none");
                ALL_PIECE.push("content" + ind);
                generateMDContent("content" + ind);              
            }
        }
    });
}





/*
-------------------------------
工具函数
-------------------------------
*/
function generateMDContent(id) {
    var EditormdView;
        
    EditormdView = editormd.markdownToHTML(id, {
        htmlDecode      : "style,script,iframe",  
        emoji           : true,
        taskList        : true,
        tex             : true,
        flowChart       : true,
        sequenceDiagram : true,
    });
}


function onceCanShow(obj){
    var content_id = $(obj).attr("content-id");
    for (id of ALL_PIECE){
        if (id == content_id){
            $("#" + id).removeClass("d-none");
        } else {
            $("#" + id).addClass("d-none");
        }
    }
}
