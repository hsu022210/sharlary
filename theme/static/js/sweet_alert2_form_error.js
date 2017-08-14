title = document.currentScript.getAttribute('title');
lang = document.currentScript.getAttribute('lang');
var error_text = "";

if (document.currentScript.getAttribute('error_msg')){
    error_text = document.currentScript.getAttribute('error_msg');
} else{
    $(".errorlist").hide();
    var error_list = $(".errorlist>li>ul").find($("li"));

    for (i = 0; i < error_list.length; i++) {
        error_text += error_list[i].innerText;
        error_text += '\n';
    }
}

swal({
  title: title,
  text: error_text,
  type: 'error',
  showConfirmButton: true
});