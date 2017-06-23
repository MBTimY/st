var showPicTable = function(data){
    $("#pages").empty();
    $("#repotbody").empty();
    if ( data.hasOwnProperty("titles") && data.hasOwnProperty("paginations") && data.titles.length > 0 ){
        template_div = "<div class=\"text-success\"><h3></h3><a></a></div>"
        for (i in data.titles) {
            temp_div = $(template_div);
            temp_div.find("a").attr("href", data.titles[i][1]);
            temp_div.find("a").attr("target", "_blank");
            temp_div.find("a").text(data.titles[i][1]);
            temp_div.find("h3").text(data.titles[i][0]);
            $("#repotbody").append(temp_div)
        }

        if (data.paginations.length >0 ) {
            var page_num = parseInt(data.paginations[0][0]);
            var liArray = [];

            if (page_num == 2){
                var temp_li = document.createElement("li");
                var temp_a = document.createElement("a");
                $(temp_li).attr("class", "disabled");
                $(temp_a).text("1");
                $(temp_li).append(temp_a);
                liArray.push(temp_li);
            }

            for (i in data.paginations){
                if (data.paginations[i][0] != page_num){
                    temp_li = document.createElement("li");
                    temp_a = document.createElement("a");
                    $(temp_li).attr("class", "disabled");
                    $(temp_a).text(page_num);
                    $(temp_li).append(temp_a);
                    liArray.push(temp_li);
                    page_num += 1;
                }
                temp_li = document.createElement("li");
                temp_a = document.createElement("a");
                $(temp_a).click(onPicPage);
                $(temp_a).attr("data-url", data.paginations[i][1])
                $(temp_a).text(data.paginations[i][0]);
                $(temp_li).append(temp_a);
                liArray.push(temp_li);
                page_num += 1;
            }

            $("#pages").append(liArray);
        }
        return true;
    }
    return false;
}

var onPicPage = function () {
    $.ajax({
        url: $(this).attr("data-url"),
        type: "get",
        dataType: "json",
        success: function(respData, status, jqXHR){

            if (!showPicTable(respData)) {
                $("#repotbody").addClass("hidden");
                $("#pages").addClass("hidden");

                $("#notice").removeClass("hidden"); //show
                $("#notice").text("SORRY, 未找到您要的内容，可能网络出错了哦。。。");
                return;
            }
        },
        error: function(jqXHR, textStatus, errorThrown ){
            $("#repotbody").addClass("hidden");
            $("#pages").addClass("hidden");
            
            $("#notice").removeClass("hidden"); //show
            $("#notice").text("SORRY, 未找到您要的内容，可能网络出错了哦。。。");
        }
    })
}

var onBtPage = function () {
    var pageNum = parseInt($(this).text());
    $.ajax({
        url: "/searchTORR",
        type: "get",
        data : {
            k: $(this).attr("data-k"),
            pn: pageNum
        },
        dataType: "json",
        success: function(respData, status, jqXHR){

            if (!showBtTable(respData)) {
                $("#repotbody").addClass("hidden");
                $("#pages").addClass("hidden");

                $("#notice").removeClass("hidden"); //show
                $("#notice").text("SORRY, 未找到您要的内容，可能网络出错了哦。。。");
                return;
            }
        },
        error: function(jqXHR, textStatus, errorThrown ){
            $("#repotbody").addClass("hidden");
            $("#pages").addClass("hidden");
            
            $("#notice").removeClass("hidden"); //show
            $("#notice").text("SORRY, 未找到您要的内容，可能网络出错了哦。。。");
        }
    })
}

var showBtTable = function (data) {
    var search_name = $("#argInput").val();
    $("#pages").empty();
    $("#repotbody").empty();
    if ( data.hasOwnProperty("list") ){
            var template_div = "<div class=\"text-success\"><h3></h3><blockquote><p class=\"text-primary\"></p></blockquote></div>"
            for (i in data.list) {
                var temp_div = $(template_div);
                temp_div.find("h3").text(data.list[i]["title"]);
                temp_div.find("p").text(decodeURI(data.list[i]["magnet"]));
                $("#repotbody").append(temp_div);
            }

            var liArray = []
            for (i = data.startPN; i <= data.endPN; i++){
                var temp_li = document.createElement("li");
                var temp_a = document.createElement("a");
                $(temp_a).click(onBtPage);
                $(temp_a).text(i);
                if (data.currentPN == i) {
                    $(temp_li).attr("class", "disabled");
                } else {
                    $(temp_a).attr("data-k", search_name)
                }
                $(temp_li).append(temp_a);
                liArray.push(temp_li);
            }
            $("#pages").append(liArray);
            return true;
    }
    return false;
}

var receiveBtReport = function () {
    $("#pages").addClass("hidden");
    $("#repotbody").addClass("hidden");

    $("#notice").removeClass("hidden"); 
    $("#notice").text("正在搜索相关种子资源，请耐心等待。。。");
    var search_name = $("#argInput").val();
    if (search_name) {
      $.ajax({
          url: "/searchTORR",
          type: "get",
          data : {
              k: search_name
          },
          dataType: "json",
          success: function(respData, status, jqXHR){
                $("#notice").addClass("hidden"); //hidden

                $("#pages").removeClass("hidden");
                $("#repotbody").removeClass("hidden"); 
                if (!showBtTable(respData)) {
                    $("#pages").addClass("hidden");
                    $("#repotbody").addClass("hidden");

                    $("#notice").removeClass("hidden"); //shows
                    $("#notice").text("SORRY, 我们没有找到相关的种子资源，请你换个关键字试试。。。");
                    return;
                }
          },
          error: function(jqXHR, textStatus, errorThrown ){
              $("#notice").text("SORRY, 我们没有找到相关的种子资源，请你换个关键字试试。。。");
          }
      })
    }
}

var receivePicReport = function() {
    $("#pages").addClass("hidden");
    $("#repotbody").addClass("hidden");

    $("#notice").removeClass("hidden"); 
    $("#notice").text("正在搜索图片所匹配的地址，请耐心等待。。。");
    var keyword = $("#argInput").val();
    if (keyword) {
      $.ajax({
          url: "/searchPIC",
          type: "get",
          data : {
              imgurl: keyword
          },
          dataType: "json",
          success: function(respData, status, jqXHR){
            $("#notice").addClass("hidden"); //hidden

            $("#pages").removeClass("hidden");
            $("#repotbody").removeClass("hidden"); 
            if (!showPicTable(respData)) {
                $("#pages").addClass("hidden");
                $("#repotbody").addClass("hidden");

                $("#notice").removeClass("hidden"); //shows
                $("#notice").text("SORRY, 您所提供的图片地址我们并没有找到什么相关内容。。。");
                return;
            }
          },
          error: function(jqXHR, textStatus, errorThrown ){
                $("#notice").text("SORRY, 您所提供的图片地址我们并没有找到什么相关内容。。。");
          }
      })
    }
    
}


var initial= function(){
    $('[data-toggle="tooltip"]').tooltip({animation: true, placement: "bottom"});   

    $("#btnbt").on("click", () => {
        receiveBtReport();
    });
    $("#btnpic").on("click", () => {
        receivePicReport();
    });
}




$("document").ready(initial)