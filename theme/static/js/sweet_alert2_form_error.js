title = document.currentScript.getAttribute('title');
lang = document.currentScript.getAttribute('lang');

$(".errorlist").hide();
var error_list = $(".errorlist>li>ul").find($("li"));

error_text = "";

for (i = 0; i < error_list.length; i++) {
    error_text += error_list[i].innerText;

//    var error_innerText_en = error_list[i].innerText;
//    var error_innerText_ch = "";
//    if (error_innerText_en.includes("two password fields")){
//        error_innerText_ch = "密碼兩欄不一樣欸";
//    } else if (error_innerText_en.includes("username already exists")){
//        error_innerText_ch = "已有相同的Email註冊過囉";
//    } else if (error_innerText_en.includes("password is too short")){
//        error_innerText_ch = "密碼需為8位數以上";
//    } else if(error_innerText_en.includes("too common")){
//        error_innerText_ch = "密碼太簡單了";
//    } else if(error_innerText_en.includes("numeric")){
//        error_innerText_ch = "密碼需至少包含一英文字母";
//    } else if(error_innerText_en.includes("correct username and password")){
//        error_innerText_ch = "帳號或密碼錯誤，請留意有大小寫之分";
//    } else{
//        error_innerText_ch = error_list[i].innerText
//    }
//
//    if (lang.includes("zh")){
//        error_text += error_innerText_ch;
//    } else{
//        error_text += error_innerText_en;
//    }

    error_text += '\n';
}

swal({
  title: title,
  text: error_text,
  type: 'error',
  showConfirmButton: true
});