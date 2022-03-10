'use strict';

window.addEventListener("load", function(){
  document.getElementById("search-input").addEventListener("keyup", function(event) {
    if (event.keyCode === 13) {
      event.preventDefault();
      document.getElementById("search-btn").click();
    }
  });
  const urlSearchParams = new URLSearchParams(window.location.search);
  const params = Object.fromEntries(urlSearchParams.entries());
  console.log(params)
  // very dumb way to support auto search by link
  if (window.location.pathname == "/search.html" && params.query != undefined) {
    document.getElementById("search-input").value = params.query;
    search()
  }
});

function search() {
  const query = document.getElementById("search-input").value
  console.log("searching: " + query);
  document.getElementById("searchresults").innerHTML = "Loading..."
  let start = performance.now();
  fetch("/search?query=" + query)
    .then(response => response.json())
    .then(data => {
      console.log(data);
      const time = (performance.now() - start).toFixed(0)/1000;
      const foundMsg = "Found " + data.length + " results (" + time + " seconds) ";
      console.log(foundMsg);
      document.getElementById("searchresultsnumber").innerHTML = foundMsg;
      var template = document.getElementById('results-template').innerHTML;
      var rendered = Mustache.render(template, {results: data});
      document.getElementById('searchresults').innerHTML = rendered;
      window.history.pushState({page: "another"}, "search: " + query, "index.html?query=" + query);
      // console.log(rendered);
    });
}
