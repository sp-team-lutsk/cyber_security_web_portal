window.onload = function() {

  setTimeout(function() {
    var preloader = document.getElementById('page-preloader');
    if ( !preloader.classList.contains('done') ) {
      preloader.classList.add('done');
    }
  }, 1000);

}
function readMore() {
  let more = document.getElementById("more");
  let btn = document.getElementById("btn");
  let text = document.getElementById("text");



  if (more.style.maxHeight) {
    btn.innerHTML = "Докладніше";
    more.style.maxHeight = null;
    text.style.opacity = "0";
  }else {
    btn.innerHTML = "Закрити";
    more.style.maxHeight = more.scrollHeight + 'px';
    text.style.opacity = "1";
  }
}

