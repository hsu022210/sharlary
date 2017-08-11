var user_restaurant_list_exist = document.currentScript.getAttribute('user_restaurant_list_exist');
var ajax_url = document.currentScript.getAttribute('ajax_url');
var csrf_token = document.currentScript.getAttribute('csrf_token');

$(function () {
  $('.user_saved_list').click(function () {
    saveFunction($(this));
    var action_type = $(this).data('save_restaurant_type');

    if (action_type == "save"){
       $(this).text('favorite');
       $(this).data('save_restaurant_type',"unsave");
    }else{
       $(this).text('favorite_border');
       $(this).data('save_restaurant_type',"save");
       if(user_restaurant_list_exist){
        $(this).parents('.card').parent().fadeOut();
       }
    }

   });
});

function saveFunction(caller) {
  var company_id = caller.data('company_id');
  var action_type = caller.data('save_restaurant_type');
  $.ajax({
      type: "POST",
      url: ajax_url,
      data: {'action': action_type, 'csrfmiddlewaretoken': csrf_token, 'company_id': company_id},
      dataType: 'json',
      success: function (response) {
      }
  });
}