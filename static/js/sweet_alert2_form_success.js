title = document.currentScript.getAttribute('title');
redirect_url = null;
if (document.currentScript.getAttribute('redirect_url')){
    redirect_url = document.currentScript.getAttribute('redirect_url');
}

swal({
  title: title,
  type: 'success',
  timer: 1500,
  showConfirmButton: false
}).then(function(){},
    function(dismiss){
        if (redirect_url !== null){
            window.location.replace(redirect_url);
        }
    }
)