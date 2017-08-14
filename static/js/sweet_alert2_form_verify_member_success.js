title = document.currentScript.getAttribute('title');
lang = document.currentScript.getAttribute('lang');
r_name = document.currentScript.getAttribute('r_name');
r_image = document.currentScript.getAttribute('r_image');
redirect_url = document.currentScript.getAttribute('redirect_url');
first_name = document.currentScript.getAttribute('first_name');
current_time = document.currentScript.getAttribute('current_time');
ajax_url = document.currentScript.getAttribute('ajax_url');
csrf_token = document.currentScript.getAttribute('csrf_token');
curr_discount_times_remain = document.currentScript.getAttribute('curr_discount_times_remain');

function discount_page_swal() {
    return swal({
      title: r_name + ' - 兌換優惠完成！',
      text: '請向店家出示此通知圖示\n' + current_time,
      type: 'success',
      showConfirmButton: true,
      confirmButtonText: '已出示',
      imageUrl: r_image,
      imageWidth: 400,
      imageHeight: 200,
      allowOutsideClick: false
    })
}

function recur_swal(discount_times_remain) {
    var discount_page_swal_code = discount_page_swal();
    discount_page_swal_code.then(function () {
        swal({
          title: '確定出示完畢?',
          text: "確定後即無法返回",
          type: 'warning',
          showCancelButton: true,
          confirmButtonColor: '#3085d6',
          cancelButtonColor: '#d33',
          confirmButtonText: '確定',
          cancelButtonText: '返回',
          allowOutsideClick: false
        }).then(function () {
            swal({
              title: '感謝您使用Eaggie！',
              text: "您本次週期優惠額度還有" + discount_times_remain + "次",
              type: 'info',
              showConfirmButton: true,
              confirmButtonText: '知道了',
              allowOutsideClick: false
            }).then(function(){
                window.location.replace(redirect_url);
            }
//            ,
//            function(dismiss){
//                if (dismiss === 'timer'){
//                  window.location.replace(redirect_url);
//                }
//            }
            )
        }, function (dismiss) {
          // dismiss can be 'cancel', 'overlay',
          // 'close', and 'timer'
          if (dismiss === 'cancel') {
          recur_swal(discount_times_remain);
          }
        })
    })
}

swal({
      title: title,
      text: "Hi! " + first_name + "，您還有" + curr_discount_times_remain + "次優惠額度，確定要於" + r_name + "兌換一次優惠？",
      type: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#d33',
      confirmButtonText: '確定兌換',
      cancelButtonText: '取消',
    }).then(function () {
        $.ajax({
              type: "POST",
              url: ajax_url,
              data: {'csrfmiddlewaretoken': csrf_token},
              dataType: 'json',
              success: function (response) {
                json_response = JSON.parse(response);
                var discount_times_remain = json_response.discount_times_remain;
                recur_swal(discount_times_remain);
              }
          });
    }, function(dismiss){
        window.location.replace(redirect_url);
    })
