$(function() {
  $("#searchbox").on("submit", function(e) {
    e.preventDefault();
    let querybox = $("#querybox");
    get_tracks(querybox.val());
    querybox.val("");
  });


  function get_tracks(query) {
    $.post( "urlparameter",
            {q: query},
            display_tracks(data, status)
          );

  }

  function display_tracks(data, status) {
    $("resultsp").text(data);
  }



});






// let searchform = document.getElementById("searchbox");

// searchform.addEventListener("submit", function(e) {
//   e.preventDefault();

//   let querybox = document.getElementById("querybox");
//   get_tracks(querybox.value)
//   querybox.value = ""
// });

// function get_tracks(query) {
//   // console.log(querybox.value)

//   // AJAX request for track list
//   if (window.XMLHttpRequest) {
//     // code for modern browsers
//     xmlhttp = new XMLHttpRequest();
//   }
//   else {
//     // code for old IE browsers
//     xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
//   }
// }