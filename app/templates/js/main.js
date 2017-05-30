var torrS = "http://127.0.0.1:8080/searchTORR"
var picS = "http://127.0.0.1:8080/searchPIC"


var receiveBtReport = function () {
    search_name = $("#argInput").text();
    console.log(search_name);
    if (search_name) {
      $.ajax({
          url: "/searchTORR",
          type: "get",
          data : {
              k: search_name
          },
          dataType: "json",
          success: function(respData, status, jqXHR){
              console.log(respData)
          }
      })
    }
}

var receivePicReport = function() {
     $("#repotable").attr("style","display:none");
}


var initial= function(){
    $("#btnbt").on("click", () => {
        receiveBtReport();
    });
    $("#btnpic").on("click", () => {
        receivePicReport();
    });
}




$("document").ready(initial)