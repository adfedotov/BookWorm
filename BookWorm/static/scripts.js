$(document).ready(function() {
  $('#dashboard-search').on('input', function(e){
    var input = $(this).val();
    $('div.card').each(function(){
      if ($(this).find('h5.card-title').text().search(new RegExp(input, "i")) < 0 && $(this).find('p.card-text').text().search(new RegExp(input, "i")) < 0) {
        $(this).fadeOut();
      } else {
        $(this).show();
      }
    });
  });
});
