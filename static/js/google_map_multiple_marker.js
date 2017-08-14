var restaurants_locations_dict = document.currentScript.getAttribute('restaurants_locations_dict');
restaurants_locations_dict = JSON.parse(restaurants_locations_dict)

var ggl_map_zoom_value = document.currentScript.getAttribute('ggl_map_zoom_value');
ggl_map_zoom_value = Number(ggl_map_zoom_value);

var ggl_map_center_lat_lng_arr = document.currentScript.getAttribute('ggl_map_center_lat_lng_arr');
ggl_map_center_lat_lng_arr = JSON.parse(ggl_map_center_lat_lng_arr)

var marker_url = document.currentScript.getAttribute('marker_url');

var infowindow = new google.maps.InfoWindow();
var geocoder;

<!--var convert_addr_to_lat_lng = function() {-->
  <!--for(i = 0; i < locations.length; i++){-->
      <!--var loc_name = locations[i][0];-->
      <!--geocoder = new google.maps.Geocoder();-->
      <!--geocoder.geocode({-->
            <!--'address': locations[i][1]-->
        <!--}, function (results, status) {-->
            <!--if (status == google.maps.GeocoderStatus.OK) {-->
                <!--var loc_lat = results[0].geometry.location.lat();-->
                <!--var loc_lng = results[0].geometry.location.lng();-->
                <!--var temp_arr = [];-->
                <!--temp_arr.push(loc_name);-->
                <!--temp_arr.push(loc_lat);-->
                <!--temp_arr.push(loc_lng);-->
                <!--locations_lat_lng_arr.push(temp_arr);-->

                <!--&lt;!&ndash;$('#lat').text(results[0].geometry.location.lat());&ndash;&gt;-->
                <!--&lt;!&ndash;$('#lng').text(results[0].geometry.location.lng());&ndash;&gt;-->
        <!--}-->
    <!--});-->
  <!--}-->
<!--}-->

<!--convert_addr_to_lat_lng();-->


var map = new google.maps.Map(document.getElementById('map'), {
zoom: ggl_map_zoom_value,
center: new google.maps.LatLng(ggl_map_center_lat_lng_arr[0], ggl_map_center_lat_lng_arr[1]),
mapTypeId: google.maps.MapTypeId.ROADMAP
});

var make_map = function() {
  var marker, i;
  for (i = 0; i < restaurants_locations_dict.length; i++) {
    marker = new google.maps.Marker({
      url: marker_url + restaurants_locations_dict[i].pk,
      position: new google.maps.LatLng(restaurants_locations_dict[i].latitude, restaurants_locations_dict[i].longitude),
      title: restaurants_locations_dict[i].name,
      zIndex: i,
      map: map
    });

    google.maps.event.addListener(marker, 'click', (function(marker, i) {
      return function() {
        infowindow.setContent('<a href=\"' + marker.url + '\" style=\"color:inherit;\">' + marker.title +'</a>');
        infowindow.open(map, marker);
      }
    })(marker, i));
  }
}

make_map();