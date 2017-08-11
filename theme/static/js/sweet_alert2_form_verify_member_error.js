title = document.currentScript.getAttribute('title');
lang = document.currentScript.getAttribute('lang');
error_type = document.currentScript.getAttribute('error_type');

error_text = "";

if (error_type == "not_member"){
    error_text = "請輸入正確的使用者名稱和密碼，皆有大小寫之分";
} else if (error_type == "no_discount_remain") {
    error_text = "您的優惠額度用完囉，快去加購吧！";
} else {
    error_text = "您還沒為此週期繳月費所以還不能享受餐廳優惠哦";
}

swal({
  title: title,
  text: error_text,
  type: 'error',
  showConfirmButton: true
});