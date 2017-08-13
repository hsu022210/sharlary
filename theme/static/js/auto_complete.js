id_name = document.currentScript.getAttribute('id_name');
id_name = "#" + id_name;
source = document.currentScript.getAttribute('source');
source = JSON.parse(source);

$( id_name ).autocomplete({
  source: source
});