$(document).ready(function() {
  $('#dashboard-search').on('input', function(e){
    var input = $(this).val();
    $('div.card').each(function(){
      if ($(this).find('h5').text().search(new RegExp(input, "i")) < 0) {
                $(this).fadeOut();
      } else {
        $(this).show();
      }
    });
  });
});

function get_books(books) {
  $("div.book_content").empty();
  for (i = 0; i < books.length; i++) {
    console.log('loop executed ' + i);
    $.getJSON({
        url: "http://openlibrary.org/search.json",
        beforeSend: function(xhr){
          if (xhr.overrideMimeType){
            xhr.overrideMimeType("application/json");
          }
          console.log(i);
        },
        dataType: 'json',
        data: {q: books[i][1]},
        success: function(results){
          $("div.book_content").append('<div class="card m-2" style="width: 18rem;" onclick="location.href=#"><img class="card-img-top" src="http://covers.openlibrary.org/b/isbn/' + books[i-1][1] + '-M.jpg" alt="Card image cap"><div class="card-body"><h5 class="card-title">' + results["docs"][0]["title"] + '</h5><p class="card-text">by ' + results["docs"][0]["author_name"][0] + '</p><a href="#" class="btn btn-primary">Go somewhere</a></div></div>');

        }
    });
  }
}
