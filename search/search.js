let searchform = document.getElementById("searchbox");

function searchTitle(title) {
  
}

searchform.addEventListener("submit", function(e) {
  e.preventDefault();

  let request = document.getElementById("request").value;
  searchTitle(request);
});