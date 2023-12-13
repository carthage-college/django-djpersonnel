/**
 * simple function to show/hide an element based on the value
 * of another dom object and then reset the value of dependent
 * object if hide
 */
function toggle(dis, val, dom, rent=false) {
  if (dis == val) {
    if (rent) {
      dom.show();
    } else {
      $('#' + dom).show();
    }
  } else {
    if (rent) {
      dom.hide();
    } else {
      $('#' + dom).hide();
      $('#id_' + dom).val('');
    }
  }
}

function set_icon(check){
  icon = '';
  if (check == true) {
    icon = '<i class="fa fa-check green" title="Tested Positive"><span style="display:none;">x</span></i>';
  }
  return icon;
}

$(function(){
  /* clear django cache object by cache key and refresh content */
  $('.clear-cache').on('click', function(e){
    e.preventDefault();
    var $dis = $(this);
    var $cid = $dis.attr('data-cid');
    var $target = '#' + $dis.attr('data-target');
    var $html = $dis.html();
    $dis.html('<i class="fa fa-refresh fa-spin"></i>');
    $.ajax({
      type: 'POST',
      url: $clearCacheUrl,
      data: {'cid':$cid},
      success: function(data) {
        $.growlUI("Cache", "Clear");
        $($target).html(data);
        $dis.html('<i class="fa fa-refresh"></i>');
      },
      error: function(data) {
        $.growlUI("Error", data);
      }
    });
    return false;
  });
});
