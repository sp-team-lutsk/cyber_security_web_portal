var mybutton = document.getElementsByClassName("scrol");
//var myBtn = document.querySelector('.scrol');
window.onscroll = function() {scrollFunction()};
function scrollFunction() {
  if (document.body.scrollTop > 1000 || document.documentElement.scrollTop > 1000) {
    document.querySelector('.scrol').style.display = "block";
  } else {
    document.querySelector('.scrol').style.display = "none";
  }
}
function topFunction() {
  $('body,html').animate({
          scrollTop : 0
      }, 500);
}
